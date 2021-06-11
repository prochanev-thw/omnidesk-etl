# omnidesk-etl
Разработка ETL для получения данных из сервиса omnidesk `https://omnidesk.ru/`

1. Скачать репозиторий
2. Активировать виртуальное окружение
3. Выполнить `pip install -r requirements.txt`
4. Создать файл `.env` в корне проекта, который будет содержать 2 переменные  
`
OMNIDESK_USER_EMAIL = <емеил, который использовался для регистрации в omnidesk>
OMNIDESK_TOKEN = <токен, который был получен в omnidesk>
`
Либо можно их добавить в переменные окружения перед запуском скрипта
в файле `develop.env` содержится шаблон, можно подсмотреть там.
5. В файле `config.py` присвоить переменной `OMNIDESK_API_URL` значение `https://[omnidesk-user].omnidesk.ru/api/`, где `omnidesk-user` имя пользователя omnidesk
6. Выполнить `alembic revision --autogenerate -m "create tables"` для создания необходимых таблиц.  будет создана sqllite база `cases.db` и скрипт миграции.
7. Накатить миграцию командой `alembic upgrade head`.
8. Сама загрузка запускается командой `python -m omnidesk_etl --from_time YYYY-MM-DD`  
параметр `--from_time` отвечает за то с какого момента будут загружаться обращения.
9. Данные сохранятся в базе sqllite `cases.db`. будут созданы таблицы
`cases - таблица с обращениями`
`labels - таблица с метками`
`case_label - связь между метками и обраащениями`
