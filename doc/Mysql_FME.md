# Mysql及微表情识别相关说明

9月4日的commit之后，原有项目可能出现无法运行的情况，需要做一些相关配置。

首先进到虚拟环境下重新执行一遍 ``pip install -r requirements.txt``

这次提交迁移了原来的settings.py文件到settings_common.py，然后根据每个人情况对settings_common进行继承重写，参考我的配置文件：``settings_charles.py``。然后将settings.py软链接到个人配置文件实现每个人不同的需求，避免调试时频繁注释代码。

[Windows如何配置软链接](https://blog.csdn.net/m0_51977577/article/details/125416891)

Linux/MacOSX: ``ln -snf settings_xxx.py settings.py``

字段配置说明：

1. KINECT_RECORD: 默认False。Ture则使用kinect录制视频并进行动作识别流程，False则禁用动作识别流程。
2. CAMERA_RECORD: 默认False。Ture则使用摄像头录制视频并进行微表情识别流程，False则禁用微表情识别流程。
3. CAMERA_ID: 默认0。调用摄像头的id，根据个人电脑条件不同动态配置
4. FAKE_FME: 默认False。True则调用假的表情识别代码，加快调试速度，False则会调用真正的表情识别代码。

## 关于Mysql

建议去官网或者清华镜像源等地方下载mysql，[参考链接](https://blog.csdn.net/weixin_43423484/article/details/124408565)。我的版本是8.0.29，供参考。

下载安装配置完之后 ``mysql -uroot -p`` 然后输入自己设定的密码进入数据库。

先 ``show databases``测试一下数据库是否正常，如果正常显示一些默认的数据库，执行 ``create database mind_system_mysql_db``创建一个新的数据库，最后的名字可以自定义，我这里写的是我的数据库名，为了方便可以与我相同。

如果没有报错的话说明数据库创建成功，回到项目的MindSystemBackend目录下，找到settings_charles.py文件，这是我个人的配置信息，建议复制一份然后以自己的名字作为后缀，将settings.py 文件软链接到自己新建的settings_xxx.py文件。然后在DATABASE的字典里把 NAME/USER/PASSWORD字段换成自己的信息，命令行内跑一遍 ``python3 manage.py migrate``对数据库进行迁移完成后即可恢复正常启动程序。

## 关于微表情识别

news: 最新版本已经替换为了FERModule，下方具体路径谨慎参考。

昨天（2022/09/03）晚上我把项目文件的压缩包放在了群里，下载完解压后放在本项目的根目录下，建议命名为FMEDetection，然后手动在该目录下再新建一个output文件夹。

docker image 拉取命令： ``docker pull chamberharr/fmedetection:v1``

在docker desktop界面的images tab上找到对应的image，点击run，展开optional settings，container name设置为FMEDetection。

下方Volumes需要挂载两个文件夹：

1. 将本地根目录下的FMEDetection文件夹挂载到docker内的 ``/home/FMEDetection``
2. 将本地根目录下的VideoData文件夹挂载到docker内的 ``/home/FMEDetection/VideoData``

container启动完毕后，在命令行中执行 ``docker exec -it FMEDetection bin/bash``

查看是否能够正常进入容器。正常进入后 ``cd /home/FMEDetection``,查看是否映射出来了对应的文件。

如果有相应文件则执行 ``python3 FMEDetection.py ./sub01-1.mp4 ./output``测试能否正常输出文件，如果没有问题则配置完成。在settings里将CAMERA_RECORD/CAMERA_ID/FAKE_FME配置完成后即可正常启动表情识别流程。
