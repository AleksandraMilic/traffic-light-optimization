# -*- coding: utf-8 -*-
"""
Python code of Gravitational Search Algorithm (GSA)
Reference: Rashedi, Esmat, Hossein Nezamabadi-Pour, and Saeid Saryazdi. "GSA: a gravitational search algorithm." 
Information sciences 179.13 (2009): 2232-2248.	

Coded by: Mukesh Saraswat (saraswatmukesh@gmail.com), Himanshu Mittal (emailid: himanshu.mittal224@gmail.com) and Raju Pal (emailid: raju3131.pal@gmail.com)
The code template used is similar given at link: https://github.com/7ossam81/EvoloPy and matlab version of GSA at mathworks.

-- Purpose: Defining the benchmark function code 
and its parameters: function Name, lowerbound, upperbound, dimensions

Code compatible:
-- Python: 2.* or 3.*
"""

import numpy
import math
import pyodbc


    
def F1(x):
	""" Spere Function """
	s=numpy.sum(x**2)
	return s

def getFunctionDetails(a):
# [name, lb, ub, dim]
	param = {  0: ["F1",-100,100,3],
            }
	return param.get(a, "nothing")

# ----------------
from math import sqrt

def c_func(s_list,solution):
	"""returns list of traffic flow capacity"""
	c_list = []
	C = solution[0]
	g_list = solution[1:]
	for s,g in zip(s_list,g_list):
		c = s/(g/C)
		c_list.append(c)
	
	return c_list


def X(q_list, c_list, solution):
	"""returns the ratio of average number of arrivals/cycle to the maximum
	number of departures/cycle """
	X_list = []
	C = solution[0]
	g_list = solution[1:]
	for q,c in zip(q_list,c_list):
		X = q/c
		X_list.append(X)
		

	return(X_list)

def d(X_list, T, solution):
	"""returns the average delay to a pcu on the approach """
	d_list = []
	C = solution[0]
	g_list = solution[1:]
	for g,X in zip(g_list, X_list):
		
		d1 = (0.5 * C * ((1 - g/C)**2)) / (1 - (min(1,X)*(g/C)))
		d2 = 900 * T *((X-1) + sqrt((X-1)**2 + (4*X)/(c*T) ))

		d = d1+d2
		d_list.append(d)

	return(d_list)

def F2(s_list,X_list,T,solution):
	"""returns """
	C = solution[0]
	g_list = solution[1:]
	d_list = d(X_list, T, solution)
	D = sum([q*d for q, d in zip(q_list, d_list)]) / sum(q_list)
	
	return D





def getTrafficData(F,test):
    """parameter: number of phases
    returns traffic data: traffic flow name, flow saturation, flow value"""
    traffic_data = {}
    list_q = []
    list_s = []

    # conn = 0
    # command1=0
    # command2=0
    # print(test)
    if test == 1:
        conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\\trafic-light-optimization\\database.accdb;')
        command1 = 'select traffic_flow_value from test1_1'
        command2 = 'select traffic_flow_name, saturation_flow_rate, green_light from test1_2 \
        where phase = ' + str(F)
    elif test == 21:
        conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\\trafic-light-optimization\\Database2.accdb;')
        command1 = 'select traffic_flow_value from test2_b1'
        command2 = 'select traffic_flow_name, saturation_flow_rate, green_light from test2__b1 \
        where phase = ' + str(F)
    elif test == 22:
        conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\\trafic-light-optimization\\Database2.accdb;')
        command1 = 'select traffic_flow_value from test2_b2'
        command2 = 'select traffic_flow_name, saturation_flow_rate, green_light from test2__b2 \
        where phase = ' + str(F)
    elif test == 31:
        conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\\trafic-light-optimization\\Database3.accdb;')
        command1 = 'select traffic_flow_value from test3_b1'
        command2 = 'select traffic_flow_name, saturation_flow_rate, green_light from test3__b1 \
        where phase = ' + str(F)
    elif test == 32:
        conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\\trafic-light-optimization\\Database3.accdb;')
        command1 = 'select traffic_flow_value from test3_b2'
        command2 = 'select traffic_flow_name, saturation_flow_rate, green_light from test3__b2 \
        where phase = ' + str(F)
    elif test == 41:
        conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\\trafic-light-optimization\\Database4.accdb;')
        command1 = 'select traffic_flow_value from test4_b1'
        command2 = 'select traffic_flow_name, saturation_flow_rate, green_light from test4__b2 \
        where phase = ' + str(F)
    elif test == 42:	
        conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\\trafic-light-optimization\\Database4.accdb;')
        command1 = 'select traffic_flow_value from test4_b2'
        command2 = 'select traffic_flow_name, saturation_flow_rate, green_light from test4__b2 \
        where phase = ' + str(F)


    cursor = conn.cursor()
    cursor.execute(command1)

    for row in cursor.fetchall():
        list_q.append(row[0])

    # print(list_q)


    cursor.execute(command2)
    for row in cursor.fetchall():
        list_s.append(row)


    for i, j in zip(list_s,list_q):
        traffic_data[i[0]] = [i[1],j]


    # print(traffic_data)


    return traffic_data

def distributionOfLanes(F,test):
	"""parameter: number of phases
	distribution of lanes by phases"""
	if test == 41 or test == 42:
		lanes = [('C','H'),('D','L'),('A','B'),('A','G','F','E'),('G','F','E')]


	else:
		if F == 2:
			lanes = [('A','B','C','D','E','F'), ('G','H','L','M','R','T')]
		elif F == 3:
			lanes = [('A','B','C','D','E','F'), ('H','L','M','R'), ('G','T')]
		elif F == 4:
			lanes = [('A','B','E','F'), ('C','D'), ('H','L','M','R'), ('G','T')]
		elif F == 5:
			lanes = [('A','B','E','F'), ('C','D'), ('R','H'), ('L','M'),('R','T')]
		elif F == 6:
			lanes = [('B','E'), ('A','F'), ('C','D'), ('R','H'), ('L','M'),('R','T')]

	return lanes



    ########## real intersection
    # elif test == 41:
    #     conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\\trafic-light-optimization\\Database4.accdb;')
    #     command1 = 'select traffic_flow_value from test4_b1'
    #     command2 = 'select traffic_flow_name, saturation_flow_rate, green_light from test4__b2 \
    #     where phase = ' + str(F)
    # elif test == 42:	
    #     conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\\trafic-light-optimization\\Database4.accdb;')
    #     command1 = 'select traffic_flow_value from test4_b2'
    #     command2 = 'select traffic_flow_name, saturation_flow_rate, green_light from test4__b2 \
    #     where phase = ' + str(F)

    