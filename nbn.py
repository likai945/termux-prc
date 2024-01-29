letters=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

for i in letters:
    ccc=0
    for j in letters:
        if j == i:
            ccc += 1
        else:
            ccc = 0
        if ccc == 2:
            continue
        for k in letters:
            if k == j:
                ccc += 1
            else:
                ccc = 0
            if ccc == 2:
                continue
            for l in letters:
                if l == k:
                    ccc += 1
                else:
                    ccc = 0
                if ccc == 2:
                    continue
                for m in letters:
                    if m == l:
                        ccc += 1
                    else:
                        ccc = 0
                    if ccc == 2:
                        continue
                    for n in letters:
                        if n == m:
                            ccc += 1
                        else:
                            ccc = 0
                        if ccc == 2:
                            continue
                        for o in letters:
                            if o == n:
                                ccc += 1
                            else:
                                ccc = 0
                            if ccc == 2:
                                continue
                            for p in letters:
                                if p == o:
                                    ccc += 1
                                else:
                                    ccc = 0
                                if ccc == 2:
                                    continue
                                for q in letters:
                                    if q == p:
                                        ccc += 1
                                    else:
                                        ccc = 0
                                    if ccc == 2:
                                        continue

                                    name=i+j+k+l+m+n+o+p+q
                                    print(name)
