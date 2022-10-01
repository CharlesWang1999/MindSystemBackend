import webbrowser
import os, sys

template_html_path = os.path.dirname(__file__) + '/template.html'
temp_html_path = os.path.dirname(__file__) + '/temp.html'


def play(video_path: str):
    _replace_video_path(video_path)
    # Open URL in new window, raising the window if possible.
    webbrowser.open_new(temp_html_path)


def _replace_video_path(video_path: str):
    template = open(template_html_path, "rt")
    data = template.read()
    template.close()
    data = data.replace('VIDEO_PATH', video_path)
    tempHTML = open(temp_html_path, "wt")
    tempHTML.write(data)
    tempHTML.close()


if __name__ == '__main__':
    print('@25---', sys.argv)
    if len(sys.argv) != 2:
        print('error num argvs')
        sys.exit()
    video_name = sys.argv[1]
    play('VideoSource/' + video_name)
    # play('absolute\\video\\path.mp4')
