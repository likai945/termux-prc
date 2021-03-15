#!/data/data/com.termux/files/usr/bin/python
f=set()
g=[]                                        
a=list(range(1,35))                         
for j in a:
    f.add(str(j))
for i in range(5):
    b = int(f.pop())
    g.append(b)
g.sort()

fb=set()                                    
gb=[]                                       
ab=list(range(1,12))
for jb in ab:                               
    fb.add(str(jb))
for ib in range(2):
    bb = int(fb.pop())
    gb.append(bb)
gb.sort()                                       

for m in g:
    print('%s '% m, end= '')
print(' + ',end='')
for mb in gb:
    print(' %s '% mb, end='')
print('\n')
