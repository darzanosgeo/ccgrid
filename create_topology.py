import numpy as np
import random


def create_topology(I, L, Loc_prob, resource_profile, resource_types):
    T = {}
    # assign providers to multiple locations
    for i in range(1,I+1):
        #put each provider to at least one location
        ll = random.randint(1,L)
        for l in range(1,L+1):
            # returns 1 with probability 'Loc_prob' -- 1 means the provider i has presence in region l
            if random.random() < Loc_prob or ll == l:
                for r_type in resource_types:
                    # assign resource capacities to the different providers
                    T[i, l, r_type] = np.round(np.random.normal(1, 0.2, 1) * resource_profile[r_type])

    #check if at least one provider has presence in each location
    for l in range(1,L+1):
        for i in range(1,I+1):
            if (i,l,r_type) in T:
                break
        if i == I:
            # if no provider appears in a location randomly choose and add one
            ii = random.randint(1,I)
            for r_type in resource_types:
                # assign resource capacities to the different providers
                T[i, l, r_type] = np.round(np.random.normal(1, 0.2, 1) * resource_profile[r_type])

    return T
