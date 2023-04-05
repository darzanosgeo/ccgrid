import matplotlib.pyplot as plt
import re

Results = {}
file = open("results_greedy_vs_solver.txt", "r")
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
                total_profit = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                serv_perc = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                total_profit_hr = float(temp[0])

                line = file.readline()
                temp = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                serv_perc_hr = float(temp[0])

                if (Providers, top, locs, reqs) not in Results.keys():
                    Results[Providers, top, locs, reqs] = dict()

                Results[Providers, top, locs, reqs]['total_profit'] = total_profit
                Results[Providers, top, locs, reqs]['total_profit_hr'] = total_profit_hr
                Results[Providers, top, locs, reqs]['serv_perc'] = serv_perc
                Results[Providers, top, locs, reqs]['serv_perc_hr'] = serv_perc_hr








I = [3, 5, 10]
T = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
L = [2, 3, 5]
R = [5, 10, 20, 30, 40, 50, 70, 100, 140]

for i in I:
    for l in L:

        reqs = []
        tot_prof = []
        serv_perc = []

        tot_prof_hr = []
        serv_perc_hr = []
        for r in R:
            temp_tot_prof = 0
            temp_tot_prof_hr = 0
            temp_serv_perc = 0
            temp_serv_perc_hr = 0
            counter = 0
            for t in T:
                if (i, t, l, r) in Results.keys():
                    counter += 1
                    temp_tot_prof += Results[i, t, l, r]['total_profit']
                    temp_tot_prof_hr += Results[i, t, l, r]['total_profit_hr']
                    temp_serv_perc += Results[i, t, l, r]['serv_perc']
                    temp_serv_perc_hr += Results[i, t, l, r]['serv_perc_hr']

            if counter != 0:
                reqs.append(r)

                tot_prof.append(temp_tot_prof/counter)
                serv_perc.append(temp_serv_perc / counter)

                tot_prof_hr.append(temp_tot_prof_hr / counter)
                serv_perc_hr.append(temp_serv_perc_hr / counter)

        if tot_prof == []:
            continue

        plt.rcParams.update({'font.size': 14})
        plt.rcParams.update({'axes.labelsize': 14})

        plt.plot(reqs, tot_prof, color='black', linestyle='solid', linewidth=3,
                 marker='x', markerfacecolor='red', markersize=10)

        counter = 0
        for ii,jj in zip(reqs,tot_prof):
            temp = int(round(serv_perc[counter]*100,2))
            plt.text(ii,jj+1000,f'{temp}'+'%',fontsize=12,color='black', ha='right', va='bottom')
            counter += 1

        plt.plot(reqs, tot_prof_hr, color='blue', linestyle=':', linewidth=3,
                 marker='o', markerfacecolor='blue', markersize=10)

        counter = 0
        for ii, jj in zip(reqs, tot_prof_hr):
            temp = int(round(serv_perc_hr[counter] * 100, 2))
            plt.text(ii, jj-1000, f'{temp}' + '%', fontsize=12, color='blue', ha='left', va='top')
            counter += 1


        plt.xlim(0, max(reqs))
        plt.grid()

        # naming the x axis
        plt.xlabel('Total # of requests')
        # naming the y axis
        plt.ylabel('Total profit ($/h)')

        # giving a title to my graph
        # plt.title('Total Profit, ' + str(i) + ' Providers, ' + str(l) + ' Locations')
        plt.legend(['Optimal allocation',  'Greedy algorithm'])
        plt.savefig('Total Profit, ' + str(i) + ' Providers, ' + str(l) + ' Locations', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close('all')
