# beta3.0
# 用法：将导出的资料分别按照kx3.csv、kx41.csv、kx42.csv、kx5.csv命名，放置在本工具所在目录后双击稍事等待即可得到名为jzx.csv和fzx.csv的文件，分别对应均值和峰值
# by Li Kai



import os


def shengcheng_sbm(chu, zhong, weizhi, kz):
    if os.path.exists(chu):
        k = kz
        wen = open(zhong, "a", encoding='utf_8_sig')
        for i in open(chu, encoding='utf_8_sig'):
            k += 1
            inkey = "no"
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
                else:
                    psbm = vmn.split("-")[7]
                    if "ZX" in psbm:
                        sbm = str(psbm[:psbm.index("ZX")] + "ZX")
                    else:
                        sbm = psbm
                if sbm in dy:
                    sbm = dy[sbm]
                    inkey = "yes"
                vnfname = "," + sbm
                if inkey == "yes":
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


def lbpingjun(lb):
    pingjun = sum(lb) / len(lb)
    return pingjun


def lbzuida(lb):
    zuida = max(lb)
    return zuida


def xunhuanlb(chu, shengchenglieming):
    jihe = set('')
    for i in open(chu, encoding='utf_8_sig'):
        lst = i.split(",")[shengchenglieming]
        jihe.add(lst)
    lbjihe = list(jihe)
    return lbjihe


def chuli(chu, zhong, panduan, quzhi, shengchenglieming, gongneng):
    if os.path.exists(chu):
        wen = open(zhong, "a", encoding='utf_8_sig')
        lbjihe = xunhuanlb(chu, shengchenglieming)
        for j in lbjihe:
            sclb = liebiao(chu, j, panduan, quzhi)
            if gongneng == "pjz":
                pingjunzhi = lbpingjun(sclb)
                pingjunzhi = str(pingjunzhi)
                j = j.rstrip('\n')
                hang = j + ',' + pingjunzhi
                wen.write(str(hang) + "\n")
            elif gongneng == "zdz":
                zuidazhi = lbzuida(sclb)
                zuidazhi = str(zuidazhi)
                j = j.rstrip('\n')
                hang = j + ',' + zuidazhi
                wen.write(str(hang) + "\n")


def zidian(chu):
    shengchengzd = {}
    for i in open(chu, encoding='utf_8_sig'):
        lst = i.split(",")[1]
        fst = i.split(",")[0]
        shengchengzd[fst] = lst
    return shengchengzd


def shengcheng_yingshe(chu, zhong):
    if os.path.exists(chu):
        wen = open(zhong, "a", encoding='utf_8_sig')
        sczd = zidian("fz3.csv")
        for i in open(chu, encoding='utf_8_sig'):
            vnfname = i.split(",")[0]
            line = i.rstrip("\n") + "," + sczd[vnfname].rstrip("\n")
            wen.write(str(line) + "\n")


#######program#######

if os.path.exists("dy.csv"):
    dy = zidian("dy.csv")
else:
    print("File dy.csv in need!")
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

chuli("sbmkx3.csv", "jz3.csv", 7, 4, 7, "pjz")
print("Average of kx3 done.")
chuli("sbmkx4.csv", "jz4.csv", 7, 4, 7, "pjz")
print("Average of kx4 done.")
chuli("sbmkx5.csv", "jz5.csv", 7, 4, 7, "pjz")
print("Average of kx5 done.")

print("This part may take a long time, just wait or do whatever you like :)")
chuli("sbmkx3.csv", "zj3.csv", 3, 4, 3, "zdz")
chuli("sbmkx4.csv", "zj4.csv", 3, 4, 3, "zdz")
chuli("sbmkx5.csv", "zj5.csv", 3, 4, 3, "zdz")
shan_wendang("sbmkx3.csv")
shan_wendang("sbmkx4.csv")
shan_wendang("sbmkx5.csv")
shengcheng_sbm("zj3.csv", "zd3.csv", 0, 1)
shengcheng_sbm("zj4.csv", "zd4.csv", 0, 1)
shengcheng_sbm("zj5.csv", "zd5.csv", 0, 1)
shan_wendang("zj3.csv")
shan_wendang("zj4.csv")
shan_wendang("zj5.csv")
chuli("zd3.csv", "fz3.csv", 2, 1, 2, "pjz")
print("Max of kx3 done.")
chuli("zd4.csv", "fz4.csv", 2, 1, 2, "pjz")
print("Max of kx4 done.")
chuli("zd5.csv", "fz5.csv", 2, 1, 2, "pjz")
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
shengcheng_yingshe("jz3.csv", "jzfz.csv")
print("Done!")

shan_wendang("jz3.csv")
shan_wendang("fz3.csv")
