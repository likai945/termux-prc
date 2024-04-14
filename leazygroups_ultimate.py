#by LiKai
#March 24, 2024
#将主机列表按组分别以每行一个贴入txt或csv文件，文件名为组名，执行脚本将生成完整的groups.txt文件，贴入clushshell组配置文件即可。
#March 25, 2024 增加含控制节点场景，增加多种格式
#March 30, 2024 结果更加综合化
#April 13, 2024 结果更加综合化
#April 14, 2024 适用范围更广，可同时用于dbs节点

import os
import glob


def make_list(f):
    hostSet=set()
    for line in f:
        line=line.strip()
        if len(line)!=0:
            hostSet.add(line.upper())
    hList=list(hostSet)
    hList.sort()
    return hList


def prdc_file(file):
    with open(file) as f:
        allList=make_list(f)
        return allList


def fmt_string(lst):
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
    return string


def init_list(hList,pI,sI,m):
    dct={}
    for host in hList:
        mI=host.index('-',30,31) if m==1 else 0
        prefix=host[:mI+pI]
        root=host[mI+pI:mI+sI]
        suffix=host[sI+mI:]
        key=(prefix,suffix)
        dct.setdefault(key,[])
        dct[key].append(root)

    return dct


def predo_it(lst,pI,sI,m):
    hostDict=init_list(lst,pI,sI,m)
    groupList=[]
    dList=list(hostDict)
    dList.sort()

    for host in dList:
        numList=hostDict[host]
        if len(numList)==1:
            fmtHName=host[0]+numList[0]+host[1]
        else:
            batchHName=f'[{fmt_string(numList)}]'
            fmtHName=f'{host[0]}{batchHName}{host[1]}'
        groupList.append(fmtHName)

    return groupList


def do_it(file):
    prdList=prdc_file(file)
    fstList=predo_it(prdList,1,3,1)
    scnList=predo_it(fstList,22,24,0)
    return scnList


def pre_write(file):
    groupName=file[:-4]
    gList=do_it(file)
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
