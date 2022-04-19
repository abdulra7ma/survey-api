# survey-api
Survey api is backend API that has been developed using DRF. 

## INSTALLATION PROCESS
Running an instance of this backend won't be a big thing if proceeded steps will be followed carefully.

## -> Regular Method
------------------------
1. initialize git and clone the project `work` branch
```
git init
git clone -b work  git@gitlab.com:gd-services/isayfly.com-backend.git
```
2. initialize virtual environment using pipenv and install requirements
```
pipenv install
pipenv install -r requirements/development.txt
```
3. create app migrations and apply it
```
python manage.py makemigrations account survey
python manage.py migrate
```
4. create a django super user
```
python manage.py createsuperuser
```
5. run server
```
python manage.py runserver
```

** Regular Method is the using uri of 127.0.0.1 with port 8000 

## -> Docker Method
------------------------
1. check the docker version
```
docker version
```
if the command output are not clear please make sure that you have installed docker on your development machine

2. start docker container
```
sudo docker-compose up
```

** Docker Method is the usin uri of 0.0.0.0 with port 8000
** if you are going to use the docker method. you got to uncomment the postgres settings in the core/settings/development.py

* if you have correctly followed the installation setup, you are going to have a running instance of our project.

## API Docementation
This API facilitate the user interaction with API endpoints via an interface called Swagger.
To access the swagger web interface you could to run an instance of this backend and hit the endpoint of "127.0.0.1/swagger/" if your are using thr regular installation method, but if you are using the docker installation than you have to hit this endpoint "0.0.0.0/swagger/"

## **NOTE**

In this project we have used `pipenv` as our main python virtual environment. So we highly recommand you to use it as your `venv`.
