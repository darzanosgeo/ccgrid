from system_model_functions import K


def FirstPriceAuction(X, tot_prof_a, R, R_i, B_i, req, B, price, I, resource_types, L, price_m):
    profits = dict()
    prices = dict()
    for i in range(1, I + 1):
        profits[i] = K(X, req, R_i[i], B)

    for s in req:
        s_temp = {s:req[s]}
        prices[s] = K(X, s_temp, R, B) + price_m
    return profits, prices