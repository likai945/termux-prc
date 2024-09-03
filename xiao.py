import random
import sys

def select_one():
    return random.randint(0,11)


def select_five():
    balls=list(range(1,49))
    random.shuffle(balls)
    zodiacs=[i%12 for i in balls]
    return zodiacs[:5]


def stir_balls():
    balls=list(range(1,49))
    random.shuffle(balls)
    outbs=balls[:7]

    return outbs


def buy_mark():
    one=select_one()
    five=select_five()
    balls=stir_balls()
    zodiacs=[i%12 for i in balls]
    print('-----')
    print(zl[one])
    print([zl[i] for i in five])
    print(balls)
    print([zl[i] for i in zodiacs])

    global money

    if one in zodiacs:
        money+=1
    else:
        money-=1

    for i in five:
        if i in zodiacs:
            zodiacs.remove(i)
    if len(zodiacs)<3:
        money+=100
        print('win')
    else:
        money-=1

    return money


money=0
zl=['🐍','🐲','🐰','🐯','🐮','🐀','🐷','🐶','🐔','🐒','🐑','🐴']

if __name__=='__main__':
    for i in range(int(sys.argv[1])):
        buy_mark()

    print(money)

