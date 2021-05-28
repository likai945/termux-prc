#!/usr/bin/python
# -*- coding: utf-8 -*-
def shengcheng_sbm(chu,zhong):
    import os
    if os.path.exists(chu):
        k=0
        wen=open(zhong,"a")
        for i in open(chu):
            k+=1
            vmn=i.split(",")[3]
            if k==1:
                sbm=",识别码"
            elif k>1:
                psbm=vmn.split("-")[7]
                if "ZX" in psbm:
                    sbm=str(","+psbm[:psbm.index("ZX")]+"ZX")
                else:
                    sbm=","+psbm
            line=i.rstrip()+sbm
            wen.write(str(line)+"\n")

def hebing_wendang(jia,yi):
    import os
    if os.path.exists(yi):
        if os.path.exists(jia):
            jiawen=open(jia,"a")
            q=0
            for i in open(yi):
                q+=1
                if q>1:
                    jiawen.write(str(i.rstrip())+"\n")
        else:
            os.rename(yi,jia)

def shan_wendang(wendang):
    import os
    if os.path.exists(wendang):
        os.remove(wendang)

#######program#######
shan_wendang("sbmkx3.csv")
shan_wendang("sbmkx4.csv")
shan_wendang("sbmkx5.csv")
hebing_wendang(jia="kx41.csv",yi="kx42.csv")
shengcheng_sbm(chu="kx3.csv",zhong="sbmkx3.csv")
shengcheng_sbm(chu="kx41.csv",zhong="sbmkx4.csv")
shengcheng_sbm(chu="kx5.csv",zhong="sbmkx5.csv")
shan_wendang("kx3.csv")
shan_wendang("kx41.csv")
shan_wendang("kx42.csv")
shan_wendang("kx5.csv")
