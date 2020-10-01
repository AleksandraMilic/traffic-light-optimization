from math import sqrt
# from traffic-data import extractTrafficData


def c_func(test,s_list,signals,green_light,lanes_list):
	"""returns list of traffic flow capacity"""
	c_list = []
	C = signals[0]
	# g_list = signals[1:]
	
	for s,i,lane in zip(s_list,green_light,lanes_list):
		
		g = signals[i]
		#print('g, i',g,i)
		
		if test == 41 or test == 42:
			if lane == "A":
				g3 = signals[3]
				g += g3
			elif lane == "B":
				g-=7 #77777777
			elif lane == "D":
				g += 6
			elif lane == "E":
				g5 = signals[5]
				g += g5
			elif lane == "F":
				g5 = signals[5]
				g += g5
			elif lane == "G":
				g5 = signals[5]
				g += g5
			elif lane == "H":
				g -= 5

		
		c = s*(g/C)
		# c = round(c)
		# ##print(c)
		c_list.append(c)
	# print('s,g,C,c',s,g,C,c)

	return c_list


def X(q_list, c_list, test):
	"""returns the ratio of average number of arrivals/cycle to the maximum
	number of departures/cycle """
	X_list = []
	# C = signals[0]
	# g_list = signals[1:]
	for q,c in zip(q_list,c_list):
		##print('q,c',q,c)
		X = q/c
		if test == 41:
			X = round(X,2)
		if test == 42:
			X = round(X,2)
		# print('q,c,X',q,c,X)
		
		X_list.append(X)
		

	return(X_list)





def d(X_list, T, signals, c_list, green_light,Q, lanes_list,test):
	"""returns the average delay to a pcu on the approach """
	d_list = []
	C = signals[0]
	
	# for X, Qb in zip(X_list, Q):
	# 	if X <= 1 and Qb[0] == 0:
	# 		case = "1"
	# 	elif X > 1 and Qb[0] == 0:
	# 		case = "2"
	# 	elif X <= 1 and Qb[0] > 0:
	# 		case = "3,4"
	# 	elif X > 1 and Qb[0] > 0:
	# 		case = "5"
	
	# g_list = signals[1:]
	for i,X,c,Qb,lane in zip(green_light, X_list, c_list, Q, lanes_list):
		# ##print('X',X)
		g = signals[i]
		if test == 41 or test == 42:
			if lane == "A":
				g4 = signals[3]
				g += g4 
			elif lane == "B":
				g-=7
			elif lane == "D":
				g += 6
			elif lane == "E":
				g5 = signals[4]
				g += g5
			elif lane == "F":
				g5 = signals[4]
				g += g5
			elif lane == "G":
				g5 = signals[4]
				g += g5
			elif lane == "H":
				g -= 5

		d2 = 900 * T *((X-1) + sqrt((X-1)**2 + (4*X)/(c*T) ))
		
		##### unsaturated flow #####
		'''
		if X <= 1:
			# ##print("111111111111111")
			if X == 1:
				t = T
			else:
				t = min(T, Qb[0]/(c*(1-min(1,X))))		
			
			
			if t<T: 
				u = 0
			else: 

				u = 1 - (c*T*(1-min(1,X))/ Qb[0]) #u=1
				#zero division
				# ##print("u", u)
			d3 = (1800*Qb[0]*(1+u)*t)/c*T
			
			ds = 0.5 * C * (1 - g/C)
			du = 0.5 * C * (1 - g/C)**2  /  (1 - (min(1,X)*(g/C))) #  du=d1
			
			if u == 0:
				d1 = ds * t/T + du * ((T-t)/T)
			else:
				d1 = ds
		##### saturated flow #####
		else:
			# ##print("222222222222222")
			t = T 
			u = 1
			d3 = (1800*Qb[0]*(1+u)*t)/c*T
			d1 = 0.5 * C * (1 - g/C)
			# ##print(d1)



		'''
		if X <= 1 and Qb[0] == 0:
			#print("case 1")
			d1 = 0.5 * C * (1 - g/C)**2  /  (1 - (min(1,X)*(g/C)))
			d3 = 0
			t = 0
			u = 0
		
		elif X > 1 and Qb[0] == 0:
			#print("case 2")
			d1 = 0.5 * C * (1 - g/C)**2  /  (1 - (min(1,X)*(g/C)))
			d3 = 0
			t = 0
			u = 0
		
		##### saturated flow #####
		
		elif X <= 1 and Qb[0] > 0:

			if X == 1:
				t = T
			else:
				t = min(T, Qb[0]/(c*(1-min(1,X))))		
			
			
			if t<T: #case 3
				#print("case 3")
				u = 0
			else: #case 4
				#print("case 4")
				# u ??
				u = 1 - (c*T*(1-min(1,X))/ Qb[0]) #u=1
				

			d3 = (1800*Qb[0]*(1+u)*t)/c*T
			
			ds = 0.5 * C * (1 - g/C)
			du = 0.5 * C * (1 - g/C)**2  /  (1 - (min(1,X)*(g/C))) # du=d1
			d1 = ds * t/T + du * ((T-t)/T)
		


		elif X > 1 and Qb[0] > 0:
			#print("case 5")
			t = T		
			u = 1	

			d3 = (1800*Qb[0]*(1+u)*t)/c*T
			
			ds = 0.5 * C * (1 - g/C)
			du = 0.5 * C * (1 - g/C)**2  /  (1 - (min(1,X)*(g/C))) # du=d1
			d1 = ds * t/T + du * ((T-t)/T)
		
		
		#####
		
		d = d1+d2+d3
		# print(d1,d2,d3)
		d_list.append(d)
	# ##print(d_list)
	return(d_list)





def GetNewQ(Q,c_list,X_list,T): # Q = [[0,10],[0,0]...za svaku traku - 12] 
	# for i,c,q in zip(Q,c_list,q_list):
	for i,c,X in zip(Q,c_list,X_list):
		c1 = round(c)
		Qnew = max(0,i[0] + round(c*T*(X-1)))
		# Qnew = max(0,i[0] + round(c1*T*(round(q/c1,2)-1)))
		# Qnew = max(0,i[0] + q-c1)
		i[1] = Qnew

	return Q






def FitnessFunction(signals,trafficdata,Q,test):
	"""returns sum of all delays
	Q sum, Q list, X list"""
	# trafficdata = list(trafficdata)
	# ##print(trafficdata)
	
	lanes_list = [i[0] for i in trafficdata]
	s_list = [i[1] for i in trafficdata]
	q_list = [i[2] for i in trafficdata]
	green_light = [i[3] for i in trafficdata]
	# ##print(green_light) #lista indeksa koji prikazuju odgovarajuce zeleno vreme za svaki saobracajni tok
	c_list = c_func(test,s_list, signals, green_light, lanes_list)
	X_list = X(q_list, c_list,test)
	C = signals[0]
	g_list = signals[1:]
	T = 1 #(hours)
	
	###broj neopsluzenih vozila
	Q = GetNewQ(Q,c_list,X_list,T)
	###
	
	d_list = d(X_list, T, signals, c_list, green_light, Q, lanes_list, test)
	qd = 0
	for q, d1 in zip(q_list, d_list):
		qd += q*d1
	# D = sum([q*d for q, d in zip(q_list, d_list)]) / sum(q_list)
	D = qd/sum(q_list)
	
	Qb = 0
	Qb_1 = 0
	
	for i in Q:
		Qb += i[0]
		Qb_1 += i[1]

	Q_sum = [Qb,Qb_1]

	return D,Q_sum,Q,X_list


	


# if __name__ == "__main__":
# 	#two phases
# 	F = 2
# 	L = 10
# 	trafficdata = tuple(extractTrafficData(F))
	##print(trafficdata)

# 	lb = [30, 7, 7]
# 	ub = [120, 80, 80]

# 	# s_list = [i[1] for i in trafficdata]
# 	# q_list = [i[2] for i in trafficdata]

	##print(s_list)

# 	d = FitnessFunction([45,14,25],trafficdata)
	# ##print(d)
	
# 	# signal_opt, fopt = pso(func=FitnessFunction, lb=lb, ub=ub, f_ieqcons=constraint, args=trafficdata)
	##print(signal_opt)
	##print(fopt)