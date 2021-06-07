# beta3.0
# 脚本名为leazycutter，为ezcutter的升级版，更为方便省心。
# 此脚本用于快速提取虚拟机名称内的识别码部分，即第八段中开头至ZX的字符串。并将该部分与原内容合并成新的文档，便于直接模板采用，同时会将可信4的两部分合并为一。
# 将自TECS导出的资料按kx3.csv、kx41.csv、kx42.csv、kx5.csv命名后拖至指定目录双击leazycutter运行即可生成以sbm开头的新csv文档，这时会发现各文档新增了“识别码”一列，可信4两部分已合二为一。
# 脚本运行开始会自动删除上次的sbm文本，完成后会自动删除已经处理的原始文本，以便下次使用。
#此次更新增加了对管理网元的支持。
# by Li Kai

def shengcheng_sbm(chu, zhong):
    import os
    if os.path.exists(chu):
        k = 0
        wen = open(zhong, "a", encoding='UTF-8')
        for i in open(chu, encoding='UTF-8'):
            k += 1
            vmn = i.split(",")[3]
            if k == 1:
                sbm = ",识别码"
            elif k > 1:
                if "-OMC-" in vmn:
                    sbm = ",OMC"
                elif "NFVO" in vmn:
                    sbm = ",NFVO"
                elif "xnqVNFM3" in vmn:
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


#######program#######

shan_wendang("sbmkx3.csv")
shan_wendang("sbmkx4.csv")
shan_wendang("sbmkx5.csv")
hebing_wendang(jia="kx41.csv", yi="kx42.csv")
shengcheng_sbm(chu="kx3.csv", zhong="sbmkx3.csv")
shengcheng_sbm(chu="kx41.csv", zhong="sbmkx4.csv")
shengcheng_sbm(chu="kx5.csv", zhong="sbmkx5.csv")
shan_wendang("kx3.csv")
shan_wendang("kx41.csv")
shan_wendang("kx42.csv")
shan_wendang("kx5.csv")
