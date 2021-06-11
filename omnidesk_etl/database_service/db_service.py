from omnidesk_etl.db_models import (
    cases as cases_table,
    case_label as case_label_table,
    lables as lables_table,
    metadata
)
import logging


logger = logging.getLogger(__name__)


class DbService:

    def __init__(self, engine):
        self.engine = engine

    def clear_db(self):
        logger.info('Очистка базы данных')
        with self.engine.connect() as connection:
            with connection.begin():
                for table in metadata.sorted_tables:
                    connection.execute(table.delete())
        logger.info('База данных успешно очищена')

    def load_cases(self, cases):

        logger.info('Загрузка обращений начата')

        cases_lables = [
            lable
            for case in filter(lambda x: bool(x.labels_objects), cases)
            for lable in case.labels_objects
        ]

        with self.engine.connect() as connection:
            with connection.begin():
                connection.execute(cases_table.insert(), [case.to_dict() for case in cases])
                connection.execute(case_label_table.insert(), [case_lable.to_dict() for case_lable in cases_lables])
        logger.info('Загрузка обращений завершена')

    def load_lables(self, lables):
        logger.info('Обновление меток начато')
        with self.engine.connect() as connection:
            with connection.begin():
                connection.execute(lables_table.insert(), [lable.to_dict() for lable in lables])
        logger.info('Обновление меток завершено')
