from datetime import datetime
from dateutil import parser as datetime_parser
from dataclass_factory import Factory, Schema
from dataclasses import asdict


def convert_to_timestamp(datetime_value):
    return int(datetime_value.timestamp())


factory = Factory(
    schemas={
        datetime: Schema(
            parser=datetime_parser.parse,
            serializer=datetime.isoformat
        )
    }
)


datetime_to_timestamp_factory = Factory(
    schemas={
        datetime: Schema(
            parser=convert_to_timestamp,
            serializer=datetime.fromtimestamp
        )
    }
)


class IgnoreNoneValues(dict):

    def __init__(self, *args, **kwargs):
        args = list(filter(lambda x: x[1] is not None, args[0]))
        super().__init__(args, **kwargs)


class BaseModel:

    @classmethod
    def make(cls, **data):
        return factory.load(data, cls)

    def to_dict(self):
        return asdict(self)


class WithoutNoneSerializebleModel:
    def to_dict(self):
        '''
            Сериализует датакласс в словарь, исключая поля со значением None
        '''
        return asdict(
            datetime_to_timestamp_factory.load(asdict(self), self.__class__), dict_factory=IgnoreNoneValues
        )
