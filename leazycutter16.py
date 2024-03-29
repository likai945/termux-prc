# beta16
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


def shan_wendang(*wendang):
    for wd in wendang:
        if os.path.exists(wd):
            os.remove(wd)


def danbianli(c,dxweizhi,wydct):
    with open(c, encoding='utf_8_sig') as nwen:
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


def bianli(dxweizhi,*chu):
    wydct = {}
    for c in chu:
        if os.path.exists(c):
            danbianli(c,dxweizhi,wydct)
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
    jieguo = [jzjg,sljg]
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
    jieguo = [fzjg,xtjg]
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


def chuli_jzfz_wendang(dct,func):
    for vnf in dct:
        zd[vnf]=zd.get(vnf,[])
        jg = func(dct[vnf])
        zd[vnf]+=jg


def chuli_vmjzfz_wendang(yi, dct):
    with open(yi, "a", encoding='utf_8_sig') as yiwen:
        title='大区,网元唯一标识,虚拟机名称,虚拟机IP,CPU均值利用率（%）,CPU峰值利用率（%）\n'
        yiwen.write(title)
        for vnf in dct:
            for line in vmjzfz(dct[vnf]):
                yiwen.write(f'西南大区,{vnf},{line}\n')


def chuli_wendang(yi,*chu):
    dct = bianli(3,*chu)
    chuli_jzfz_wendang(dct,junzhisl)
    print("Average and number done.")
    if dct:
        chuli_vmjzfz_wendang(yi, dct)
        print("AvgVM and MaxVM done.")
    dct = bianli(0,*chu)
    chuli_jzfz_wendang(dct,fengzhixt)
    print("Max and sysavg done.")


def zidian(chu, lstweizhi, fstweizhi):
    shengchengzd = {}
    with open(chu, encoding='utf_8_sig') as nwen:
        for i in nwen:
            lst = i.split(",")[lstweizhi]
            fst = i.split(",")[fstweizhi]
            shengchengzd[fst] = lst
    return shengchengzd


def shengcheng_biaoge(biao):
    with open(biao, "a", encoding='utf_8_sig') as wen:
        title = '网元,系统均值,均值,峰值,虚机数量\n'
        wen.write(title)
        for vnf in zd: 
            vnfname=vnf
            xtjunzhi=zd[vnf][3]
            junzhi=zd[vnf][0]
            fengzhi=zd[vnf][2]
            shuliang=zd[vnf][1]
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
    shan_wendang("jzfz.csv", "vmjzfz.csv")
    print("Old files removed yet.")

    chuli_wendang('vmjzfz.csv', 'kx3.csv','kx41.csv','kx42.csv','kx5.csv')
    if zd:
        shengcheng_biaoge("jzfz.csv")
        print("Done!")

    shan_wendang("kx3.csv", "kx41.csv", "kx42.csv", "kx5.csv")


def extra():
    if man:
        print('\nCheck VMs below:')
        for i in man:
            print(f'• {i}')
        print('\nPress <ENTER> to quit.')
        input()


man=set()
zd={}


if __name__ == '__main__':
    check_dy_exists()
    main()
    extra()
