# MindSystemBackend
MindSystemBackend
## How to Start Django Environment
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

## Develop steps
1. Try to move ARPictureBook from node server to Django. --via. Charles 2022/08/07
2. Finish add start page, try to add second and third page, code review today later. --via. Charles 2022/08/08 morning
3. Finish add second and third page, code review, find mobile phone must use ssl server to use camera. --via. Charles 2022/08/08 night