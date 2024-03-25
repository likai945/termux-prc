#by LiKai
#March 24, 2024
#将主机列表按组分别以每行一个贴入txt或csv文件，文件名为组名，执行脚本将生成完整的groups.txt文件，贴入clushshell组配置文件即可。
#March 25, 2024 增加含控制节点场景，增加多种格式

import os
import glob


def make_list(f):
    ctlrSet=set()
    hostSet=set()
    for line in f:
        line=line.strip()
        if len(line)!=0:
            if 'VM' in line:
                ctlrSet.add(line)
            else:
                hostSet.add(line)
    cList=list(ctlrSet)
    hList=list(hostSet)
    cList.sort()
    hList.sort()
    hList.append(hList[-1])
    return cList,hList


def prdc_file(file):
    with open(file) as f:
        allList=make_list(f)
        return allList


def do_it(file):
    global allList
    allList=prdc_file(file)
    hostList=allList[1]
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


def pre_write(file):
    groupName=file[:-4]
    gHList=do_it(file)
    gCList=allList[0]
    gList=gCList+gHList
    longName=f'{groupName}:'

    for element in gList:
        longName+=f'{element},'
    return longName


def write_group(file):
    longName=pre_write(file)
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

