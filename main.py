from create_topology import create_topology
from generate_service_requests import generate_service_requests
from bidding import bidding


if __name__ == '__main__':
    ###############################
    #      Input Parameters     #
    ##############################

    # ######## System Dimensioning Parameters
    InfP = [10]  # number of Inf Service Providers

    Loc = [5]  # number of geographic locations
    Loc_prob = 0.4 #region density --- probability for a Provider to appear in a region

    SS = [50, 100, 150, 200, 250, 300]  # total number of service request

    random_topologies = 10  # number of random topologies

    # ##### Resources Characteristics
    # Resource types based on our example
    # IoT Core, Kinesis Firehose, Kinesis Data Analytics, S3, EMR, QuickSight
    resource_types = {'IoT', 'Firehose', 'Analytics', 'S3', 'EMR','Quick'}
    ResProf_prob = 0.35 # large profit with probability

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
        elif r_type == 'Analytics':
            # number of Data Analytics processing units available by each Provider in each region
            resource_profile_small[r_type] = 100
            resource_profile_large[r_type] = 500
        elif r_type == 'S3':
            # maximum number of TBs can be stored by each Provider in each region
            resource_profile_small[r_type] = 500
            resource_profile_large[r_type] = 2500
        elif r_type == 'EMR':
            # number of vCPUs maintained by a single providers in a single location
            resource_profile_small[r_type] = 1000
            resource_profile_large[r_type] = 5000
        elif r_type == 'Quick':
            # number of Qyicksight instances can be supported by a single providers in a single location
            resource_profile_small[r_type] = 10**6  # THIS IN FACT MEANS NO LIMITATION
            resource_profile_large[r_type] = 10**6

    # Cost per unit of resource based on AWS prices
    cost = dict()

    cost['IoT'] = 0.096/(10**6)  # cost per minutes of connection
    cost['Firehose'] = 0.034  # cost per GB
    cost['Analytics'] = 0.127/60  # cost per minutes per processing unit
    cost['S3'] = 0.024 # cost per GB of data stored
    cost['EMR'] = 0.06/60 # cost per vCPU per minute
    cost['Quick'] = 34 # cost per month


    # ##### Service Characteristics
    # mean default load of service requests # we consider the AWS connected mobility service presented in the example
    Load_Edge = dict()
    Load_Core = dict()
    # 1. AWS IoT Core --> number of connected devices (all day)
    # 2. AWS Kinesis Firehose --> TBs per day streamed into the component
    # 3. AWS Kinesis Data Analytics --> Processing units always active for a month
    Load_Edge[1] = {'IoT': 1000, 'Firehose': 20, 'Analytics': 10}

    # 1. AWS S3 --> TBs/month stored to the core cloud
    # 2. AWS EMR (Serverless)) --> average number of vCPUs/hour utilized per day
    # 3. AWS QuickSight --> Monthly fee for a load of Questions and Sessions
    Load_Core[1] = {'S3': 50, 'EMR': 100, 'Quick': 1}
    # Load_Core[1] = [100, 200, 1]
    # Load_Core[1] = [200, 400, 1]

    # service price base
    price_s = 100 # $/hour

    # probability of addition service region
    prob_region = 0.2

    ###############################
    #       Init Process          #
    ##############################

    # for all combinations of number of Providers/ number Regions/number of random topologies per combination of number Providers and number of Regions
    for I in InfP:
        for L in Loc:
            for top in range(1,random_topologies):
                # create topology
                T = create_topology(I, L, Loc_prob, ResProf_prob, resource_profile_small, resource_profile_large, resource_types)

                # Providers place bids for their resources
                B = bidding(T, cost)

                # Generate Requests for different total loads
                req = dict()
                # for different total loads -- number of total requests
                for S in SS:
                    # create requests
                    req[S] = generate_service_requests(S, L, Load_Core[1], Load_Edge[1], price_s, prob_region)


