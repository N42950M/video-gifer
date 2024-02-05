#the logic for gifski and ffmpeg
import ffmpeg
import cv2
import os

def get_resolution(filepath):
    video_opencv = cv2.VideoCapture(filepath)
    height = round(video_opencv.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = round(video_opencv.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_opencv.release()
    video_resolution = f"{width}x{height}"
    return video_resolution

def trim_and_encode(filepath, subtitle_track, audio_track, start_time, end_time, video_resolution):
    #takes a file, cuts it from a certain time and reencodes
    if subtitle_track != "":
        file_in = ffmpeg.input(filepath)
        video = file_in.video.filter('subtitles', filepath, video_resolution, None, False, "UTF-8", subtitle_track)
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
    else:
        file_in = ffmpeg.input(filepath)
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

if __name__ == "__main__":
    filepath = r"/home/angry/Media/test2.mkv"
    subtitle_track = 0 #stars from 0
    audio_track = 0 #starts from 0
    start_time = "00:14:23.00"
    end_time = "00:14:30.00"
    video_resolution = get_resolution(filepath)
    os.mkdir("temporary-directory")
    os.chdir("temporary-directory")
    trim_and_encode(filepath,subtitle_track,audio_track,start_time,end_time, video_resolution)