import os


class ActionAnalysis:
    def __init__(self):
        # may start docker there (necessary?)
        pass

    def analysis(self, video_path):
        print(f'Start action analysis {video_path}')
        docker_command = f'python deploy/pphuman/pipeline.py --config deploy/pphuman/config/infer_cfg.yml --video_file={video_path} --device=cpu --enable_action=True'
        command = f'docker exec -it PaddleDetection {docker_command}'
        os.system(command)
        print(f'Action analysis {video_path} finish')


if __name__ == '__main__':
    video_path = ""
    micro_expression_analysis = ActionAnalysis()
    analysis_result = micro_expression_analysis.analysis(video_path)
    print(analysis_result)
