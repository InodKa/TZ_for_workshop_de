# TZ_for_workshop_de
Выполнение тестового задания для кандидата на Backend-практикум «От SQL до DWH»

### Загрузчик данных в PostgreSQL

Данное приложение использует открытый источник данных https://jsonplaceholder.typicode.com. Этот API возвращает список пользователей, постов и комментариев в формате JSON. Разработанное приложение выкачивает данные в JSON формате и сохраняет в экземпляре PostgreSQL.

#### Компоненты системы:
- Скрипт Python для загрузки данных
- База данных PostgreSQL

#### Структура файлов проекта

```
project/
├── README.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
│
├── app/
│   └── main.py
│
└── sql/
    └── init.sql
```
### Развертывание

- Клонируйте репозиторий командой ```git clone https://github.com/InodKa/TZ_for_workshop_de```
- Имя БД, логин и пароль уже указаны в файле docker-compose.yml 
- Запустите контейнеры ```docker-compose up -d --build```
- Вы можете посмотреть логи приложения. Для этого воспользуйтесь командой ```docker-compose logs -f app```
- Для просмотра логов базы данных используйте команду: ```docker-compose logs db```

Теперь вы можете подключиться к базе данных PostgreSQL через любой SQL-клиент (например, DBeaver) со следующими параметрами:

Host: localhost\
Port: 5432\
Database: mydb \
User: myuser\
Password: mypassword 

Или напрямую зайти в БД с помощью команды
```docker exec -it  <container-name> psql -U myuser -W mydb```\
Password: mypassword



