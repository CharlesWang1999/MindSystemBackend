from .settings_common import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mind_system_mysql_db',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'syjmysql'
    }
}

KINECT_RECORD = False
CAMERA_RECORD = False
# KINECT_RECORD = True
# CAMERA_RECORD = True
CAMERA_ID = 0
FAKE_FME = False
