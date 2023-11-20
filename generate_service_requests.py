# Generate S requests that span across the L regions.
# Each request requires presence in at least on region--- more regions are added with a probability.
# The core service components, i.e., S3, EMR, QuickSight, are only deployed to one location and have no location restrictions
import random
import numpy as np


def generate_service_requests(S, L, Load_Core, Load_Edge, price_s, prob_region):
    reqs = dict()
    price = dict()

    for s in range(1, S + 1):

        #################################
        # Determine the service regions
        # randomly select one region from L
        locs = random.sample(range(1,L+1),2)
        #locs = random.sample(range(1, L + 1), 1)

        # add more locations with a probability
        for l in range(1, L):
            if random.random() < prob_region and l not in locs:
                locs.append(l)


        #################################
        # edge service components should be placed in all regions, while core service components should be placed once
        # the actual load of each component is determined by the based load
        reqs[s] = dict()

        # first generate the core service components S3, EMR and QuickSight
        # the base value for load increases with the number of edge regions supported
        mult = len(locs)

        # random value based on normal distribution are assigned to all components
        comp_counter = 1
        for comp_prof in Load_Core:
            val = float(np.random.normal(1, 0.1, 1) * Load_Core[comp_prof] * mult)
            reqs[s][comp_counter] = {'type': comp_prof, 'load': val, 'region': 0}
            comp_counter += 1

        # next generate the edge service components in all locations
        for l in locs:
            for comp_prof in Load_Edge:
                val = float(np.random.normal(1, 0.1, 1) * Load_Edge[comp_prof])
                reqs[s][comp_counter] = {'type': comp_prof, 'load': val, 'region': l}
                comp_counter += 1

        #################################
        # set the price of the service
        # the price is randomly selected based on a normal distribution for a default value multiplied by
        # the number of regions that the service is available
        # price[s] = float(np.random.normal(1, 0.3, 1) * mult * price_s)
        price[s] = price_s + (mult-1) * price_s * (2/3) * float(np.random.normal(1, 0.1, 1))

        #################################
    return reqs, price
