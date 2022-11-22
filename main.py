# This is a sample Python script.
import numpy as np
from create_topology import create_topology

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.


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

    # Resource Capacities are assigned based on a normal distribution
    resource_profile = dict()
    for r_type in resource_types:
        if r_type == 'IoT':
            # number of IoT Devices can be supported by a single providers in a single location
            resource_profile[r_type] = 10000
        elif r_type == 'Firehose':
            # maximum number of TBs that can be streamed into Firehose resources
            resource_profile[r_type] = 200
        elif r_type == 'Analytics':
            # number of Data Analytics processing units available by each Provider in each region
            resource_profile[r_type] = 100
        elif r_type == 'S3':
            # maximum number of TBs can be stored by each Provider in each region
            resource_profile[r_type] = 500
        elif r_type == 'EMR':
            # number of vCPUs maintained by a single providers in a single location
            resource_profile[r_type] = 1000
        elif r_type == 'Quick':
            # number of Qyicksight instances can be supported by a single providers in a single location
            resource_profile[r_type] = 10**6  # THIS IN FACT MEANS NO LIMITATION

    # ##### Service Characteristics
    # mean default load of service requests # we consider the AWS connected mobility service presented in the example
    Load_Edge = dict()
    Load_Core = dict()
    # 1. AWS IoT Core --> number of connected devices (all day)
    # 2. AWS Kinesis Firehose --> TBs per day streamed into the component
    # 3. AWS Kinesis Data Analytics --> Processing units always active for a month
    Load_Edge[1] = [1000, 20, 10]

    # 1. AWS S3 --> TBs/month stored to the core cloud
    # 2. AWS EMR (Serverless)) --> average number of vCPUs/hour utilized per day
    # 3. AWS QuickSight --> Monthly fee for a load of Questions and Sessions
    Load_Core[1] = [50, 100, 1]
    # Load_Core[1] = [100, 200, 1]
    # Load_Core[1] = [200, 400, 1]

    price_s = 100 # $/hour
    ###############################
    #       Init Process          #
    ##############################

    # for all combinations of number of Providers/ number Regions/number of random topologies per combination of number Providers and number of Regions
    for I in InfP:
        for L in Loc:
            for top in range(1,random_topologies):
                # create topology
                T = create_topology(I, L, Loc_prob, resource_profile, resource_types)

                # Generate Requests for different global loads
                req = dict()
                for S in SS:
                    req[S] = generate_service_requests(S, L,Load_Core,Load_Edge, price_s)
