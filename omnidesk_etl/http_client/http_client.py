import requests
from requests_toolbelt.sessions import BaseUrlSession
from typing import Optional
import enum
import logging
from .errors import UnexpectedResponseError
from .pagination_session import PaginationSession
from .sort_enum import CaseSort
from .request_log_record import RequestLogRecord, ResponseLogRecord
import config

logger = logging.getLogger(__name__)


class HttpClient():

    class HttpMethod(str, enum.Enum):
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        DELETE = 'DELETE'

    methods = HttpMethod

    def __init__(self, url: str, email: str, token: str):
        self._session = BaseUrlSession(url)
        self._session.auth = requests.auth.HTTPBasicAuth(email, token)
        self.pagination_session = PaginationSession(self._request, self.methods)

    def _request(
        self,
        method: HttpMethod,
        relative_url: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None
    ):

        try:
            response = self._session.request(method, relative_url, json=data, params=params)
            logger.info(RequestLogRecord(response.request))
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            logger.exception('Ошибка во время выполнения запроса, response - %s', ResponseLogRecord(response))
            raise UnexpectedResponseError(f'Ошибка в запросе {response.text}')
        logger.info(ResponseLogRecord(response))

        try:
            api_calls_left = int(response.headers['api_calls_left'])
        except KeyError:
            raise UnexpectedResponseError('Ключ api_calls_left не представлен в заголовках ответа от сервера')

        if config.AppConfig.API_CALLS_LEFT_ALERT > api_calls_left:
            logger.warning('Количество оставшихся запросов достигло критического минимума, %d', api_calls_left)

        return response.json()

    def add_case(self, data):
        self._request(
            method=self.methods.POST,
            relative_url='cases.json',
            data=data
        )

    def get_cases(self, params: dict = None):
        return self.pagination_session.get_results_from_all_pages(
            entity_name='cases.json',
            filter_params=params,
            sort=CaseSort.BY_CREATED_ASC
        )

    def get_labels(self, params: dict = None):
        return self.pagination_session.get_results_from_all_pages(
            entity_name='labels.json',
            filter_params=params
        )
