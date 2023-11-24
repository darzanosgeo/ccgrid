# Allocate resources to service requests aiming to maximize the 'Revenues-Bids'
import gurobipy as gp
from gurobipy import GRB
from system_model_functions import U, K, z, zz


def resource_allocationSA(R, R_i, S, B, price, I, resource_types, L,price_m):
    m = gp.Model('Allocation')

    #########################
    # Generate Variables
    x_vars = {}
    for r in R:
        for s in S:
            for sigma in S[s]:
                x_vars[r, s, sigma] = m.addVar(vtype=GRB.BINARY,
                                               name='x' + '_' + str(r) + '_' + str(s) + '_' + str(sigma))

    ########################
    # Generate Objective Function
    obj = gp.quicksum(gp.quicksum(gp.quicksum(
        x_vars[r, s, sigma] * ((price[s] / len(S[s])) - B[r].subs('l', S[s][sigma]['load']))
        for sigma in S[s])
                                  for s in S)
                      for r in R)

    # set the problem objective
    m.setObjective(obj, GRB.MAXIMIZE)

    ########################
    # Generate Constraints

    # each resource to at most one service component
    for r in R:
        for s in S:
            m.addConstr(gp.quicksum(x_vars[r, s, sigma] for sigma in S[s]) <= 1, name='res_to_comp')

    # each service component is served by at most one resource
    for s in S:
        for sigma in S[s]:
            m.addConstr(gp.quicksum(x_vars[r, s, sigma] for r in R) <= 1, name='comp_to_res')

    # the assigned resource should be  in the appropriate location
    for r in R:
        for s in S:
            for sigma in S[s]:
                m.addConstr(x_vars[r, s, sigma] * (r[1] - S[s][sigma]['region']) * S[s][sigma]['region'] == 0,
                            name='location')

    # the assigned resource should be of the appropriate type
    for r in R:
        for s in S:
            for sigma in S[s]:
                if S[s][sigma]['type'] == r[2]:
                    temp_val = 1
                else:
                    temp_val = 0
                m.addConstr(x_vars[r, s, sigma] * (1 - temp_val) == 0, name='type')

    # capacity constraint
    for i in range(1, I + 1):
        for l in range(1, L + 1):
            for t in resource_types:
                m.addConstr(gp.quicksum(gp.quicksum(gp.quicksum(x_vars[r, s, sigma] * S[s][sigma]['load'] * z(r, t, l)
                                                                for sigma in S[s])
                                                    for s in S)
                                        for r in R_i[i])
                            <= R[i, l, t], name='capacity')

    # none or all resource
    for s in S:
        for sig in S[s]:
            m.addConstr(gp.quicksum(gp.quicksum(x_vars[r, s, sigma] for sigma in S[s])
                                    for r in R)
                        == gp.quicksum(x_vars[r, s, sig] * len(S[s]) for r in R), name='none_all')

    for i in range(1, I+1):
        for s in S:
            for sig in S[s]:
                m.addConstr(gp.quicksum(gp.quicksum(x_vars[r, s, sigma] * zz(r, i) for sigma in S[s])
                                        for r in R)
                            == gp.quicksum(x_vars[r, s, sig] * len(S[s]) * zz(r, i) for r in R), name='all_same_provider')


    # price is greater than the cost
    for s in S:
        m.addConstr(gp.quicksum(gp.quicksum(x_vars[r, s, sigma] * B[r].subs('l', S[s][sigma]['load'])
                                            for sigma in S[s])
                                for r in R) + price_m
                    <= price[s], name='price_cost')

    ########################
    # RUN OPTIMIZATION
    # m.setParam(GRB.Param.TimeLimit, 300.0)
    m.optimize()

    # CHECK IF NOT FEASIBLE SOLUTION FOUND
    if GRB.OPTIMAL == 3:
        return -1

    # ##############  STRUCTURE THE SOLUTION OUTPUT  ###############
    try:
        sol_var = m.getAttr(GRB.Attr.X)
    except:
        sol_var = 0

    if sol_var != 0:
        sol_obj = m.objVal

        x = {}
        count = 0

        for r in R:
            for s in S:
                for sigma in S[s]:
                    x[r, s, sigma] = sol_var[count]
                    count += 1
                    if x[r, s, sigma] > 0.99:
                        x[r, s, sigma] = 1
                    elif x[r, s, sigma] <0.01:
                        x[r, s, sigma] = 0
                    else:
                        stop = 0
    else:
        sol_obj = 0

        x = {}
        count = 0

        for r in R:
            for s in S:
                for sigma in S[s]:
                    x[r, s, sigma] = 0



    # double check results
    Total_Profit = U(x, S, R, price) - K(x, S, R, B)
    if round(Total_Profit) == round(sol_obj):
        print("We are OK")
    else:
        stop = 1


    # services that eventually provisioned
    serv_prov = []
    for s in S:
        serv_provisioned = 1
        for sigma in S[s]:
            comp_provisioned = 0
            for r in R:
                if x[r, s, sigma] == 1:
                    comp_provisioned = 1
                    break

            if comp_provisioned == 0:
                serv_provisioned = 0
                break

        serv_prov.append(serv_provisioned)
    serv_Prov_perc = serv_prov.count(1)/len(serv_prov)


    return x, Total_Profit, serv_prov, serv_Prov_perc
