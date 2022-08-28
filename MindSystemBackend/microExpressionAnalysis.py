class MicroExpressionAnalysis:
    def __init__(self):
        pass

    def analysis(self, video_path):
        print(f'Start micro expression analysis {video_path}')
        analysis_result = []
        print(f'Micro expression analysis {video_path} finish')
        return analysis_result


if __name__ == '__main__':
    video_path = ""
    microExpressionAnalysis = MicroExpressionAnalysis()
    analysisResult = microExpressionAnalysis.analysis(video_path)
    print(analysisResult)
