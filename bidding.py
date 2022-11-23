# In this script, we define the bidding for each resource


# A load-based bidding function is assigned to each resource
def B_f(cur_type, cur_load,cost):
    if cur_type == 'IoT':
        bid = cur_load * cost[cur_type]
    elif cur_type == 'Firehose':
        bid = cur_load * cost[cur_type]
    elif cur_type == 'Analytics':
        bid = cur_load * cost[cur_type]
    elif cur_type == 'S3':
        bid = cur_load * cost[cur_type]
    elif cur_type == 'EMR':
        bid = cur_load * cost[cur_type]
    elif cur_type == 'Quick':
        bid = cur_load * cost[cur_type]
    else:
        print('There is a type that is not on the list')
    return bid



def bidding(T, cost):
    B = dict()

    # for each resource in topology

    for r in T:
        # characteristics of the current resource
        cur_prov = r[0]
        cur_loc = r[1]
        cur_type = r[2]
        cur_load = T[r]

        # estimate the bid for this resource
        B[cur_prov, cur_loc, cur_type] = B_f(cur_type,cur_load,cost)
    return B