# project_zai

## Flake8 (PEP8) lint

```shell
flake8 --ignore E701,E501,E704 puppy_shelter/
```

## Docker

```shell
docker-compose build
docker-compose up db -d
# poczekac az db sie zrobi
docker-compose logs db -f
docker-compose up djangoapp -d
# http://localhost:8001/api
# migracje i superuser
docker-compose exec djangoapp python manage.py migrate
docker-compose exec djangoapp python manage.py createsuperuser
# testy
docker-compose exec djangoapp pytest -vvv

# !!! na api dodac grupe "employees" !!!

# klikac REST'a na testowajce ;)

# zatrzymanie srodowiska docker
docker-compose down
```

## Tworzenie userow i adopterow

Dodajemy usera

Dodajemy adopter'a dla tego usera (!!! jeden user moze miec tylko jednego adoptera 1:1 !!!)

Jesli pracownik (employee)
* dodajemy mu grupe employee
* nie koniecznie dodajemy adopter'a dla tego usera (pracownik nie musi byc adopterem, ale zwykly user tak)
