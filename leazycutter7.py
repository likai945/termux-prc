# beta7.0
# 立等可取
# 用法：将导出的资料分别按照kx3.csv、kx41.csv、kx42.csv、kx5.csv命名，放置在本工具所在目录后双击稍事等待即可得到名为jzfz.csv的文件，由四列构成，分别为网元名、对应系统均值、均值、峰值和网元的虚机数量，与需填报的报表相对应。
# 需配合dy.csv文件使用
# by Li Kai


import os


def shengcheng_sbm(chu, zhong, kz):
    if os.path.exists(chu):
        k = kz
        with open(zhong, "a", encoding='utf_8_sig') as wen:
            with open(chu, encoding='utf_8_sig') as nwen:
                for i in nwen:
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
        for line in nwen:
            vnf = line.split(",")[-1].rstrip()
            duixiang = line.split(",")[dxweizhi]
            dxzhi = line.split(",")[4]
            wydct[vnf] = wydct.get(vnf, {})
            wydct[vnf][duixiang] = wydct[vnf].get(duixiang, [])
            wydct[vnf][duixiang].append(float(dxzhi.strip('%')))
    return wydct


def junzhisl(dct):
    fengzhilb = []
    for item in dct:
        vmlbs = dct[item]
        yuansu = max(vmlbs)
        fengzhilb.append(yuansu)
    jzjg = sum(fengzhilb) / len(fengzhilb)
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
    xtjg = sum(junzhilb) / len(junzhilb)
    jieguo = f'{fzjg},{xtjg}'
    return jieguo


def chuli_wendang(chu, zhong, dxwz, jzorfzorxtorsl):
    if os.path.exists(chu):
        with open(zhong, "a", encoding='utf_8_sig') as wen:
            dct = bianli(chu, dxwz)
            for vnf in dct:
                if jzorfzorxtorsl == 'jzsl':
                    jg = junzhisl(dct[vnf])
                elif jzorfzorxtorsl == 'fzxt':
                    jg = fengzhixt(dct[vnf])
                wen.write(vnf + ',' + str(jg) + '\n')


def zidian(chu, lstweizhi, fstweizhi):
    shengchengzd = {}
    with open(chu, encoding='utf_8_sig') as nwen:
        for i in nwen:
            if i != "\n":
                lst = i.split(",")[lstweizhi]
                fst = i.split(",")[fstweizhi]
                shengchengzd[fst] = lst
    return shengchengzd


def shengcheng_yingshe(chu, zhong):
    if os.path.exists(chu):
        with open(zhong, "a", encoding='utf_8_sig') as wen:
            sczdjz = zidian("jzsl3.csv", 1, 0)
            sczdfz = zidian("fzxt3.csv", 1, 0)
            sczdxt = zidian("fzxt3.csv", -1, 0)
            sczdsl = zidian("jzsl3.csv", -1, 0)
            with open(chu, encoding='utf_8_sig') as nwen:
                for i in nwen:
                    vnfname = i.split(",")[0].rstrip()
                    xtjunzhi = sczdxt[vnfname].rstrip()
                    junzhi = sczdjz[vnfname].rstrip()
                    fengzhi = sczdfz[vnfname].rstrip()
                    shuliang = sczdsl[vnfname].rstrip()
                    line = f'{vnfname},{xtjunzhi},{junzhi},{fengzhi},{shuliang}'
                    wen.write(str(line) + "\n")


#######program#######

if os.path.exists("dy.csv"):
    dy = zidian("dy.csv", 1, 0)
else:
    print("File dy.csv does not exist!")
    input("\nPress Enter to quit.")
    exit(1)

shan_wendang("jzfz.csv")
shan_wendang("sbmkx3.csv")
shan_wendang("sbmkx4.csv")
shan_wendang("sbmkx5.csv")
shan_wendang("jzsl4.csv")
shan_wendang("jzsl5.csv")
shan_wendang("fzxt4.csv")
shan_wendang("fzxt5.csv")
shan_wendang("jzsl3.csv")
shan_wendang("fzxt3.csv")
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

chuli_wendang('sbmkx3.csv', 'jzsl3.csv', 3, 'jzsl')
print("Average and number of kx3 done.")
chuli_wendang('sbmkx4.csv', 'jzsl4.csv', 3, 'jzsl')
print("Average and number of kx4 done.")
chuli_wendang('sbmkx5.csv', 'jzsl5.csv', 3, 'jzsl')
print("Average and number of kx5 done.")

chuli_wendang('sbmkx3.csv', 'fzxt3.csv', 0, 'fzxt')
print("Max and sysavg of kx3 done.")
chuli_wendang('sbmkx4.csv', 'fzxt4.csv', 0, 'fzxt')
print("Max and sysavg of kx4 done.")
chuli_wendang('sbmkx5.csv', 'fzxt5.csv', 0, 'fzxt')
print("Max and sysavg of kx5 done.")

shan_wendang("sbmkx3.csv")
shan_wendang("sbmkx4.csv")
shan_wendang("sbmkx5.csv")

hebing_wendang("jzsl3.csv", "jzsl4.csv", 1)
hebing_wendang("jzsl3.csv", "jzsl5.csv", 1)
shan_wendang("jzsl4.csv")
shan_wendang("jzsl5.csv")
hebing_wendang("fzxt3.csv", "fzxt4.csv", 1)
hebing_wendang("fzxt3.csv", "fzxt5.csv", 1)
shan_wendang("fzxt4.csv")
shan_wendang("fzxt5.csv")

shengcheng_yingshe("jzsl3.csv", "jzfz.csv")
print("Done!")

shan_wendang("jzsl3.csv")
shan_wendang("fzxt3.csv")
