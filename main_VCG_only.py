from FirstPriceAuction import FirstPriceAuction
from FirstPriceAuctionAdapted import FirstPriceAuctionAdapted
from MTHG import MTHG
from create_topology import create_topology
from generate_service_requests import generate_service_requests
from bidding import bidding, place_higher_bid, place_lower_bid
from resource_allocation import resource_allocation
from VCG_revenue_sharing import VCG_revenue_sharing
from resource_allocationSA import resource_allocationSA
from system_model_functions import U, K
import numpy as np
from copy import deepcopy


if __name__ == '__main__':
    ###############################
    #      Input Parameters     #
    ##############################

    # ######## System Dimensioning Parameters
    InfP = [5]  # number of Inf Service Providers

    Loc = [5]  # number of geographic locations

    Loc_prob = 0.35  # region density --- probability for a Provider to appear in a region

    SS = [5, 10, 20, 30, 50, 70, 100]  # total number of service request

    random_topologies = 10  # number of random topologies

    # ##### Resources Characteristics
    # Resource types based on our example
    # IoT Core, Kinesis Firehose, Kinesis Data Analytics, S3, EMR, QuickSight

    resource_types = {'IoT', 'Firehose', 'EMR'}
    ResProf_prob = 0.35  # large profit with probability

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
        elif r_type == 'EMR':
            # number of vCPUs maintained by a single providers in a single location
            resource_profile_small[r_type] = 1000
            resource_profile_large[r_type] = 5000

    # Cost per unit of resource based on AWS prices
    # We assume that these are the cost values based on which the Providers determine their bids
    cost = dict()

    cost['IoT'] = 0.096 / (10 ** 6)  # cost per minutes of connection
    cost['Firehose'] = 0.034  # cost per GB
    cost['EMR'] = 0.06  # cost per vCPU per hour

    # Providers follow
    bid_markup = 1  # %100 - double the cost

    # ##### Service Characteristics
    # mean default load of service requests # we consider the AWS connected mobility service presented in the example
    Load_Edge = dict()
    Load_Core = dict()
    # 1. AWS IoT Core --> number of connected devices (all day)
    # 2. AWS Kinesis Firehose --> TBs per day streamed into the component
    # 3. AWS Kinesis Data Analytics --> Processing units always active per day
    Load_Edge[1] = {'IoT': 1000, 'Firehose': 10}

    # 1. AWS S3 --> TBs/month stored to the core cloud
    # 2. AWS EMR (Serverless)) --> average number of vCPUs/hour utilized per day
    # 3. AWS QuickSight --> Monthly fee for a load of Questions and Sessions
    # Load_Core[1] = {'S3': 50, 'EMR': 100, 'Quick': 1}
    Load_Core[1] = {'EMR': 100}

    # service price base
    price_s_base = 1500  # $/hour

    # probability of addition service region
    prob_region = 0.2

    # blockchain markup price
    price_m = 0  # $/request
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
                req_tot, req_tot_price = generate_service_requests(tot_S, L, Load_Core[1], Load_Edge[1], price_s_base, prob_region)

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

                    # Each service can be only served by one and only InfSP or none
                    X_a, total_Profit_a, serv_prov_a, serv_Prov_perc_a = resource_allocationSA(R, R_i, req[S], B, price[S], I, resource_types, L, 0)

                    ##############
                    # The decentralized platform determines the resource allocation for the federated scenario
                    X, total_Profit, serv_prov, serv_Prov_perc = resource_allocation(R, R_i, req[S], B, price[S], I, resource_types, L, price_m)

                    # Perform Revenue Sharing
                    payments = VCG_revenue_sharing(X, R, R_i, B_i, req[S], B, price[S], I, resource_types, L, price_m)

                    # select one provider that places a higher and lower bid - select the provider with the highest profits
                    i = np.random.randint(1, I+1)

                    # set higher price
                    B_h, B_i_h = place_higher_bid(B, B_i, i, R_i)
                    X_h, total_Profit_h, serv_prov_h, serv_Prov_perc_h = resource_allocation(R, R_i, req[S], B_h, price[S], I,
                                                                                     resource_types, L, price_m)

                    payments_h = VCG_revenue_sharing(X_h, R, R_i, B_i_h, req[S], B_h, price[S], I, resource_types, L, price_m)

                    # set lower price
                    B_l, B_i_l = place_lower_bid(B, B_i, i, R_i)
                    X_l, total_Profit_l, serv_prov_l, serv_Prov_perc_l = resource_allocation(R, R_i, req[S], B_l,
                                                                                             price[S], I,
                                                                                             resource_types, L, price_m)

                    payments_l = VCG_revenue_sharing(X_l, R, R_i, B_i_l, req[S], B_l,
                                                                     price[S], I, resource_types, L, price_m)


                    profit = dict()
                    profit_h = dict()
                    profit_l = dict()
                    profit_aa = dict()
                    final_payments = dict()

                    for ii in range(1, I+1):
                        profit[ii] = payments[ii] - K(X, req[S], R_i[ii], B)
                        profit_h[ii] = payments_h[ii] - K(X_h, req[S], R_i[ii], B)
                        profit_l[ii] = payments_l[ii] - K(X_l, req[S], R_i[ii], B)
                        profit_aa[ii] = U(X_a, req[S], R_i[ii], price[S]) - K(X_a, req[S], R_i[ii], B)

                    surplus = U(X, req[S], R, price[S]) - sum(payments.values())
                    initial_surplus = surplus
                    # surplus_h = sum(revenues_h.values()) - sum(profit.values())
                    # surplus_l = sum(revenues_l.values()) - sum(profit.values())

                    new_profit = dict()
                    new_profit_l = dict()
                    new_profit_h = dict()

                    for ii in range(1, I + 1):
                        #new_profit[ii] = profit[ii] + surplus / I
                        if surplus <= 0:
                            new_profit[ii] = profit[ii]
                            final_payments[ii] = payments[ii]
                        elif profit[ii] < profit_aa[ii] and surplus >= profit_aa[ii] - profit[ii]:
                            new_profit[ii] = profit_aa[ii]
                            surplus = surplus - (profit_aa[ii] - profit[ii])
                            final_payments[ii] = payments[ii] + (profit_aa[ii] - profit[ii])
                        elif profit[ii] < profit_aa[ii] and surplus < profit_aa[ii] - profit[ii]:
                            new_profit[ii] = profit[ii] + surplus
                            final_payments[ii] = payments[ii] + surplus
                            surplus = 0
                        else:
                            new_profit[ii] = profit[ii]
                            final_payments[ii] = payments[ii]

                    if surplus > 0:
                        for ii in range(1, I + 1):
                            final_payments[ii] = final_payments[ii] + surplus/I
                            new_profit[ii] = new_profit[ii] + surplus/I
                            #new_profit[ii] = new_profit[ii] + (profit[ii]/sum(profit.values())) * surplus
                        # new_profit_l[ii] = profit_l[ii] + (profit_aa[ii] / sum(profit_aa.values())) * surplus_l
                        # new_profit_h[ii] = profit_h[ii] + (profit_aa[ii] / sum(profit_aa.values())) * surplus_h
                        #new_profit_l[ii] = profit_l[ii] + surplus_l / I
                        #new_profit_h[ii] = profit_h[ii] + surplus_h / I

                    print(i)
                    print("Profit", profit)
                    print("Profit_h", profit_h)
                    print("Profit_l", profit_l)
                    print("Total Profits", sum(profit.values()))
                    print("Total Profits h", sum(profit_h.values()))
                    print("Total Profits l", sum(profit_l.values()))
                    print("Total VSP payments", sum(price[S].values()))
                    print("Total VCG payments", sum(payments.values()))
                    print("Surplus", initial_surplus)

                    print("")
                    print("Final payments", final_payments)
                    print("New Profits", new_profit)
                    # print(new_profit_h)
                    # print(new_profit_l)
                    print("New Total Profits", sum(new_profit.values()))
                    # print(sum(new_profit_h.values()))
                    # print(sum(new_profit_l.values()))

                    print("Standalone Profits", profit_aa)
                    print("Standalone Total Profits", sum(profit_aa.values()))

                    file = open("results_NEW_VCG.txt", "a")
                    file.write("\n" + "--- New experiment --" + "\n")
                    file.write("Providers = " + repr(I) + "\n")
                    file.write("Topology = " + repr(top) + "\n")
                    file.write("Locations = " + repr(L) + "\n")
                    file.write("Requests = " + repr(S) + "\n")
                    file.write("Utilization = " + repr(serv_Prov_perc) + "\n")
                    file.write("VCG_payments = " + repr(list(payments.values())) + "\n")
                    file.write("VCG_payments_total = " + repr(sum(payments.values())) + "\n")
                    file.write("VSP_payments = " + repr(list(price[S].values())) + "\n")
                    file.write("VSP_payments_total = " + repr(sum(price[S].values())) + "\n")
                    file.write("Surplus= " + repr(initial_surplus) + "\n")
                    file.write("InfSP_costs = " + repr(list(np.subtract(list(payments.values()),list(profit.values())))) + "\n")
                    file.write("InfSP_total_cost = " + repr(sum(payments.values()) - sum(profit.values())) + "\n")
                    file.write("Total_Profit = " + repr(sum(profit.values())) + "\n")
                    file.write("Strategic_Provider = " + repr(i) + "\n")
                    file.write("Individual_Profit_VCG = " + repr(list(profit.values())) + "\n")
                    file.write("Individual_Profit_VCG_l = " + repr(list(profit_l.values())) + "\n")
                    file.write("Individual_Profit_VCG_h = " + repr(list(profit_h.values())) + "\n")
                    file.write("Final_InfSP_payments = " + repr(list(final_payments.values())) + "\n")
                    file.write("Individual_Profits_after_surplus_distribution = " + repr(list(new_profit.values())) + "\n")
                    file.write("Individual_Profits_StandAlone= " + repr(list(profit_aa.values())) + "\n")

                    file.write("\n")
                    file.close()

                    test = 0



