import matplotlib.pyplot as plt
import numpy as np
import re

Results = {}
file = open("results_NEW_MultipleIterations.txt", "r")
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
                it = float(temp[0]) + 1

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                reqs = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                utilization = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                VCG_payments = temp
                for _ in range(len(VCG_payments)):
                    VCG_payments[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                VCG_payments_total = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Final_InfSP_payments = temp
                for _ in range(len(Final_InfSP_payments)):
                    Final_InfSP_payments[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Final_InfSP_payments_total = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                VSP_payments = temp
                for _ in range(len(VSP_payments)):
                    VSP_payments[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Surplus = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                currentIt_Surplus = float(temp[0])

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
                total_Profit_Final = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Individual_Profit_final = temp
                for _ in range(len(Individual_Profit_final)):
                    Individual_Profit_final[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Stand_alone_profits = temp
                for _ in range(len(Stand_alone_profits)):
                    Stand_alone_profits[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"-+?\d*\.\d+|\d+", line)
                # = temp

                topology = []
                iii = 0
                while iii != len(temp):
                    topology.append((int(temp[iii]), int(temp[iii+1])))
                    iii = iii + 2

                if (Providers, top, locs, reqs) not in Results.keys():
                    Results[Providers, top, locs, it, reqs] = dict()

                Results[Providers, top, locs, it, reqs]['utilization'] = utilization
                Results[Providers, top, locs, it, reqs]['VSP_payments'] = VSP_payments
                Results[Providers, top, locs, it, reqs]['Surplus'] = Surplus
                Results[Providers, top, locs, it, reqs]['InfSP_cost'] = InfSP_cost
                Results[Providers, top, locs, it, reqs]['total_InfSP_cost'] = total_InfSP_cost
                Results[Providers, top, locs, it, reqs]['total_Profit_Final'] = total_Profit_Final
                Results[Providers, top, locs, it, reqs]['Individual_Profit_final'] = Individual_Profit_final
                Results[Providers, top, locs, it, reqs]['Stand_alone_profits'] = Stand_alone_profits
                Results[Providers, top, locs, it, reqs]['VCG_Payments'] = VCG_payments
                Results[Providers, top, locs, it, reqs]['Final_InfSP_Payments'] = Final_InfSP_payments
                Results[Providers, top, locs, it, reqs]['topology'] = topology

X = 13

I = 5
T = list(np.arange(1, X+1))
l = 5
R = [10, 20, 30, 50, 70, 40, 50, 30, 10, 20]

surplus = {}
ind_fin_prof = {}
stand_al_prof = {}
vcg_payments = {}
final_payments = {}

for t in T:
    for i in range(1, I+1):
        ind_fin_prof[t, i] = []
        stand_al_prof[t, i] = []
        vcg_payments[t, i] = []
        final_payments[t, i] = []

for t in T:
    surplus[t] = []
    it = 0
    for r in R:
        it += 1
        surplus[t].append(Results[I, t, l, it, r]['Surplus'])
        for i in range(1, I+1):
            ind_fin_prof[t, i].append(Results[I, t, l, it, r]['Individual_Profit_final'][i-1])
            stand_al_prof[t, i].append(Results[I, t, l, it, r]['Stand_alone_profits'][i-1])
            vcg_payments[t, i].append(Results[I, t, l, it, r]['Individual_Profit_final'][i - 1])
            final_payments[t, i].append(Results[I, t, l, it, r]['Individual_Profit_final'][i - 1])

plt.rcParams.update({'font.size': 14})
plt.rcParams.update({'axes.labelsize': 14})

rr = [i for i in range(1, len(R)+1)]


for t in T:
    plt.plot(rr, surplus[t], color='blue', linestyle='solid', linewidth=3, marker='o', markerfacecolor='blue', markersize=10)

    plt.xlim(0, max(rr))
    default_x_ticks = range(len(rr))
    plt.xticks(rr, R)
    # Add horizontal gridlines
    #plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.grid()

    # naming the x axis
    plt.xlabel('Total # of requests', fontsize=16)
    # naming the y axis
    plt.ylabel('Surplus ($/h)', fontsize=16)


    plt.savefig('SurplusTopologies ' + str(i) + ' Providers, ' + str(l) + ' Locations' + str(t) + ' Locations', dpi=300, bbox_inches='tight')
    #plt.show()
    plt.close('all')