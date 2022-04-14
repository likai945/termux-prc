import random

def crt_lst(num,n):
    lst=[]
    for i in range(num):
        ball=random.randint(1,n)
        lst.append(ball)
    return lst

def think(lst):
    ballslen=len(lst)
    ballsset=set(lst)
    bslen=len(ballsset)
    if ballslen==bslen:
        lst.sort()
        return lst

def lotto(num,n):
    while True:
        lst=think(crt_lst(num,n))
        if lst:
            return lst


def print_blls(balls,color):
    colors={'red':31,'blue':34}
    for i in balls:
        print(f'\033[{colors[color]}m{i} \033[0m',end='')

def do_it():
    redb=lotto(5,35)
    blb=lotto(2,12)
    print_blls(redb,'red')
    print('+ ',end='')
    print_blls(blb,'blue')
    print('')

if __name__ == '__main__':
    do_it()
