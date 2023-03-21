from copy import deepcopy


# desirability
def desir(s, S, sigma, r, B, price_s, price_m):
    # p_sigma = (price_s-price_m)/len(S[s])
    # d = p_sigma/B[r].subs('l', S[s][sigma]['load'])
    #d = (price_s - price_m) / B[r].subs('l', S[s][sigma]['load'])
    d = (price_s - price_m) / len(S[s]) / B[r].subs('l', S[s][sigma]['load'])
    return d


def value(price_s, price_m, s, S):
    val = (price_s - price_m) / len(S[s])
    # val = price_s - price_m
    return val


def cost(B, r, s, S, sigma):
    cos = B[r].subs('l', S[s][sigma]['load'])
    return cos


def MTHG(R, R_i, S, B, price, I, resource_types, L, price_m):
    # service component cost --> b_r(lambda_sigma)
    # service component value --> val = p_sigma = p_s/len(s)  OR val = p_sigma - b_r(lambda_sigma)
    # desirability --> des = p_sigma/b_r(lambda_sigma) OR des = (p_sigma - b_r(lambda_sigma))/lambda_sigma
    X = dict()
    for r in R:
        for s in S:
            for sigma in S[s]:
                X[r, s, sigma] = 0

    # Service and service component provisioning flags
    s_prov = dict()
    sigma_prov = dict()
    sigma_bid = dict()
    prev_unassinged = 0
    feasible_res = dict()
    infeas_serv = dict()
    desirability = dict()
    maxdes = dict()
    maxdes_r = dict()
    maxdes2 = dict()
    maxdes2_r = dict()
    total_profit = 0

    for s in S:
        s_prov[s] = 0
        infeas_serv[s] = 0
        for sigma in S[s]:
            sigma_prov[s, sigma] = 0
            sigma_bid[s, sigma] = 0
            ############
            feasible_res[s, sigma] = []
            desirability[s, sigma] = dict()
            maxdes[s, sigma] = 0
            maxdes_r[s, sigma] = []
            maxdes2[s, sigma] = 0
            maxdes2_r[s, sigma] = []

    cur_unassigned = len(sigma_prov)

    infeasible = 0

    while prev_unassinged != cur_unassigned:
        prev_unassinged = cur_unassigned
        winner = -1
        winner_val = -1
        for s in S:
            if s_prov[s] == 1:
                continue

            for sigma in S[s]:
                if sigma_prov[s, sigma] == 1:
                    continue

                for r in R:
                    # check if the capacity is feasible
                    if S[s][sigma]['load'] >= R[r]:
                        continue

                    # check if the resource type is feasible
                    if S[s][sigma]['type'] != r[2]:
                        continue

                    # check if the location is feasible
                    if S[s][sigma]['region'] != r[1] and S[s][sigma]['region'] != 0:
                        continue

                    # if sigma == 5:
                    #     stop = 0
                    # check if the budget is feasible
                    # We find how many components of the service remain unsigned
                    # and how much budget has not been consumed,
                    # assuming that the assigned components pay only for the bid of assigned resource
                    sig_counter = 0
                    sig_bid = 0
                    # find the number of unassigned components and the remaining budget
                    for sig in S[s]:
                        if sigma_prov[s, sig] != 0:
                            sig_counter += 1
                            sig_bid += sigma_bid[s, sig]
                    # after dividing the remaining budget equally to the remaining components
                    # determine if budget of component sigma is enough to pay resource r
                    if (price[s] - price_m - sig_bid) / (len(S[s]) - sig_counter) <= B[r].subs('l',
                                                                                               S[s][sigma]['load']):
                        continue

                    # mark this resource as feasible assignment for component sigma
                    feasible_res[s, sigma].append(r)
                    desirability[s, sigma][r] = desir(s, S, sigma, r, B, price[s], price_m)

                # if there is no feasible resource for component sigma, then service s cannot be served
                if len(feasible_res[s, sigma]) == 0:
                    # infeas_serv[s] = 1
                    continue
                # if there is feasible resource
                else:
                    # select the resource with the highest desirability
                    maxdes[s, sigma] = max(desirability[s, sigma].values())
                    maxdes_r[s, sigma] = max(desirability[s, sigma], key=desirability[s, sigma].get)
                    # if there are multiple feasible solutions, then find the second most desirable
                    if len(feasible_res[s, sigma]) > 1:
                        temp = deepcopy(desirability[s, sigma])
                        temp.pop(maxdes_r[s, sigma])
                        try:
                            maxdes2[s, sigma] = max(temp.values())
                        except:
                            stop = 0
                        maxdes2_r[s, sigma] = max(temp, key=temp.get)

                    des = maxdes[s, sigma] - maxdes2[s, sigma]

                    if des > winner_val:
                        winner_val = des
                        winner = [maxdes_r[s, sigma], s, sigma]

        # If there is a winner
        if winner != -1:
            # make the value of the proper assignment parameter 1
            X[tuple(winner)] = 1

            # estimate the value added to the system with this assignment value-cost
            total_profit += value(price[winner[1]], price_m, winner[1], S) - cost(B, winner[0], winner[1], S, winner[2])
            # reduce the capacity of the assigned resource
            R[winner[0]] = R[winner[0]] - S[winner[1]][winner[2]]['load']

            # set the bid for the assigned resource
            sigma_bid[winner[1], winner[2]] = B[winner[0]].subs('l', S[winner[1]][winner[2]]['load'])
            sigma_prov[winner[1], winner[2]] = 1
            # reduce the number of unassigned resources
            cur_unassigned -= 1
            # if all the service components of a services are provisioned the mark service as provisioned
            for sig in S[winner[1]]:
                if sigma_prov[winner[1], sig] == 0:
                    s_prov[winner[1]] = 0
                    break
                else:
                    s_prov[winner[1]] = 1

        for s in S:
            for sigma in S[s]:
                feasible_res[s, sigma] = []
                desirability[s, sigma] = dict()
                maxdes[s, sigma] = 0
                maxdes_r[s, sigma] = []
                maxdes2[s, sigma] = 0
                maxdes2_r[s, sigma] = []

    ############################################################################################
    ##### IMPROVEMENT STEP
    # For the services that remain unassigned sort them based on the number of components that remains unassigned
    # For those that have equal number of pending components short the based on value/price of the service
    # Fit as many services as possible

    # count how many components of the incomplete services are assigned in the current solution
    comp_count = dict()
    for s in S:
        if s_prov[s] == 0:
            comp_count[s] = 0
            for sigma in S[s]:
                if sigma_prov[s, sigma] == 1:
                    comp_count[s] += 1

                    # mark resource as unassigned
                    sigma_prov[s, sigma] = 0

                    # free the capacity that had been reserved and value that has been added
                    for r in R:
                        if X[r, s, sigma] == 1:

                            X[r, s, sigma] = 0

                            # restore capacity
                            R[r] = R[r] + S[s][sigma]['load']

                            # reduce the total value
                            total_profit -= value(price[s], price_m, s, S) - cost(B, r, s, S, sigma)

    # sort the services for prioritization
    sorted_comp_count = sorted(comp_count.items(), key=lambda x:x[1],reverse=True)

    # the maximum number of iteration is the number of unassigned services
    for choice,_ in sorted_comp_count:

        selected_resource = dict()
        # For the selected service, try to assign all the service components
        for sigma in S[choice]:
            min_bid_res = 0
            for r in R:
                # check if the capacity is feasible
                if S[choice][sigma]['load'] >= R[r]:
                    continue

                # check if the resource type is feasible
                if S[choice][sigma]['type'] != r[2]:
                    continue

                # check if the location is feasible
                if S[choice][sigma]['region'] != r[1] and S[choice][sigma]['region'] != 0:
                    continue

                # find the resource with the lowest bid for this service component
                if B[r].subs('l', S[choice][sigma]['load']) < min_bid_res or min_bid_res == 0:
                    min_bid_res = B[r].subs('l', S[choice][sigma]['load'])
                    selected_resource[sigma] = r

            # if there is no feasible resource
            if selected_resource == {}:
                break
            elif list(selected_resource)[-1] != sigma:
                break

            # assign this resource
            X[selected_resource[sigma], choice, sigma] = 1
            sigma_prov[choice, sigma] = 1

            # Reduce capacity
            R[selected_resource[sigma]] = R[selected_resource[sigma]] - S[choice][sigma]['load']

            # Increase Profit
            total_profit += value(price[choice], price_m, choice, S) - cost(B, selected_resource[sigma], choice, S, sigma)

        # if all resource assigned calculate the total cost
        total_cost = 0
        if len(selected_resource) == len(S[choice]):
            s_prov[choice] = 1
            for sigma in S[choice]:
                total_cost += B[selected_resource[sigma]].subs('l', S[choice][sigma]['load'])
        else:
            s_prov[choice] = 0

        # if not all components have served and the price is not feasible
        # then rollback the assignments and move to the next service
        if total_cost > price[choice] or s_prov[choice] == 0:
            s_prov[choice] = 0
            for sigma in S[choice]:
                if sigma_prov[choice, sigma] == 1:
                    sigma_prov[choice, sigma] = 0

                    X[selected_resource[sigma], choice, sigma] = 0

                    # Reduce capacity
                    R[selected_resource[sigma]] = R[selected_resource[sigma]] + S[choice][sigma]['load']

                    # Increase Profit
                    total_profit -= value(price[choice], price_m, choice, S) - cost(B, selected_resource[sigma], choice,
                                                                                    S, sigma)

    ##################################################################################################
    # services that eventually provisioned
    serv_Prov_perc = sum(s_prov.values())/len(s_prov)

    for s in S:
        if s_prov[s] == 0:
            for sigma in S[s]:
                for r in R:
                    X[r, s, sigma] = 0

    return X, total_profit, s_prov.values(), serv_Prov_perc
