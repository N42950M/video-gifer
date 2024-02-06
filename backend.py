#the logic for gifski and ffmpeg
import ffmpeg
import cv2
import os
import subprocess
import shutil
from PIL import Image 

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

def create_gif(quality, fps, speed, video_resolution, scale, text, text_size, text_location, font):
    # requires gifski on path, no gifski python so needed manually
    # also requires imagemagick to be installed, wand didn't suit my needs so not using it
    width, height = video_resolution.split("x")
    gifski_commands(scale, width, height)
    if text != "" and speed == "1":
        file_in = ffmpeg.input("gif.gif")
        file_out = ffmpeg.output(file_in, "frame%04d.png")
        file_out.run()
        first = True
        firstimg = ""
        for image in os.listdir("."):
            if (image.endswith(".png")):
                if first:
                    firstimg = image
                    first = False
                    width, height = Image.open(firstimg).size
                imagemagick_commands(text_location, image, text_size, font, text, width)
        if text_location == "above_image":
            scale = True
            width, height = Image.open(f"text-{firstimg}").size
        gifski_commands(scale, width, height, text)
        shutil.move("text-gif.gif", "../text-gif.gif")
    elif text != "" and speed != "1":
        # if speed is used, gifski reconversion for better quality doesnt work (doesn't respect the set speed) so imagemagick is used directly instead
        image = "gif.gif"
        imagemagick_commands(text_location, image, text_size, font, text, width)
        shutil.move("text-gif.gif", "../text-gif.gif")
    shutil.move("gif.gif", "../gif.gif")
    shutil.move("output.mp4", "../output.mp4")
    os.chdir("../")
    shutil.rmtree("temporary-directory/")

def gifski_commands(scale, width = "0", height = "0", text = ""):
    if not scale and text == "":
        subprocess.run(f"gifski --quality={quality} --fast-forward={speed} --fps={fps} -o gif.gif output.mp4",shell=True)
    elif scale and text == "":
        subprocess.run(f"gifski --quality={quality} --fast-forward={speed} --fps={fps} --width={width} --height={height} -o gif.gif output.mp4",shell=True)
    elif scale:
        subprocess.run(f"gifski --quality={quality} --fps={fps} --width={width} --height={height} -o text-gif.gif text-*.png",shell=True)
    else:
        subprocess.run(f"gifski --quality={quality} --fps={fps} -o text-gif.gif text-*.png",shell=True)

def imagemagick_commands(text_location, image, text_size, font, text, width):
    match text_location:
        case "above_image":
            subprocess.run(f"magick {image} -background white -size {width}x -font {font} -pointsize {text_size} -gravity Center caption:\"{text}\" +swap -append text-{image}", shell=True)
        case "on_image":
            subprocess.run(f"magick {image} -gravity North -pointsize {text_size} -font {font} -fill white -stroke black -strokewidth 3 -annotate +0+0 \'{text}\' text-{image}",shell=True)
        case "above_image_speed":
            # subprocess.run(f"magick \"{image}[0]\" temp.png",shell=True)
            width, height = Image.open(image).size
            # subprocess.run(f"magick temp.png -background white -size {width}x -font {font} -pointsize {text_size} -gravity Center caption:\"{text}\" +swap -append captioned.png", shell=True)
            # width, height = Image.open("captioned.png").size
            subprocess.run(f"magick -size {width}x -background white -gravity center -font {font} -pointsize {text_size} caption:\"{text}\" -set option:HH %h +delete {image} -layers coalesce -resize {width}x -background None -gravity North -splice '0x%[HH]+0+0' NULL: -size {width} -background white -gravity center -font {font} -pointsize {text_size} caption:\"{text}\" -gravity North -compose Over -layers composite -layers optimize text-{image}", shell=True)

if __name__ == "__main__":
    filepath = r"/home/angry/Media/testvideo2.mkv"
    subtitle_track = "" #stars from 0
    audio_track = 0 #starts from 0
    start_time = "00:14:23.00"
    end_time = "00:14:30.00"
    video_resolution, fps = get_video_information(filepath)
    os.mkdir("temporary-directory")
    os.chdir("temporary-directory")
    trim_and_encode(filepath, subtitle_track, audio_track, start_time, end_time, video_resolution)
    quality = 100
    speed = "1"
    scale = True # whether to keep the gif to the original resolution
    text = "me when i code"
    text_size = "Default" # pointsize imagemagick
    text_location = "above_image" # above or on image
    font = "Default" # font on system
    match text_location:
        case "above_image":
            if font == "Default":
                font = "roboto-condensed-bold"
            if text_size == "Default":
                text_size = "100"
        case "on_image":
            if font == "Default":
                font = "impact"
            if text_size == "Default":
                text_size = "100"
    if text_location == "above_image" and speed != "1":
        text_location = "above_image_speed"
    create_gif(quality, fps, speed, video_resolution, scale, text, text_size, text_location, font)