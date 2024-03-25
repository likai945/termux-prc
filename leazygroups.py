#by LiKai
#March 24, 2024
#将主机列表按组分别以每行一个贴入txt或csv文件，文件名为组名，执行脚本将生成完整的groups.txt文件，贴入clushshell组配置文件即可。

import os
import glob


def make_list(file):
    fSet=set()
    with open(file) as f:
        for line in f:
            line=line.strip()
            if len(line)!=0:
                fSet.add(line)
        fList=list(fSet)
        fList.sort()
        fList.append(fList[-1])
        return fList


def do_it(hostFile):
    hostList=make_list(hostFile)
    cntns=0
    lastPx='null'
    lastSx='0'
    groupList=[]
    for host in hostList:
        prefix=host[:-2]
        suffix=host[-2:]
        iSuffix=int(suffix)
        cmpSx=int(lastSx)+1

        if (prefix==lastPx and iSuffix==cmpSx):
            cntns+=1
            end=suffix
        else:
            if cntns==1: 
                oneElmt=lastHost
                groupList.append(oneElmt)
            if cntns>1:
                oneElmt=lastPx+'['+start+'-'+end+']'
                groupList.append(oneElmt)

            cntns=1
            start=suffix
            lastHost=host

        lastPx=prefix
        lastSx=suffix

    return groupList


def write_group(hostFile):
    groupName=hostFile[:-4]
    groupList=do_it(hostFile)
    longName=f'{groupName}:'

    for element in groupList:
        longName+=f'{element},'

    with open('groups.txt','a',encoding='utf_8_sig') as f:

        longName=longName.rstrip(',')+'\n'
        f.write(longName) 


if __name__=='__main__':
    if os.path.exists('groups.txt'):
            os.remove('groups.txt')

    groups=glob.glob('*.txt')+glob.glob('*.csv')
    groups.sort()
    for group in groups:
        write_group(group)
        os.remove(group)

