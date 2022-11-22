# Generate S requests that span across the L regions.
# Each request requires presence in at least on region--- more regions are added with a probability.
# The core service components, i.e., S3, EMR, QuickSight, are only deployed to one location and have no location restrictions
import random

def generate_service_requests(S, L, Load_Core, Load_Edge, price_s, prob_region):
    reqs = dict()
    for s in range(1, S+1):

        #################################
        # Determine the service regions
        # randomly select one region from L
        locs = []
        locs[1] = random.randint(1, L)

        # add more locations with a probability
        for l in range(1, L):
            if random.random() < prob_region:
                locs.append(l)
        #################################

        #################################
        # edge service components should be placed in all regions, while core service components should be placed once

        #################################
    return reqs