import random

def split(money,quantity):
    intM=float(money)*100
    splQ=int(quantity)-1
    divQ=1 if splQ==0 else splQ
    lmtM=intM//4*3//divQ
    lmtM=1 if lmtM==0 else lmtM
    lowM=lmtM//3
    lowM=1 if lowM==0 else lowM

    if intM//int(quantity)==0:
        print("low to earth!")
        return 2

    for i in range(0,splQ):
        oneM=random.randint(lowM,intM-splQ*lmtM)
        spLst.append(oneM/100)
        splQ-=1
        intM-=oneM

    spLst.append(intM/100)
    random.shuffle(spLst)

#    print(spLst)

def lishi():
    name=input("win:")
    getM=spLst.pop()
    if getM==luckyM:
        luckyG.append(name)
    print(f'\t{name} ¥{getM}')

def main():
    while True:
        money=input('money:')
        quantity=input('quantity:')
        split(money,quantity)
        if spLst:
            break

    global luckyM
    luckyM=max(spLst)

    while True:
        lishi()
        if not spLst:
            print('\nno money')
            print(f'lucky guy is {luckyG}, he got ¥{luckyM}.')
            return

spLst=[]
luckyG=[]

if __name__=='__main__':
    main()
