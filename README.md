# Used technology
- Python 3.11-buster;
- FastApi ( Web framework for building APIs );
- Docker and Docker Compose ( containerization );
- PostgreSQL ( database );
- SQLAlchemy ( working with database from Python );
- Alembic ( database migrations made easy );
- Pydantic ( models )



### Installation

```sh
docker-compose build
```

```sh
docker-compose up
```



### Migrations

```sh
docker-compose exec backend alembic revision --autogenerate -m "name"
```

```sh
docker-compose exec backend alembic upgrade head
```
