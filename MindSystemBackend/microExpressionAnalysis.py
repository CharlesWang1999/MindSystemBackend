import os
from django.conf import settings


class MicroExpressionAnalysis:
    def __init__(self):
        pass

    def analysis(self, video_path):
        print(f'Start micro expression analysis {video_path}')
        print('@11--', settings.FAKE_FME)
        detection_file = 'FMEDetectionTest.py' if settings.FAKE_FME else 'FMEDetection.py'
        analysis_result = []
        docker_command = f'python3 /home/FMEDetection/{detection_file} /home/FMEDetection/{video_path} /home/FMEDetection/output'
        command = f'docker exec -it FMEDetection {docker_command}'
        # command = 'pwd'
        # docker exec -it FMEDetection python3 /home/FMEDetection/FMEDetectionTest.py /home/FMEDetection/sub01-1.mp4 /home/FMEDetection/output
        # python3 FMEDetection.py VideoData/2022_09_03_23_32_17/camera_micro_expression.avi ./output
        os.system(command)
        print(f'Micro expression analysis {video_path} finish')
        return analysis_result


if __name__ == '__main__':
    video_path = ""
    microExpressionAnalysis = MicroExpressionAnalysis()
    analysisResult = microExpressionAnalysis.analysis(video_path)
    print(analysisResult)
