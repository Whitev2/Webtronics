[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=WebTronics&size=40&pause=1000&color=F7F7F7&width=435&lines=The+WebTronics)](https://git.io/typing-svg)

## Used technology
- Python 3.11-buster;
- FastApi ( Web framework for building APIs );
- Docker and Docker Compose ( containerization );
- PostgreSQL ( database );
- SQLAlchemy ( working with database from Python );
- Alembic ( database migrations made easy );
- Pydantic ( models )

<hr/>

![image](templates/img.png)

<hr/>

### Установка и запуск

1. Клонировать проект в удобное место:

```sh
git clone https://github.com/Whitev2/Webtronics.git
```

2. Собрать и запустить контейнеры:
```sh
docker-compose up -d --build
```

3. Создать миграции баз:
```sh
docker-compose exec app alembic upgrade head
```
#### Остановка контейнеров:
```sh
docker-compose down -v
```
#### Запуск контейнеров:
```sh
docker-compose up
```


<hr/>


### Миграции

```sh
docker-compose exec app alembic revision --autogenerate -m "name"
```

```sh
docker-compose exec app alembic upgrade head
```

<hr/>

### API:  Регистрация и аунтификация

#### POST [/sign-up]() - Регистрация пользователя
#### POST [/sign-in]() - Аунтификация пользователя







