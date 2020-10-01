import random
import math
from GSA import Initialization
from fitness import FitnessFunction
import traffic_data
import numpy 



class Particle:
    def __init__(self,x0):
        self.position_i=[]          # particle position
        self.velocity_i=[]          # particle velocity
        self.pos_best_i=[]          # best position individual
        self.err_best_i=-1          # best error individual
        self.err_i=-1               # error individual
        self.Q = [] #0/20
        self.Qb = [] # [[0,200],[0,0]...]
        self.X_ = [] 

        for i in range(0,num_dimensions):
            self.velocity_i.append(random.uniform(0,1))
            self.position_i.append(x0[i])

    # evaluate current fitness
    def evaluate(self,costFunc,trafficdata,QQ,test):
        self.err_i,self.Q1,self.Qb,self.X_=costFunc(self.position_i,trafficdata,QQ,test)

        # check to see if the current position is an individual best
        if self.err_i<self.err_best_i or self.err_best_i==-1:
            self.pos_best_i=self.position_i.copy()
            self.err_best_i=self.err_i
                    
    # update new particle velocity
    def update_velocity(self,pos_best_g):
        w=0.5       # 0,5 constant inertia weight (how much to weigh the previous velocity)
        c1=1        # 1cognative constant
        c2=2        # 2social constant
        
        for i in range(0,num_dimensions):
            r1=random.random()
            r2=random.random()
            
            vel_cognitive=c1*r1*(self.pos_best_i[i]-self.position_i[i])
            vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
            self.velocity_i[i]=w*self.velocity_i[i]+vel_cognitive+vel_social

    
    
    # update the particle position based off new velocity updates

    def update_position(self,test):
        # print(self.position_i)
        z1 = 0 # razlika izmedju nove i stare vrednosti ciklusa (C_new - C_prev)
        z2 = 0 #zbir razlika izmedju nove i stare vrednosti faza (g1_new - g1_prev)+(g2_new - g2_prev)... 
        # C_prev = 0
        # g_prev = 0 #prethodna vrednost 
        first_pos = 0 #vrednost prethodnog resenja
        subtraction = 0 #z1-z2 ili z2-z1
        #izjednaciti sum(g) i C-L

        for i in range(0,num_dimensions):

            first_pos = self.position_i[i]
            self.position_i[i]=self.position_i[i]+self.velocity_i[i]
            self.position_i[i]=round(self.position_i[i])
            # print(self.position_i, i)
            if i == 0:
                # z1 = vel[i,j]
                z1 = self.position_i[i] - first_pos
                if self.position_i[i] > 120:
                    self.position_i[i] = 120
                    z1 = 120 - first_pos
                elif self.position_i[i] < 30:
                    self.position_i[i] = 30
                    z1 = 30 - first_pos
            else:
                
                if self.position_i[i] > 80:
                    # print("pass1")
                    self.position_i[i] = 80
                    z2 += 80 - first_pos
                elif self.position_i[i] <= 7:
                    # print("pass2")
                    self.position_i[i] = 7
                    if (test ==  41 or test == 42) and i == 3: # 3. faza je veca od 7 u datom test primeru
                        # print('8',pos[i])
                        self.position_i[i] = 8
                        # print('8',pos[i])
                    
                    z2 += self.position_i[i] - first_pos
                else:
                    # print("pass3")
                    z2 += self.position_i[i]-first_pos
            first_pos = 0
        # print('-----')
        # print(self.position_i)
        if z1 > z2:
            # print('z1 > z2')
            subtraction = z1 - z2
            t = False
            for i in range(1,num_dimensions):
                if 7<=self.position_i[i]+subtraction and self.position_i[i]+subtraction<=80:
                    # print('z1 > z2, g' + str(subtraction))
                    self.position_i[i] += subtraction 
                    t = True
                    break
            if t == False:
                # print('z1 > z2, C'+ str(subtraction))
########################

                self.position_i[0] -= subtraction 

            

        
        elif z2 > z1:
            # print('z1 < z2')
            
            subtraction = z2 - z1
            if 30<=self.position_i[0]+subtraction and self.position_i[0]+subtraction<=120:
                # print('z2 > z1, C'+ str(subtraction))
                self.position_i[0] += subtraction
            else:
                # print('z2 > z1, g'+ str(subtraction))
                # g = max(self.position_i[1:])
                # if g-7 >= subtraction:
                #     index = self.position_i.index(g)
                #     self.position_i[index] -= subtraction
                # else:
                for i in range(1,num_dimensions):
                    if subtraction > self.position_i[i]-7:
                        if (test == 41):
                            if i!=3:
                                subtraction -= (self.position_i[i]-7)
                                self.position_i[i] = 7
                        elif (test == 42):
                            if i!=3:
                                subtraction -= (self.position_i[i]-7)
                                self.position_i[i] = 7
                        else:
                            if i!= 3: 
                                subtraction -= (self.position_i[i]-7)
                                self.position_i[i] = 7
                    else: #uslov1
                        if (test == 41):
                            if i!=3:
                                self.position_i[i] -= subtraction
                                subtraction = 0
                                break
                        elif (test == 42):
                            if i!=3:
                                self.position_i[i] -= subtraction
                                subtraction = 0
                                break
                        else:
                            self.position_i[i] -= subtraction
                            subtraction = 0
                            break   
                    ####### ako se uslov1 ne ispuni
                if subtraction != 0:
                    self.position_i[0] += subtraction



        # print('----'+str(self.position_i))



            
        


#-------------------------------------------------------------------------------
class PSO():
    def __init__(self, costFunc, num_particles, dim, maxiter, F, trafficdata, QQ, test, verbose=False):
        global num_dimensions
        num_dimensions = dim

        x0 = Initialization(F, num_particles, dim, test)
        self.convergence_curve=numpy.zeros(maxiter)
        self.X_ = []
        self.Q = []
        self.QbQ1 = []
        self.err_best_g=-1                   # best error for group
        self.pos_best_g=[]                   # best position for group

        # establish the swarm
        swarm=[]
        for i in range(0,num_particles):
            swarm.append(Particle(x0[i]))

        # begin optimization loop
        i=0
        while i<maxiter:
            ############ INICIJALIZACIJA NA POCETKU SVAKE POPULACIJE
            if i!= 0:
                x0 = Initialization(F, num_particles, dim, test)
                swarm=[]
                for k in range(0,num_particles):
                    swarm.append(Particle(x0[k]))
            if verbose: print(f'iter: {i:>4d}, best solution: {self.err_best_g:10.6f} ', self.pos_best_g)
            # cycle through particles in swarm and evaluate fitness
            for j in range(0,num_particles):
                swarm[j].evaluate(costFunc,trafficdata,QQ,test)

                # determine if current particle is the best (globally)
                if swarm[j].err_i<self.err_best_g or self.err_best_g==-1:
                    self.pos_best_g=list(swarm[j].position_i)
                    self.err_best_g=float(swarm[j].err_i)
                    self.Q = swarm[j].Qb
                    self.QbQ1 = swarm[j].Q1
                    self.X_= swarm[j].X_
            
            # cycle through swarm and update velocities and position
            for j in range(0,num_particles):
                swarm[j].update_velocity(self.pos_best_g)
                swarm[j].update_position(test)
            self.convergence_curve[i]=self.err_best_g
            i+=1
        # s.convergence=convergence_curve
        # print final results
        print('\nFINAL SOLUTION:')
        print(f'   > {self.pos_best_g}')
        print(f'   > {self.err_best_g}\n')


if __name__ == "__main__":
    F=5
    PopSize=15
    dim=F+1
    iters=20
    test1=41
    # test1 = 41
    Q = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    trafficdata1 = traffic_data.extractTrafficData(F,test1)
    # print(trafficdata1)
    
    # solution1 = PSO(FitnessFunction, PopSize, dim, iters, F, trafficdata1, Q, test1, verbose=True)
    # print(solution1.pos_best_g,
    # solution1.err_best_g,
    # solution1.X_)
    objf1=FitnessFunction([120, 29, 10, 15, 28, 25],trafficdata1,Q,test1) #30, 28.0, 12.0, 26.0, 24.0, 18.0
    print(objf1)
    # Q[10][1] -= 1
    Qb1 = []
    test = 32
    for i in objf1[2]:
        Qb1.append([i[1],i[0]])

    trafficdata2 = traffic_data.extractTrafficData(F,test)
    objf1=FitnessFunction([120, 29, 10, 15, 28, 25],trafficdata2,Qb1,test)
    print(objf1)
    # import fitness
    
    # objf=fitness.FitnessFunction(solution1.pos_best_g,trafficdata2,Qb1,test)
    # print(objf)
