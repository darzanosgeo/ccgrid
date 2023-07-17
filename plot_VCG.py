import matplotlib.pyplot as plt
import numpy as np
import re

Results = {}
file = open("results_NEW2_VCG.txt", "r")
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
                Individual_Profit_VCG_l = temp
                for _ in range(len(Individual_Profit_VCG_l)):
                    Individual_Profit_VCG_l[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Individual_Profit_VCG_h = temp
                for _ in range(len(Individual_Profit_VCG_h)):
                    Individual_Profit_VCG_h[_] = float(temp[_])

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
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Stand_Alone_profit = temp
                for _ in range(len(Stand_Alone_profit)):
                    Stand_Alone_profit[_] = float(temp[_])

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
                Results[Providers, top, locs, reqs]['Individual_Profit_VCG_l'] = Individual_Profit_VCG_l
                Results[Providers, top, locs, reqs]['Individual_Profit_VCG_h'] = Individual_Profit_VCG_h
                Results[Providers, top, locs, reqs]['Final_InfSP_Payments'] = Final_InfSP_Payments
                Results[Providers, top, locs, reqs]['Final_InfSP_Profit'] = Final_InfSP_Profit
                Results[Providers, top, locs, reqs]['Stand_Alone_profit'] = Stand_Alone_profit


i = 5
T = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
l = 5
R = [5, 10, 20, 30, 50, 70, 100]

individual_Profit = []
individual_Profit_l = []
individual_Profit_h = []
standAlone = []
Final_Profit = []
utilizationn = []
surplus = []
for r in R:
    strategic_provider_individual_Profit = 0
    strategic_provider_individual_Profit_l = 0
    strategic_provider_individual_Profit_h = 0
    stand_alone_profit = 0
    final_profit = 0
    utilizationn_agr = 0
    for t in T:
        strategic_provider = Results[i, t, l, r]['strategic_provider']
        strategic_provider_individual_Profit += Results[i, t, l, r]['Individual_Profit_VCG'][strategic_provider-1]/len(T)
        strategic_provider_individual_Profit_l += Results[i, t, l, r]['Individual_Profit_VCG_l'][strategic_provider-1]/len(T)
        strategic_provider_individual_Profit_h += Results[i, t, l, r]['Individual_Profit_VCG_h'][strategic_provider-1]/len(T)
        stand_alone_profit += Results[i, t, l, r]['Stand_Alone_profit'][strategic_provider - 1] / len(T)
        final_profit += Results[i, t, l, r]['Final_InfSP_Profit'][strategic_provider - 1] / len(T)
        surplus.append(Results[i, t, l, r]['Surplus'])
        utilizationn_agr += Results[i, t, l, r]['utilization']/len(T)

    individual_Profit.append(strategic_provider_individual_Profit)
    individual_Profit_l.append(strategic_provider_individual_Profit_l)
    individual_Profit_h.append(strategic_provider_individual_Profit_h)
    standAlone.append(stand_alone_profit)
    Final_Profit.append(final_profit)
    utilizationn.append(utilizationn_agr)

plt.rcParams.update({'font.size': 14})
plt.rcParams.update({'axes.labelsize': 14})

plt.plot(R, individual_Profit, color='black', linestyle='solid', linewidth=3, marker='', markerfacecolor='black', markersize=10)
plt.plot(R, individual_Profit_l, color='blue', linestyle='solid', linewidth=3, marker='o', markerfacecolor='blue', markersize=10)
plt.plot(R, individual_Profit_h, color='red', linestyle='solid', linewidth=3, marker='+', markerfacecolor='red', markersize=10)

counter = 0
for ii, jj in zip(R, individual_Profit):
    temp = int(round(utilizationn[counter] * 100, 2))
    plt.text(ii, jj + 1000, f'{temp}' + '%', fontsize=12, color='black', ha='right', va='bottom')
    counter += 1


plt.xlim(0, max(R))
plt.grid()

# naming the x axis
plt.xlabel('Total # of requests', fontsize=16)
# naming the y axis
plt.ylabel('Individual provider profit ($/h)', fontsize=16)

# giving a title to my graph
# plt.title('Total Profit, ' + str(i) + ' Providers, ' + str(l) + ' Locations')
plt.legend(['announces true cost',  'announces lower cost', 'announces higher cost'])
plt.savefig('Strategic Behavior, ' + str(i) + ' Providers, ' + str(l) + ' Locations', dpi=300, bbox_inches='tight')
plt.show()
plt.close('all')

# ##############################################################################################
# ##############################################################################################
plt.rcParams.update({'font.size': 14})
plt.rcParams.update({'axes.labelsize': 14})

plt.plot(R, individual_Profit, color='black', linestyle='solid', linewidth=3, marker='', markerfacecolor='black', markersize=10)
plt.plot(R, standAlone, color='blue', linestyle='solid', linewidth=3, marker='o', markerfacecolor='blue', markersize=10)
plt.plot(R, Final_Profit, color='red', linestyle='solid', linewidth=3, marker='+', markerfacecolor='red', markersize=10)

# counter = 0
# for ii, jj in zip(R, individual_Profit):
#     temp = int(round(utilizationn[counter] * 100, 2))
#     plt.text(ii, jj + 1000, f'{temp}' + '%', fontsize=12, color='black', ha='right', va='bottom')
#     counter += 1


plt.xlim(0, max(R))
plt.grid()

# naming the x axis
plt.xlabel('Total # of requests', fontsize=16)
# naming the y axis
plt.ylabel('Individual provider profit ($/h)', fontsize=16)

# giving a title to my graph
# plt.title('Total Profit, ' + str(i) + ' Providers, ' + str(l) + ' Locations')
plt.legend(['Federation Profit - VCG only', 'StandAlone Profit', 'Federation Profit - Budget imbalance mitigation'], loc='upper left')
plt.savefig('StandAlone, ' + str(i) + ' Providers, ' + str(l) + ' Locations', dpi=300, bbox_inches='tight')
plt.show()
plt.close('all')

# ##############################################################################################
# ##############################################################################################

plt.rcParams.update({'font.size': 14})
plt.rcParams.update({'axes.labelsize': 14})

# rr = []
# for _ in R:
#     for times in range(len(T)):
#         rr.append(_)
rr = [i for i in range(1, 18*len(R)+1)]

colors = plt.cm.Dark2(np.arange(len(R)*18) // 18 / (len(R)-1))
# colors = plt.cm.Set3(np.arange(len(R)*18) // 18 / (len(R)-1))
# colors = plt.cm.Blues(np.arange(len(R)*18) // 18 / (len(R)-1))

plt.bar(rr, surplus, color=colors, linestyle='solid')

plt.xlim(0, max(rr))
# Add vertical gridlines at every 18th bar
for i in range(18, len(rr), 18):
    plt.axvline(i + 0.5, color='gray', linewidth=0.5)

# Add horizontal gridlines
plt.grid(axis='y', linestyle='--', linewidth=0.5)
# plt.grid()

# naming the x axis
plt.xlabel('Total # of requests', fontsize=16)
# naming the y axis
plt.ylabel('Surplus ($/h)', fontsize=16)

# Set the values at the center of each grid box
values = [5, 10, 20, 30, 50, 70, 100]
xticks = [(18*i + 18*(i+1))/2 for i in range(len(R))]
plt.xticks(xticks, values)

# giving a title to my graph
# plt.title('Total Profit, ' + str(i) + ' Providers, ' + str(l) + ' Locations')
# plt.legend(['Surplus' ])
plt.savefig('Surplus, ' + str(i) + ' Providers, ' + str(l) + ' Locations', dpi=300, bbox_inches='tight')
plt.show()
plt.close('all')