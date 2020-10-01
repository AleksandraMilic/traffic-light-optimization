# -*- coding: utf-8 -*-
"""
Python code of Gravitational Search Algorithm (GSA)
Reference: Rashedi, Esmat, Hossein Nezamabadi-Pour, and Saeid Saryazdi. "GSA: a gravitational search algorithm." 
Information sciences 179.13 (2009): 2232-2248.	
Coded by: Mukesh Saraswat (saraswatmukesh@gmail.com), Himanshu Mittal (emailid: himanshu.mittal224@gmail.com) and Raju Pal (emailid: raju3131.pal@gmail.com)
The code template used is similar given at link: https://github.com/7ossam81/EvoloPy and matlab version of GSA at mathworks.

Purpose: Main file of Gravitational Search Algorithm(GSA) 
            for minimizing of the Objective Function

Code compatible:
-- Python: 2.* or 3.*
"""

import random
import numpy
import math
from solution import solution
import time
import massCalculation
import gConstant
import gField
import move
import benchmarks

import random
import fitness

def Y(traffic_data,lanes):
    y_list = []
    for phase in lanes:
        yj_list = []
        y = 0
        for i in phase:
            s = traffic_data[i][0]
            q = traffic_data[i][1]
            y += q/s
            # #print(y)
            yj_list.append(y)
        yj = max(yj_list)
        # #print(yj)
        y_list.append(yj)
        


    return y_list



def Initialization(F,PopSize,dim,test):
    pos=numpy.zeros((PopSize,dim))
    traffic_data = benchmarks.getTrafficData(F,test)
    lanes = benchmarks.distributionOfLanes(F,test)
    y_list = Y(traffic_data,lanes)

    if test == 41 or test == 42:
        # #print('test',test)

        for i in range(len(pos)):
            C = random.randint(54,120)
            
            L = 2*6 + 7 #19
            C1 = C - L
            g_list = []
            pos[i,0] = C
            C -= 7+5

            for j in range(F):
                if j == F-1:
                    g = C1 - sum(g_list)
                else:
                    if j == 0:
                        g = int(y_list[j]/sum(y_list) * C1) + 5
                        # #print('5',g)
                    # elif j == 1:
                    #     g = int(y_list[j]/sum(y_list) * C1) + 6
                    elif j == 2:
                        g = int(y_list[j]/sum(y_list) * C1) + 7
                        # #print('7',g)
                    else:
                        g = int(y_list[j]/sum(y_list) * C1) # ogranicenja????
                        
                g_list.append(g)        
                pos[i,j+1] = g
            # #print('C,g_list',C,g_list)

                
                


    else:
        for i in range(len(pos)):
            if F == 2:
                L = 10
                C = random.randint(30,120)
            elif F == 3:
                L = 12
                C = random.randint(33,120)
            elif F == 4:
                L = 14
                C = random.randint(42,120)
            elif F == 5:
                L = 16
                C = random.randint(51,120)
            elif F == 6:
                L = 18
                C = random.randint(60,120)

            
            C1 = C - L
            g_list = []
            pos[i,0] = C

            for j in range(F):
                if j == F-1:
                    g = C1 - sum(g_list)
                else:
                    g = int(y_list[j]/sum(y_list) * C1) # ogranicenja????

                g_list.append(g)        
                pos[i,j+1] = g

    # #print('pos',pos)
    return pos
        


        
    







        
# def GSA(objf,lb,ub,dim,PopSize,iters,F):
def GSA(objf,dim,PopSize,iters,F,trafficdata,QQ,test): # QQ = [[0,0],[0,0]...]
    # GSA parameters
    ElitistCheck =1
    Rpower = 1 

    s=solution()
        
    """ Initializations """
    
    vel = numpy.zeros((PopSize,dim))
    fit = numpy.zeros(PopSize)
    M = numpy.zeros(PopSize)
    gBest = numpy.zeros(dim)
    gBestScore = float("inf")
    
    # pos=numpy.random.uniform(0,1,(PopSize,dim)) * (ub-lb)+lb
    
    pos = Initialization(F, PopSize, dim, test)
    Qb_list = []
    Q = []
    X_list = []
    # #print(pos)

    convergence_curve=numpy.zeros(iters)
    
    #print("GSA is optimizing  \""+objf.__name__+"\"")  
    # #print('pos', pos)
    
    timerStart=time.time() 
    s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    
    for l in range(0,iters):
        ############ INICIJALIZACIJA NA POCETKU SVAKE POPULACIJE
        if l!=0:
            pos = Initialization(F, PopSize, dim, test)
        # print('pos',pos)

        for i in range(0,PopSize):
            # l1 = [None] * dim
            # for j in range(F):
                # l1=numpy.clip(pos[i,j], lb[j], ub[j])
            
            
            # pos[i,:]=l1
            l1 = pos[i,:] 
            # #print('l1', l1)
            #Calculate objective function for each particle
            # fitness=[]
            fitness,Q1,Qb,X=objf(l1,trafficdata,QQ, test)
            # #print('fitness,l1', fitness,l1)
            fit[i]=fitness
            Q.append(Q1)
            Qb_list.append(Qb)
            X_list.append(X)

            
            # #print('fitness', fitness)
    
                
            if(gBestScore>fitness):
                # #print("pass")
                gBestScore=fitness
                gBest = []
                for i in range(dim):
                    gBest.append(l1[i])  
                s.best = gBestScore
                s.bestIndividual = gBest

                k=[gBestScore,gBest]
                # #print('--------gBestScore,gBest',k)
                Qb_best = Qb[:]
                Q_b = Q1[:]
                X_best = X[:]

            # #print('gBestScore,gBest',gBestScore,gBest)
        
        # #print(['At iteration '+ str(l+1)+ ' the best fitness is '+ str(s.best) + str(s.bestIndividual)])
        """ Calculating Mass """
        M = massCalculation.massCalculation(fit,PopSize,M)

        """ Calculating Gravitational Constant """        
        G = gConstant.gConstant(l,iters)        
        
        """ Calculating Gfield """        
        acc = gField.gField(PopSize,dim,pos,M,l,iters,G,ElitistCheck,Rpower)
        
        """ Calculating Position """        
        pos, vel = move.move(PopSize,dim,pos,vel,acc,test)
        
        convergence_curve[l]=gBestScore
        # #print('convergence_curve',convergence_curve)
        # #print('pos',pos)
        if (l%1==0):
            print(['At iteration '+ str(l+1)+ ' the best fitness is '+ str(s.best) + str(s.bestIndividual)])
    
    
    timerEnd=time.time()  
    s.endTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime=timerEnd-timerStart
    s.convergence=convergence_curve
    s.Algorithm="GSA"
    s.objectivefunc=objf.__name__
    s.best = gBestScore
    s.bestIndividual = gBest
    s.Qb = Qb_best
    s.Q = Q_b
    s.X_ = X_best
    #print('The best fitness is '+ str(s.best) + str(s.bestIndividual))
    # #print('solution: ' + str(gBest))
    # #print(k)


    return s

if __name__ == "__main__":
    import traffic_data
    PopSize = 20
    iters = 10

    F=5
    dim=F+1
    ##period analysis 1
    test = 31
    Q = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    
    trafficdata = traffic_data.extractTrafficData(F,test)
    # #print(trafficdata1)
    
    solution1 = GSA(fitness.FitnessFunction,dim,PopSize,iters,F,trafficdata,Q,test)