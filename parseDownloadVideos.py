import re
import subprocess
import json

#holds the annotation information to be passed into FFmpeg
fileDicts= []
# url = youtube-dl -g https://www.youtube.com/watch?v=A0xAXXysHUo | sed -n 1p
#start =
#duration =
def parseLine(x,words,j):
    #from the jsondict get the eventname,subaction name
    eventname = "_".join([words[1],words[2],words[3]])
    subaction = "_".join([words[4],words[5],words[6]])
    #subaction starts at event_time+subaction_start_time. start time is used in FFmpeg to mark the start_time of the clip.
    subactionStart = round(float(words[2])+j[eventname]["segments"][subaction]["timestamps"][0][0],2)
    #subaction ends at event_time+subaction_end_time
    subactionEnd = round(float(words[2])+j[eventname]["segments"][subaction]["timestamps"][0][1],2)
    #duration time is used in FFmpeg to mark the duration of the clip.
    duration = round(subactionEnd -subactionStart,2)
    info = {
        'fileName': x+".mp4",
        'url': "youtube-dl -g https://www.youtube.com/watch?v=" + words[0],
        'startAt' : str(subactionStart),
        'duration' : str(duration)
    }
    fileDicts.append(info)

# read the text file
with open("./gymanno/gym99_train_element_v1.1.txt") as f:
    lines = f.readlines()

#read the annotations file
with open("./gymanno/finegym_annotation_info_v1.1.json") as j:
    jfile = json.load(j)


# the maximum number of videos to be downloaded. lower_limit
i=0

#read each line from the text file
for line in lines:
    # using regular expression get the name of the file
    line = re.split(" [0-9]+", line)
    #split the name with the separator '_' to feed it into json file
    words = line[0].split('_')
    #jfile[words[0]] will load that file-annotation into the memory
    #use parseLine() method to get annotation information
    parseLine(line[0],words,jfile[words[0]])
    i +=1
    #the maximum number of videos to be downloaed. upper_limit
    if i==10: break

#use subprocess to call the bash-script file and send the relevant parameters to download the video
for x in fileDicts:
    print (x["url"])
    subprocess.call(['bash', 'videocut.sh', x["url"],x["startAt"],x["duration"],x["fileName"]])

# ffmpeg -ss "start_at" -i $("url") -to "duration" -c copy "filename"
#this will download a youtube clip from a youtube video which starts at "start_at" time
# and the duration of the clip will be "duration" time and output file name will be the "file_name"
