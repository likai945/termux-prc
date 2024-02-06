
def last_one():
    lastone=input('last one:')
    return lastone

def crt_ranges(pos):
  if lastone=='':
    Zr=letters
  else:
    Z=lastone[pos]
    Zi=letters.index(Z)
    Zr=letters[Zi:] if pos < 8 else letters[Zi+1:]
  return Zr
  
def print_names():
  global Ir,Jr,Kr,Lr,Mr,Nr,Or,Pr,Qr
  with open('names','a',encoding='utf_8_sig') as f:
    for i in Ir:
      for j in Jr:
        for k in Kr:
          if k == j and j == i:
            continue
          for l in Lr:
            if l == k and k == j:
              continue
            for m in Mr:
              if m == l and l == k:
                continue
              for n in Nr:
                if n == m and m == l:
                  continue
                for o in Or:
                  if o == n and n == m:
                    continue
                  for p in Pr:
                    if p == o and o == n:
                      continue
                    for q in Qr:
                      if q == p and p == o:
                        continue
    
                      name=i+j+k+l+m+n+o+p+q
                      print(name)

                    Qr=letters
                  Pr=letters
                Or=letters
              Nr=letters
            Mr=letters
          Lr=letters
        Kr=letters


if __name__=='__main__':
  letters=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  lastone=last_one()
  Ir=crt_ranges(0)
  Jr=crt_ranges(1)
  Kr=crt_ranges(2)
  Lr=crt_ranges(3)
  Mr=crt_ranges(4)
  Nr=crt_ranges(5)
  Or=crt_ranges(6)
  Pr=crt_ranges(7)
  Qr=crt_ranges(8)
  print_names()
