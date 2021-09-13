# beta3.0
# 两步到位
# by Li Kai

def shengcheng_sbm(chu, zhong,weizhi):
    import os
    if os.path.exists(chu):
        k = 0
        wen = open(zhong, "a", encoding='UTF-8')
        for i in open(chu, encoding='UTF-8'):
            k += 1
            vmn = i.split(",")[weizhi]
            if k > 1:
                if "-OMC-" in vmn:
                    sbm = ",OMC"
                elif "-NFVO-" in vmn:
                    sbm = ",NFVO"
                elif "-xnqVNFM3" in vmn:
                    sbm = ",VNFM03"
                elif "-VNFM-" in vmn:
                    sbm = ",VNFM"
                else:
                    psbm = vmn.split("-")[7]
                    if "ZX" in psbm:
                        sbm = str("," + psbm[:psbm.index("ZX")] + "ZX")
                    else:
                        sbm = "," + psbm
                line = i.rstrip() + sbm
                wen.write(str(line) + "\n")

def hebing_wendang(jia, yi):
    import os
    if os.path.exists(yi):
        if os.path.exists(jia):
            jiawen = open(jia, "a", encoding='UTF-8')
            q = 0
            for i in open(yi, encoding='UTF-8'):
                q += 1
                if q > 1:
                    jiawen.write(str(i.rstrip()) + "\n")
        else:
            os.rename(yi, jia)

def shan_wendang(wendang):
    import os
    if os.path.exists(wendang):
        os.remove(wendang)

def liebiao(chu, zhuti,panduan,quzhi):
    shengchenglb = []
    for i in open(chu, encoding='UTF-8'):
        lst = i.split(",")[panduan]
        fft = i.split(",")[quzhi]
        if lst == zhuti:
            shengchenglb.append(float(fft.strip('%')))
    return shengchenglb

def lbpingjun(lb):
    pingjun = sum(lb) / len(lb)
    return pingjun

def lbzuida(lb):
    zuida=max(lb)
    return zuida

def xunhuanlb(chu,shengchenglieming): 
    jihe = set('')
    for i in open(chu, encoding='UTF-8'):
        lst = i.split(",")[shengchenglieming]
        jihe.add(lst)
    lbjihe = list(jihe)
    return lbjihe

def chuli(chu, zhong,panduan,quzhi,shengchenglieming,gongneng):
    wen = open(zhong, "a", encoding='UTF-8')
    lbjihe = xunhuanlb(chu,shengchenglieming)
    for j in lbjihe:
        sclb = liebiao(chu, j,panduan,quzhi)
        if gongneng == "pjz":
            pingjunzhi = lbpingjun(sclb)
            pingjunzhi = str(pingjunzhi)
            j=j.rstrip('\n')
            hang = j + ',' + pingjunzhi
            wen.write(str(hang) + "\n")
        elif gongneng == "zdz":
            zuidazhi = lbzuida(sclb)
            zuidazhi = str(zuidazhi)
            j=j.rstrip('\n')
            hang = j + ',' + zuidazhi
            wen.write(str(hang) + "\n")

#######program#######

shan_wendang("jz3.csv")
shan_wendang("jz4.csv")
shan_wendang("jz5.csv")
shan_wendang("fz3.csv")
shan_wendang("fz4.csv")
shan_wendang("fz5.csv")
hebing_wendang(jia="kx41.csv", yi="kx42.csv")
shengcheng_sbm(chu="kx3.csv", zhong="sbmkx3.csv",weizhi=3)
shengcheng_sbm(chu="kx41.csv", zhong="sbmkx4.csv",weizhi=3)
shengcheng_sbm(chu="kx5.csv", zhong="sbmkx5.csv",weizhi=3)
shan_wendang("kx3.csv")
shan_wendang("kx41.csv")
shan_wendang("kx42.csv")
shan_wendang("kx5.csv")
chuli("sbmkx3.csv", "jz3.csv",7,4,7,"pjz")
chuli("sbmkx4.csv", "jz4.csv",7,4,7,"pjz")
chuli("sbmkx5.csv", "jz5.csv",7,4,7,"pjz")
chuli("sbmkx3.csv", "zj3.csv",3,4,3,"zdz")
chuli("sbmkx4.csv", "zj4.csv",3,4,3,"zdz")
chuli("sbmkx5.csv", "zj5.csv",3,4,3,"zdz")
shengcheng_sbm("zj3.csv", "zd3.csv",0)
shengcheng_sbm("zj4.csv", "zd4.csv",0)
shengcheng_sbm("zj5.csv", "zd5.csv",0)
chuli("zd3.csv", "fz3.csv",2,1,2,"pjz")
chuli("zd4.csv", "fz4.csv",2,1,2,"pjz")
chuli("zd5.csv", "fz5.csv",2,1,2,"pjz")
shan_wendang("sbmkx3.csv")
shan_wendang("sbmkx4.csv")
shan_wendang("sbmkx5.csv")
shan_wendang("zj3.csv")
shan_wendang("zj4.csv")
shan_wendang("zj5.csv")
shan_wendang("zd3.csv")
shan_wendang("zd4.csv")
shan_wendang("zd5.csv")
