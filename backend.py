#the logic for gifski and ffmpeg
import ffmpeg

def trim_and_encode(filepath, subtitle_track, start_time, end_time):
    #takes a file, cuts it from a certain time and reencodes
    if subtitle_track != "":
        (
            ffmpeg
            .input(filepath)
            .filter('subtitles',filepath)
            .output(
                "output.mp4", 
                **{"codec:v": "libx264"}, 
                **{"codec:a": "copy"}, 
                crf=15, 
                preset="ultrafast", 
                ss=start_time,
                to=end_time
            )
            .run()
        )
    else:
        (
            ffmpeg
            .input(filepath)
            .output(
                "output.mp4", 
                **{"codec:v": "libx264"}, 
                **{"codec:a": "copy"}, 
                crf=15, 
                preset="ultrafast", 
                ss=start_time,
                to=end_time
            )
            .run()
        )

if __name__ == "__main__":
    subtitle_track = 0
    start_time = "00:00:10.135"
    end_time = "00:00:18.060"
    filepath = r""
    trim_and_encode(filepath,subtitle_track,start_time,end_time)