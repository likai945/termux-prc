import random
import csv
import time

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
        j=j.replace('•','🎯')
        print(f'\033[{c-10}m{chr(65+k)}•\033[0m{j}')
        k+=1


def mark_ans(oldAns,ops):
    for i in oldAns:
        ops[ord(i)-65]=f'•{ops[ord(i)-65]}'
    return ops


def new_ans(markedOps):
    ans=''
    for i in markedOps:
        if '•' in i:
            ans+=chr(markedOps.index(i)+65)
    return ans


def sort_ans(ans):
    lsAns=[]
    sortedAns=''
    for i in ans:
        lsAns.append(i)
    lsAns.sort()
    for j in lsAns:
        sortedAns+=j
    return sortedAns


def test_one(file,point,number,color,wronglst,cls):
    quizs=read_quiz(file)
    random.shuffle(quizs)
    chosenQ=quizs
    for i in chosenQ:
        num=chosenQ.index(i)+1
        num=f'{cls}{str(num)}'
        if cls !='J':
            ops=i[2:]
            ops=mark_ans(i[1],ops)
            random.shuffle(ops)
            i[2:]=ops
            rightAns=new_ans(ops)
            i[1]=rightAns

        show_quiz(i,num,color)
        ans=input('Answer:').upper().replace(' ','')
        ans=sort_ans(ans)
        if ans==i[1]:
            global score
            score+=point
        else:
            wronglst.append([ans,i])
            print(f'\033[31mRight:{i[1]}\033[0m')


def test_all():
    test_one('danxuan',2,20,42,wrongS,'S')
    test_one('duoxuan',2,20,45,wrongM,'M')
    test_one('panduan',1,20,46,wrongJ,'J')


def show_wrong(wrong,color,cls):
    for i in wrong:
        show_quiz(i[1],f'[{cls}]',color)
        print(f'\033[{color}mRight:{i[1][1]}\033[0m')
        print(f'Yours:{i[0]}')


def show_all_wrong():
    if wrongS or wrongM or wrongJ:
        review=input('\nReview all the wrong choices?')
        if review != 'no':
            show_wrong(wrongS,32,'S')
            show_wrong(wrongM,33,'M')
            show_wrong(wrongJ,34,'J')


def score_time(starttime):
    endtime=time.time()
    costtime=round(endtime-starttime)
    fmtmin=costtime//60
    fmtsec=costtime%60
    print(f'\nscore:\033[32m{score}\033[0m')
    print(f'cost:\033[32m{fmtmin}m {fmtsec}s\033[0m')


def main():
    starttime=time.time()
    test_all()
    score_time(starttime)
    show_all_wrong()


if __name__ == '__main__':
    main()
