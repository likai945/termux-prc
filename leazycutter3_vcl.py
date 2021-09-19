# beta3.5
# 用法：将导出的资料分别按照kx3.csv、kx41.csv、kx42.csv、kx5.csv命名，放置在本工具所在目录后双击稍事等待即可得到名为jzfz.csv的文件，由四列构成，分别为网元名、对应均值、峰值和网元的虚机数量，与需填报的报表相对应。
# 需配合dy.csv文件使用
# by Li Kai


import os


def shengcheng_sbm(chu, zhong, weizhi, kz):
    if os.path.exists(chu):
        k = kz
        wen = open(zhong, "a", encoding='utf_8_sig')
        for i in open(chu, encoding='utf_8_sig'):
            k += 1
            vmn = i.split(",")[weizhi]
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


def liebiao(chu, zhuti, panduan, quzhi):
    shengchenglb = []
    for i in open(chu, encoding='utf_8_sig'):
        lst = i.split(",")[panduan]
        fft = i.split(",")[quzhi]
        if lst == zhuti:
            shengchenglb.append(float(fft.strip('%')))
    return shengchenglb


def xunhuanlb(chu, shengchenglieming):
    jihe = set('')
    for i in open(chu, encoding='utf_8_sig'):
        lst = i.split(",")[shengchenglieming]
        jihe.add(lst)
    lbjihe = list(jihe)
    return lbjihe


def chuli(chu, zhong, panduan, quzhi, shengchenglieming, gongneng, shuliangpanduan):
    if os.path.exists(chu):
        wen = open(zhong, "a", encoding='utf_8_sig')
        lbjihe = xunhuanlb(chu, shengchenglieming)
        for j in lbjihe:
            sclb = liebiao(chu, j, panduan, quzhi)
            if gongneng == "pjz":
                pingjunzhi = sum(sclb) / len(sclb)
                pingjunzhi = str(pingjunzhi)
                j = j.rstrip('\n')
                if shuliangpanduan == "yes":
                    shuliang = len(sclb)
                    shuliang = str(shuliang)
                    hang = j + ',' + pingjunzhi + ',' + shuliang
                else:
                    hang = j + ',' + pingjunzhi
                wen.write(str(hang) + "\n")
            elif gongneng == "zdz":
                zuidazhi = max(sclb)
                zuidazhi = str(zuidazhi)
                j = j.rstrip('\n')
                hang = j + ',' + zuidazhi
                wen.write(str(hang) + "\n")


def zidian(chu, lstweizhi, fstweizhi):
    shengchengzd = {}
    for i in open(chu, encoding='utf_8_sig'):
        if i != "\n":
            lst = i.split(",")[lstweizhi]
            fst = i.split(",")[fstweizhi]
            shengchengzd[fst] = lst
    return shengchengzd


def shengcheng_yingshe(chu, zhong, lstweizhi, scdweizhi, fstweizhi):
    if os.path.exists(chu):
        wen = open(zhong, "a", encoding='utf_8_sig')
        sczdfz = zidian("fz3.csv", scdweizhi, fstweizhi)
        sczdsl = zidian("fz3.csv", lstweizhi, fstweizhi)
        for i in open(chu, encoding='utf_8_sig'):
            vnfname = i.split(",")[0]
            line = i.rstrip("\n") + "," + sczdfz[vnfname].rstrip("\n") + "," + sczdsl[vnfname].rstrip("\n")
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
shan_wendang("zj3.csv")
shan_wendang("zj4.csv")
shan_wendang("zj5.csv")
shan_wendang("zd3.csv")
shan_wendang("zd4.csv")
shan_wendang("zd5.csv")
shan_wendang("jz4.csv")
shan_wendang("jz5.csv")
shan_wendang("fz4.csv")
shan_wendang("fz5.csv")
shan_wendang("jz3.csv")
shan_wendang("fz3.csv")

print("Old files removed yet.")
hebing_wendang(jia="kx41.csv", yi="kx42.csv", qz=0)
shengcheng_sbm(chu="kx3.csv", zhong="sbmkx3.csv", weizhi=3, kz=0)
shengcheng_sbm(chu="kx41.csv", zhong="sbmkx4.csv", weizhi=3, kz=0)
shengcheng_sbm(chu="kx5.csv", zhong="sbmkx5.csv", weizhi=3, kz=0)
print("SBM files done.")

shan_wendang("kx3.csv")
shan_wendang("kx41.csv")
shan_wendang("kx42.csv")
shan_wendang("kx5.csv")

chuli("sbmkx3.csv", "jz3.csv", 7, 4, 7, "pjz", "no")
print("Average of kx3 done.")
chuli("sbmkx4.csv", "jz4.csv", 7, 4, 7, "pjz", "no")
print("Average of kx4 done.")
chuli("sbmkx5.csv", "jz5.csv", 7, 4, 7, "pjz", "no")
print("Average of kx5 done.")

print("This part may take a long time, just wait or do whatever you like :)")
chuli("sbmkx3.csv", "zj3.csv", 3, 4, 3, "zdz", "no")
chuli("sbmkx4.csv", "zj4.csv", 3, 4, 3, "zdz", "no")
chuli("sbmkx5.csv", "zj5.csv", 3, 4, 3, "zdz", "no")
shan_wendang("sbmkx3.csv")
shan_wendang("sbmkx4.csv")
shan_wendang("sbmkx5.csv")
shengcheng_sbm("zj3.csv", "zd3.csv", 0, 1)
shengcheng_sbm("zj4.csv", "zd4.csv", 0, 1)
shengcheng_sbm("zj5.csv", "zd5.csv", 0, 1)
shan_wendang("zj3.csv")
shan_wendang("zj4.csv")
shan_wendang("zj5.csv")
chuli("zd3.csv", "fz3.csv", 2, 1, 2, "pjz", "yes")
print("Max of kx3 done.")
chuli("zd4.csv", "fz4.csv", 2, 1, 2, "pjz", "yes")
print("Max of kx4 done.")
chuli("zd5.csv", "fz5.csv", 2, 1, 2, "pjz", "yes")
print("Max of kx5 done.")

shan_wendang("zd3.csv")
shan_wendang("zd4.csv")
shan_wendang("zd5.csv")

hebing_wendang("jz3.csv", "jz4.csv", 1)
hebing_wendang("jz3.csv", "jz5.csv", 1)
shan_wendang("jz4.csv")
shan_wendang("jz5.csv")
hebing_wendang("fz3.csv", "fz4.csv", 1)
hebing_wendang("fz3.csv", "fz5.csv", 1)
shan_wendang("fz4.csv")
shan_wendang("fz5.csv")
shengcheng_yingshe("jz3.csv", "jzfz.csv", 2, 1, 0)
print("Done!")

shan_wendang("jz3.csv")
shan_wendang("fz3.csv")
