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

    Iterations = 10 # number of provisioning windows that will run

    SS = [10, 20, 30, 50, 70, 40, 50, 30, 10, 20]  # total number of service request

    random_topologies = 20  # number of random topologies that will run for multiple iterations

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

                topology = []
                for _ in R:
                    if R[_]!=0:
                        if (_[0],_[1]) not in topology:
                            topology.append((_[0],_[1]))

                # Providers place bids for their resources
                B, B_i = bidding(I, R, cost, bid_markup, max_Caps)

                # Generate Requests for different iterations

                req = []
                price = []

                for it in range(Iterations):
                    # create requests
                    temp_req, temp_price = generate_service_requests(SS[it], L, Load_Core[1], Load_Edge[1], price_s_base, prob_region)
                    req.append(temp_req)
                    price.append(temp_price)

                surplus = 0
                threshold = 3500 * 15

                # for different iterations - provisioning periods
                for it in range(Iterations):


                    # Standalone profit - Each service can be only served by one and only InfSP or none
                    X_a, total_Profit_a, serv_prov_a, serv_Prov_perc_a = resource_allocationSA(R, R_i, req[it], B,
                                                                                               price[it], I,
                                                                                               resource_types, L, 0)
                    P_a = dict()
                    for ii in range(1,I+1):
                        # Standalone profit of providers
                        P_a[ii] = U(X_a, req[it], R_i[ii], price[it]) - K(X_a, req[it], R_i[ii], B)
                        # P_a[ii] = U(X_a, req[it], R_i[ii], price[it]) - K(X_a, req[it], R_i[ii], B) - (sum(serv_prov_a)*price_m)

                    ##############
                    # The decentralized platform determines the resource allocation for the federated scenario
                    X, total_Profit, serv_prov, serv_Prov_perc = resource_allocation(R, R_i, req[it], B, price[it], I, resource_types, L, price_m)

                    # Perform Revenue Sharing
                    payments = VCG_revenue_sharing(X, R, R_i, B_i, req[it], B, price[it], I, resource_types, L, price_m)


                    VCG_profit = dict()
                    KK = dict()
                    for ii in range(1, I+1):
                        KK[ii] = K(X, req[it], R_i[ii], B)
                        VCG_profit[ii] = payments[ii]-KK[ii]
                        #VCG_profit[ii] = payments[ii] - (sum(serv_prov)*price_m)

                    # calculate total deficit that the surplus pool should cover
                    # AND the current total surplus or deficit created in this iteration
                    tot_deficit = 0
                    cur_surplus = 0
                    for ii in range(1, I + 1):
                        cur_surplus = U(X, req[it], R, price[it]) - sum(payments.values()) - (sum(serv_prov)*price_m)
                        if VCG_profit[ii] < P_a[ii]:
                            tot_deficit += P_a[ii] - VCG_profit[ii]


                    final_payments = dict()
                    final_prices = dict()

                    surplus += cur_surplus
                    # if total deficit can be covered by the pool
                    if tot_deficit < surplus:
                        # Individual rationality - Guaranteed profit
                        for ii in range(1, I + 1):
                            # if less profit with VCG payments
                            if VCG_profit[ii] < P_a[ii]:
                                final_payments[ii] = payments[ii] + P_a[ii] - VCG_profit[ii]
                                surplus = surplus - (P_a[ii] - VCG_profit[ii]) - (sum(serv_prov)*price_m)
                            else:
                                final_payments[ii] = payments[ii]

                        # if surplus is more than the threshold, then share the rest to InfSPs evenly
                        if surplus > threshold:
                            for ii in range(1,I+1):
                                final_payments[ii] += (surplus-threshold)/I
                            surplus = threshold
                        final_prices = price[it]
                    else: # if total deficit CANNOT be covered by the pool
                        # modified first price auction
                        # InfSP payments are their cost
                        # revert surplus update
                        surplus -= cur_surplus
                        for ii in range(1, I + 1):
                            final_payments[ii] = KK[ii]
                        # half of the current surplus is shared as discount to the customers
                        cur_surplus = U(X, req[it], R, price[it]) - sum(KK.values())
                        for s in price[it]:
                            final_prices[s] = max(price[it][s] - (cur_surplus/len(price[it]))/2,0)
                        surplus = surplus + cur_surplus/2

                    final_Profit = dict()
                    for ii in range(1,I+1):
                        final_Profit[ii] = final_payments[ii] - KK[ii]

                    new_profit = dict()
                    new_profit_l = dict()
                    new_profit_h = dict()

                    print(it)
                    print("Surplus Status", surplus)
                    print("Threshold", threshold)
                    print("Total Profits", sum(final_Profit.values()))
                    print("Total Profits StandAlone", sum(P_a.values()))
                    print("Total VSP payments", sum(final_prices.values()))
                    print("Total VCG payments", sum(final_payments.values()))

                    file = open("results_NEW_MultipleIterations.txt", "a")
                    file.write("\n" + "--- New experiment --" + "\n")
                    file.write("Providers = " + repr(I) + "\n")
                    file.write("Topology = " + repr(top) + "\n")
                    file.write("Locations = " + repr(L) + "\n")
                    file.write("Iteration = " + repr(it) + "\n")
                    file.write("Requests = " + repr(SS[it]) + "\n")
                    file.write("Utilization = " + repr(serv_Prov_perc) + "\n")
                    file.write("VCG_payments = " + repr(list(payments.values())) + "\n")
                    file.write("VCG_payments_total = " + repr(sum(payments.values())) + "\n")
                    file.write("Final_InfSP_payments = " + repr(list(final_payments.values())) + "\n")
                    file.write("Final_InfSP_payments_total = " + repr(sum(final_payments.values())) + "\n")
                    file.write("VSP_payments = " + repr(list(final_prices.values())) + "\n")
                    file.write("Surplus= " + repr(surplus) + "\n")
                    file.write("Current Iteration Surplus= " + repr(cur_surplus) + "\n")
                    file.write("InfSP_costs = " + repr(list(KK.values())) + "\n")
                    file.write("InfSP_total_cost = " + repr(sum(KK.values())) + "\n")
                    file.write("Total_Profit_Final = " + repr(sum(final_Profit.values())) + "\n")
                    file.write("Individual_Profit_Final = " + repr(list(final_Profit.values())) + "\n")
                    file.write("Stand_alone_profits = " + repr(list(P_a.values())) + "\n")


                    file.write("\n")
                    file.close()

                    test = 0



