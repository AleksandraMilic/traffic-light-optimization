import pyodbc
#--------EXTRACT DATA-----------
def extractTrafficData(F,test):
	"""return traffic data:
	traffic flow name
	saturation flow (s)
	average arrival rate (q)

	for defined phase F"""
	list_q = []
	list_s  = []
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

	########## real intersection
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

	# print(conn)
	# elif test==2:
    # elif test==3:
    # elif test==4:
	cursor = conn.cursor()
	cursor.execute(command1)

	for row in cursor.fetchall():
		list_q.append(row[0])

	# print(list_q)

	
	cursor.execute(command2)
	for row in cursor.fetchall():
		list_s.append(row)

	traffic_data = []
	for i, j in zip(list_s,list_q):
		traffic_data.append([i[0], i[1], j, i[2]])


	return traffic_data


