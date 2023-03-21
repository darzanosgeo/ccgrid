# Each Provider receives a compensation that equals its VCG payment
from copy import deepcopy

from system_model_functions import K, U
from resource_allocation import resource_allocation


def VCG_revenue_sharing_Double(X, R, R_i, B_i, req, B, price, I, resource_types, L, price_m):
    # revenues = dict()
    coeff = dict()
    revenue_ISP = dict()
    revenue_VSP = dict()
    # for each Infrastructure Provider
    for i in range(1, I + 1):
        R_no_i = dict()
        B_no_i = dict()
        R_i_no_i = dict()
        B_i_no_i = dict()

        # build resources and bids when Provider 'i' does not participate
        # zero resource availability
        for ii in range(1, I+1):
            if ii != i:
                R_no_i.update(deepcopy(R_i[ii]))
                B_no_i.update(deepcopy(B_i[ii]))
                R_i_no_i[ii] = deepcopy(R_i[ii])
                B_i_no_i[ii] = deepcopy(B_i[ii])
            else:
                R_i_no_i[ii] = {key: 0 for key in R_i[ii]}
                R_no_i.update(deepcopy(R_i_no_i[ii]))
                B_i_no_i[ii] = {key: B_i[ii][key] * 10**9 for key in B_i[ii]}
                B_no_i.update(deepcopy(B_i_no_i[ii]))

        for r in R:
            if R[r] < 0:
                capacity_problem = 0
                print("Capacity Problem")

        # estimate the resource allocation if Provider 'i' do not participate in the federation
        X_no_i, tot_prof_no_i, serv_prov_no_i, serv_prov_perc_no_i = resource_allocation(R_no_i, R_i_no_i, req, B_no_i, price, I, resource_types, L, price_m)

        # estimate the compensation of provider 'i'
        if (U(X, req, R, price) - K(X, req, R, B)) - (U(X_no_i, req, R_no_i, price) - K(X_no_i, req, R_no_i, B_no_i)) < 0:
            coeff[i] = K(X, req, R_i[i], B)
        else:
            coeff[i] = K(X, req, R_i[i], B) + (U(X, req, R, price) - K(X, req, R, B)) - (U(X_no_i, req, R_no_i, price) - K(X_no_i, req, R_no_i, B_no_i))

    for i in range(1, I+1):
        revenue_ISP[i] = coeff[i]

    coeff = dict()
    # Estimate the VCG payments of VSPs - remove one request each time
    for cur_req in req:
        test = 0
        temp_req = deepcopy(req)
        temp_price = deepcopy(price)

        temp_req.pop(cur_req)
        temp_price.pop(cur_req)

        # estimate the resource allocation if Provider 'i' do not participate in the federation
        X_no_v, tot_prof_no_v, serv_prov_no_v, serv_prov_perc_no_v = resource_allocation(R, R_i, temp_req, B, temp_price, I, resource_types, L, price_m)

        # estimate the compensation of provider 'i'
        coeff[cur_req] = (U(X_no_v, temp_req, R, temp_price) - K(X_no_v, temp_req, R, B))/2 - (U(X, req, R, price) - K(X, req, R, B))/2 + price[cur_req]

        revenue_VSP[cur_req] = coeff[cur_req]

    return revenue_ISP, revenue_VSP
