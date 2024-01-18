#the logic for gifski and ffmpeg
import ffmpeg
import cv2

def trim_and_encode(filepath, subtitle_track, audio_track, start_time, end_time):
    #takes a file, cuts it from a certain time and reencodes
    if subtitle_track != "":
        #video = cv2.VideoCapture(filepath)
        #height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        #print(f"{width}x{height}")
        #going to make a function later to determine the different resolutions for this https://ffmpeg.org/ffmpeg-utils.html#video-size-syntax, manually set for testing
        file_in = ffmpeg.input(filepath)
        video = file_in.video.filter('subtitles', filepath, "ntsc", "", False, "", subtitle_track)
        audio = file_in[f'a:{audio_track}']
        file_out = ffmpeg.output(
            video,
            audio,
            "output.mp4", 
            **{"codec:v": "libx264"}, 
            **{"codec:a": "copy"}, 
            crf=15, 
            preset="ultrafast", 
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
            preset="ultrafast", 
            ss=start_time,
            to=end_time
        )
        file_out.run()

if __name__ == "__main__":
    filepath = r"/home/angry/Downloads/testvideo.mkv"
    subtitle_track = 3 #stars from 0
    audio_track = 3 #starts from 0
    start_time = "00:00:23.790"
    end_time = "00:00:27.494"
    trim_and_encode(filepath,subtitle_track,audio_track,start_time,end_time)