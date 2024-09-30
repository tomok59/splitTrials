import pandas as pd
import os
import cv2
import random
import subprocess

ffmpeg = input("Please enter absolute location of ffmpeg: ")

xcel = input("Please enter the location of the excel sheet: ")

def get_sec(time_str):
    minutes, tenth = time_str.split('.')
    m, s = minutes.split(':')
    return  float(m) * 60 + float(s) + float('0.' + tenth)


## transfrom sheets into easy to read dataframe
data = pd.read_excel(xcel)
data = data.dropna(how='all')
data['Bridge Time'] = data[['Bridge Time', 'Incorrect Time', 'Abort Time']].agg(lambda x: ''.join(x.dropna()), axis=1)
data = data.drop(columns=['Clang', 'Unnamed: 8', 'Incorrect Time', 'Abort Time'])
data['Bridge Time'] = data['Bridge Time'].apply(get_sec)
data['Target Time'] = data['Target Time'].apply(get_sec)
data['Target Frame'] = data['Target Time'] * 59.94
data['Bridge Frame'] = data['Bridge Time'] * 59.94
data['Target Frame'] = data['Target Frame'].astype(int)
data['Bridge Frame'] = data['Bridge Frame'].astype(int)
data['Trial Number'] = data['Trial Number'].astype(int)
videos = data['File Name'].unique()

#getting input/output file
def grabUserInput(input_file, output_file, start_time =0, end_time =1):

    user_input_dict = {}

    user_input_dict["input_file"] = input_file
    user_input_dict["output_file"] = output_file
    user_input_dict["video_codec"] = "libx264"

    return user_input_dict

#run ffmpeg command to trim video
def buildFFmpegCommand(input_file, output_file, start_time =0, end_time =1):

    if os.path.exists(output_file):
        os.remove(output_file)
    final_user_input = grabUserInput(input_file, output_file, start_time =0, end_time =1)

    commands_list = [
        ffmpeg,
        "-i",
        final_user_input["input_file"],
        "-c:v",
        final_user_input["video_codec"],
        "-ss",
        start_time,
        "-to",
        end_time,
        final_user_input["output_file"]
        ]

    return commands_list

def runFFmpeg(commands):

    print(commands)
    if subprocess.run(commands).returncode == 0:
        print ("FFmpeg Script Ran Successfully")
    else:
        print ("There was an error running your FFmpeg script")

for name in videos:
    sub_data = data[data['File Name'] == name]
    for index, row in sub_data.iterrows():
        trial_num = row['Trial Number']
        startframe = row['Target Time']
        endframe = row['Bridge Time']
        runFFmpeg(buildFFmpegCommand(name, name[:-4] + 'trial' +  str(trial_num) +'.mp4', str(startframe), str(endframe)))