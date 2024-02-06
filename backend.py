#the logic for gifski and ffmpeg
import ffmpeg
import cv2
import os
import subprocess
import shutil

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

def create_gif(quality, fps, speed, video_resolution, scale, text, text_size, variant, font, location):
    # requires gifski on path, no gifski python so needed manually
    # also requires imagemagick to be installed, wand didn't suit my needs so not using it
    gifski_commands(scale, video_resolution)
    if text != "" and speed == "1":
        file_in = ffmpeg.input("output.mp4")
        file_out = ffmpeg.output(file_in, "frame%04d.png")
        file_out.run()
        for image in os.listdir("."):
            if (image.endswith(".png")):
                if variant == "on_image":
                    subprocess.run(f"convert {image} -gravity {location} -pointsize {text_size} -font {font} -fill white -stroke black -strokewidth 3 -annotate +0+0 '{text}' text-{image}",shell=True)
                if variant == "above_image":
                    print("not implemented")
        gifski_commands(scale, video_resolution, text)
        shutil.move("text-gif.gif", "../text-gif.gif")
    elif text != "" and speed != "1":
        # if speed is used, gifski reconversion for better quality doesnt work (doesn't respect the set speed) so imagemagick is used directly instead
        # this results in slight artifacting however idc
        subprocess.run(f"convert gif.gif -gravity {location} -pointsize {text_size} -font {font} -fill white -stroke black -strokewidth 3 -annotate +0+0 '{text}' text-gif.gif",shell=True)
        shutil.move("text-gif.gif", "../text-gif.gif")
    shutil.move("gif.gif", "../gif.gif")
    shutil.move("output.mp4", "../output.mp4")
    os.chdir("../")
    shutil.rmtree("temporary-directory/")

def gifski_commands(scale, video_resolution = "0", text = ""):
    width, height = video_resolution.split("x")
    if not scale and text == "":
        subprocess.run(f"gifski --quality={quality} --fast-forward={speed} --fps={fps} -o gif.gif output.mp4",shell=True)
    elif scale and text == "":
        subprocess.run(f"gifski --quality={quality} --fast-forward={speed} --fps={fps} --width={width} --height={height} -o gif.gif output.mp4",shell=True)
    elif not scale:
        subprocess.run(f"gifski --quality={quality} --fps={fps} -o text-gif.gif text-*.png",shell=True)
    else:
        subprocess.run(f"gifski --quality={quality} --fps={fps} --width={width} --height={height} -o text-gif.gif text-*.png",shell=True)

if __name__ == "__main__":
    filepath = r"/home/angry/Media/testvideo.mkv"
    subtitle_track = "" #stars from 0
    audio_track = 3 #starts from 0
    start_time = "00:14:23.00"
    end_time = "00:14:30.00"
    video_resolution, fps = get_video_information(filepath)
    os.mkdir("temporary-directory")
    os.chdir("temporary-directory")
    trim_and_encode(filepath, subtitle_track, audio_track, start_time, end_time, video_resolution)
    quality = 100
    speed = 2
    scale = False # whether to keep the gif to the original resolution
    text = "TEST"
    text_size = 100 # pointsize imagemagick
    variant = "on_image" # above or on image
    font = "Impact" # font on system
    location = "North" # gravity imagemagick
    create_gif(quality, fps, speed, video_resolution, scale, text, text_size, variant, font, location)