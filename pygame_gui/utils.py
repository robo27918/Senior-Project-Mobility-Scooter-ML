def check_video_file(filepath):
    video_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.mkv']
    file_extension = os.path.splitext(filepath)[1]
    if file_extension in video_extensions:
        print(f"{filepath} is a video file.")
    else:
        print(f"{filepath} is not a video file.")