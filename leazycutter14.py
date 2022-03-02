# beta14
# 针对不同资源池虚机存在相同识别码的处理
# 用法：将导出的资料分别按照kx3.csv、kx41.csv、kx42.csv、kx5.csv命名，放置在本工具所在目录后双击稍事等待即可得到名为jzfz.csv的文件，由四列构成，分别为网元名、对应系统均值、均值、峰值和网元的虚机数量，与需填报的报表相对应。
# 需配合dy.csv文件使用
# by Li Kai


import os


def zhaodao_vnfname(vmn):
    rpn = vmn.split('-')[3][1]
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
        vmlst = list(vmn.split('-'))
        vmind = vmlst.index('VM')
        if vmind == len(vmlst)-1:
            psbm = 'noSBM'
            man.add(vmn)
        else:
            psbm = vmlst[vmind+1]
        if "ZX" in psbm:
            sbm = psbm[:psbm.index("ZX") + 2]
        else:
            sbm = psbm
    sbm = rpn + sbm
    vnfname = dy.get(sbm, 'novnf')
    return vnfname


def hebing_wendang(jia, yi, qz):
    if os.path.exists(yi):
        if os.path.exists(jia):
            with open(jia, "a", encoding='utf_8_sig') as jiawen:
                q = qz
                with open(yi, encoding='utf_8_sig') as yiwen:
                    for i in yiwen:
                        q += 1
                        if q > 1:
                            jiawen.write(str(i.rstrip()) + "\n")
        else:
            os.rename(yi, jia)


def shan_wendang(wendang):
    if os.path.exists(wendang):
        os.remove(wendang)


def bianli(chu, dxweizhi):
    wydct = {}
    with open(chu, encoding='utf_8_sig') as nwen:
        k = 0
        for line in nwen:
            k += 1
            if k > 1:
                vmn = line.split(",")[3].rstrip()
                vnf = zhaodao_vnfname(vmn).rstrip()
                duixiang = line.split(",")[dxweizhi]
                dxzhi = line.split(",")[4]
                wydct[vnf] = wydct.get(vnf, {})
                wydct[vnf][duixiang] = wydct[vnf].get(duixiang, [])
                wydct[vnf][duixiang].append(float(dxzhi.strip('%\n')))
    if 'novnf' in wydct:
        del wydct['novnf']
    return wydct


def junzhisl(dct):
    fengzhilb = []
    for item in dct:
        vmlbs = dct[item]
        yuansu = max(vmlbs)
        fengzhilb.append(yuansu)
    jzjg = sum(fengzhilb) / len(fengzhilb)
    jzjg = round(jzjg,2)
    sljg = len(dct)
    jieguo = f'{jzjg},{sljg}'
    return jieguo


def fengzhixt(dct):
    junzhilb = []
    for item in dct:
        sjlbs = dct[item]
        yuansu = sum(sjlbs) / len(sjlbs)
        junzhilb.append(yuansu)
    fzjg = max(junzhilb)
    fzjg = round(fzjg,2)
    xtjg = sum(junzhilb) / len(junzhilb)
    xtjg = round(xtjg,2)
    jieguo = f'{fzjg},{xtjg}'
    return jieguo


def vmjzfz(dct):
    jieguo = []
    for vm in dct:
        vmavg = sum(dct[vm]) / len(dct[vm])
        vmavg = round(vmavg,2)
        vmmax = max(dct[vm])
        vmavg = str(vmavg)
        vmmax = str(vmmax)
        yihang = f'{vm},,{vmavg},{vmmax}'
        jieguo.append(yihang)
    return jieguo


def chuli_jzfz_wendang(jia,dct,func):
    with open(jia, "a", encoding='utf_8_sig') as wen:
        for vnf in dct:
            jg = func(dct[vnf])
            wen.write(vnf + ',' + str(jg) + '\n')


def chuli_vmjzfz_wendang(yi, dct):
    with open(yi, "a", encoding='utf_8_sig') as yiwen:
        title='大区,网元唯一标识,虚拟机名称,虚拟机IP,CPU均值利用率（%）,CPU峰值利用率（%）\n'
        yiwen.write(title)
        for vnf in dct:
            for line in vmjzfz(dct[vnf]):
                yiwen.write(f'西南大区,{vnf},{line}\n')


def chuli_wendang(chu, jia, yi, dxwz, func):
    if os.path.exists(chu):
        dct = bianli(chu, dxwz)
        chuli_jzfz_wendang(jia,dct,func)
        if func is junzhisl:
            chuli_vmjzfz_wendang(yi, dct)


def zidian(chu, lstweizhi, fstweizhi):
    shengchengzd = {}
    with open(chu, encoding='utf_8_sig') as nwen:
        for i in nwen:
            lst = i.split(",")[lstweizhi]
            fst = i.split(",")[fstweizhi]
            shengchengzd[fst] = lst
    return shengchengzd


def shengcheng_yingshe(chu, zhong):
    if os.path.exists(chu):
        with open(zhong, "a", encoding='utf_8_sig') as wen:
            title = '网元,系统均值,均值,峰值,虚机数量\n'
            wen.write(title)
            sczdjz = zidian("jzsl.csv", 1, 0)
            sczdfz = zidian("fzxt.csv", 1, 0)
            sczdxt = zidian("fzxt.csv", -1, 0)
            sczdsl = zidian("jzsl.csv", -1, 0)
            with open(chu, encoding='utf_8_sig') as nwen:
                for i in nwen:
                    vnfname = i.split(",")[0].rstrip()
                    xtjunzhi = sczdxt[vnfname].rstrip()
                    junzhi = sczdjz[vnfname].rstrip()
                    fengzhi = sczdfz[vnfname].rstrip()
                    shuliang = sczdsl[vnfname].rstrip()
                    line = f'{vnfname},{xtjunzhi},{junzhi},{fengzhi},{shuliang}'
                    wen.write(str(line) + "\n")


def check_dy_exists():
    if os.path.exists("dy.csv"):
        global dy
        dy = zidian("dy.csv", -1, 0)
    else:
        print("File dy.csv does not exist!")
        input("\nPress Enter to quit.")
        exit(1)


def main():
    lst = ["jzfz.csv", "jzsl.csv", "fzxt.csv", "vmjzfz.csv"]
    for f in lst:
        shan_wendang(f)
    print("Old files removed yet.")

    hebing_wendang("kx41.csv", "kx42.csv", 0)
    hebing_wendang("kx3.csv", "kx41.csv", 0)
    hebing_wendang("kx3.csv", "kx5.csv", 0)

    chuli_wendang('kx3.csv', 'jzsl.csv', 'vmjzfz.csv', 3, junzhisl)
    print("Average and number done.")
    print("AvgVM and MaxVM done.")
    chuli_wendang('kx3.csv', 'fzxt.csv', None, 0, fengzhixt)
    print("Max and sysavg done.")

    shengcheng_yingshe("jzsl.csv", "jzfz.csv")
    print("Done!")

    lst2 = ["kx3.csv", "kx41.csv", "kx42.csv", "kx5.csv", "jzsl.csv", "fzxt.csv"]
    for fl in lst2:
        shan_wendang(fl)


def extra():
    if man:
        print('\nCheck VMs below:')
        for i in man:
            print(f'• {i}')
        print('\nPress <ENTER> to quit.')
        input()


man=set()


if __name__ == '__main__':
    check_dy_exists()
    main()
    extra()
