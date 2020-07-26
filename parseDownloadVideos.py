import re
import subprocess
fileDicts= []

# url = youtube-dl -g https://www.youtube.com/watch?v=A0xAXXysHUo | sed -n 1p
#start =
#duration =
def parseLine(x):
    r = re.split(" [0-9]+",x)
    # print(r[0])
    words = r[0].split('_')
    # print(words)

    info = {
        'fileName': r[0]+".mp4",
        'url': "youtube-dl -g https://www.youtube.com/watch?v=" + words[0],
        'startAt' : str(float(words[2])),
        'duration' : str(float(words[6]) - float(words[5]))
    }
    fileDicts.append(info)

with open("./gymanno/gym99_train_element_v1.1.txt") as f:
    lines = f.readlines()

i=0
for x in lines:
    # print(x)
    parseLine(x)
    i +=1
    if i==500: break

for x in fileDicts:
    print (x["url"])
    subprocess.call(['bash', 'videocut.sh', x["url"],x["startAt"],x["duration"],x["fileName"]])

