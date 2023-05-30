from create_topology import create_topology
from generate_service_requests import generate_service_requests
from bidding import bidding, place_lower_and_higher_wtp, B_f
from resource_allocation import resource_allocation
from VCG_revenue_sharing_Double import VCG_revenue_sharing_Double
from system_model_functions import U, K
import numpy as np
from copy import deepcopy


if __name__ == '__main__':
    ###############################
    #      Input Parameters     #
    ##############################

    # ######## System Dimensioning Parameters
    InfP = [3]  # number of Inf Service Providers

    Loc = [3]  # number of geographic locations

    Loc_prob = 0.35  # region density --- probability for a Provider to appear in a region

    SS = [5, 10, 20, 30, 50, 70, 100]  # total number of service request

    random_topologies = 10  # number of random topologies

    # ##### Resources Characteristics
    # Resource types based on our example
    # IoT Core, Kinesis Firehose, Kinesis Data Analytics, S3, EMR, QuickSight
    # resource_types = {'IoT', 'Firehose', 'Analytics', 'S3', 'EMR','Quick'}
    resource_types = {'IoT', 'Firehose', 'EMR'}
    ResProf_prob = 0.2  # large profit with probability

    # Resource Capacities are assigned based on a normal distribution
    resource_profile_small = dict()
    resource_profile_large = dict()
    for r_type in resource_types:
        if r_type == 'IoT':
            # number of IoT Devices can be supported by a single providers in a single location
            resource_profile_small[r_type] = 10000
            resource_profile_large[r_type] = 50000
        elif r_type == 'Firehose':
            # maximum number of TBs that can be streamed into Firehose resources
            resource_profile_small[r_type] = 200
            resource_profile_large[r_type] = 1000
        # elif r_type == 'Analytics':
        #     # number of Data Analytics processing units available by each Provider in each region
        #     resource_profile_small[r_type] = 100
        #     resource_profile_large[r_type] = 500
        # elif r_type == 'S3':
        #     # maximum number of TBs can be stored by each Provider in each region
        #     resource_profile_small[r_type] = 500
        #     resource_profile_large[r_type] = 2500
        elif r_type == 'EMR':
            # number of vCPUs maintained by a single providers in a single location
            resource_profile_small[r_type] = 1000
            resource_profile_large[r_type] = 5000
        # elif r_type == 'Quick':
        #     # number of Qyicksight instances can be supported by a single providers in a single location
        #     resource_profile_small[r_type] = 10**6  # THIS IN FACT MEANS NO LIMITATION
        #     resource_profile_large[r_type] = 10**6

    # Cost per unit of resource based on AWS prices
    # We assume that these are the cost values based on which the Providers determine their bids
    cost = dict()

    cost['IoT'] = 0.096/(10**6)  # cost per minutes of connection
    cost['Firehose'] = 0.034  # cost per GB
    #ost['Analytics'] = 0.127  # cost per hour per processing unit
    #cost['S3'] = 0.024  # cost per GB of data stored
    cost['EMR'] = 0.06  # cost per vCPU per hour
    #cost['Quick'] = 34/30  # cost per day

    # Providers follow
    bid_markup = 1  # %100 - double the cost

    # ##### Service Characteristics
    # mean default load of service requests # we consider the AWS connected mobility service presented in the example
    Load_Edge = dict()
    Load_Core = dict()
    # 1. AWS IoT Core --> number of connected devices (all day)
    # 2. AWS Kinesis Firehose --> TBs per day streamed into the component
    # 3. AWS Kinesis Data Analytics --> Processing units always active per day
    # Load_Edge[1] = {'IoT': 1000, 'Firehose': 10, 'Analytics': 10}
    Load_Edge[1] = {'IoT': 1000, 'Firehose': 10}

    # 1. AWS S3 --> TBs/month stored to the core cloud
    # 2. AWS EMR (Serverless)) --> average number of vCPUs/hour utilized per day
    # 3. AWS QuickSight --> Monthly fee for a load of Questions and Sessions
    # Load_Core[1] = {'S3': 50, 'EMR': 100, 'Quick': 1}
    Load_Core[1] = {'EMR': 100}
    # Load_Core[1] = [100, 200, 1]
    # Load_Core[1] = [200, 400, 1]

    # service price base
    price_s_base = 1500  # $/hour
    # price_s_base = 0
    # for load in Load_Edge[1]:
    #     price_s_base += B_f(load, cost, bid_markup).subs('l', Load_Edge[1][load]) * 3.5
    # for load in Load_Core[1]:
    #     price_s_base += B_f(load, cost, bid_markup).subs('l', Load_Core[1][load]) * 1.5

    # probability of addition service region
    prob_region = 0.2

    # blockchain markup price
    price_m = 0 # $/request
    ###############################
    #       Init Process          #
    ##############################

    # for all combinations of number of Providers/ number Regions/number of random topologies per combination of
    # number Providers and number of Regions
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

                    # The decentralized platform determines the resource allocation for the federated scenario
                    X, total_Profit, serv_prov, serv_Prov_perc = resource_allocation(R, R_i, req[S], B, price[S], I, resource_types, L, price_m)

                    # Perform Revenue Sharing
                    payment_ISP, payment_VSP = VCG_revenue_sharing_Double(X, serv_prov, R, R_i, B_i, req[S], B, price[S], I, resource_types, L, price_m)
                    for cur_req in req[S]:
                        if serv_prov[cur_req-1] == 0:
                            payment_VSP[cur_req-1] = 0

                    ########### set lower/higher w-t-p

                    # select a random request
                    i = np.random.randint(1, S+1)

                    price_l, price_h = place_lower_and_higher_wtp(price[S], i)

                    # The decentralized platform determines the resource allocation for the federated scenario
                    X_l, total_Profit_l, serv_pro_l, serv_Prov_perc_l = resource_allocation(R, R_i, req[S], B, price_l, I, resource_types, L, price_m)

                    # Perform Revenue Sharing
                    payment_ISP_l, payment_VSP_l = VCG_revenue_sharing_Double(X_l, serv_pro_l, R, R_i, B_i, req[S], B, price_l, I, resource_types, L, price_m)
                    for cur_req in req[S]:
                        if serv_pro_l[cur_req - 1] == 0:
                            payment_VSP_l[cur_req - 1] = 0

                    # The decentralized platform determines the resource allocation for the federated scenario
                    X_h, total_Profit_h, serv_pro_h, serv_Prov_perc_h = resource_allocation(R, R_i, req[S], B, price_h, I, resource_types, L, price_m)

                    # Perform Revenue Sharing
                    payment_ISP_h, payment_VSP_h = VCG_revenue_sharing_Double(X_h, serv_pro_h, R, R_i, B_i, req[S], B, price_h, I, resource_types, L, price_m)
                    for cur_req in req[S]:
                        if serv_pro_h[cur_req - 1] == 0:
                            payment_VSP_h[cur_req - 1] = 0

                    profit_ISP = dict()
                    profit_ISP_h = dict()
                    profit_ISP_l = dict()
                    profit_VSP = dict()
                    profit_VSP_l = dict()
                    profit_VSP_h = dict()

                    for ii in range(1, I+1):
                        profit_ISP[ii] = payment_ISP[ii] - K(X, req[S], R_i[ii], B)
                        profit_ISP_h[ii] = payment_ISP_h[ii] - K(X, req[S], R_i[ii], B)
                        profit_ISP_l[ii] = payment_ISP_l[ii] - K(X, req[S], R_i[ii], B)

                    for cur_req in req[S]:
                        if payment_VSP[cur_req] != 0:
                            profit_VSP[cur_req] = price[S][cur_req] - payment_VSP[cur_req]
                        else:
                            profit_VSP[cur_req] = 0

                        if payment_VSP_l[cur_req] != 0:
                            profit_VSP_l[cur_req] = price[S][cur_req] - payment_VSP_l[cur_req]
                        else:
                            profit_VSP_l[cur_req] = 0

                        if payment_VSP_h[cur_req] != 0:
                            profit_VSP_h[cur_req] = price[S][cur_req] - payment_VSP_h[cur_req]
                        else:
                            profit_VSP_h[cur_req] = 0

                    print("normal", profit_ISP)
                    print("high", profit_ISP_h)
                    print("low", profit_ISP_l)

                    print("")
                    print(i)
                    print("normal", profit_VSP)
                    print("high", profit_VSP_h)
                    print("low", profit_VSP_l)
                    print("")
                    print("normal", sum(payment_VSP.values()) - sum(payment_ISP.values()))
                    print("high", sum(payment_VSP_h.values()) - sum(payment_ISP_h.values()))
                    print("low", sum(payment_VSP_l.values()) - sum(payment_ISP_l.values()))


                    test = 0



