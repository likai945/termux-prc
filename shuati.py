import random
import csv

ab=['A','B','C','D','E']
score=0
wrongS=[]
wrongM=[]
wrongJ=[]


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
        print(f'\033[{c-10}m{ab[k]}•\033[0m{j}')
        k+=1


def test_one(file,point,number,color,wronglst):
    quizs=read_quiz(file)
    random.shuffle(quizs)
    chosenQ=quizs[:number]
    for i in chosenQ:
        num=chosenQ.index(i)+1
        show_quiz(i,num,color)
        ans=input('Answer:').upper()
        if ans==i[1]:
            global score
            score+=point
        else:
            wronglst.append([ans,i])


def test_all():
    test_one('danxuan',2,20,42,wrongS)
    test_one('duoxuan',3,15,43,wrongM)
    test_one('panduan',1.5,10,44,wrongJ)


def show_wrong(wrong,color):
    for i in wrong:
        show_quiz(i[1],'|',color)
        print(f'\033[{color}mRight:{i[1][1]}\033[0m')
        print(f'Yours:{i[0]}')


def show_all_wrong():
    show_wrong(wrongS,32)
    show_wrong(wrongM,33)
    show_wrong(wrongJ,34)


def main():
    test_all()
    print(f'score:\033[32m{score}\033[0m')
    review=input('\nReview all the wrong choices?')
    if review != 'no':
        show_all_wrong()


if __name__ == '__main__':
    main()
