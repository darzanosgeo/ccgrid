import matplotlib.pyplot as plt
import numpy as np
import re

Results = {}
file = open("results_NEW_TopologiesOLDNEW.txt", "r")
line = file.readline()
while line != '':
    line = file.readline()
    if "New experiment" in line:
        while "\n" != line:
            line = file.readline()
            if "Providers =" in line:

                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Providers = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                top = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                locs = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                reqs = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                utilization = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                InfSP_payments = temp
                for _ in range(len(InfSP_payments)):
                    InfSP_payments[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                total_InfSP_payments = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                VSP_payments = temp
                for _ in range(len(VSP_payments)):
                    VSP_payments[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                total_VSP_payments = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Surplus = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                InfSP_cost = temp
                for _ in range(len(InfSP_cost)):
                    InfSP_cost[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                total_InfSP_cost = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                total_InfSP_Profit = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                strategic_provider = int(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Individual_Profit_VCG = temp
                for _ in range(len(Individual_Profit_VCG)):
                    Individual_Profit_VCG[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Final_InfSP_Payments = temp
                for _ in range(len(Final_InfSP_Payments)):
                    Final_InfSP_Payments[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Final_InfSP_Profit = temp
                for _ in range(len(Final_InfSP_Profit)):
                    Final_InfSP_Profit[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"-+?\d*\.\d+|\d+", line)
                # = temp
                topology = []
                iii = 0
                while iii != len(temp):
                    topology.append((int(temp[iii]), int(temp[iii+1])))
                    iii = iii + 2

                if (Providers, top, locs, reqs) not in Results.keys():
                    Results[Providers, top, locs, reqs] = dict()

                Results[Providers, top, locs, reqs]['utilization'] = utilization
                Results[Providers, top, locs, reqs]['InfSP_payments'] = InfSP_payments
                Results[Providers, top, locs, reqs]['total_InfSP_payments'] = total_InfSP_payments
                Results[Providers, top, locs, reqs]['VSP_payments'] = VSP_payments
                Results[Providers, top, locs, reqs]['total_VSP_payments'] = total_VSP_payments
                Results[Providers, top, locs, reqs]['Surplus'] = Surplus
                Results[Providers, top, locs, reqs]['InfSP_cost'] = InfSP_cost
                Results[Providers, top, locs, reqs]['total_InfSP_cost'] = total_InfSP_cost
                Results[Providers, top, locs, reqs]['total_InfSP_Profit'] = total_InfSP_Profit
                Results[Providers, top, locs, reqs]['strategic_provider'] = strategic_provider
                Results[Providers, top, locs, reqs]['Individual_Profit_VCG'] = Individual_Profit_VCG
                Results[Providers, top, locs, reqs]['Final_InfSP_Payments'] = Final_InfSP_Payments
                Results[Providers, top, locs, reqs]['Final_InfSP_Profit'] = Final_InfSP_Profit
                Results[Providers, top, locs, reqs]['topology'] = topology

X = 39

i = 5
T = list(np.arange(1, X+1))
l = 5
R = [50]


ssurplus = []
ttopology = {}
for r in R:
    strategic_provider_individual_Profit = 0
    stand_alone_profit = 0
    final_profit = 0
    utilizationn_agr = 0
    for t in T:
        ssurplus.append(Results[i, t, l, r]['Surplus'])
        utilizationn_agr += Results[i, t, l, r]['utilization']/len(T)
        ttopology[t] = (Results[i, t, l, r]['topology'])

topology_count = dict.fromkeys(T,0)
for _ in range(1,len(T)+1):

    cur_top = ttopology[_]
    loc_pres = {}
    for ii in range(1,l+1):
        loc_pres[ii] = []
    for cur in cur_top:
        loc_pres[cur[1]].append(cur[0])
    for ii in range(1,l+1):
        if len(loc_pres[ii]) <= 1:
            topology_count[_] += 1






plt.rcParams.update({'font.size': 14})
plt.rcParams.update({'axes.labelsize': 14})


tt = [i for i in range(1, X*len(R)+1)]

#colors = plt.cm.Dark2(np.arange(len(R)*34) // 34 / (len(R)-1))

plt.bar(tt, ssurplus, color='blue', linestyle='solid')

plt.xlim(0, max(tt))

# Add horizontal gridlines
plt.grid(axis='y', linestyle='--', linewidth=0.5)
# plt.grid()

# naming the x axis
plt.xlabel('Total # of requests', fontsize=16)
# naming the y axis
plt.ylabel('Surplus ($/h)', fontsize=16)

# Loop through each value and add it on top of the bar
for x, y, k in zip(tt, ssurplus, topology_count.values()):
    plt.text(x, y, str(k), ha='center', va='bottom', fontsize=12)

# Set the values at the center of each grid box
# values = [5, 10, 20, 30, 50, 70, 100]
# xticks = [(18*i + 18*(i+1))/2 for i in range(len(R))]
# plt.xticks(xticks, values)

# giving a title to my graph
# plt.title('Total Profit, ' + str(i) + ' Providers, ' + str(l) + ' Locations')
# plt.legend(['Surplus' ])
plt.savefig('SurplusTopologies ' + str(i) + ' Providers, ' + str(l) + ' Locations', dpi=300, bbox_inches='tight')
plt.show()
plt.close('all')