import random

def randoms(mess):
    n = 0
    sl = ''
    b_ans = []
    ans = ''
    f = 0
    for i in mess:
        print(f, n, i, sl, b_ans, ans)
        if i == '@' and n == 0:
            n = 1
        elif n == 1:
            if i == '[':
                n = 3
            else:
                n = 0
        elif n == 3:
            if i == ']':
                b_ans.append(sl)
                ans += random.choice(b_ans)
                b_ans = []
                n = 0
            elif i != '/':
                sl += i
            else:
                b_ans.append(sl)
                sl = ''
        else:
            ans += i
        f += 1

    return ans
