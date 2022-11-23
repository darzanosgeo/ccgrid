# In this script, we define the bidding for each resource
from sympy import Symbol, Function


################### bidding functions per service component type
# bid per number of minutes per connected device per day
# estimates the charge per day of l devices are connected all day
def b_iot(l, c, m): return c * 60 * 24 * l * m


# bid per number of TBs feed into the Firehose component per day
def b_fir(l, c, m): return c * 1000 * l * m


# bid per number of processing units active per day
def b_ana(l, c, m): return c * 60 * 24 * l * m


# A load-based bidding function is assigned to each resource
def B_f(cur_type, cur_capacity, cost, markup):
    l = Symbol('l')
    if cur_type == 'IoT':
        # bid = cur_capacity * cost[cur_type]
        bid = b_iot(l, cost[cur_type], markup)
        # test = bid.subs(l,1)
    elif cur_type == 'Firehose':
        bid = b_fir(l, cost[cur_type], markup)
    elif cur_type == 'Analytics':
        bid = b_ana(l, cost[cur_type], markup)
    elif cur_type == 'S3':
        bid = cur_capacity * cost[cur_type]
    elif cur_type == 'EMR':
        bid = cur_capacity * cost[cur_type]
    elif cur_type == 'Quick':
        bid = cur_capacity * cost[cur_type]
    else:
        print('There is a type that is not on the list')
    return bid


def bidding(T, cost, markup):
    B = dict()

    # for each resource in topology

    for r in T:
        # characteristics of the current resource
        cur_prov = r[0]
        cur_loc = r[1]
        cur_type = r[2]
        cur_capacity = T[r]

        # estimate the bid for this resource
        B[cur_prov, cur_loc, cur_type] = B_f(cur_type, cur_capacity, cost, markup)
    return B
