def MTHG(R, R_i, S, B, price, I, resource_types, L, price_m):
    # service component cost --> b_r(lambda_sigma)
    # service component value --> val = p_sigma = p_s/len(s)  OR val = p_sigma - b_r(lambda_sigma)
    # desirability --> des = p_sigma/b_r(lambda_sigma) OR des = (p_sigma - b_r(lambda_sigma))/lambda_sigma
    X = dict()
    for r in R:
        for s in S:
            for sigma in s:
                X[r, s, sigma] = 0

    # Service and service component provisioning flags
    s_prov = dict()
    sigma_prov = dict()
    for s in S:
        s_prov = 0
        for sigma in s:
            sigma_prov[s, sigma] = 0


    return X