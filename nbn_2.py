letters=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

for i in letters:
    for j in letters:
        for k in letters:
            if k == j and j == i:
                continue
            for l in letters:
                if l == k and k == j:
                    continue
                for m in letters:
                    if m == l and l == k:
                        continue
                    for n in letters:
                        if n == m and m == l:
                            continue
                        for o in letters:
                            if o == n and n == m:
                                continue
                            for p in letters:
                                if p == o and o == n:
                                    continue
                                for q in letters:
                                    if q == p and p == o:
                                        continue

                                    name=i+j+k+l+m+n+o+p+q
                                    print(name)
