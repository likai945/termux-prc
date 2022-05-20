# for key index table.
# by Li Kai


import csv
import xlsxwriter as xw
import os
import re


def merge_files(one, two):
    with open(one, "a", encoding='utf_8_sig') as nf:
        with open(two, encoding='utf_8_sig') as f:
            cnt = 0
            for i in f:
                cnt += 1
                if cnt > 1:
                    nf.write(i)


def init_files():
    remove_files(beforeLst)
    merge_files('vmkx41.csv', 'vmkx42.csv')
    os.rename('vmkx41.csv', 'vmkx4.csv')


def check_event(hint):
    while True:
        num = input(hint)
        try:
            num = int(num)
            if num % 2 == 1:
                print('\t\athis is an odd number.')
            elif num < 0:
                print('\t\athis is a negative number.')
            else:
                return num
        except ValueError:
            print('\t\athe input number may be wrong, have a check.')


def read_numbers():
    cntnts = []
    for i in range(3, 6):
        cntnt = ['西南大区', f'可信{i}资源池']
        words = ['total', 'used']
        for j in range(2):
            hint = f'srvkx{i} {words[j]} vCPUs: '
            num = check_event(hint)
            cntnt.append(num / 2)
        cntnt.append('')
        cntnt.append(cntnt[-2])
        rate = cntnt[-1] / cntnt[2] * 100
        cntnt.append(rate)
        cntnts.append(cntnt)
    return cntnts


def write_cells(sheet, line, row, stColumn):
    column = stColumn
    for cell in line:
        if column - stColumn + 1 == len(line):
            cell = str(round(cell, 2)) + '%'
        sheet.write(row, column, cell, fmtDct[sheet.name][column][-1])
        column += 1


def write_sheet_cmp_rsc():
    sheet = sheetCmpRsc
    title = ['大区', '资源池', '总可分配物理核', '实际已分配物理核', '施工图设计会审的预分配物理核', '各类虚拟化应用分配物理核总量', '计算资源分配率（%）']
    sheet.write_row(0, 0, title, tfmt)
    cntnts = read_numbers()
    row = 0
    column = 0
    for line in cntnts:
        row += 1
        write_cells(sheet, line, row, column)


def walk_the_file(file):
    with open(file) as f:
        fl = csv.reader(f)
        next(fl)
        dct = {}
        for line in fl:
            key = line[-2]
            val = line[-1].rstrip('%\n')
            if not key.endswith('-VM'):
                val = float(val)
                val = val if val >= 0 else 0
                dct.setdefault(key, [])
                dct[key].append(val)
        return dct


def fmt_the_dct(file):
    dct = walk_the_file(file)
    fmtedDct = {}
    lst = list(dct.keys())
    lst.sort()
    for k in dct:
        valLst = dct[k]
        avg = sum(valLst) / len(valLst)
        fmtedDct[k] = avg
    return fmtedDct, lst


def write_st_e_s_cntnt(tup, row):
    sheet = sheetEchSrv
    for srv in tup[1]:
        row += 1
        column = 2
        ha = srvHaDct.get(srv, 'null')
        az = hazDct.get(ha, 'null')
        preGen = ha[-5:]
        preGen = re.sub('\d', '', preGen)
        genre = genreDct.get(preGen, 'null')
        val = tup[0][srv]
        line = [srv, genre, ha, az, val]
        write_cells(sheet, line, row, column)
        check_null(srv, ha, az, None, None)
    return row


def write_sheet_srv(tup3, tup4, tup5, cntntFunc, sheet, title):
    sheet.write_row(0, 0, title, tfmt)
    r3 = cntntFunc(tup3, 0)
    r4 = cntntFunc(tup4, r3)
    r5 = cntntFunc(tup5, r4)
    sheet.merge_range(1, 1, r3, 1, '可信3资源池', cfmt)
    sheet.merge_range(r3 + 1, 1, r4, 1, '可信4资源池', cfmt)
    sheet.merge_range(r4 + 1, 1, r5, 1, '可信5资源池', cfmt)
    sheet.merge_range(1, 0, r5, 0, '西南大区', cfmt)


def crt_cls_srv_dct(tup):
    dct = {}
    for srv in tup[0]:
        ha = srvHaDct.get(srv, 'null')
        preGen = ha[-5:]
        preGen = re.sub('\d', '', preGen)
        genre = genreDct.get(preGen, 'null')
        dct.setdefault(genre, {})
        dct[genre].setdefault(ha, [])
        val = tup[0][srv]
        dct[genre][ha].append(val)
    return dct


def sort_the_dct(dct):
    lst = list(dct.keys())
    lst.sort()
    return lst


def write_st_c_s_cntnt(tup, row):
    dct = crt_cls_srv_dct(tup)
    sheet = sheetClsSrv
    for cls in sort_the_dct(dct):
        sr = row + 1
        for ha in sort_the_dct(dct[cls]):
            row += 1
            column = 3
            num = len(dct[cls][ha])
            avg = sum(dct[cls][ha]) / len(dct[cls][ha])
            num = str(num) + '台'
            az = hazDct.get(ha, 'null')
            line = [num, ha, az, avg]
            write_cells(sheet, line, row, column)
        if len(dct[cls]) == 1:
            sheet.write(row, 2, cls, cfmt)
        else:
            sheet.merge_range(sr, 2, row, 2, cls, cfmt)
    return row


def write_srv_sheets():
    tup3 = fmt_the_dct('srvkx3.csv')
    tup4 = fmt_the_dct('srvkx4.csv')
    tup5 = fmt_the_dct('srvkx5.csv')
    titleEch = ['大区', '资源池', '服务器名称', '物理机承载业务', '所在HA', '所在AZ', '物理机CPU利用率']
    titleCls = ['大区', '资源池', '物理机承载业务', '物理机台数', '所在HA', '所在AZ', '各类物理机CPU利用率']
    write_sheet_srv(tup3, tup4, tup5, write_st_e_s_cntnt, sheetEchSrv, titleEch)
    write_sheet_srv(tup3, tup4, tup5, write_st_c_s_cntnt, sheetClsSrv, titleCls)


def get_vnf(vmn):
    dy = crt_dct('base/dy.csv')
    others = crt_lst('base/vnf.csv')
    if "ZTE_EMSplus_RPT" in vmn:
        sbm = "ZTE_EMSplus_RPT"
    else:
        psbm = vmn.split("-")[7]
        if "ZX" in psbm:
            sbm = psbm[:psbm.index("ZX") + 2]
        else:
            sbm = psbm
    vnfname = dy.get(sbm, 'null')
    if vnfname == 'null':
        for i in others:
            if i in vmn:
                vnfname = i

    return vnfname


def write_st_e_vm(file, sheet, row):
    dct = walk_the_file(file)
    vnfDct = {}
    row = row
    for vm in sort_the_dct(dct):
        row += 1
        column = 0
        vnf = get_vnf(vm)
        avg = sum(dct[vm]) / len(dct[vm])
        line = ['西南大区', f'可信{vm[12]}资源池', vnf, vm, '中兴', avg]
        write_cells(sheet, line, row, column)

        check_null(None, None, None, vm, vnf)

        vnfDct.setdefault(vnf, [])
        vnfDct[vnf].append(avg)
    return row, vnfDct


def write_st_c_vm(dct, sheet, row, rp):
    for vnf in sort_the_dct(dct):
        row += 1
        column = 0
        avg = sum(dct[vnf]) / len(dct[vnf])
        line = ['西南大区', f'可信{rp}资源池', vnf, '中兴', avg]
        write_cells(sheet, line, row, column)
    return row


def write_sheet_vms():
    sheetE = sheetEchVM
    titleE = ['大区', '资源池', '网元名称', '虚机名称', '厂家', '虚机vCPU 利用率']
    sheetE.write_row(0, 0, titleE, tfmt)
    sheetC = sheetClsVM
    titleC = ['大区', '资源池', '网元名称', '厂家', '网元虚机vCPU 利用率']
    sheetC.write_row(0, 0, titleC, tfmt)

    er3 = write_st_e_vm('vmkx3.csv', sheetE, 0)
    er4 = write_st_e_vm('vmkx4.csv', sheetE, er3[0])
    er5 = write_st_e_vm('vmkx5.csv', sheetE, er4[0])

    cr3 = write_st_c_vm(er3[1], sheetC, 0, 3)
    cr4 = write_st_c_vm(er4[1], sheetC, cr3, 4)
    write_st_c_vm(er5[1], sheetC, cr4, 5)


def crt_dct(file):
    dct = {}
    with open(file) as f:
        for l in f:
            key = l.split(',')[0]
            val = l.split(',')[1].rstrip()
            dct[key] = val
    return dct


def crt_lst(file):
    lst = []
    with open(file) as f:
        for l in f:
            lst.append(l.rstrip())
    return lst


def check_null(srv, ha, az, vm, vnf):
    if ha == 'null':
        notMatchLsts[0].append(srv)
    if az == 'null':
        notMatchLsts[1].append(ha)
    if vnf == 'null':
        notMatchLsts[2].append(vm)


def write_null_lists(lst, file):
    with open(file, 'a', encoding='utf_8_sig') as f:
        for line in lst:
            f.write(f'{line}\n')


def echo_manual_op():
    lists = notMatchLsts
    if lists[0]:
        print('\n\t\aview the srvhanull file')
        write_null_lists(lists[0], 'srvhanull.csv')
        print('\n\t\afix the srvha.csv, then run again.')
    elif lists[1]:
        print('\n\t\aview the haznull file')
        write_null_lists(lists[1], 'haznull.csv')
        print('\n\t\afix the haz.csv, then run again.')
    if lists[2]:
        print('\n\t\aview the vnfnull file')
        write_null_lists(lists[2], 'vnfnull.csv')
        print('\n\t\afix the vnf.csv, then run again.')


def remove_files(fileList):
    for file in fileList:
        if os.path.exists(file):
            os.remove(file)


def check_files_exist():
    notExstFls = []
    for file in fileLst:
        file = f'{file}.csv'
        if not os.path.exists(file):
            notExstFls.append(file)
    if notExstFls:
        for file in notExstFls:
            print(f'{file} does not exist, have a check.')
        exit(1)


def set_columns_width():
    sheets = (sheetCmpRsc, sheetEchSrv, sheetClsSrv, sheetEchVM, sheetClsVM)
    for s in sheets:
        for c in fmtDct[s.name]:
            s.set_column(c, c, fmtDct[s.name][c][0])


def do_it():
    init_files()
    write_sheet_cmp_rsc()
    write_srv_sheets()
    write_sheet_vms()
    set_columns_width()
    book.close()


def main():
    check_files_exist()
    do_it()
    echo_manual_op()
    remove_files(afterLst)


bookName = '附件2：网络云资源利用率关键指标.xlsx'
book = xw.Workbook(bookName)
sheetCmpRsc = book.add_worksheet('计算资源分配率')
sheetEchSrv = book.add_worksheet('单物理机CPU利用率')
sheetClsSrv = book.add_worksheet('资源池各类物理机CPU利用率')
sheetEchVM = book.add_worksheet('单虚机CPU利用率')
sheetClsVM = book.add_worksheet('网元虚机CPU利用率')

hazDct = crt_dct('base/haz.csv')
srvHaDct = crt_dct('base/srvha.csv')
genreDct = {'--': 'VIM服务器', 'MNG': '以虚机方式部署的管理域服务器', 'VIC': '业务域服务器', 'null': 'null'}

notMatchLsts = [[], [], []]
beforeLst = ('vnfnull.csv', 'haznull.csv', 'srvhanull.csv')
afterLst = ('srvkx3.csv', 'srvkx4.csv', 'srvkx5.csv', 'vmkx3.csv', 'vmkx4.csv', 'vmkx42.csv', 'vmkx5.csv')
fileLst = (
'base/srvha', 'base/haz', 'base/dy', 'base/vnf', 'srvkx3', 'srvkx4', 'srvkx5', 'vmkx3', 'vmkx41', 'vmkx42', 'vmkx5')

cfmt = book.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
lfmt = book.add_format({'align': 'left', 'valign': 'vcenter', 'border': 1})
rfmt = book.add_format({'align': 'right', 'valign': 'vcenter', 'border': 1})
tfmt = book.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': True, 'font_size': 12})

fmtDct = {
    sheetCmpRsc.name:
        {0: (14, cfmt), 1: (13, cfmt), 2: (17, lfmt), 3: (19, lfmt), 4: (34, lfmt), 5: (34, lfmt), 6: (24, rfmt)},
    sheetEchSrv.name:
        {0: (10,), 1: (12,), 2: (36, lfmt), 3: (30, cfmt), 4: (31, cfmt), 5: (27, cfmt), 6: (24, rfmt)},
    sheetClsSrv.name:
        {0: (10,), 1: (13,), 2: (30,), 3: (12, rfmt), 4: (30, cfmt), 5: (27, cfmt), 6: (24, rfmt)},
    sheetEchVM.name:
        {0: (10, cfmt), 1: (12, cfmt), 2: (42, lfmt), 3: (69, lfmt), 4: (10, cfmt), 5: (23, rfmt)},
    sheetClsVM.name:
        {0: (10, cfmt), 1: (12, cfmt), 2: (40, lfmt), 3: (10, cfmt), 4: (28, rfmt)}
}

if __name__ == '__main__':
    main()
