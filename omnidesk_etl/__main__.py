import config
from dateutil import parser as datetime_parser
import sqlalchemy
from omnidesk_etl.http_client import HttpClient
from omnidesk_etl.omnidesk_service import OmnideskService
from omnidesk_etl.models.filter import CaseFilter
from omnidesk_etl.database_service import DbService
import click
import sys
import logging


logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s %(message)s')
logging.getLogger('requests').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


omnidesk_service = OmnideskService(
    HttpClient(
        config.AppConfig.OMNIDESK_API_URL,
        config.AppConfig.USER,
        config.AppConfig.TOKEN,
    )
)

db_service = DbService(
    sqlalchemy.create_engine(
        config.AppConfig.STORAGE_DB_URL
    )
)

@click.command()
@click.option('--from_time', help='Дата, с которой нужно взять обращения', required=True)
def main(from_time):
    logger.info('Начало загрузки')
    try:
        from_time = datetime_parser.parse(from_time)
    except Exception:
        click.echo('Неверный формат даты, нужно %Y-%m-%d')
        sys.exit()

    cases = omnidesk_service.get_cases(CaseFilter(from_time=from_time))
    lables = omnidesk_service.get_labels()

    try:
        db_service.clear_db()
        db_service.load_cases(cases)
        db_service.load_lables(lables)
    except sqlalchemy.exc.OperationalError:
        print()
        click.echo('Загрузка не удалась')
        click.echo('Перед запуском выполните команды для подготовки бд')
        click.echo('alembic init')
        click.echo('alembic upgrade head')
        sys.exit()

    logger.info('Загрузка завершена')


if __name__ == '__main__':
    main()
