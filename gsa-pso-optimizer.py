"""
Kod testiranja u 3. scenariju period analize b=1 se u potpunosti, sa svim
ulaznim i izlaznim podacima, poklapa sa periodom analize b=1 u test scenariju 2. 
"""

import GSA as gsa
import PSO
import fitness
import numpy
import time
import csv
import traffic_data


def gsa_opt(F,PopSize,dim,iters,test,Q,trafficdata):

    Export=True
    #ExportToFile="YourResultsAreHere.csv"
    #Automaticly generated name by date and time
    ExportToFile="gsa test "+str(test)+time.strftime("%Y-%m-%d-%H-%M-%S")+".csv" 

    # Check if it works at least once
    atLeastOneIteration=False 


    # CSV Header for for the cinvergence 
    CnvgHeader=[]

    for l in range(0,iters):
        CnvgHeader.append("Iter"+str(l+1))


    solution=gsa.GSA(fitness.FitnessFunction,dim,PopSize,iters,F,trafficdata,Q,test)
    if(Export==True):
        with open(ExportToFile, 'a') as out:
            writer = csv.writer(out,delimiter=',')
            if (atLeastOneIteration==False): # just one time to write the header of the CSV file
                header= numpy.concatenate([['phase'+str(F),'test'+str(test)],["Optimizer","objfname","startTime","EndTime","ExecutionTime"],CnvgHeader,["BestFitness","BestIndividual"],['X','Q']])
                writer.writerow(header)
            a=numpy.concatenate([["-","-"],[solution.Algorithm,solution.objectivefunc,solution.startTime,solution.endTime,solution.executionTime],solution.convergence,[solution.best,solution.bestIndividual],solution.X_,solution.Q])
            writer.writerow(a)
        out.close()
    atLeastOneIteration=True # at least one experiment

    if (atLeastOneIteration==False): # Faild to run at least one experiment
        print("No Optomizer or Cost function is selected. Check lists of available optimizers and cost functions") 

    return(solution)


def pso_opt(F,PopSize,dim,iters,test,Q,trafficdata):

    Export=True
    #ExportToFile="YourResultsAreHere.csv"
    #Automaticly generated name by date and time
    ExportToFile="pso test "+str(test)+time.strftime("%Y-%m-%d-%H-%M-%S")+".csv" 

    # Check if it works at least once
    atLeastOneIteration=False 


    # CSV Header for for the cinvergence 
    CnvgHeader=[]

    for l in range(0,iters):
        CnvgHeader.append("Iter"+str(l+1))


    solution=PSO.PSO(fitness.FitnessFunction, PopSize, dim, iters, F, trafficdata, Q, test, verbose=True)
    if(Export==True):
        with open(ExportToFile, 'a') as out:
            writer = csv.writer(out,delimiter=',')
            if (atLeastOneIteration==False): # just one time to write the header of the CSV file
                header = numpy.concatenate([['phase'+str(F),'test'+str(test)],["Optimizer","objfname"],CnvgHeader,["BestFitness","BestIndividual",'X','Q']])
                writer.writerow(header)
            a=numpy.concatenate([["-","-"],['PSO','FitnessFunction'],solution.convergence_curve,[solution.err_best_g,solution.pos_best_g,solution.X_,solution.QbQ1]])
            writer.writerow(a)
        out.close()
    atLeastOneIteration=True # at least one experiment

    if (atLeastOneIteration==False): # Faild to run at least one experiment
        print("No Optomizer or Cost function is selected. Check lists of available optimizers and cost functions") 

    return(solution)

################--------------------------------------------------------------------

if __name__=="__main__":
    PopSize=100
    iters=50
    
    test = 1
    for F in range(2,7):
        dim=F+1
        Q = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        
        trafficdata = traffic_data.extractTrafficData(F,test)
        # print(trafficdata1)
        
        solution1 = gsa_opt(F,PopSize,dim,iters,test,Q,trafficdata)
        solution2 = pso_opt(F,PopSize,dim,iters,test,Q,trafficdata)

    
    #### test 2
    ##period analysis 1
    for F in range(2,7):
        test = 21
        dim=F+1
        Q = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        
        trafficdata = traffic_data.extractTrafficData(F,test)
        # print(trafficdata1)
        
        solution1 = gsa_opt(F,PopSize,dim,iters,test,Q,trafficdata)
        solution2 = pso_opt(F,PopSize,dim,iters,test,Q,trafficdata)
    ##period analysis 2
        test = 22
        Qb1 = []
        Qb2 = []
        
        for i in solution1.Qb:
            Qb1.append([i[1],i[0]])
        
        for i in solution2.Q:
            Qb2.append([i[1],i[0]])
        trafficdata = traffic_data.extractTrafficData(F,test)
        # print(trafficdata1)
        
        solution1 = gsa_opt(F,PopSize,dim,iters,test,Qb1,trafficdata)
        solution2 = pso_opt(F,PopSize,dim,iters,test,Qb2,trafficdata)
    



    #### test 3
    ##period analysis 1
    for F in range(2,7):
        test = 31
        dim=F+1
        Q = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        
        trafficdata = traffic_data.extractTrafficData(F,test)
        # print(trafficdata1)
        
        solution1 = gsa_opt(F,PopSize,dim,iters,test,Q,trafficdata)
        solution2 = pso_opt(F,PopSize,dim,iters,test,Q,trafficdata)
    ##period analysis 2
        test = 32
        Qb1 = []
        Qb2 = []
        
        for i in solution1.Qb:
            Qb1.append([i[1],i[0]])
        
        for i in solution2.Q:
            Qb2.append([i[1],i[0]])
        trafficdata = traffic_data.extractTrafficData(F,test)
        # print(trafficdata1)
        
        solution1 = gsa_opt(F,PopSize,dim,iters,test,Qb1,trafficdata)
        solution2 = pso_opt(F,PopSize,dim,iters,test,Qb2,trafficdata)
    
    
    
    
    #### test 4
    F=5
    dim=F+1
    ##period analysis 1
    test = 41
    Q = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    
    trafficdata = traffic_data.extractTrafficData(F,test)
    # print(trafficdata1)
    
    solution1 = gsa_opt(F,PopSize,dim,iters,test,Q,trafficdata)
    solution2 = pso_opt(F,PopSize,dim,iters,test,Q,trafficdata)
    
    ##period analysis 2
    test = 42
    Qb1 = []
    Qb2 = []

    for i in solution1.Qb:
        Qb1.append([i[1],i[0]])

    for i in solution2.Q:
        Qb2.append([i[1],i[0]])
    trafficdata2 = traffic_data.extractTrafficData(F,test)
    
    objf=fitness.FitnessFunction(solution1.bestIndividual,trafficdata2,Qb1,test)
    objf2=fitness.FitnessFunction(solution2.pos_best_g,trafficdata2,Qb2,test)

    ExportToFile="gsa test "+str(test)+time.strftime("%Y-%m-%d-%H-%M-%S")+".csv" 
    with open(ExportToFile, 'a') as out:
        writer = csv.writer(out,delimiter=',')
        header= numpy.concatenate([['sum of all delays D'], ['Q'], ['Q list'], ['X list']])
        writer.writerow(header)
        x = objf[0]
        y = objf[1]
        z = objf[2]
        t = objf[3]
        a=numpy.concatenate([[x,y,z,t]])
        writer.writerow(a)
    out.close()
    
    ExportToFile="pso test "+str(test)+time.strftime("%Y-%m-%d-%H-%M-%S")+".csv" 
    with open(ExportToFile, 'a') as out:
        writer = csv.writer(out,delimiter=',')
        header= numpy.concatenate([['sum of all delays D'], ['Q'], ['Q list'], ['X list']])
        writer.writerow(header)
        x = objf2[0]
        y = objf2[1]
        z = objf2[2]
        t = objf2[3]
        a=numpy.concatenate([[x,y,z,t]])

        # a=numpy.concatenate([[i] for i in objf2])
        writer.writerow(a)
    out.close()






    #### period analysis 2
    # Qb2 = []
    # test2 = 22
    # for i in solution1.Qb:
    #     Qb2.append([i[1],i[0]])
    # trafficdata2 = traffic_data.extractTrafficData(F,test2)

    # solution2 = gsa_opt(F,PopSize,dim,iters,test2,Qb2,trafficdata2)
    





    # objf1=fitness.FitnessFunction([120,29,10,15,
    # 22,25],trafficdata1,Q)
    # print(objf1)
    # Qb2 = []
    # for i in objf1[2]:
    #     Qb2.append([i[1],i[0]])
    # test=42
    # trafficdata2 = traffic_data.extractTrafficData(F,test)
    # objf2=fitness.FitnessFunction([120,29,10,15,
    # 22,25],trafficdata2,Qb2)
    # print(objf2)


    # objf1=fitness.FitnessFunction([120,37,7,36,
    # 12,12],trafficdata,Q)120.0, 21.0, 8.0, 13.0, 37.0, 23.0


    # objf1=fitness.FitnessFunction([119,33,12,7,
    # 28,10,11 ],trafficdata,Q)
    # objf1=fitness.FitnessFunction([120.0, 55.510555851850455, 54.48944414814955],trafficdata,Q)
    # print(objf1)





    # Qb2 = []
    # for i in objf1[2]:
    #     Qb2.append([i[1],i[0]])
    # # print(Qb2)
    # test=32
    # test=22
    # trafficdata = traffic_data.extractTrafficData(F,test)

    # objf2=fitness.FitnessFunction([118,23,16,7,
    # 27,15,12],trafficdata,Qb2)


    # objf2=fitness.FitnessFunction([120,34,7,38,11,14],trafficdata,Qb2)

    # objf2=fitness.FitnessFunction([120,30,8,33,
    # 17,16],trafficdata,Qb2)



# print(objf2)



