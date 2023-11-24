import matplotlib.pyplot as plt
import numpy as np
import re

Results = {}
file = open("results_NEW3_MultipleIterations.txt", "r")
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
                utilization_fed = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                utilization_stnd = float(temp[0])

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
                InfSP_cost = temp
                for _ in range(len(InfSP_cost)):
                    InfSP_cost[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                total_InfSP_cost = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                total_Profit_final = float(temp[0])

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
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Initial_VSP_payments = temp
                for _ in range(len(Initial_VSP_payments)):
                    Initial_VSP_payments[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Final_VSP_payments = temp
                for _ in range(len(Final_VSP_payments)):
                    Final_VSP_payments[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Service_cost = temp
                for _ in range(len(Service_cost)):
                    Service_cost[_] = float(temp[_])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Surplus = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                Threshold = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                currentIt_Surplus = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                first_price = float(temp[0])

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

                Results[Providers, top, locs, it, reqs]['utilization_fed'] = utilization_fed
                Results[Providers, top, locs, it, reqs]['utilization_stnd'] = utilization_stnd
                Results[Providers, top, locs, it, reqs]['Initial_VSP_payments'] = Initial_VSP_payments
                Results[Providers, top, locs, it, reqs]['Final_VSP_payments'] = Initial_VSP_payments
                Results[Providers, top, locs, it, reqs]['Surplus'] = Surplus
                Results[Providers, top, locs, it, reqs]['Cur_Surplus'] = currentIt_Surplus
                Results[Providers, top, locs, it, reqs]['InfSP_cost'] = InfSP_cost
                Results[Providers, top, locs, it, reqs]['total_InfSP_cost'] = total_InfSP_cost
                Results[Providers, top, locs, it, reqs]['total_Profit_Final'] = total_Profit_final
                Results[Providers, top, locs, it, reqs]['Individual_Profit_final'] = Individual_Profit_final
                Results[Providers, top, locs, it, reqs]['Stand_alone_profits'] = Stand_alone_profits
                Results[Providers, top, locs, it, reqs]['VCG_Payments'] = VCG_payments
                Results[Providers, top, locs, it, reqs]['Final_InfSP_Payments'] = Final_InfSP_payments
                Results[Providers, top, locs, it, reqs]['topology'] = topology
                Results[Providers, top, locs, it, reqs]['first_price'] = first_price

X = 19

I = 5
T = list(np.arange(1, X+1))
l = 5
R = [10, 10, 10, 10, 20, 30, 50, 50, 30, 50, 30, 10, 20, 30, 30, 50, 50, 60, 50, 50, 50, 50, 40, 10, 20, 10, 10, 10, 10, 10]

surplus = {}
ind_fin_prof = {}
stand_al_prof = {}
vcg_payments = {}
final_payments = {}
first_price = {}
sum_prof_increase = {}
sum_stand_prof = {}
top_utilization_fed = {}
top_utilization_stnd = {}

for t in T:
    for i in range(1, I+1):
        ind_fin_prof[t, i] = []
        stand_al_prof[t, i] = []
        vcg_payments[t, i] = []
        final_payments[t, i] = []

for t in T:
    surplus[t] = []
    first_price[t] = []
    sum_prof_increase[t] = []
    sum_stand_prof[t] = []
    top_utilization_fed[t] = []
    top_utilization_stnd[t] = []

    it = 0
    for r in R:
        it += 1
        surplus[t].append(Results[I, t, l, it, r]['Surplus'])
        first_price[t].append(Results[I, t, l, it, r]['first_price'])
        sum_prof_increase[t].append(sum(Results[I, t, l, it, r]['Individual_Profit_final']) - sum(Results[I, t, l, it, r]['Stand_alone_profits']))
        sum_stand_prof[t].append(sum(Results[I, t, l, it, r]['Stand_alone_profits']))
        top_utilization_fed[t].append(Results[I, t, l, it, r]['utilization_fed']*r)
        top_utilization_stnd[t].append(Results[I, t, l, it, r]['utilization_stnd']*r)
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

    counter = 0
    for ii, jj in zip(rr, surplus[t]):
        if first_price[t][ii-1] == 0:
            temp = 'V'
        else:
            temp = 'F'
        plt.text(ii-0.3, jj + 100, temp , fontsize=12, color='black', ha='right', va='bottom')
        counter += 1


    Profit_increase = sum(sum_prof_increase[t])/sum(sum_stand_prof[t])*100
    tot_prof= sum(sum_prof_increase[t])+sum(sum_stand_prof[t])
    tot_stand= sum(sum_stand_prof[t])


    fed_perc = sum(top_utilization_fed[t])/sum(R)
    stand_perc = sum(top_utilization_stnd[t])/sum(R)

    if t == 18:
        plt.text(ii-4, max(surplus[t]) +1500, 'Total Profit Increase Achieve='+str(int(Profit_increase))+'%, '+ 'Total Federation Profit='+str(int(tot_prof))+', ('+ fed_perc+'% of the requests served)'+' Total Standlone Profit='+str(int(tot_stand))+', ('+ stand_perc+'% of the requests served)', fontsize=12, color='green', ha='right', va='bottom')
    else:
        plt.text(ii - 4, max(surplus[t]) + 500, 'Total Federation Profit Increase=' + str(
            int(Profit_increase)) + '%, ' + 'Total Federation Profit=' + str(
            int(tot_prof)) + ', Total Standlone Profit=' + str(int(tot_stand)), fontsize=12, color='green', ha='right',
                 va='bottom')
    plt.legend(['Suplus Balance'])
    plt.savefig('Surplus_Topologies,' + str(i) + ' Providers, ' + str(l) + ' Locations' + str(t) + ' topology', dpi=300, bbox_inches='tight')
    plt.show()



    plt.close('all')

    ################################################################################################

    for i in range(1,I+1):

        plt.plot(rr, ind_fin_prof[t,i], color='blue', linestyle='solid', linewidth=3, marker='o', markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, i], color='black', linestyle='solid', linewidth=3, marker='x',
                 markerfacecolor='black',
                 markersize=10)

        plt.xlim(0, max(rr))
        default_x_ticks = range(len(rr))
        plt.xticks(rr, R)
        # Add horizontal gridlines
        # plt.grid(axis='y', linestyle='--', linewidth=0.5)
        plt.grid()

        # naming the x axis
        plt.xlabel('Total # of requests', fontsize=16)
        # naming the y axis
        plt.ylabel('Profit ($/h)', fontsize=16)

        plt.savefig('Profit_Topologies, ' + str(i) + ' Providers, ' + str(l) + ' Locations' + str(t) + ' Topology' + str(i) + 'Provider', dpi=300,
                    bbox_inches='tight')
        # plt.show()
        plt.close('all')

    if t == 4:
        plt.plot(rr, ind_fin_prof[t, 5], color='black', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='black',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 5], color='black', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='black',
                 markersize=10)
        plt.plot(rr, ind_fin_prof[t, 3], color='blue', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 3], color='blue', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, ind_fin_prof[t, 2], color='green', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='green',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 2], color='green', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='green',
                 markersize=10)

        plt.xlim(0, max(rr))
        default_x_ticks = range(len(rr))
        plt.xticks(rr, R)
        # Add horizontal gridlines
        # plt.grid(axis='y', linestyle='--', linewidth=0.5)
        plt.grid()

        # naming the x axis
        plt.xlabel('Total # of requests', fontsize=16)
        # naming the y axis
        plt.ylabel('Profit ($/h)', fontsize=16)

        plt.savefig('Profit_Topologies, ' + str(i) + ' Providers, ' + str(l) + ' Locations' + str(t) + ' Topology' + 'Multiple' + 'Provider', dpi=300,
            bbox_inches='tight')
        # plt.show()
        plt.close('all')

    if t == 12:
        plt.plot(rr, ind_fin_prof[t, 4], color='black', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='black',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 4], color='black', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='black',
                 markersize=10)
        plt.plot(rr, ind_fin_prof[t, 5], color='blue', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 5], color='blue', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, ind_fin_prof[t, 1], color='green', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 1], color='green', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='blue',
                 markersize=10)

        plt.xlim(0, max(rr))
        default_x_ticks = range(len(rr))
        plt.xticks(rr, R)
        # Add horizontal gridlines
        # plt.grid(axis='y', linestyle='--', linewidth=0.5)
        plt.grid()

        # naming the x axis
        plt.xlabel('Total # of requests', fontsize=16)
        # naming the y axis
        plt.ylabel('Profit ($/h)', fontsize=16)

        plt.savefig('Profit_Topologies, ' + str(i) + ' Providers, ' + str(l) + ' Locations' + str(
            t) + ' Topology' + 'Multiple' + 'Provider', dpi=300,
                    bbox_inches='tight')
        # plt.show()
        plt.close('all')

    if t == 16:
        plt.plot(rr, ind_fin_prof[t, 1], color='black', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='black',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 1], color='black', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='black',
                 markersize=10)
        plt.plot(rr, ind_fin_prof[t, 3], color='blue', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 3], color='blue', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, ind_fin_prof[t, 5], color='green', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 5], color='green', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='blue',
                 markersize=10)

        plt.xlim(0, max(rr))
        default_x_ticks = range(len(rr))
        plt.xticks(rr, R)
        # Add horizontal gridlines
        # plt.grid(axis='y', linestyle='--', linewidth=0.5)
        plt.grid()

        # naming the x axis
        plt.xlabel('Total # of requests', fontsize=16)
        # naming the y axis
        plt.ylabel('Profit ($/h)', fontsize=16)

        plt.savefig('Profit_Topologies, ' + str(i) + ' Providers, ' + str(l) + ' Locations' + str(
            t) + ' Topology' + 'Multiple' + 'Provider', dpi=300,
                    bbox_inches='tight')
        # plt.show()
        plt.close('all')

    if t == 18:
        plt.plot(rr, ind_fin_prof[t, 2], color='black', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='black',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 2], color='black', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='black',
                 markersize=10)
        plt.plot(rr, ind_fin_prof[t, 4], color='blue', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 4], color='blue', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, ind_fin_prof[t, 5], color='green', linestyle='solid', linewidth=3, marker='o',
                 markerfacecolor='blue',
                 markersize=10)
        plt.plot(rr, stand_al_prof[t, 5], color='green', linestyle='dashed', linewidth=3, marker='',
                 markerfacecolor='blue',
                 markersize=10)

        plt.xlim(0, max(rr))
        default_x_ticks = range(len(rr))
        plt.xticks(rr, R)
        # Add horizontal gridlines
        # plt.grid(axis='y', linestyle='--', linewidth=0.5)
        plt.grid()

        # naming the x axis
        plt.xlabel('Total # of requests', fontsize=16)
        # naming the y axis
        plt.ylabel('Profit ($/h)', fontsize=16)

        plt.savefig('Profit_Topologies, ' + str(i) + ' Providers, ' + str(l) + ' Locations' + str(
            t) + ' Topology' + 'Multiple' + 'Provider', dpi=300,
                    bbox_inches='tight')
        # plt.show()
        plt.close('all')