import numpy as np
import pandas as pd
pd.set_option("display.precision", 3)
# M/M/s : FCFS/infi/infi
n = input("Enter the number of seconds for simulation: ")
n = float(n)

lamb = input("Enter lambda value: ")
lamb = int(lamb)

s = input('Enter number of servers: ')
s = int(s)

print('Enter mu value for all servers: ')
mus = []
for i in range(s):
	mu = input()
	mus.append(int(mu))

mus = np.array(mus)
# max. time for simulation
TMAX = n
# dictionary for selecting name of next event 
event_dict = {
	0: 'A',
	1: 'D',
	2: 'T',
}
time = 0
rows = []
# time of first arrival
x1 = np.random.exponential(1/lamb)
# array of flags denoting idleness of servers
STS_flag = np.array([1]*s)
CE = 'START'
NAT = x1
NDT = [TMAX+1]*s
CNA = 0
CND = 0
NS = 0
NQ = 0
CWTS = 0
CWTQ = 0
CIDT = np.array([0]*s)
IAT = x1
ST = ['-']*s
NET = x1
NE = 'A'
while True:
	combined = []
	for tup in zip(ST, NDT, STS_flag, CIDT):
		combined.extend([tup[0], tup[1], tup[2], tup[3]])
	if NAT < TMAX and min(NDT) >= TMAX:
		# arrival
		rows.append([time, CE, CNA, CND, NS, NQ, CWTS, CWTQ, IAT, NAT] + combined + [NET, NE])
		IAT = np.random.exponential(1/lamb)
		DT = NAT - time
		CWTS = CWTS + NS*DT
		CWTQ = CWTQ + NQ*DT
		CIDT = CIDT + STS_flag*DT
		NS += 1
		CNA += 1
		time = NAT
		NAT = time + IAT
		if np.sum(STS_flag) > 0:
			# select the idle server with largest service rate
			index = np.where(STS_flag == 1)[0]
			index_max = np.argmax(mus[index])
			index_max = index[index_max]
			mu = mus[index_max]
			# generate service time for this server
			ST[index_max] = np.random.exponential(1/mu)
			NDT[index_max] = time + ST[index_max]
			indices = np.where(STS_flag == 0)[0]
			for i in indices:
				ST[i] = '-'
			# set this server as busy
			STS_flag[index_max] = 0
		else:
			# if all servers are busy, add to queue
			NQ += 1
			indices = np.where(STS_flag == 0)[0]
			for i in indices:
				ST[i] = '-'

		# next event is the minimum of NAT, NDT and TMAX
		NET = min(NAT, min(NDT), TMAX)
		NE = event_dict[np.argmin([NAT, min(NDT), TMAX])]
		if NE == 'D':
			NE += str(np.argmin(NDT) + 1)
		CE = 'A'

	elif NAT < TMAX and min(NDT) < TMAX and min(NDT) >= NAT:
		# arrival
		rows.append([time, CE, CNA, CND, NS, NQ, CWTS, CWTQ, IAT, NAT] + combined + [NET, NE])
		IAT = np.random.exponential(1/lamb)
		DT = NAT - time
		CWTS = CWTS + NS*DT
		CWTQ = CWTQ + NQ*DT
		CIDT = CIDT + STS_flag*DT
		NS += 1
		CNA += 1
		time = NAT
		NAT = time + IAT
		if np.sum(STS_flag) > 0:
			# select the idle server with largest service rate
			index = np.where(STS_flag == 1)[0]
			index_max = np.argmax(mus[index])
			index_max = index[index_max]
			mu = mus[index_max]
			# generate service time for this server
			ST[index_max] = np.random.exponential(1/mu)
			NDT[index_max] = time + ST[index_max]
			indices = np.where(STS_flag == 0)[0]
			for i in indices:
				ST[i] = '-'
			# set this server as busy
			STS_flag[index_max] = 0
		else:
			# if all servers are busy, add to queue
			NQ += 1
			indices = np.where(STS_flag == 0)[0]
			for i in indices:
				ST[i] = '-'

		# next event is the minimum of NAT, NDT and TMAX
		NET = min(NAT, min(NDT), TMAX)
		NE = event_dict[np.argmin([NAT, min(NDT), TMAX])]
		if NE == 'D':
			NE += str(np.argmin(NDT) + 1)
		CE = 'A'

	elif (NAT < TMAX and min(NDT) < TMAX and min(NDT) < NAT) or (NAT >= TMAX and min(NDT) < TMAX):
		# departure
		rows.append([time, CE, CNA, CND, NS, NQ, CWTS, CWTQ, IAT, NAT] + combined + [NET, NE])
		DT = min(NDT) - time
		CWTS = CWTS + NS*DT
		CWTQ = CWTQ + NQ*DT
		CIDT = CIDT + STS_flag*DT
		NS -= 1
		CND += 1
		time = min(NDT)
		index = np.argmin(NDT)
		if NS >= s:
			# if s customers present after the departure, then remove one customer from queue and add to freed server
			NQ -= 1
			mu = mus[index]
			indices = np.where(STS_flag == 0)[0]
			for i in indices:
				ST[i] = '-'
			# generate service time for this customer
			ST[index] = np.random.exponential(1/mu)
			NDT[index] = time + ST[index]
		else:
			# else just mark the server freed as idle
			STS_flag[index] = 1
			NDT[index] = TMAX+1
			ST[index] = '-'
			indices = np.where(STS_flag == 0)[0]
			for i in indices:
				ST[i] = '-'

		# next event is the minimum of NAT, NDT and TMAX
		NET = min(NAT, min(NDT), TMAX)
		NE = event_dict[np.argmin([NAT, min(NDT), TMAX])]
		if NE == 'D':
			NE += str(np.argmin(NDT) + 1)
		CE = 'D' + str(index+1)
		IAT = '-'

	elif NAT >= TMAX and min(NDT) >= TMAX:
		# stop simulation
		rows.append([time, CE, CNA, CND, NS, NQ, CWTS, CWTQ, IAT, NAT] + combined + [NET, NE])
		DT = TMAX - time
		CWTS = CWTS + NS*DT
		CWTQ = CWTQ + NQ*DT
		CIDT = CIDT + STS_flag*DT
		L = CWTS/TMAX
		L_q = CWTQ/TMAX
		W = CWTS/CNA
		W_q = CWTQ/CNA
		repeating_columns = ['ST', 'NDT', 'STS', 'CIDT']*s
		data = pd.DataFrame(data=rows, columns=['Time','CE','CNA','CND','NS','NQ','CWTS','CWTQ','IAT','NAT'] + repeating_columns + ['NET','NE'])
		print("*************************************************************************************************************")
		print(data)
		print("*************************************************************************************************************")
		print('Average number of customers in system: ', L)
		print('Average number of customers in queue: ', L_q)
		print('Average waiting time in system: ', W)
		print('Average waiting time in queue: ', W_q)
		for i in range(s):
			print(f'Proportion of time, server {i+1} is idle: {CIDT[i]/TMAX}')
		break
