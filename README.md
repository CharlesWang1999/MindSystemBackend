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

**Windows**

[click here to learn how to activate virtualenv](https://blog.csdn.net/weixin_38346042/article/details/108944235)

Then fllow the step 7-9. (maybe use pip instead of pip3)

## How to Strat This Project
1. clone
2. cd root dir
3. ```python3 manage.py runserver 0.0.0.0:8080```
4. open browser and goto: http://localhost:8080

## Develop steps
Try to move ARPictureBook from node server to Django. --via. Charles 2022/08/07