import random
import csv


ab=['A','B','C','D','E']
score=0


def read_quiz(file):
    quizs=[]
    with open(file,encoding='utf_8_sig') as f:
        fl=csv.reader(f)
        for quiz in fl:
            qlst=[]
            for i in quiz:
                qlst.append(i)
            quizs.append(qlst)
    return quizs


def show_quiz(i,n,c): 
    print(f'\033[{c}m{n} {i[0]}\033[0m')
    k=0
    for j in i[2:]: 
        print(f'{ab[k]}•{j}')
        k+=1


def test_one(file,point,number,color):
    quizs=read_quiz(file)
    random.shuffle(quizs)
    chosenQ=quizs[:number]
    for i in chosenQ:
        num=chosenQ.index(i)+1
        show_quiz(i,num,color)
        ans=input('Answer:')
        if ans==i[1]:
            global score
            score+=point
        else:
            print(f'\033[31mRight:{i[1]}\033[0m')


def test_all():
    test_one('danxuan',2,20,42)
    test_one('duoxuan',3,15,43)
    test_one('panduan',1.5,10,44)


def main():
    test_all()
    print(f'score:\033[32m{score}\033[0m')


if __name__ == '__main__':
    main()
