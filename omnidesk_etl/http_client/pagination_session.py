from typing import Optional
from functools import partial
import logging
import concurrent.futures
import multiprocessing

import requests

import config
from .errors import UnexpectedResponseError
from .sort_enum import Sort


logger = logging.getLogger(__name__)


def get_count_thread_workers(pages_count: int) -> int:
    workers_count: int = None
    cpu_dependend_workers_count: int = \
        multiprocessing.cpu_count() * config.AppConfig.CPU_MULTIPLIER
    if pages_count - 1 < cpu_dependend_workers_count:
        workers_count = pages_count - 1
    else:
        workers_count = cpu_dependend_workers_count
    return workers_count


def get_page_count_from_response(response: requests.Response) -> int:
    try:
        total_count: int = response['total_count']
    except KeyError:
        logger.exception("Unexpected response, key 'total_count' does't exist in response")
        raise UnexpectedResponseError("Unexpected response, key 'total_count' does't exist in response")
    return (total_count // config.AppConfig.RESULT_PER_API_PAGE) + 1


class PaginationSession:

    page_limit = config.AppConfig.RESULT_PER_API_PAGE

    def __init__(self, request_caller, methods):
        self._request = request_caller
        self._methods = methods

    def _get_entities_from_one_page(
        self,
        entity_name: str,
        page: int = 1,
        filter_params: Optional[dict] = None,
        sort: Optional[Sort] = None
    ):

        params_with_pagination = {
            **{'page': page},
            **{'limit': self.page_limit},
        }

        if filter_params:
            params_with_pagination.update(filter_params)
        if sort:
            params_with_pagination.update({'sort': sort})

        return self._request(
            method=self._methods.GET,
            relative_url=entity_name,
            params=params_with_pagination
        )

    def _get_entities_from_all_pages(
        self,
        entity_name: str,
        page_count: int,
        params: dict,
        sort: Optional[Sort] = None
    ):

        all_entities = []

        partial_get_entities_from_one_page = partial(
            self._get_entities_from_one_page,
            entity_name=entity_name,
            filter_params=params,
            sort=sort
        )

        count_workers = get_count_thread_workers(page_count)
        logger.info('Count workers [%d] for entity [%s]', count_workers, entity_name)

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=count_workers
        ) as executor:
            futures = [
                executor.submit(
                    partial_get_entities_from_one_page,
                    page=page_number
                )
                for page_number in range(2, page_count + 1)
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    entities_from_page = future.result()
                except UnexpectedResponseError as exc:
                    logger.exception()
                    raise exc
                else:
                    all_entities.append(entities_from_page)

            return all_entities

    def get_results_from_all_pages(self, entity_name, filter_params: dict = None, sort=None):

        all_entities = []

        first_page = self._get_entities_from_one_page(
            filter_params=filter_params,
            entity_name=entity_name,
            page=1,
            sort=sort
        )

        all_entities.append(first_page)
        page_count = get_page_count_from_response(first_page)
        logger.info('Количество страниц [%d] для объекта [%s]', page_count, entity_name)

        if page_count == 1:
            return all_entities
        else:
            for entity in self._get_entities_from_all_pages(entity_name, page_count, filter_params, sort):
                all_entities.append(entity)

        return all_entities
