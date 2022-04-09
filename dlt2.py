import random

redballs=list(range(1,36))
blueballs=list(range(1,13))

def slct_blls(balls,num):
    random.shuffle(balls)
    chsn=balls[:num]
    chsn.sort()
    return chsn

def print_blls(balls,color):
    colors={'red':31,'blue':34}
    for i in balls:
        print(f'\033[{colors[color]}m{i} \033[0m',end='')

def do_it():
    redb=slct_blls(redballs,5)
    blb=slct_blls(blueballs,2)
    print_blls(redb,'red')
    print('+ ',end='')
    print_blls(blb,'blue')
    print('')

if __name__ == '__main__':
    do_it()
