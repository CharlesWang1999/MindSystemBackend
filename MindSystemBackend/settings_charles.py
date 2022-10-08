from .settings_common import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mind_system_mysql_db',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'www11830'
    }
}

KINECT_RECORD = False
CAMERA_RECORD = False
CAMERA_ID = 0
FAKE_FME = True
