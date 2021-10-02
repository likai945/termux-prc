# beta5.0
# 用法：将导出的资料分别按照kx3.csv、kx41.csv、kx42.csv、kx5.csv命名，放置在本工具所在目录后双击稍事等待即可得到名为jzfz.csv的文件，由四列构成，分别为网元名、对应系统均值、均值、峰值和网元的虚机数量，与需填报的报表相对应。
# 需配合dy.csv文件使用
# by Li Kai


import os


def shengcheng_sbm(chu, zhong, kz):
    if os.path.exists(chu):
        k = kz
        wen = open(zhong, "a", encoding='utf_8_sig')
        for i in open(chu, encoding='utf_8_sig'):
            k += 1
            vmn = i.split(",")[3]
            if k > 1:
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
                        sbm = str(psbm[:psbm.index("ZX")] + "ZX")
                    else:
                        sbm = psbm
                if sbm in dy:
                    sbm = dy[sbm]
                    vnfname = "," + sbm
                    line = i.rstrip() + vnfname
                    wen.write(str(line))


def hebing_wendang(jia, yi, qz):
    if os.path.exists(yi):
        if os.path.exists(jia):
            jiawen = open(jia, "a", encoding='utf_8_sig')
            q = qz
            for i in open(yi, encoding='utf_8_sig'):
                q += 1
                if q > 1:
                    jiawen.write(str(i.rstrip()) + "\n")
        else:
            os.rename(yi, jia)


def shan_wendang(wendang):
    if os.path.exists(wendang):
        os.remove(wendang)


def xunhuanlb(chu, shengchenglieming):
    jihe = set('')
    for i in open(chu, encoding='utf_8_sig'):
        lst = i.split(",")[shengchenglieming]
        jihe.add(lst)
    lbjihe = list(jihe)
    return lbjihe


def bianli(chu, dxweizhi, vnfname):
    wydct = {}
    for line in open(chu, encoding='utf_8_sig'):
        dxpd = line.split(",")[-1]
        duixiang = line.split(",")[dxweizhi]
        dxzhi = line.split(",")[4]
        if dxpd == vnfname:
            wydct[duixiang] = wydct.get(duixiang, [])
            wydct[duixiang].append(float(dxzhi.strip('%')))
    return wydct


def junzhi(dct):
    fengzhilb = []
    for item in dct:
        vmlbs = dct[item]
        yuansu = max(vmlbs)
        fengzhilb.append(yuansu)
    jieguo = sum(fengzhilb) / len(fengzhilb)
    return jieguo


def fengzhi(dct):
    junzhilb = []
    for item in dct:
        sjlbs = dct[item]
        yuansu = sum(sjlbs) / len(sjlbs)
        junzhilb.append(yuansu)
    jieguo = max(junzhilb)
    return jieguo


def xtjunzhi(chu,vnfname):
    xtjzlb = []
    for line in open(chu, encoding='utf_8_sig'):
        dxpd = line.split(",")[-1]
        dxzhi = line.split(",")[4]
        if dxpd == vnfname:
            xtjzlb.append(float(dxzhi.strip('%')))
    jieguo = sum(xtjzlb) / len(xtjzlb)
    return jieguo


def shuliang(dct):
    jieguo = len(dct)
    return jieguo


def chuli_wendang(chu, zhong, jzorfzorxtorsl):
    global jg
    if os.path.exists(chu):
        wen = open(zhong, "a", encoding='utf_8_sig')
        sclb = xunhuanlb(chu, -1)
        for vnf in sclb:
            if jzorfzorxtorsl == 'jz':
                dct = bianli(chu, 3, vnf)
                jg = junzhi(dct)
            elif jzorfzorxtorsl == 'fz':
                dct = bianli(chu, 0, vnf)
                jg = fengzhi(dct)
            elif jzorfzorxtorsl == 'xtjz':
                jg = xtjunzhi(chu,vnf)
            elif jzorfzorxtorsl == 'sl':
                dct = bianli(chu, 3, vnf)
                jg = shuliang(dct)
            wen.write(vnf.rstrip() + ',' + str(jg) + '\n')


def zidian(chu, lstweizhi, fstweizhi):
    shengchengzd = {}
    for i in open(chu, encoding='utf_8_sig'):
        if i != "\n":
            lst = i.split(",")[lstweizhi]
            fst = i.split(",")[fstweizhi]
            shengchengzd[fst] = lst
    return shengchengzd


def shengcheng_yingshe(chu, zhong):
    if os.path.exists(chu):
        wen = open(zhong, "a", encoding='utf_8_sig')
        sczdjz = zidian("jz3.csv", -1, 0)
        sczdfz = zidian("fz3.csv", -1, 0)
        sczdsl = zidian("sl3.csv", -1, 0)
        for i in open(chu, encoding='utf_8_sig'):
            vnfname = i.split(",")[0]
            line = i.rstrip() + "," + sczdjz[vnfname].rstrip() + "," + sczdfz[vnfname].rstrip() + ',' + sczdsl[
                vnfname].rstrip()
            wen.write(str(line) + "\n")


#######program#######

if os.path.exists("dy.csv"):
    dy = zidian("dy.csv", 1, 0)
else:
    print("File dy.csv in need!")
    input("\nPress Enter to quit.")
    exit(1)

shan_wendang("jzfz.csv")
shan_wendang("sbmkx3.csv")
shan_wendang("sbmkx4.csv")
shan_wendang("sbmkx5.csv")
shan_wendang("sl3.csv")
shan_wendang("sl4.csv")
shan_wendang("sl5.csv")
shan_wendang("jz4.csv")
shan_wendang("jz5.csv")
shan_wendang("fz4.csv")
shan_wendang("fz5.csv")
shan_wendang("jz3.csv")
shan_wendang("fz3.csv")
shan_wendang("xtjz5.csv")
shan_wendang("xtjz3.csv")
shan_wendang("xtjz4.csv")
print("Old files removed yet.")

hebing_wendang(jia="kx41.csv", yi="kx42.csv", qz=0)
shengcheng_sbm(chu="kx3.csv", zhong="sbmkx3.csv", kz=0)
shengcheng_sbm(chu="kx41.csv", zhong="sbmkx4.csv", kz=0)
shengcheng_sbm(chu="kx5.csv", zhong="sbmkx5.csv", kz=0)
print("SBM files done.")

shan_wendang("kx3.csv")
shan_wendang("kx41.csv")
shan_wendang("kx42.csv")
shan_wendang("kx5.csv")

chuli_wendang('sbmkx3.csv', 'jz3.csv', 'jz')
print("Average of kx3 done.")
chuli_wendang('sbmkx4.csv', 'jz4.csv', 'jz')
print("Average of kx4 done.")
chuli_wendang('sbmkx5.csv', 'jz5.csv', 'jz')
print("Average of kx5 done.")

chuli_wendang('sbmkx3.csv', 'fz3.csv', 'fz')
print("Max of kx3 done.")
chuli_wendang('sbmkx4.csv', 'fz4.csv', 'fz')
print("Max of kx4 done.")
chuli_wendang('sbmkx5.csv', 'fz5.csv', 'fz')
print("Max of kx5 done.")

chuli_wendang('sbmkx3.csv', 'xtjz3.csv', 'xtjz')
print("Sysavg of kx3 done.")
chuli_wendang('sbmkx4.csv', 'xtjz4.csv', 'xtjz')
print("Sysavg of kx4 done.")
chuli_wendang('sbmkx5.csv', 'xtjz5.csv', 'xtjz')
print("Sysavg of kx5 done.")

chuli_wendang('sbmkx3.csv', 'sl3.csv', 'sl')
print("Number of kx3 done.")
chuli_wendang('sbmkx4.csv', 'sl4.csv', 'sl')
print("Number of kx4 done.")
chuli_wendang('sbmkx5.csv', 'sl5.csv', 'sl')
print("Number of kx5 done.")

shan_wendang("sbmkx3.csv")
shan_wendang("sbmkx4.csv")
shan_wendang("sbmkx5.csv")

hebing_wendang("jz3.csv", "jz4.csv", 1)
hebing_wendang("jz3.csv", "jz5.csv", 1)
shan_wendang("jz4.csv")
shan_wendang("jz5.csv")
hebing_wendang("fz3.csv", "fz4.csv", 1)
hebing_wendang("fz3.csv", "fz5.csv", 1)
shan_wendang("fz4.csv")
shan_wendang("fz5.csv")
hebing_wendang("xtjz3.csv", "xtjz4.csv", 1)
hebing_wendang("xtjz3.csv", "xtjz5.csv", 1)
shan_wendang("xtjz4.csv")
shan_wendang("xtjz5.csv")
hebing_wendang("sl3.csv", "sl4.csv", 1)
hebing_wendang("sl3.csv", "sl5.csv", 1)
shan_wendang("sl4.csv")
shan_wendang("sl5.csv")

shengcheng_yingshe("xtjz3.csv", "jzfz.csv")
print("Done!")

shan_wendang("jz3.csv")
shan_wendang("fz3.csv")
shan_wendang("xtjz3.csv")
shan_wendang("sl3.csv")
