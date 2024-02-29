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

def trim_and_encode(filepath, start_time,  end_time, audio_track, subtitle_track):
    video_resolution, fps = get_video_information(filepath)
    if audio_track == "":
        audio_track = 0
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
        strict="experimental",
        ss=start_time,
        to=end_time
    )
    file_out.run()

def create_gif(filepath, original_res, speed, text, font, font_size, text_location):
    # requires gifski on path, no gifski python so needed manually
    # also requires imagemagick to be installed, wand didn't suit my needs so not using it
    video_resolution, fps = get_video_information(filepath)
    width, height = video_resolution.split("x")
    if font_size == "":
        font_size = "100"
    if speed == "":
        speed = "1"
    if font_size == "":
        font_size = "100"
    if font == "":
        match text_location:
            case "above_image":
                font = "roboto-condensed-bold"
            case "on_image":
                font = "impact"
    if text_location == "above_image" and speed != "1":
        text_location = "above_image_speed"
    gifski_commands(original_res, fps, speed, width, height)
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
                imagemagick_commands(text_location, image, font_size, font, text, width)
        if text_location == "above_image":
            original_res = True
            width, height = Image.open(f"text-{firstimg}").size
        gifski_commands(original_res, fps, speed, width, height, text)
        # shutil.move("text-gif.gif", "../text-gif.gif")
    elif text != "" and speed != "1":
        # if speed is used, gifski reconversion for better quality doesnt work (doesn't respect the set speed) so imagemagick is used directly instead
        image = "gif.gif"
        imagemagick_commands(text_location, image, font_size, font, text, width)
        # shutil.move("text-gif.gif", "../text-gif.gif")
    # shutil.move("gif.gif", "../gif.gif")
    # os.chdir("../")
    # shutil.rmtree("temporary-directory/")

def gifski_commands(original_res, fps, speed, width = "0", height = "0", text = ""):
    if not original_res and text == "":
        subprocess.run(f"gifski --quality=100 --fast-forward={speed} --fps={fps} -o gif.gif output.mp4",shell=True)
    elif original_res and text == "":
        subprocess.run(f"gifski --quality=100 --fast-forward={speed} --fps={fps} --width={width} --height={height} -o gif.gif output.mp4",shell=True)
    elif original_res:
        subprocess.run(f"gifski --quality=100 --fps={fps} --width={width} --height={height} -o text-gif.gif text-*.png",shell=True)
    else:
        subprocess.run(f"gifski --quality=100 --fps={fps} -o text-gif.gif text-*.png",shell=True)

def imagemagick_commands(text_location, image, font_size, font, text, width):
    match text_location:
        case "above_image":
            subprocess.run(f"magick {image} -background white -size {width}x -font {font} -pointsize {font_size} -gravity Center caption:\"{text}\" +swap -append text-{image}", shell=True)
        case "on_image":
            subprocess.run(f"magick {image} -gravity North -pointsize {font_size} -font {font} -fill white -stroke black -strokewidth 3 -annotate +0+0 \'{text}\' text-{image}",shell=True)
        case "above_image_speed":
            width, height = Image.open(image).size
            subprocess.run(f"magick -size {width}x -background white -gravity center -font {font} -pointsize {font_size} caption:\"{text}\" -set option:HH %h +delete {image} -layers coalesce -resize {width}x -background None -gravity North -splice '0x%[HH]+0+0' NULL: -size {width} -background white -gravity center -font {font} -pointsize {font_size} caption:\"{text}\" -gravity North -compose Over -layers composite -layers optimize text-{image}", shell=True)

def cli(filepath = "", start_time = "", end_time = "", original_res = "", speed = "", text = "", font = "", text_location = "", font_size = "", audio_track = "", subtitle_track = ""):
    filepath = input("file: ").encode('unicode-escape').decode()
    start_time = input("start time: ")
    end_time = input("end time: ")
    print("Leave the rest blank for defaults")
    original_res = input("Keep original video resolution?\nworse quality, True or False only: ")
    speed = input("Multiply video by speed value: ")
    text = input("text to put on the gif: ").encode('unicode-escape').decode()
    font = input("Font(replace spaces with -): ")
    text_location = input("text above like a caption gif(above_image) or on text like a 2010 meme(on_image): ")
    font_size = input("Text Size (integer): ")
    audio_track = input("Audio track (starts at 0): ")
    subtitle_track = input("subtitle track (starts at 0, leave blank for none): ")
    if original_res == "":
        original_res = False
    elif original_res == "True":
        original_res = True
    else:
        original_res = False
    if text_location == "":
        text_location = "above_image"
    return filepath, start_time, end_time, original_res, speed, text, font, text_location, font_size, audio_track, subtitle_track

if __name__ == "__main__":
    if "temporary-directory" not in os.listdir() and "temporary-directory" not in os.getcwd():
        os.mkdir("temporary-directory")
        os.chdir("temporary-directory")
    elif "temporary-directory" in os.listdir():
        os.chdir("temporary-directory")
    filepath, start_time, end_time, original_res, speed, text, font, text_location, font_size, audio_track, subtitle_track = cli()
    trim_and_encode(filepath, start_time, end_time, audio_track, subtitle_track)
    create_gif(filepath, original_res, speed, text, font, font_size, text_location)