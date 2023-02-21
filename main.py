from FirstPriceAuction import FirstPriceAuction
from FirstPriceAuctionAdapted import FirstPriceAuctionAdapted
from MTHG import MTHG
from create_topology import create_topology
from generate_service_requests import generate_service_requests
from bidding import bidding, place_higher_bid, place_lower_bid
from resource_allocation import resource_allocation
from VCG_revenue_sharing import VCG_revenue_sharing
from system_model_functions import U, K
import numpy as np
from copy import deepcopy


if __name__ == '__main__':
    ###############################
    #      Input Parameters     #
    ##############################

    # ######## System Dimensioning Parameters
    InfP = [3]  # number of Inf Service Providers

    Loc = [2]  # number of geographic locations

    Loc_prob = 0.5 # region density --- probability for a Provider to appear in a region

    SS = [1, 2, 5, 10, 20, 50, 100, 150, 200, 250, 300]  # total number of service request
    #SS = [10, 20, 50, 100, 150, 200, 250, 300]  # total number of service request
    random_topologies = 10  # number of random topologies

    # ##### Resources Characteristics
    # Resource types based on our example
    # IoT Core, Kinesis Firehose, Kinesis Data Analytics, S3, EMR, QuickSight
    resource_types = {'IoT', 'Firehose', 'Analytics', 'S3', 'EMR','Quick'}
    ResProf_prob = 0.35 # large profit with probability

    # Resource Capacities are assigned based on a normal distribution
    resource_profile_small = dict()
    resource_profile_large = dict()
    for r_type in resource_types:
        if r_type == 'IoT':
            # number of IoT Devices can be supported by a single providers in a single location
            resource_profile_small[r_type] = 10000
            resource_profile_large[r_type] = 50000
            # resource_profile_small[r_type] = 3000
            # resource_profile_large[r_type] = 15000
        elif r_type == 'Firehose':
            # maximum number of TBs that can be streamed into Firehose resources
            resource_profile_small[r_type] = 200
            resource_profile_large[r_type] = 1000
            # resource_profile_small[r_type] = 60
            # resource_profile_large[r_type] = 300
        elif r_type == 'Analytics':
            # number of Data Analytics processing units available by each Provider in each region
            resource_profile_small[r_type] = 100
            resource_profile_large[r_type] = 500
            # resource_profile_small[r_type] = 30
            # resource_profile_large[r_type] = 150
        elif r_type == 'S3':
            # maximum number of TBs can be stored by each Provider in each region
            resource_profile_small[r_type] = 500
            resource_profile_large[r_type] = 2500
            # resource_profile_small[r_type] = 150
            # resource_profile_large[r_type] = 750
        elif r_type == 'EMR':
            # number of vCPUs maintained by a single providers in a single location
            resource_profile_small[r_type] = 1000
            resource_profile_large[r_type] = 5000
            # resource_profile_small[r_type] = 150
            # resource_profile_large[r_type] = 750
        elif r_type == 'Quick':
            # number of Qyicksight instances can be supported by a single providers in a single location
            resource_profile_small[r_type] = 10**6  # THIS IN FACT MEANS NO LIMITATION
            resource_profile_large[r_type] = 10**6

    # Cost per unit of resource based on AWS prices
    # We assume that these are the cost values based on which the Providers determine their bids
    cost = dict()

    cost['IoT'] = 0.096/(10**6)  # cost per minutes of connection
    cost['Firehose'] = 0.034  # cost per GB
    cost['Analytics'] = 0.127  # cost per hour per processing unit
    cost['S3'] = 0.024  # cost per GB of data stored
    cost['EMR'] = 0.06  # cost per vCPU per hour
    cost['Quick'] = 34/30  # cost per day

    # Providers follow
    bid_markup = 1  # %100 - double the cost

    # ##### Service Characteristics
    # mean default load of service requests # we consider the AWS connected mobility service presented in the example
    Load_Edge = dict()
    Load_Core = dict()
    # 1. AWS IoT Core --> number of connected devices (all day)
    # 2. AWS Kinesis Firehose --> TBs per day streamed into the component
    # 3. AWS Kinesis Data Analytics --> Processing units always active per day
    Load_Edge[1] = {'IoT': 1000, 'Firehose': 10, 'Analytics': 10}

    # 1. AWS S3 --> TBs/month stored to the core cloud
    # 2. AWS EMR (Serverless)) --> average number of vCPUs/hour utilized per day
    # 3. AWS QuickSight --> Monthly fee for a load of Questions and Sessions
    Load_Core[1] = {'S3': 50, 'EMR': 100, 'Quick': 1}
    # Load_Core[1] = [100, 200, 1]
    # Load_Core[1] = [200, 400, 1]

    # service price base
    price_s_base = 1500  # $/hour

    # probability of addition service region
    prob_region = 0.2

    # blockchain markup price
    price_m = 0 # $/request
    ###############################
    #       Init Process          #
    ##############################

    # for all combinations of number of Providers/ number Regions/number of random topologies per combination of number Providers and number of Regions
    for I in InfP:
        for L in Loc:
            for top in range(1,random_topologies):
                # create topology
                R, R_i, max_Caps = create_topology(I, L, Loc_prob, ResProf_prob, resource_profile_small, resource_profile_large, resource_types)

                # Providers place bids for their resources
                B, B_i = bidding(I, R, cost, bid_markup, max_Caps)

                # Generate Requests for different total loads
                tot_S = SS[-1]
                # create requests
                req_tot, req_tot_price = generate_service_requests(tot_S, L, Load_Core[1], Load_Edge[1], price_s_base,
                                                             prob_region)
                # for different total loads -- number of total requests
                for S in SS:
                    req = dict()
                    price = dict()

                    req[S] = deepcopy(req_tot)
                    price[S] = deepcopy(req_tot_price)

                    # Pick only the first S requests for this simulation
                    for s in range(1, SS[-1]+1):
                        if s > S:
                            req[S].pop(s)
                            price[S].pop(s)

                    ################
                    # Resource allocation if each Cloud Provider Operated alone
                    X_a = {}
                    total_Profit_a = {}
                    serv_prov_a = {}
                    serv_Prov_perc_a = {}
                    for i in range(1, I+1):
                        #set to zero capacity the resources of all other providers
                        R_a = {key: 0 for key in R}
                        for _ in R_i[i]:
                            R_a[_] = R_i[i][_]

                        X_a[i], total_Profit_a[i], serv_prov_a[i], serv_Prov_perc_a[i] = resource_allocation(R_a, R_i, req[S], B, price[S], I,
                                                                                     resource_types, L, 0)

                    Rtemp = {}
                    for _ in R:
                        Rtemp[_] = R[_]
                    if Rtemp is R:
                        stop = 0
                    ##############
                    # The decentralized platform determines the resource allocation for the federated scenario
                    X, total_Profit, serv_prov, serv_Prov_perc = resource_allocation(R, R_i, req[S], B, price[S], I, resource_types, L, price_m)

                    X_hr, total_profit_hr, serv_prov_hr, serv_Prov_perc_hr = MTHG(deepcopy(R), deepcopy(R_i), req[S], B, price[S], I, resource_types, L, price_m)

                    # Perform Revenue Sharing
                    FPA_revenues, FPA_prices = FirstPriceAuction(X, total_Profit_a, R, R_i, B_i, req[S], B, price[S], I, resource_types, L, price_m)
                    coeff, revenues, revenues_s = VCG_revenue_sharing(X,total_Profit_a, R, R_i, B_i, req[S], B, price[S], I, resource_types, L,price_m)

                    # select one provider that places a higher and lower bid - select the provider with the highest profits
                    i = np.random.randint(1, I+1)

                    # set higher price
                    B_h, B_i_h = place_higher_bid(B, B_i, i, R_i)
                    X_h, total_Profit_h, serv_prov_h, serv_Prov_perc_h = resource_allocation(R, R_i, req[S], B_h, price[S], I,
                                                                                     resource_types, L, price_m)
                    FPA_revenues_h, FPA_prices_h = FirstPriceAuction(X_h, total_Profit_a, R, R_i, B_i_h, req[S], B_h, price[S], I,
                                                                 resource_types, L, price_m)
                    coeff_h, revenues_h,  revenues_s_h = VCG_revenue_sharing(X_h, total_Profit_a, R, R_i, B_i_h, req[S], B_h, price[S], I,
                                                                 resource_types, L, price_m)

                    # set lower price
                    B_l, B_i_l = place_lower_bid(B, B_i, i, R_i)
                    X_l, total_Profit_l, serv_prov_l, serv_Prov_perc_l = resource_allocation(R, R_i, req[S], B_l,
                                                                                             price[S], I,
                                                                                             resource_types, L, price_m)
                    FPA_revenues_l, FPA_prices_l = FirstPriceAuction(X_l, total_Profit_a, R, R_i, B_i_l, req[S], B_l,
                                                                     price[S], I,
                                                                     resource_types, L, price_m)
                    coeff_l, revenues_l, revenues_s_l = VCG_revenue_sharing(X_l, total_Profit_a, R, R_i, B_i_l, req[S], B_l,
                                                                     price[S], I,
                                                                     resource_types, L, price_m)

                    if coeff[i] - K(X, req[S], R_i[i], B) < coeff_l[i] - K(X_l, req[S], R_i[i], B):
                        stop = 1

                    profit = dict()
                    profit_h = dict()
                    profit_l = dict()
                    profit_s = dict()
                    profit_s_h = dict()
                    profit_s_l = dict()
                    FPA_profit = dict()
                    FPA_profit_h = dict()
                    FPA_profit_l = dict()
                    for ii in range(1, I+1):
                        profit[ii] = revenues[ii] - K(X, req[S], R_i[ii], B)
                        profit_h[ii] = revenues_h[ii] - K(X_h, req[S], R_i[ii], B)
                        profit_l[ii] = revenues_l[ii] - K(X_l, req[S], R_i[ii], B)
                        profit_s[ii] = revenues_s[ii] - K(X, req[S], R_i[ii], B)
                        profit_s_h[ii] = revenues_s_h[ii] - K(X_h, req[S], R_i[ii], B)
                        profit_s_l[ii] = revenues_s_l[ii] - K(X_l, req[S], R_i[ii], B)
                        FPA_profit[ii] = FPA_revenues[ii] - K(X, req[S], R_i[ii], B)
                        FPA_profit_h[ii] = FPA_revenues_h[ii] - K(X_h, req[S], R_i[ii], B)
                        FPA_profit_l[ii] = FPA_revenues_l[ii] - K(X_l, req[S], R_i[ii], B)
                        # profit[ii] = coeff[ii] - K(X, req[S], R_i[ii], B)
                        # profit_h[ii] = coeff_h[ii] - K(X_h, req[S], R_i[ii], B)
                        # profit_l[ii] = coeff_l[ii] - K(X_l, req[S], R_i[ii], B)

                    print(i)
                    print(FPA_profit)
                    print(FPA_profit_h)
                    print(FPA_profit_l)
                    print(sum(FPA_profit.values()))
                    print(sum(FPA_profit_h.values()))
                    print(sum(FPA_profit_l.values()))

                    print(profit_s)
                    print(profit_s_h)
                    print(profit_s_l)
                    print(sum(profit_s.values()))
                    print(sum(profit_s_h.values()))
                    print(sum(profit_s_l.values()))
                    #print(K(X, req[S], R, B))
                    print(total_Profit)
                    print(total_profit_hr)
                    print((U(X_hr, req[S], R, price[S]) - K(X_hr, req[S], R, B)))

                    print(profit)
                    print(profit_h)
                    print(profit_l)
                    print(sum(profit.values()))
                    print(sum(profit_h.values()))
                    print(sum(profit_l.values()))
                    print(total_Profit)



                    print(total_Profit_a)

                    if profit_s[i] < profit_s_l[i] or profit_s[i] < profit_s_h[i]:
                        test = 0
                    if profit[i] < profit_l[i] or profit[i] < profit_h[i]:
                        test = 0

                    test = 0


