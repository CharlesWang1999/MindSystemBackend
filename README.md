# MindSystemBackend
MindSystemBackend


## Clone this project

It is recommended that you fork this project and then clone it for development.

## Create a python environment and install dependencies

It is recommended that you use Anaconda to create virtual environments.

python >= 3.7 is recommended

Run ```pip install -r requirements.txt``` to install dependencies.


## Install MySQL database

All versions may work, but we only tested on version 8.0.29.

After you have finished installing mysql, be sure to add the installation directory to your environment variables.

You can run ```mysql -uroot -p``` to confirm that the installation is complete.

Then run ```create databases <database_name>``` to create a new database where the recommended name for the ```<database_name>``` is ```mind_system_mysql_db```


## Install Docker

Download Docker Desktop on offical website.

Then run ```docker pull chamberharr/fmedetection:v1``` to pull the docker image.

Download file FERMoudle.7z in [Google Drive](https://drive.google.com/file/d/1zF7bt3Bi2pFf2i6mPnIPW2xzTcQvvlf5/view?usp=sharing) or [Baidu Netdisk](https://pan.baidu.com/s/1G9RpcxBcgPUvO6nFFAIFkw?pwd=v02b). Then unzip it to the project root directory.

Use docker run to create container from image.
```
docker run --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --volume=.\FERMoudle:/home/FERMoudle --volume=.\VideoData:/home/FERMoudle/VideoData --runtime=runc --name=FERModule -dit chamberharr/fmedetection:v1
```
**Hint: --volume is based on your system.**

Then run ```docker start FERModule``` to start the container.

## Start Django server

1. Create a file ```settings_<your_name>.py``` in MindSystemBackend folder. You can reference ```settings_yuji.py``` and [Tutorial](./doc/Mysql_FME.md). Change the database configuration information.
2. Make a Symbolic link ```settings.py``` to ```settings_<your_name>.py```. E.g.```ln -snf settings_<your_name>.py settings.py``` for Linux/MacOSX. ```mklink settings.py settings_<your_name>.py``` for Windows CMD. ```New-Item -ItemType SymbolicLink -Path settings.py -Target .\settings_<your_name>.py``` for Windows Terminal.
3. Run ```python manage.py migrate``` to migrate the database.
4. Run ```python manage.py createsuperuser```, then create a user. If raise python exception, please modify the error line from ```query = query.decode(errors='replace')``` to ```query = query.encode(errors='replace').decode(errors='replace')```
5. Run ```python manage.py runsslserver 0.0.0.0:8080```
6. The main page url of this project is https://localhost:8080/ARPicture/login/
7. Use superuser to login.
8. Django databases page url is https://localhost:8080/admin/. You can create new user here.


## Test the system
1. Check your phone/pad is at the same local network with your server.
2. Use your phone/pad visit https://x.x.x.x:8080
3. Login and follow the prompt message.


----


## This is old readme version, for reference only.

**Hint: Based on Linux/MacOSX**
1. ```pip3 install virtualenv```
2. ```mkdir -p /app/ENV/```
3. ```cd /app/ENV```
4. ```virtualenv django-2.2-tutorial```
5. ```source django-2.2-tutorial/bin/activate```
6. (now you should see django-2.2-tutorial in the prompt, meaning you are inside the virtualenv)
7. ```pip3 install django==2.2.27```
8. ```pip3 install pylint #make sure use the pylint in virtualenv would be used```
9. ```pip3 install pylint-django```
10. ```pip3 install django-sslserver``` (add at 2022/08/08 to run ssl server)

**Windows**

[click here to learn how to activate virtualenv](https://blog.csdn.net/weixin_38346042/article/details/108944235)

Then fllow the step 7-10. (maybe use pip instead of pip3)

## How to Strat This Project
**Hint: May use ```python``` instead of ```python3``` command if show error in Windows**
1. clone
2. cd root dir
3. if this is first time to start project or have change the database, try ```python3 manage.py makemigrations``` and ```python3 manage.py migrate```
4. ```python3 manage.py runserver 0.0.0.0:8080```
5. open browser and goto: http://localhost:8080

## How to Run SSL server
1. activate the virtualenv
2. ```pip/pip3 install django-sslserver```
3. ```python3 manage.py runsslserver 0.0.0.0:8080```
4. open browser and goto: https://localhost:8080
5. check your ip and use other device in same LAN and goto: https://x.x.x.x:8080

## Where to find url
1. find the file MindSystemBackend/urls.py
2. find the include file in url patterns. e.g.:ARPictureBook.urls
3. find the url pattern in the file of step 2.
4. concat the final url. e.g.: localhost:8080/ARPicture/start

## Use Django Admin see models
1. The admin site is http(s)://localhost:8080/admin
2. Create super user in terminal by use command ```python3 manage.py createsuperuser```
3. Create your own model in file models.py
4. Registe your model in file admin.py
5. Login admin site, then you can see all your registed model there.

## Develop steps
1. Try to move ARPictureBook from node server to Django. --via. Charles 2022/08/07
2. Finish add start page, try to add second and third page, code review today later. --via. Charles 2022/08/08 morning
3. Finish add second and third page, code review, find mobile phone must use ssl server to use camera. --via. Charles 2022/08/08 night
4. Try to use ajax to send data from frontend to backend, quick demo. Use UnderScoreCase in backend, keep CamelCase in frontend. --via. Charles 2022/08/09
5. Create models to save the query result. --via. Charles 2022/08/11
6. Finish save result logic. --via Charles 2022/08/12




