# beta9.2
# 此版本增加虚机文档生成功能
# 立等可取
# 用法：将导出的资料分别按照kx3.csv、kx41.csv、kx42.csv、kx5.csv命名，放置在本工具所在目录后双击稍事等待即可得到名为jzfz.csv的文件，由四列构成，分别为网元名、对应系统均值、均值、峰值和网元的虚机数量，与需填报的报表相对应。
# 需配合dy.csv文件使用
# by Li Kai


import os


def zhaodao_vnfname(vmn):
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
                wydct[vnf][duixiang].append(float(dxzhi.strip('%')))
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


def vmjzfz(dct):
    jieguo = []
    for vm in dct:
        vmavg = sum(dct[vm]) / len(dct[vm])
        vmmax = max(dct[vm])
        vmavg = str(vmavg)
        vmmax = str(vmmax)
        yihang = f'{vm},{vmavg},{vmmax}'
        jieguo.append(yihang)
    return jieguo


def chuli_wendang(chu, zhong, dxwz, jzorfzorxtorsl):
    if os.path.exists(chu):
        with open(zhong, "a", encoding='utf_8_sig') as wen:
            dct = bianli(chu, dxwz)
            for vnf in dct:
                if jzorfzorxtorsl == 'jzsl':
                    jg = junzhisl(dct[vnf])
                    wen.write(vnf + ',' + str(jg) + '\n')
                elif jzorfzorxtorsl == 'fzxt':
                    jg = fengzhixt(dct[vnf])
                    wen.write(vnf + ',' + str(jg) + '\n')
                elif jzorfzorxtorsl == 'vmjzfz':
                    for line in vmjzfz(dct[vnf]):
                        wen.write(f'西南大区,{vnf},{line}\n')


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
        dy = zidian("dy.csv", 1, 0)
    else:
        print("File dy.csv does not exist!")
        input("\nPress Enter to quit.")
        exit(1)


def main():
    lst = ["jzfz.csv", "jzsl.csv", "fzxt.csv", "vmjzfz.csv"]
    for f in lst:
        shan_wendang(f)
    print("Old files removed yet.")

    hebing_wendang(jia="kx41.csv", yi="kx42.csv", qz=0)
    hebing_wendang(jia="kx3.csv", yi="kx41.csv", qz=0)
    hebing_wendang(jia="kx3.csv", yi="kx5.csv", qz=0)

    chuli_wendang('kx3.csv', 'jzsl.csv', 3, 'jzsl')
    print("Average and number done.")

    chuli_wendang('kx3.csv', 'fzxt.csv', 0, 'fzxt')
    print("Max and sysavg done.")

    chuli_wendang('kx3.csv', 'vmjzfz.csv', 3, 'vmjzfz')
    print("AvgVM and MaxVM done.")

    shan_wendang("kx3.csv")
    shan_wendang("kx41.csv")
    shan_wendang("kx42.csv")
    shan_wendang("kx5.csv")

    shengcheng_yingshe("jzsl.csv", "jzfz.csv")
    print("Done!")

    shan_wendang("jzsl.csv")
    shan_wendang("fzxt.csv")


if __name__ == '__main__':
    check_dy_exists()
    main()
