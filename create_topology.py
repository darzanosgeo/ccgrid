import numpy as np
import random


def create_topology(I, L, Loc_prob, ResProf_prob, resource_profile_small, resource_profile_large, resource_types):
    T = dict()
    # store tha maximum capacities found across all providers to be used for resource-availability based bidding.
    max_caps = {'IoT': 0, 'Firehose': 0, 'Analytics': 0, 'S3': 0, 'EMR': 0, 'Quick': 0}
    # assign providers to multiple locations
    for i in range(1, I + 1):
        # put each provider to at least one location
        ll = random.randint(1, L)
        for l in range(1, L + 1):
            # returns 1 with probability 'Loc_prob' -- 1 means the provider i has presence in region l
            if random.random() < Loc_prob or ll == l:
                for r_type in resource_types:
                    # assign resource capacities to the different providers
                    # randomly choose small or large resource profiles -- with a probability
                    if random.random() > ResProf_prob:
                        T[i, l, r_type] = int(np.random.normal(1, 0.3, 1) * resource_profile_small[r_type])
                    else:
                        T[i, l, r_type] = int(np.random.normal(1, 0.3, 1) * resource_profile_large[r_type])
                    # Check if it is the largest infrastructure
                    if max_caps[r_type] < T[i, l, r_type]:
                        max_caps[r_type] = T[i, l, r_type]

    # check if at least one provider has presence in each location
    for l in range(1, L + 1):
        for i in range(1, I + 1):
            if (i, l, r_type) in T:
                break
        if i == I:
            # if no provider appears in a location randomly choose and add one
            ii = random.randint(1, I)
            for r_type in resource_types:
                # assign resource capacities to the different providers
                # randomly chose small or large resource profiles -- with a probability
                if random.random() > ResProf_prob:
                    T[ii, l, r_type] = int(np.random.normal(1, 0.3, 1) * resource_profile_small[r_type])
                else:
                    T[ii, l, r_type] = int(np.random.normal(1, 0.3, 1) * resource_profile_large[r_type])

                # Check if it is the largest infrastructure
                if max_caps[r_type] < T[i, l, r_type]:
                    max_caps[r_type] = T[i, l, r_type]

    return T, max_caps
