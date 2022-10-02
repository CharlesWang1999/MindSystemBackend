import os
from django.conf import settings
from ARPictureBook.models import (
    AnswerResult,
    UserAnswerInfo,
    FinalResult
)


class MicroExpressionAnalysis:
    def __init__(self):
        pass

    def analysis(self, video_path, uaid, page_round, round_num):
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

        fp = open('FMEDetection/output/result.txt', 'r')
        fme_result = fp.readlines()[-1].strip().split(':')[-1]
        print('@27---', uaid, page_round, round_num)
        user_answer_info = UserAnswerInfo.objects.filter(pk=uaid).first()
        final_result_queryset = FinalResult.objects.filter(
            answer_info=user_answer_info,
            page_round=page_round,
            round_num=round_num
        )
        final_result = None
        if final_result_queryset:
            final_result = final_result_queryset.first()
        else:
            final_result = FinalResult(
                answer_info=user_answer_info,
                page_round=page_round,
                round_num=round_num
            )
        final_result.micro_expression_detection_result = fme_result
        final_result.save()
        # answer_result = AnswerResult.objects.filter(
        #     answer_info=user_answer_info,
        #     page_name=page_name,
        #     question_num=question_num
        # ).first()
        # if not answer_result:
        #     answer_result = AnswerResult(
        #         answer_info=user_answer_info,
        #         page_name=page_name,
        #         question_num=question_num
        #     )
        # answer_result.micro_expression_detection_result = fme_result
        # answer_result.save()
        
        # if start_id is not None:
        #     start_id = int(start_id)
        #     start_page = StartPageResult.objects.filter(id=start_id).first()
        #     micro_expression_result = MicroExpressionDetectionResult.objects.filter(
        #         start_page_result=start_page,
        #         page_name=page_name,
        #         question_num=question_num
        #     )
        #     if micro_expression_result:
        #         micro_expression_result = micro_expression_result.first()
        #         micro_expression_result.detection_result = fme_result
        #     else:
        #         micro_expression_result = MicroExpressionDetectionResult(
        #             start_page_result=start_page,
        #             page_name=page_name,
        #             question_num=question_num,
        #             detection_result=fme_result
        #         )
        #     micro_expression_result.save()
        print('@22---', fme_result)
        print(f'Micro expression analysis {video_path} finish')
        return analysis_result


if __name__ == '__main__':
    # video_path = ""
    # microExpressionAnalysis = MicroExpressionAnalysis()
    # analysisResult = microExpressionAnalysis.analysis(video_path)
    # print(analysisResult)
    # with open('FMEDetection/output/log.txt', encoding='utf-8') as file:
    #     content = file.read()
    # # for line in content:
    # #     print(line)
    # print(content)
    fp = open('FMEDetection/output/result.txt', 'r')
    print('@22---', fp.readlines()[-1].strip().split(':')[-1])
