from omnidesk_etl.models import CaseFilter
from typing import List
from omnidesk_etl.http_client import HttpClient
from omnidesk_etl.models import CaseExtracting, CaseCreating, Label
from .parse_nested_elements import parse_nested_elements
import itertools


class OmnideskService:

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def add_case(self, case: CaseCreating):
        self.http_client.add_case(
            data=case.to_dict()
        )

    def get_labels(self) -> List[Label]:
        labels_response = self.http_client.get_labels()
        return [Label.make(**raw_label) for raw_label in itertools.chain(*[
            parse_nested_elements(label, 'label') for label in labels_response
        ])]

    def get_cases(self, api_filter: CaseFilter = None) -> List[CaseExtracting]:
        params = api_filter.to_dict() if api_filter else None
        cases_response = self.http_client.get_cases(
            params=params
        )
        return [CaseExtracting.make(**raw_case) for raw_case in itertools.chain(*[
            parse_nested_elements(case, 'case') for case in cases_response
        ])]
