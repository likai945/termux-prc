import csv
import xlsxwriter as xw
import time
import os

def prd_alrm_dct(csvfile,d,s,e,n):
    with open(csvfile) as f:
        fl=csv.reader(f)
        c=0
        dct={}
        for l in fl:
            c+=1
            if c>1:
                desc=l[d]
                start=l[s]
                endt=l[e]
                objn=l[n]
                dct[desc]=dct.get(desc,[[],[],[]])
                dct[desc][0].append(start)
                dct[desc][1].append(endt)
                dct[desc][2].append(objn)
    return dct
                

def mult_lines_to_one(lst):
    blox=''
    for i in range(len(lst)):
        blox=blox+lst[i]+'\n'
    blox=blox.rstrip()
    return blox


def one_line_to_write(dct):
    lines=[]
    total=0
    for k in dct:
        desc=k
        line=[]
        start=mult_lines_to_one(dct[k][0])
        endt=mult_lines_to_one(dct[k][1])
        objn=mult_lines_to_one(dct[k][2])
        number=len(dct[k][0])
        line.append(start)
        line.append(endt)
        line.append(objn)
        line.append(desc)
        line.append(number)
        lines.append(line)
        total+=number
    return lines,total


def prd_his_alllines(his3,his4,his5):
    dct3=prd_alrm_dct(his3,4,7,9,6)
    dct4=prd_alrm_dct(his4,2,5,7,4)
    dct5=prd_alrm_dct(his5,2,5,7,4)

    lines3=one_line_to_write(dct3)[0]
    lines4=one_line_to_write(dct4)[0]
    lines5=one_line_to_write(dct5)[0]
    alllines=[lines3,lines4,lines5]

    global htotal3,htotal4,htotal5

    htotal3=one_line_to_write(dct3)[1]
    htotal4=one_line_to_write(dct4)[1]
    htotal5=one_line_to_write(dct5)[1]

    return alllines

def prd_crt_alllines(crt3,crt4,crt5):
    dct3=prd_alrm_dct(crt3,3,7,10,6)
    dct4=prd_alrm_dct(crt4,1,5,8,4)
    dct5=prd_alrm_dct(crt5,1,5,8,4)

    lines3=one_line_to_write(dct3)[0]
    lines4=one_line_to_write(dct4)[0]
    lines5=one_line_to_write(dct5)[0]
    alllines=[lines3,lines4,lines5]

    global ctotal3,ctotal4,ctotal5

    ctotal3=one_line_to_write(dct3)[1]
    ctotal4=one_line_to_write(dct4)[1]
    ctotal5=one_line_to_write(dct5)[1]

    return alllines

def write_contents(sheet,hisorcrt): 
    if hisorcrt=='his':
        alllines=prd_his_alllines(his3,his4,his5)
    elif hisorcrt=='crt':
        alllines=prd_crt_alllines(crt3,crt4,crt5)
    r=2
    rs=[]
    for lines in alllines:
        for line in lines:
            line=line+['']
            if hisorcrt=='crt':
                line=line+['是','']
            sheet.write_row(r,2,line,cfmt)
            r+=1
        rs.append(r)
    return rs

def write_his_sheet(sheet):
    sheet.merge_range(0,0,0,7,'历史告警',lfmt)
    title=['时间','资源池','告警时间','清除时间','对象名称','告警描述','数量','处理结果']
    sheet.write_row(1,0,title,cfmts)
    hisrows=write_contents(sheet,'his')
    sheet.merge_range(2,0,hisrows[2]-1,0,date,lfmt)
    sheet.merge_range(2,1,hisrows[0]-1,1,'可信3',lfmt)
    sheet.merge_range(hisrows[0],1,hisrows[1]-1,1,'可信4',lfmt)
    sheet.merge_range(hisrows[1],1,hisrows[2]-1,1,'可信5',lfmt)


def write_crt_sheet(sheet):
    sheet.merge_range(0,0,0,9,'当前告警',lfmt)
    title=['时间','资源池','告警时间','确认恢复时间','对象名称',' 告警描述','数量','处理结果','是否清除','未确认恢复原因']
    sheet.write_row(1,0,title,cfmts)
    crtrows=write_contents(sheet,'crt')
    sheet.merge_range(2,0,crtrows[2]-1,0,date,lfmt)
    sheet.merge_range(2,1,crtrows[0]-1,1,'可信3',lfmt)
    sheet.merge_range(crtrows[0],1,crtrows[1]-1,1,'可信4',lfmt)
    sheet.merge_range(crtrows[1],1,crtrows[2]-1,1,'可信5',lfmt)


def write_smr_sheet(sheet):
    title=['时间','资源池','历史告警数量','当前告警数量','当前告警清除数量','当前告警剩余']
    sheet.write_row(0,0,title,cfmts)
    sheet.merge_range(1,0,3,0,date,lfmt)
    linekx3=['可信三',htotal3,ctotal3,ctotal3,0]
    linekx4=['可信四',htotal4,ctotal4,ctotal4,0]
    linekx5=['可信五',htotal5,ctotal5,ctotal5,0]
    sheet.write_row(1,1,linekx3,cfmts)
    sheet.write_row(2,1,linekx4,cfmts)
    sheet.write_row(3,1,linekx5,cfmts)

def check_files_exist():
    files=[his3,his4,his5,crt3,crt4,crt5]
    for i in files:
        if not os.path.exists(i):
            print(f'File {i} does not exist or named wrong, have a check.')
            input('\nPress enter to quit.')
            exit()


def do_it():
    write_his_sheet(sheethis)
    write_crt_sheet(sheetcrt)
    write_smr_sheet(sheetsmr)
    book.close()


today=time.localtime()
date=f'{today[0]}-{today[1]}-{today[2]}'
his3,his4,his5='kx3_h.csv','kx4_h.csv','kx5_h.csv'
crt3,crt4,crt5='kx3_c.csv','kx4_c.csv','kx5_c.csv'
bookname=f'附件7：资源池告警处理情况表-中兴资源池{date}.xlsx'
book=xw.Workbook(bookname)
sheetsmr=book.add_worksheet('汇总')
sheethis=book.add_worksheet('历史告警处理记录')
sheetcrt=book.add_worksheet('当前告警处理记录')

lfmt=book.add_format({'align':'center','valign':'vcenter','border':1})
cfmts=book.add_format({'align':'center','valign':'vcenter','border':1})
cfmt=book.add_format({'border':1})

if __name__=='__main__':
    check_files_exist()
    do_it()
