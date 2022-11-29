# In this script, we define the bidding for each resource
from sympy import Symbol


##########################################################################
################### bidding functions per service component type

# IoT core - bid per number of minutes per connected device per day
# estimates the charge per day of l devices are connected all day
def b_iot(l, c, m): return c * (60 * 24 * l) * m


# Firehose - bid per number of TBs feed into the Firehose component per day
def b_fir(l, c, m): return c * (1000 * l) * m


# Analytics - bid per number of processing units active per day
def b_ana(l, c, m): return c * (24 * l) * m


# S3 - bid per data stored or accessed per day
def b_s(l, c, m): return c * (l * 1000 / 30) * m


# EMR - bid per vCPU/hour utilized per day
def b_emr(l, c, m): return c * l * m


# QuickSight - bid per day
def b_qui(l, c, m): return c * l * m


##########################################################################

# A load-based bidding function is assigned to each resource
def B_f(cur_type, cost, markup):
    l = Symbol('l')
    if cur_type == 'IoT':
        bid = b_iot(l, cost[cur_type], markup)
    elif cur_type == 'Firehose':
        bid = b_fir(l, cost[cur_type], markup)
    elif cur_type == 'Analytics':
        bid = b_ana(l, cost[cur_type], markup)
    elif cur_type == 'S3':
        bid = b_s(l, cost[cur_type], markup)
    elif cur_type == 'EMR':
        bid = b_emr(l, cost[cur_type], markup)
    elif cur_type == 'Quick':
        bid = b_qui(l, cost[cur_type], markup)
    else:
        print('There is a type that is not on the list')
    return bid


##############################################################################

def bidding(I, T, cost, markup,max_caps):
    B = dict()
    B_i = dict()
    for i in range(1,I+1):
        B_i[i] = dict()
    # for each resource in topology

    for r in T:
        # characteristics of the current resource
        cur_prov = r[0]
        cur_loc = r[1]
        cur_type = r[2]
        cur_capacity = T[r]

        # The markup use by each Provider depends on its resource capacity in the respective site
        # So the markup is a value
        #  ------ slightly greater than 1 (almost no markup) for Providers with high resource capacity
        #  ------- almost equal to 'markup' for Providers with low capacity
        # This tries to immitate the economy of scale, i.e, the fact that
        # the marginal cost of Providers with increased capacity will be lower
        max_capacity = max_caps[cur_type]
        mark = 1 + markup * (cur_capacity / max_capacity)

        # estimate the bid for this resource
        val = B_f(cur_type, cost, mark)
        B[cur_prov, cur_loc, cur_type] = val
        B_i[cur_prov][cur_prov, cur_loc, cur_type] = val
    return B, B_i


def place_higher_bid(B, B_i, i, R_i):
    B_h = B.copy()
    B_i_h = B_i.copy()
    for j in B_i:
        B_i_h[j] = B_i[j].copy()

    for r in R_i[i]:
        cur_loc = r[1]
        cur_type = r[2]
        val = B[i, cur_loc, cur_type] * 1.2
        B_h[i, cur_loc, cur_type] = val
        B_i_h[i][i, cur_loc, cur_type] = val
    return B_h,B_i_h


def place_lower_bid(B, B_i, i, R_i):
    B_l = B.copy()
    B_i_l = B_i.copy()
    for j in B_i:
        B_i_l[j] = B_i[j].copy()

    for r in R_i[i]:
        cur_loc = r[1]
        cur_type = r[2]
        val = B[i, cur_loc, cur_type] * 0.8
        B_l[i, cur_loc, cur_type] = val
        B_i_l[i][i, cur_loc, cur_type] = val
    return B_l, B_i_l