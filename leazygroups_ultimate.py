#by LiKai
#March 24, 2024
#将主机列表按组分别以每行一个贴入txt或csv文件，文件名为组名，执行脚本将生成完整的groups.txt文件，贴入clushshell组配置文件即可。
#March 25, 2024 增加含控制节点场景，增加多种格式
#March 30, 2024 结果更加综合化

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
    return cList,hList


def prdc_file(file):
    with open(file) as f:
        allList=make_list(f)
        return allList


def fmt_string(name,lst):
    ctns=0
    last='88888'
    string=''
    lst.append(lst[-1])
    for i in lst:
        if int(i)==int(last)+1:
            ctns+=1
            end=i
        else:
            if ctns==1:
                string+=f'{last},'
            elif ctns>1:
                string+=f'{start}-{end},'
            
            ctns=1
            start=i
        last=i

    string=string.rstrip(',')
    fullString=f'{name}[{string}]'
    return fullString


def init_list(hList):
    dct={}
    for host in hList:
        prefix=host[:-2]
        suffix=host[-2:]
        dct.setdefault(prefix,[])
        dct[prefix].append(suffix)

    return dct


def do_it(file):
    global allList
    allList=prdc_file(file)
    hostList=allList[1]
    hostDict=init_list(hostList)
    groupList=[]
    dList=list(hostDict)
    dList.sort()

    for host in dList:
        numList=hostDict[host]
        fmtHName=fmt_string(host,numList)
        groupList.append(fmtHName)

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


