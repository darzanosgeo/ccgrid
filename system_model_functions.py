# Total revenues
def U(X, S, R, price):
    sum_U = 0
    for r in R:
        for s in S:
            for sigma in S[s]:
                sum_U += price[s] * X[r, s, sigma] / (len(S[s]))
    return sum_U


# Total Cost
def K(X, S, R, B):
    sum_K = 0
    for r in R:
        for s in S:
            for sigma in S[s]:
                sum_K += X[r, s, sigma] * B[r].subs('l', S[s][sigma]['load'])
    return sum_K


# indicator functions
def z(r, t, l):
    if l != 0:
        if r[1] == l and r[2] == t:
            return 1
        else:
            return 0
    else:
        if r[2] == t:
            return 1
        else:
            return 0

