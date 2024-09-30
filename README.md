# splitTrials
A script for splitting videos on start and finish times from excel sheets

Made to run on python 3.9.19, but should work on newer versions as well.

Made to run on pandas 2.2.2, but should work on older versions as well.

Must have ffmpeg installed (I used 7.0.2) and must give the file location for it. (Dowload Link: [https://ffmpeg.org/download.html])

Example location Windows: "C:\\ffmpeg-7.0.2-essentials_build\\bin\\ffmpeg" -make sure to use double back slashes for windows

Example location Mac: "/usr/local/bin/ffmpeg"

Also must give the location for the excel file. Make sure that each of the cells is in the general type - custom cells will likely cause errors related to datetime.
