#!/data/data/com.termux/files/usr/bin/python
#beta1.0
#脚本名为ezcutter，为轻松剪取的工具之意（easy cutter）。
#此脚本用于快速提取虚拟机名称内的识别码部分，即第八段中开头至ZX的字符串。
#将虚拟机名称复制后贴入kxxnj.txt文本后保存双击此脚本即可生成名为sbm.txt的识别码文本。
#脚本运行开始会自动删除上次的sbm.txt文本，完成后会自动清空kxxnj.txt文本，以便下次使用。
#by Li Kai

####################################

import os
file='kxxnj.txt'	#虚拟机名称列表文本路径
wanc='sbm.txt'	#生成识别码的文本路径
if os.path.exists(wanc):
    os.remove(wanc)
wen=open(wanc,"a")
for i in open(file):
    e=i.split("-")[7]
    if len(i.split("-"))==8:
        if "ZX" in e:
            wen.write(str(e[:e.index("ZX")]+"ZX")+"\n")
        else:
            wen.write(str(e))
    elif "ZX" in e:
        wen.write(str(e[:e.index("ZX")]+"ZX")+"\n")
    else:
        wen.write(str(e)+"\n")
f=open(file, "r+")
f.truncate()
