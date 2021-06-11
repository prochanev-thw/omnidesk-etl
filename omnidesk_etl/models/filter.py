from dataclasses import dataclass
from datetime import datetime
from omnidesk_etl.models.base_model import WithoutNoneSerializebleModel


class Filter(WithoutNoneSerializebleModel):
    pass


@dataclass
class CaseFilter(Filter):
    from_time: datetime
    show_merged_cases: bool = True
