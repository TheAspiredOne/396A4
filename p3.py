#Avery Tan and Canopus Tong

import random
import p1
import p2
import time
import sys
import matplotlib.pyplot as plt
import numpy as np


size=512 #dimensions of board


def make_buckets():
	'''
	creates a dictionary so that we can organize the data according to buckets
	of size 8
	returns a list containing all the buckets where the bucket with id=8 is 
	the bucket containing results from trails where the total stepcost is 
	between 1 and 8. Bucket with id=16 is the bucket with tot stepcost is between
	9 and 16
	'''
	index_to_values = dict()
	categories = list()
	for i in range(8,520,8):
		categories.append(i)
		index_to_values[i] = []
	return (categories,index_to_values)


def make_board():
	"""
	creates the game board according to the set size=512
	It also generates obstacles pseudorandomly

	returns a 2d python list representing the board
	"""
	column = []
	for i in range(size):
		row = []
		for j in range(size):
			randomness = random.randint(1,10)

			#roughly 20% of the board will be obstacles. I calculated this
			#from the sample board given in our assignment spec. It too had
			#about 20% of the baord being obstacles. 
			if randomness in [1,2]: 
				row.append('*')
			else:
				row.append('.')
		column.append(row)
	return column


def get_init_start_goal(grid):
	'''
	Gets a random start and goal state. If by chance we initialize on a tile
	occupied by an obstacle, then we generate a different random start/goal
	until this is no longer the case.
	'''
	exp_start = (random.randint(0,size-1),random.randint(0,size-1))
	while grid[exp_start[1]][exp_start[0]] == '*':
		exp_start = (random.randint(0,size-1),random.randint(0,size-1))

	exp_goal = (random.randint(0,size-1),random.randint(0,size-1))
	while grid[exp_start[1]][exp_start[0]] == '*':
		exp_goal = (random.randint(0,size-1),random.randint(0,size-1))


	return (exp_start,exp_goal)


def plot():
		
	coorXmanhattan=np.load("coorXmanhattan.npy")
	coorYOpenCloseRatiomanhattan=np.load("coorYOpenCloseRatiomanhattan.npy")
	sd_err_ratiomanhattan=np.load("sd_err_ratiomanhattan.npy")
	coorYtimemanhattan=np.load("coorYtimemanhattan.npy")
	sd_timemanhattan=np.load("sd_timemanhattan.npy")

	coorXzero=np.load("coorXzero.npy")
	coorYOpenCloseRatiozero=np.load("coorYOpenCloseRatiozero.npy")
	sd_err_ratiozero=np.load("sd_err_ratiozero.npy")
	coorYtimezero=np.load("coorYtimezero.npy")
	sd_timezero=np.load("sd_timezero.npy")

	n='\n'
	# print(sd_timemanhattan, len)
	# print(len(coorXzero),len(coorYOpenCloseRatiozero),len(sd_err_ratiozero),len(coorYtimezero),len(sd_timezero))
	plt.xlabel('Buckets')
	plt.ylabel('Open/Close ratio')
	# plt.ylabel('Runtime/s')
	plt.title('The ratio of Open/Close of lazy-A*')
	# plt.title('Runtime of lazy-A*')
	plt.xlim([0,512])
	# plt.errorbar(coorXzero,coorYtimezero,sd_timezero, label="No heuristic")
	# plt.errorbar(coorXmanhattan,coorYtimemanhattan,sd_timemanhattan,label="Manhattan Distance heuristic")
	plt.errorbar(coorXmanhattan,coorYOpenCloseRatiomanhattan,sd_err_ratiomanhattan, label = 'Manhattan Distance heuristic')
	plt.errorbar(coorXzero,coorYOpenCloseRatiozero,sd_err_ratiozero, label = "No heuristic")
	plt.legend()
	plt.show()



def plotdata():
	f = open('results_H', 'r') #open our manhattan heuristics results
	g = open('results_0', 'r') #open our no heuristics implementation results
	

	#read each result, adding their values to the sum being tracked by bucket_values
	#we will also store the entire result in our raw_results list for SD calculation later
	plot_mapper = {'manhattan':f, "zero":g}
	data={}#store the result of each run with manhattan heuristics and no heuristics
	for unt in plot_mapper:

		#these lists store our coordinates for plotting
		coorX = list() #will be all the bucket ids.
		coorYOpenCloseRatio=list() #Y coordinates for Open/Closed ratio
		coorYtime = list() #Y coordinates for runtime


		bucket_values=dict()
		raw_results=dict()
		for i in range(8,520,8):
			bucket_values[i] = [0,0,0,0,0]#store additions of Open,Closed,OpenCloseCounter,stepcost, time
			raw_results[i]=[] #will store original raw results used to calculate standard deviation later



		for line in plot_mapper[unt]:
			res = line.split()
			if res[1]=='-1':#it a trivial result
				continue
			else:
				bucket_id = int(res[0])
				step_size = int(res[1])
				Open = int(res[2])
				Closed = int(res[3])
				time = float(res[4])

				bucket_values[bucket_id][0]+=Open
				bucket_values[bucket_id][1]+=Closed
				bucket_values[bucket_id][2]+=1
				bucket_values[bucket_id][3]+=step_size
				bucket_values[bucket_id][4]+=time
				raw_results[bucket_id].append(res)


		
		#calculate avg by divided all values in bucket_values by the counter
		for i in range(8,520,8):
			
			bucket_values[i][0]/=bucket_values[i][2]
			bucket_values[i][1]/=bucket_values[i][2]
			bucket_values[i][3]/=bucket_values[i][2]
			bucket_values[i][4]/=bucket_values[i][2]

			OpenCloseRatio = bucket_values[i][0]/bucket_values[i][1] #calculate Open/Closed ratio
			
			#add respective values to their list of x and y coordinates
			coorYOpenCloseRatio.append(OpenCloseRatio)
			coorYtime.append(bucket_values[i][4])
			coorX.append(i)

		#calculating standard deviation	
		sd_ratio = dict()
		sd_time = dict()
		for i in range(8,520,8):

			avg_ratio = bucket_values[i][0]/bucket_values[i][1]#Open/Closed ratio
			numerator_ratio = 0
			ratio_count = 0

			avg_time = bucket_values[i][4]
			numerator_time=0
			time_count=0

			for j in raw_results[i]:
				raw_ratio = float(j[2])/float(j[3])
				numerator_ratio += ((abs(raw_ratio- avg_ratio ))**2)
				ratio_count+=1

				numerator_time += ((abs(float(j[4])-avg_time))**2)
				time_count+=1

			sd_ratio[i]=(numerator_ratio/ratio_count)**(0.5)
			sd_time[i]=(numerator_time/time_count)**(0.5)

		#SD for the Open/Closed ratio and time lists which will be used in the plotting step
		sd_err_ratio=[]
		sd_err_time = []
		for i in range(8,520,8):
			sd_err_ratio.append(sd_ratio[i])
			sd_err_time.append(sd_time[i])

		coorX=np.asarray(coorX)
		coorYOpenCloseRatio=np.asarray(coorYOpenCloseRatio)
		sd_err_ratio=np.asarray(sd_err_ratio)
		coorYtime=np.asarray(coorYtime)
		sd_err_time=np.asarray(sd_err_time)
		print(sd_err_time, type(sd_err_ratio))

		np.save("coorX"+unt,coorX)
		np.save("coorYOpenCloseRatio"+unt,coorYOpenCloseRatio)
		np.save("sd_err_ratio"+unt,sd_err_ratio)
		np.save("coorYtime"+unt,coorYtime)
		np.save("sd_time"+unt,sd_err_time)

		data[unt]=(coorX, coorYOpenCloseRatio, sd_err_ratio, coorYtime, sd_time)

	f.close()
	g.close()
	plot()
	


if __name__ == '__main__':
	categories, index_to_values = make_buckets()
	categories,index_to_values_0=make_buckets()
	f = open('results_H','w') #where we will write our results into before final processing
	g = open('results_0', 'w')
	for i in range(100): #for 100 boards
		print('Processing board ',i,'\n')
		board = make_board() #generate a random 512x512 board
		board_astar = p1.read(board) #convert it to be readable by our A* algorithm
		for j in range(20): #for 20 different pseudorandom start,goal states,
			print('Processing trial ', j)
			start, goal = get_init_start_goal(board)

			#perform A* with manhattan distance heuristic
			starting_time = time.time()
			result = p2.a_star(start, goal, board_astar, 'M')
			end_time = time.time()
			delta_time = abs(starting_time-end_time)
			result=result.split()

			#perform A* with no heuristic
			starting_time_0 = time.time()
			result_0 = p2.a_star(start,goal,board_astar,'0')
			end_time_0=time.time()
			delta_time_0=abs(starting_time_0- end_time_0)
			result_0=result_0.split()

			#categorize data point for manhattan distance heuristic
			for k in categories:
				if int(result[1]) <= k:
					index_to_values[k].append((result[1],result[2],result[3],delta_time))
					break

			#categorize data point for A* using no heuristic
			for k in categories:
				if int(result_0[1]) <= k:
					index_to_values_0[k].append((result_0[1],result_0[2],result_0[3],delta_time))
					break


	#write the req results into our files for manhattan distance heuristics and no heuristics respectively
	for i in range(8,520,8):

		for k in index_to_values[i]:
			tot_timestep=k[0]
			Open = k[1]
			Closed = k[2]
			delta_time = k[3]
			n=' '
			string = str(i)+n+str(tot_timestep)+n+str(Open)+n+str(Closed)+n+str(delta_time)+'\n'
			f.write(string)

		for l in index_to_values_0[i]:
			tot_timestep=l[0]
			Open = l[1]
			Closed = l[2]
			delta_time = l[3]
			n=' '
			string = str(i)+n+str(tot_timestep)+n+str(Open)+n+str(Closed)+n+str(delta_time)+'\n'
			g.write(string)

	g.close()
	f.close()
	plotdata()

		






