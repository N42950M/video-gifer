#the logic for gifski and ffmpeg
import ffmpeg
import cv2
import os
import subprocess

def get_video_information(filepath):
    video_opencv = cv2.VideoCapture(filepath)
    height = round(video_opencv.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = round(video_opencv.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = video_opencv.get(cv2.CAP_PROP_FPS)
    video_opencv.release()
    video_resolution = f"{width}x{height}"
    return video_resolution, fps


def trim_and_encode(filepath, subtitle_track, audio_track, start_time, end_time, video_resolution):
    #takes a file, cuts it from a certain time and reencodes
    file_in = ffmpeg.input(filepath)
    if subtitle_track != "":
        video = file_in.video.filter('subtitles', filepath, video_resolution, None, False, "UTF-8", subtitle_track)
    else:
        video = file_in['v:0']
    audio = file_in[f'a:{audio_track}']
    file_out = ffmpeg.output(
        video,
        audio,
        "output.mp4", 
        **{"codec:v": "libx264"}, 
        **{"codec:a": "copy"}, 
        crf=15, 
        preset="veryslow", 
        ss=start_time,
        to=end_time
    )
    file_out.run()

def create_gif(quality, fps, speed, video_resolution, scale):
    # uses video instead of frames so speed can be applied
    if scale:
        width, height = video_resolution.split("x")
        subprocess.run(f"gifski --quality={quality} --fast-forward={speed} --fps={fps} --width={width} --height={height} -o gif.gif output.mp4",shell=True)
    else:
        subprocess.run(f"gifski --quality={quality} --fast-forward={speed} --fps={fps} -o gif.gif output.mp4",shell=True)


# def add_text(text, type):
#     print("hello")

if __name__ == "__main__":
    filepath = r"/home/angry/Media/testvideo.mkv"
    subtitle_track = 3 #stars from 0
    audio_track = 3 #starts from 0
    start_time = "00:14:23.00"
    end_time = "00:14:30.00"
    video_resolution, fps = get_video_information(filepath)
    os.mkdir("temporary-directory")
    os.chdir("temporary-directory")
    trim_and_encode(filepath, subtitle_track, audio_track, start_time, end_time, video_resolution)
    quality = 100
    speed = 2
    scale = False
    create_gif(quality, fps, speed, video_resolution, scale)