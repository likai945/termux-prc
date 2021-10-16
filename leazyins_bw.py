# leazyins是日常巡检的辅助工具，可实现温度的自动计算、老文件、空目录、未更名文件、未更名文件夹的自动列出
# by Li Kai
import glob
import os
import time
runlogs=glob.glob('*.runlog')
runlogs.sort()
if runlogs:
    runlog=runlogs[-1]
def walk_the_file(wz):
    i=0
    with open(runlog) as f:
        dct={}
        for line in f:
            i+=1
            if i >1:
                preitem=line.split('|')[0]
                item=preitem.split('-')[3]+preitem.split('-')[7]
                if line.split('|')[2].isdigit():
                    ivalue=int(line.split('|')[wz])
                    dct[item]=dct.get(item,[])
                    dct[item].append(ivalue)
    return dct

def compute_the_average(wz):
    dct=walk_the_file(wz)
    fmtdct={}
    for i in dct:
        avgtmp=sum(dct[i])/len(dct[i])
        fmtat=round(avgtmp,2)
        fmt=f'{fmtat}°C'
        fmtdct[i]=fmt
    return fmtdct

def fmt_print():
    cputmp=compute_the_average(2)
    for i in range(3,6):
        fmtitem=f'kx{i}_srv/kx{i}_dbs'
        k1=f'0{i}ASRV'
        k2=f'0{i}ADBS'
        k1v=cputmp.get(k1,'NO_DATA')
        k2v=cputmp.get(k2,'NO_DATA')
        fmttmp=f'{fmtitem}  {k1v}/{k2v}'
        print(fmttmp)

def print_avg_tmp():
    print('================================')
    fmt_print()
    print('================================')
    print(f'based on {runlog}')

today=time.gmtime(time.time())[1:3]
fmttoday=time.strftime("%Y%m%d", time.localtime())
crtdir=os.getcwd()
def clct_old_files():
    ofs=[]
    for root,dirs,files in os.walk(crtdir):
        for file in files:
            filepath=os.path.join(root,file)
            chgtime=os.path.getmtime(filepath)
            fmtcht=time.gmtime(chgtime)[1:3]
            if fmtcht != today:
                ofs.append(filepath)
    return ofs

def clct_empty_dirs():
    eds=[]
    for root,dirs,files in os.walk(crtdir):
        for dirc in dirs:
            dirpath=os.path.join(root,dirc)
            if not os.listdir(dirpath):
                eds.append(dirpath)
    return eds

def clct_old_nm_files():
    onfs=[]
    for root,dirs,files in os.walk(crtdir):
        for file in files:
            if '.' in file:
                slimfln=file.split('.')[-2][-8:]
            else:
                slimfln=file[-8:]
            if slimfln.isdigit() and len(slimfln)==8 and slimfln != fmttoday:
                filepath=os.path.join(root,file)
                onfs.append(filepath)
    return onfs

def clct_old_nm_dirs():
    onds=[]
    for root,dirs,files in os.walk(crtdir):
        for dirc in dirs:
            dirdate=dirc[-8:]
            if dirdate.isdigit() and len(dirdate) == 8 and dirdate != fmttoday:
                dirpath=os.path.join(root,dirc)
                onds.append(dirpath)
    return onds

def print_stuffs(opt):
    echoes={'of':'old files','ed':'empty directories','onf':'old name files','ond':'old name directories'}
    if opt=='of':
        stfs=clct_old_files()
    elif opt=='ed':
        stfs=clct_empty_dirs()
    elif opt=='onf':
        stfs=clct_old_nm_files()
    elif opt=='ond':
        stfs=clct_old_nm_dirs()

    if not stfs:
        print(f'\nNo {echoes[opt]}:)')
    else:
        print(f'\nAll the {echoes[opt]}:(')
        for stf in stfs:
            print(f'\t.{stf[len(crtdir):]}')


if runlogs:
    print_avg_tmp()
else:
    print_stuffs('of')
    print_stuffs('ed')
    print_stuffs('onf')
    print_stuffs('ond')
