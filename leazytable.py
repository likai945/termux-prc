# for key index table.
# by Li Kai


import csv
import xlsxwriter as xw
import os
import re

def merge_files(one,two,three,cnt):
    with open(three, "a", encoding='utf_8_sig') as nf:
        for fl in [one,two]:
            with open(fl, encoding='utf_8_sig') as f:
                tmp=cnt
                for i in f:
                    tmp += 1
                    if tmp > 1 and not 'VM,' in i:
                        nf.write(i)


def init_files():
#    merge_files('srvkx41m.csv','srvkx42m.csv','srvkx4m.csv',0)
#    merge_files('srvkx41e.csv','srvkx42e.csv','srvkx4e.csv',0)
    merge_files('srvkx4m.csv','srvkx4e.csv','srvkx4.csv',0)
    for i in ['srv','vm']:
        for j in range(3,6,2):
            merge_files(f'{i}kx{j}m.csv',f'{i}kx{j}e.csv',f'{i}kx{j}.csv',0)


def read_numbers():
    cntnts=[]
    for i in range(3,6):
        cntnt=['西南大区',f'可信{i}资源池']
        words=['total','used']
        for j in range(2):
            num=input(f'srvkx{i} {words[j]} vCPUs: ')
            cntnt.append(int(num)/2)
        cntnt.append('')
        cntnt.append(cntnt[-2])
        rate=cntnt[-1] / cntnt[2] * 100
        cntnt.append(rate)
        cntnts.append(cntnt)
    return cntnts


def write_sheet_cmp_rsc():
    title=['大区','资源池','总可分配物理核','实际已分配物理核','施工图设计会审的预分配物理核','各类虚拟化应用分配物理核总量','计算资源分配率（%']
    sheetCmpRsc.write_row(0,0,title,cfmt)
    cntnts=read_numbers()
    row=0
    for line in cntnts:
        row+=1
        sheetCmpRsc.write_row(row,0,line,cfmt)


def walk_the_file(file):
    with open(file) as f:
        fl=csv.reader(f)
        dct={}
        for line in fl:
            vmn=line[-2]
            val=line[-1].rstrip('%\n')
            val=float(val)
            val=val if val >= 0 else 0
            dct.setdefault(vmn,[])
            dct[vmn].append(val)
        return dct

            
def fmt_the_dct(file):
    dct=walk_the_file(file)
    fmtDct={}
    lst=list(dct.keys())
    lst.sort()
    for k in dct:
        valLst=dct[k]
        avg=sum(valLst)/len(valLst)
        fmtDct[k]=avg
    return fmtDct,lst


def write_st_e_s_cntnt(tup,row):
    for srv in tup[1]:
        row+=1
        ha=srvHaDct[srv]
        az=hazDct[ha]
        preGen=ha[-5:]
        preGen=re.sub('\d','',preGen)
        genre=genreDct[preGen]
        val=tup[0][srv]
        cntnt=[srv,genre,ha,az,val] 
        sheetEchSrv.write_row(row,2,cntnt,cfmt)
    return row


def write_sheet_srv(tup3,tup4,tup5,cntntFunc,sheet,title):
    sheet.write_row(0,0,title,cfmt)
    r3=cntntFunc(tup3,0)
    r4=cntntFunc(tup4,r3)
    r5=cntntFunc(tup5,r4)
    sheet.merge_range(1,1,r3,1,'可信3资源池',cfmt)
    sheet.merge_range(r3+1,1,r4,1,'可信4资源池',cfmt)
    sheet.merge_range(r4+1,1,r5,1,'可信5资源池',cfmt)
    sheet.merge_range(1,0,r5,0,'西南大区',cfmt)


def crt_cls_srv_dct(tup):
    dct={}
    for srv in tup[0]:
        ha=srvHaDct[srv]
        preGen=ha[-5:]
        preGen=re.sub('\d','',preGen)
        genre=genreDct[preGen]
        dct.setdefault(genre,{})
        dct[genre].setdefault(ha,[])
        val=tup[0][srv]
        dct[genre][ha].append(val)
    return dct


def sort_the_dct(dct):
    lst=list(dct.keys())
    lst.sort()
    return lst


def write_st_c_s_cntnt(tup,row):
    dct=crt_cls_srv_dct(tup)
    for cls in sort_the_dct(dct):
        sr=row+1
        for ha in sort_the_dct(dct[cls]):
            row+=1
            num=len(dct[cls][ha])
            avg=sum(dct[cls][ha])/len(dct[cls][ha])
            num=str(num)+'台'
            az=hazDct[ha]
            line=[num,ha,az,avg]
            sheetClsSrv.write_row(row,3,line,cfmt)
        if len(dct[cls]) == 1:
            sheetClsSrv.write(row,2,cls,cfmt)
        else:
            sheetClsSrv.merge_range(sr,2,row,2,cls,cfmt)
    return row


def write_srv_sheets():
    tup3=fmt_the_dct('srvkx3.csv')
    tup4=fmt_the_dct('srvkx4.csv')
    tup5=fmt_the_dct('srvkx5.csv')
    titleEch=['大区','资源池','服务器名称','物理机承载业务','所在HA','所在AZ','物理机CPU利用率']
    titleCls=['大区','资源池','物理机承载业务','物理机台数','所在HA','所在AZ','各类物理机CPU利用率']
    write_sheet_srv(tup3,tup4,tup5,write_st_e_s_cntnt,sheetEchSrv,titleEch)
    write_sheet_srv(tup3,tup4,tup5,write_st_c_s_cntnt,sheetClsSrv,titleCls)


def get_vnf(vmn):
    dy=crt_dct('dy.csv')
    others=crt_lst('vnf.csv')
    if "-OMC-" in vmn:
        sbm = "OMC"
    elif "-NFVO-" in vmn:
        sbm = "NFVO"
    elif "-xnqVNFM3" in vmn:
        sbm = "VNFM03"
    elif "-VNFM-" in vmn:
        sbm = "VNFM"
    elif "ZTE_EMSplus_RPT" in vmn:
        sbm = "ZTE_EMSplus_RPT"
    else:
        psbm = vmn.split("-")[7]
        if "ZX" in psbm:
            sbm = psbm[:psbm.index("ZX") + 2]
        else:
            sbm = psbm
    vnfname = dy.get(sbm, 'novnf')
    if vnfname == 'novnf':
        for i in others:
            if i in vmn:
                vnfname=i
        
    return vnfname


def write_sheet_ech_vm():
    merge_files('vmkx3.csv','vmkx4.csv','vmtmp.csv',0) ##change the argument
    merge_files('vmtmp.csv','vmkx5.csv','vm.csv',0)
    title=['大区','资源池','网元名称','虚机名称','厂家','虚机vCPU 利用率']
    sheetEchVM.write_row(0,0,title,cfmt)
    dct=walk_the_file('vm.csv')
    row=0
    for vm in sort_the_dct(dct):
        row+=1
        vnf=get_vnf(vm)
        avg=sum(dct[vm])/len(dct[vm])
        line=['西南大区',f'可信{vm[12]}资源池',vnf,vm,'中兴',avg]
        sheetEchVM.write_row(row,0,line,cfmt)



def do_it():
    init_files()
    write_sheet_cmp_rsc()
    write_srv_sheets()
    write_sheet_ech_vm()
    book.close()

def crt_dct(file):
    dct = {}
    with open(file) as f:
        for l in f:
            key = l.split(',')[0]
            val = l.split(',')[1].rstrip()
            dct[key] = val
    return dct


def crt_lst(file):
    lst=[]
    with open(file) as f:
        for l in f:
            lst.append(l.rstrip())
    return lst


def main():
#    check_files()
    do_it()
#    fmt_it()
#    echo_manual_op()

bookName = '附件2：网络云资源利用率关键指标.xlsx'
book = xw.Workbook(bookName)
sheetCmpRsc = book.add_worksheet('计算资源分配率')
sheetEchSrv = book.add_worksheet('单物理机CPU利用率')
sheetClsSrv = book.add_worksheet('资源池各类物理机CPU利用率')
sheetEchVM = book.add_worksheet('单虚机CPU利用率')
sheetClsVM = book.add_worksheet('网元虚机CPU利用率')

hazDct=crt_dct('haz.csv')
srvHaDct=crt_dct('srvha.csv')
genreDct={'--':'VIM服务器','MNG':'以虚机方式部署的管理域服务器','VIC':'业务域服务器'}

cfmt = book.add_format({'align': 'center', 'valign':'vcenter', 'border': 1})

if __name__ == '__main__':
    main()
