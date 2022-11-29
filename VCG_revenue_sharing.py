# Each Provider receives a compensation that equals its VCG payment
from system_model_functions import K, U
from resource_allocation import resource_allocation



def VCG_revenue_sharing(X, tot_prof_a, R, R_i, B_i, req, B, price, I, resource_types, L):
    # revenues = dict()
    coeff = dict()
    revenue = dict()
    revenue_s = dict()
    # for each Infrastructure Provider
    for i in range(1, I + 1):
        R_no_i = dict()
        B_no_i = dict()
        R_i_no_i = dict()
        B_i_no_i = dict()

        # build resources and bids when Provider 'i' do not participate
        # zero resource availability
        for ii in range(1, I+1):
            if ii != i:
                R_no_i.update(R_i[ii])
                B_no_i.update(B_i[ii])
                R_i_no_i[ii] = R_i[ii]
                B_i_no_i[ii] = B_i[ii]
            else:
                R_i_no_i[ii] = {key: 0 for key in R_i[ii]}
                R_no_i.update(R_i_no_i[ii])
                # B_i_no_i[ii] = {key: 10**6 for key in B_i[ii]}
                B_no_i.update(B_i[ii])

        # estimate the resource allocation if Provider 'i' do not participate in the federation
        X_no_i, tot_prof_no_i, serv_prov_no_i, serv_prov_perc_no_i = resource_allocation(R_no_i, R_i_no_i, req, B_no_i, price, I, resource_types, L)

        # estimate the compensation of provider 'i'
        #revenues[i] = K(X, req, R_i[i], B) + (U(X, req, R, price) - K(X, req, R, B)) - (U(X_no_i, req, R_no_i, price) - K(X_no_i, req, R_no_i, B_no_i))
        # coeff[i] = K(X, req, R_i[i], B) + (U(X, req, R, price) - K(X, req, R, B)) - (U(X_no_i, req, R_no_i, price) - K(X_no_i, req, R_no_i, B_no_i))
        coeff[i] = K(X, req, R_i[i], B) + (U(X, req, R, price) - K(X, req, R, B)) - (U(X_no_i, req, R_no_i, price) - K(X_no_i, req, R_no_i, B_no_i))

        if coeff[i] < 0:
            stop = 1

    for i in range(1, I+1):
        #profit[i] = (U(X, req, R, price) - K(X, req, R, B)) * coeff[i]/sum(coeff.values())
        #revenue[i] = K(X, req, R_i[i], B) + (U(X, req, R, price) - K(X, req, R, B)) * (coeff[i] / (sum(coeff.values())+coeff[i]))
        # #revenue[i] = K(X, req, R_i[i], B) + (U(X, req, R, price) - K(X, req, R, B)) * (coeff[i]/(sum(coeff.values())-coeff[i]+max(coeff.values())))
        # second_price = max(coeff.values())
        # for _ in coeff:
        #     if coeff[_] > coeff[i] and coeff[_] < second_price :
        #         second_price = coeff[_]

        #revenue[i] = K(X, req, R_i[i], B) + (U(X, req, R, price) - K(X, req, R, B)) * (coeff[i] / (sum(coeff.values())-coeff[i]+second_price))
        #revenue[i] = K(X, req, R_i[i], B) + (U(X, req, R, price) - K(X, req, R, B)) * (coeff[i] / (sum(coeff.values()) - coeff[i] + second_price))
        #revenue[i] = K(X, req, R_i[i], B) + (U(X, req, R, price) - K(X, req, R, B)) * ((coeff[i]**2) / (sum(coeff.values())**2))
        # revenue[i] = coeff[i] + (U(X, req, R, price) - sum(coeff.values()))*(K(X, req, R_i[i], B)/K(X, req, R, B))
        #revenue[i] = coeff[i] + (U(X, req, R, price) - sum(coeff.values()))/I
        revenue[i] = coeff[i] + U(X, req, R, price) * (tot_prof_a[i]/(.5*sum(tot_prof_a.values())))
        #revenue[i] = coeff[i] + (U(X, req, R, price) - sum(coeff.values())) * (coeff[i] / (sum(coeff.values())))
        revenue_s[i] = coeff[i] + (U(X, req, R, price) - sum(coeff.values())) * (tot_prof_a[i]/sum(tot_prof_a.values()))
    return coeff, revenue, revenue_s
