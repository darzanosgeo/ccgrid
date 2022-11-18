# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # ######## System Dimensioning Parameters #######
    InfP = [3]  # number of Inf Service Providers

    Loc = [3, 5, 10]  # number of geographic locations

    SP = 10  # number of Service Providers

    S = [30, 80, 150]  # total number of service request -- 20
    Load_Edge = {}
    Load_Core = {}

    # 1. AWS IoT Core --> number of connected devices (all day)
    # 2. AWS Kinesis Firehose --> TBs per day streamed into the component
    # 3. AWS Kinesis Data Analytics --> Processing units always active for a month
    Load_Edge[1] = [1000, 20, 10]
    Load_Edge[2] = [1000, 20, 10]
    Load_Edge[3] = [1000, 20, 10]

    # 1. AWS S3 --> TBs/month stored to the core cloud
    # 2. AWS EMR (Serverless)) --> average number of vCPUs/hour utilized per day
    # 3. AWS QuickSight --> Monthly fee for a load of Questions and Sessions
    Load_Core[1] = [50, 100, 1]
    Load_Core[1] = [100, 200, 1]
    Load_Core[1] = [200, 400, 1]



