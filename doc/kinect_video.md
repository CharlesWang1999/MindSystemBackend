# 视频，Kinect录制，动作识别部署文档

本文档将对视频，Kinect录制，动作识别接入等模块进行粗略讲解分析，包含部署步骤，注意事项，实现原理等等，力求在阅读完本文档后，能够快速跑通这三个模块的功能，并且具备一定的调试，改动能力。

注：一定要在成功运行AR项目的基础上再阅读本文档，本文假定已经安装了requirements.txt里的所有依赖项，具体来说，请确保在环境中执行过：

```shell
pip install -r .\requirements.txt
```

## 视频录制

视频录制模块主要的任务是用摄像头拍摄视频并记录在指定目录文件中，主要使用包装了`opencv`库，在`requirements.txt`里应有所体现。

若想使用`VideoRecord`类，需要为`VideoRecord`指定一个`record_camera_id`，这是一个从$0$开始的整数值，用于寻找计算机上拥有的摄像头进行绑定，通常情况下需要自己试出来，如果只有一个摄像头则是$0$，否则加$1$尝试。初始化结束后，调用`start_record`方法并指定视频存储路径（一定要确保目录存在）开始录制，调用`stop_record`结束录制。

videoRecord.py内部提供了**一段简单的测试调试代码**，取消掉`_record_thread`方法中的注释后，直接运行改文件，如果弹出一个一卡一卡的界面展示摄像机拍摄的画面，那就说明运行成功，可以在命令行按下回车结束录制，并且生成一个`test.avi`的视频文件，可以打开观看。如果指定的`record_camera_id`没有找到对应的摄像头，在命令行会有失败的信息输出。匹配摄像头有时候会花费较长时间，这倒是正常的，只要没有失败信息输出，就是正在匹配了，请耐心等待。**`_record_thread`的注释掉的代码会阻塞进程进行绘制操作，影响视频录制，因此在请在调试结束后及时再注释掉。**

VideoRecord的主要工作原理是：开始录制时，启动一个子线程`_record_thread`，在其中不断循环访问摄像头获得一帧数据，并存储起来。

## Kinect录制

Kinect是微软推出的一个可用于动作捕捉，跟踪的设备，可以录制视频，识别骨骼信息，记录生成深度图等信息。我们手中的版本是Kinect v2，早在2017年停止生产，相关支持也已经停止（因此会有较多坑）。经由讨论，我们暂时只用这台Kinect做视频录制的功能，虽然仅是如此，但是跑通Kinect的代码并进行使用，对之后的扩展开发应该会提供一定的帮助。

Kinect v2在python语言里提供的开发工具是[PyKinect2](https://github.com/Kinect/PyKinect2)，可以在它们的文档中找到前期准备与测试代码，可以作为参考，理论上应该是跑不通的（要是跑通的话下面这段可以跳过（真的有可能吗？））。PyKinect2在停止维护时还处在Python2时期，一些依赖的第三方包和Python方法还是Python2时期的，需要进行调整，代码里甚至还对版本做了检查，阅读后发现是毫无意义的，只会卡住流程……

在requirements.txt里的是一组已经调整过的第三方依赖包，应该不会出问题，然后，需要安装[Kinect for Windows SDK 2.0](https://www.microsoft.com/en-us/download/details.aspx?id=44561)，官方下载安装即可，可以参考[这个视频](https://www.youtube.com/watch?v=GehUgGG9Z-U)，确定Kinect正确连接，需要注意的是请一定要使用USB3.0的接口，然后如果连不上的话重启几次，Kinect有时候就是不太稳定。接下来找到PyKinect2的源码，删掉替换成我修改过的这两个，在KinectFix这个文件里，`PyKinectV2.py`和`PyKinectRuntime.py`，理论上不用pip安装PyKinect而是直接用这两个文件也没啥大问题，不过懒得试了。好奇的话可以比对一下我都修改了些啥，也不是很多。

接下来可以用PyKinect2提供的示例游戏[PyKinectBodyGame](https://github.com/Kinect/PyKinect2/blob/master/examples/PyKinectBodyGame.py)，或者`kinectRecord`做测试。如果使用`kinectRecord`做测试的话，与`VideoRecord`类似，我也**提供了测试调试代码**，使用方式也是取消注释后直接运行Python文件，如果运行正常的话也会弹出一个一卡一卡的界面展示摄像机拍摄的画面，那就说明运行成功，可以在命令行按下回车结束一次录制（之前为了测试写成了死循环立刻开启下一次拍摄），并且生成一个`kinect.avi`的视频文件，可以打开观看。画面前几帧可能是黑色的，这也是Kinect的不稳定，如果确定Kinect连接无误后，请耐心等几分钟，这种情况在第一次录制时会有可能出现，使用时也务必注意。**相关代码也请务必在调试成功后注释掉**。

与VideoRecord相似，KinectRecord的主要工作原理也是在一个子线程里死循环访问Kinect获得数据，存起来，不过用的是Kinect那边的接口。

需要说明的是，Kinect除了彩色画面，还会有其他数据的录制，在源文件里可以看到更多类型的接口，或者在PyKinectBodyGame里找到使用示例，我之前试着把骨骼信息绘制到了视频里，后来不需要就删了，后续如果有需要的话可以再实现一下。然后KinectRecord录制的视频理论上会比VideoRecord录制视频短一些，这是因为Kinect得到一帧数据后需要进行处理，并且Kinect还要花精力录制额外的内容，因此它的实际帧率是低一些的，不如OpenCV原本包装的那样高效，但是存的时候用了同样的帧率，因此Kinect就更短一些，但就我们的应用场景而言，这个差异理应不会造成太大的问题。

## 动作分析

这块就更复杂一些，相应的环境更苛刻。董磊学长使用了PaddlePaddle的[PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.4/deploy/pphuman)框架进行二次开发，为了兼容性与实际项目搭建的便携性，整个框架使用了Docker进行搭建，ActionAnalysis模块的实现也是基于此。

先简单说一下Docker这个东西，对之后的环境配置理解起来也会更轻松些，当然还是建议速成一下，不会很困难。他与Python的venv以及Conda类似，都是提供一个虚拟环境，起到不污染系统，提供尽可能一致的运行环境的作用。venv的方案是限制在pip与python的，他只能在固定的python版本下指定pip支持的第三方包，并提供requirements.txt来同步环境，想换python版本需要在电脑上安装对应的版本。Conda则更进一步，他甚至支持python版本的指定，可指定更广阔的的conda包管理，相较venv而言更加灵活，用于配置除python以外的环境中也是没问题的。

而Docker则更底层一些，他相对而言更接近与虚拟机的概念，可以通过镜像进行分享，同步，认为是在运行了一个虚拟系统应该更容易接受一些，但是效率方面Docker要高很多，他只跑需要的那一部分。一台计算机上可以同时跑多个Docker环境，甚至可以嵌套，并列，相互通信等。然后Docker还支持本地目录挂载到Docker中，实现文件共享，通过命令行调用Docker环境内部的命令。对于我们可能有两个不一定兼容的复杂环境的需求（动作分析和微表情分析实在两个不同的框架下完成的）来说，Docker无疑是最佳且唯一可行的方案了。

请在大致安装使用了Docker的基本功能后，再往下看我们需要进行的环境配置。

[PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.4/deploy/pphuman)官方提供了一个[Docker镜像](https://hub.docker.com/r/paddlecloud/paddledetection)，可以查文档看到，推荐使用GPU的最新版本。

启动容器时，请确保容器名为**PaddleDetection**，如果有改动请也在代码里进行修改。

接下来我们需要三个文件夹：

* **PaddleDetectionModel**：PaddleDetection训练好的模型，整个框架会根据这个模型进行识别，董磊学长之后会替换成他那里训练出来的模型，现在请下载并解压官方的[所有模型](https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.4/deploy/pphuman#1-%E6%A8%A1%E5%9E%8B%E4%B8%8B%E8%BD%BD)到改文件。在本地的位置无所谓，在Docker内部请挂载到`/home/PaddleDetection/output_inference`
* **VideoData**：存储录制视频的文件夹，是动作分析模块的输入。本地应该和ARPictureBook以及MindSystemBackend在同一目录下，在Docker内部请挂载到`/home/PaddleDetection/VideoData`
* **PaddleDetectionOutput**：PaddleDetection的输出文件夹，目前只有视频，按照董磊学长的想法，之后应该会增加文本文件的输出。在本地的位置无所谓，在Docker内部请挂载到`/home/PaddleDetection/output`。

想要测试Docker内的框架是否正常工作的话，请使用[官方提供的命令](https://github.com/PaddlePaddle/PaddleDetection/tree/release/2.4/deploy/pphuman#3-%E9%A2%84%E6%B5%8B%E9%83%A8%E7%BD%B2)在Docker中运行，指定输入视频，查看输出结果（如果终端里有进度输出的话基本上就没问题）。

上文也有提到，Docker支持在本地直接调用Docker内部的命令，即[docker exec](https://docs.docker.com/engine/reference/commandline/exec/)，请尝试在本地使用该命令调用Docker内部命令进行行为分析，ActionAnalysis的实现机制和这个过程类似，是使用python的系统包执行命令的方式，通过python调用系统命令行，执行docker exec命令的方式调用Docker内部的命令进行识别。
