from system_model_functions import K


def FirstPriceAuctionAdapted(X, tot_prof_a, R, R_i, B_i, req, B, price, I, resource_types, L, price_m):
    profits = dict()
    prices = dict()
    extra = dict()
    for i in range(1, I + 1):
        profits[i] = 0

    for s in req:
        s_temp = {s:req[s]}
        extra[s] = price[s] - K(X, s_temp, R, B) - price_m
        prices[s] = K(X, s_temp, R, B) + price_m + (len(s_temp[s]) * extra[s])/(len(s_temp[s])+1)

        for i in range(1, I + 1):
            for sigma in s_temp[s]:
                for r in R_i[i]:
                    profits[i] += X[r, s, sigma] * (B[r].subs('l', s_temp[s][sigma]['load'])+extra[s]/(len(s_temp[s])+1))
    # for s in req:
    #     s_temp = {s: req[s]}
    #     extra[s] = price[s] - K(X, s_temp, R, B) - price_m
    #     prices[s] = K(X, s_temp, R, B) + price_m + (I * extra[s]) / (I + 1)
    #
    #     for i in range(1, I + 1):
    #         for sigma in s_temp[s]:
    #             for r in R_i[i]:
    #                 profits[i] += X[r, s, sigma] * B[r].subs('l', s_temp[s][sigma]['load'])
    #
    #         profits[i] += extra[s] / (I + 1)


    return profits, prices