#!/usr/bin/python 
import os
downloadhelper = "wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.0.0.jar"
os.system(downloadhelper)
downloadhelper2 = "wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool"
os.system(downloadhelper2)
chmod1 = "chmod +x apktool"
os.system(chmod1)
move1 = "mv apktool_2.0.0.jar apktool.jar"
os.system(move1)

