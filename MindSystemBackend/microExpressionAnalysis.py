import os
from ARPictureBook.models import (
    UserAnswerInfo,
    FinalResult
)


class MicroExpressionAnalysis:
    def __init__(self):
        pass

    def analysis(self, video_path, uaid, page_round, round_num):
        print(f'Start micro expression analysis {video_path}')
        analysis_result = []
        output_path = '/home/FERMoudle/output/result.txt'
        log_path = '/home/FERMoudle/log/log.txt'
        checkpoint_path = '/home/FERMoudle/checkpoint/model_set_4.pth'
        docker_command = f'python3 /home/FERMoudle/main.py --video /home/FERMoudle/{video_path} --output {output_path} --log {log_path} --checkpoint {checkpoint_path}'
        command = f'docker exec -it FERMoudle {docker_command}'
        # command = 'pwd'
        # docker exec -it FMEDetection python3 /home/FMEDetection/FMEDetectionTest.py /home/FMEDetection/sub01-1.mp4 /home/FMEDetection/output
        # python3 FMEDetection.py VideoData/2022_09_03_23_32_17/camera_micro_expression.avi ./output
        os.system(command)

        fp = open('FERMoudle/output/result.txt', 'r')
        result_list = fp.readlines()[-1].strip().split(' ')[2:]
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
        final_result.happiness_prob = float(result_list[0].split(':')[-1])
        final_result.sadness_prob = float(result_list[1].split(':')[-1])
        final_result.neutral_prob = float(result_list[2].split(':')[-1])
        final_result.anger_prob = float(result_list[3].split(':')[-1])
        final_result.surprise_prob = float(result_list[4].split(':')[-1])
        final_result.disgust_prob = float(result_list[5].split(':')[-1])
        final_result.fear_prob = float(result_list[6].split(':')[-1])
        final_result.save()
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
    fp = open('FERMoudle/output/result.txt', 'r')
    result_list = fp.readlines()[-1].strip().split(' ')[2:]
    for item in result_list:
        print('97--', item.split(':')[0], item.split(':')[-1])
    print('@22---', result_list)
