import webbrowser
import os

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
    play('VideoSource/sub01-1.mp4')
    # play('absolute\\video\\path.mp4')
