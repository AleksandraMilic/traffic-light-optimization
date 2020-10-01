# -*- coding: utf-8 -*-
"""
Python code of Gravitational Search Algorithm (GSA)
Reference: Rashedi, Esmat, Hossein Nezamabadi-Pour, and Saeid Saryazdi. "GSA: a gravitational search algorithm." 
Information sciences 179.13 (2009): 2232-2248.	

Coded by: Mukesh Saraswat (saraswatmukesh@gmail.com), Himanshu Mittal (emailid: himanshu.mittal224@gmail.com) and Raju Pal (emailid: raju3131.pal@gmail.com)
The code template used is similar given at link: https://github.com/7ossam81/EvoloPy and matlab version of GSA at mathworks.

Purpose: Defining the move Function
            for calculating the updated position

Code compatible:
-- Python: 2.* or 3.*
"""

import random
import numpy as np

def move(PopSize,dim,pos,vel,acc,test):
    for i in range(0,PopSize):
        ########################### pracenje pomeraja vrednosti, da bi se odrzao njihov zbir
        z1 = 0 # razlika izmedju nove i stare vrednosti ciklusa (C_new - C_prev)
        z2 = 0 #zbir razlika izmedju nove i stare vrednosti faza (g1_new - g1_prev)+(g2_new - g2_prev)... 
        # C_prev = 0
        # g_prev = 0 #prethodna vrednost 
        first_pos = 0 #vrednost prethodnog resenja
        subtraction = 0 #z1-z2 ili z2-z1
        #izjednaciti sum(g) i C-L
        
        # z1 > z2 ?random odabrati fazu (ili ravnomerno rasporediti po *formuli*) kojoj se dodaje z1-z2 ako ispunjava 7<=g+(z1-z2)<=80. 
        # Ako nijedna od njih ne ispunjava uslov, onda je ciklus C_prev += z2 == C_new -= z1-z2 tj. C_new=sum(g_new)
        
        # z2 > z1, ako je 30<=C+(z2-z1)<=120, C+=(z2-z1)
        # Ako uslov ne vazi, odabrati najvece g: g-=z2-z1
        ###########################
        
        
        for j in range(0,dim):
            r1=random.random()
            #print((i,j),pos[i,j],vel[i,j])

            vel[i,j]=r1*vel[i,j]+acc[i,j]
            # #print(vel[i,j])
            first_pos = pos[i,j]
            pos[i,j]=pos[i,j]+vel[i,j]
######################################## ciklus i zelena vremena - celi brojevi ????? ###########################3
            pos[i,j]=round(pos[i,j])
            #print((i,j),pos[i,j],vel[i,j])
            
            if j == 0:
                # z1 = vel[i,j]
                z1 = pos[i,j]-first_pos
                if pos[i,j] > 120:
                    pos[i,j] = 120
                    z1 = 120 - first_pos
                elif pos[i,j] < 30:
                    pos[i,j] = 30
                    z1 = 30 - first_pos
            else:
                
                if pos[i,j] > 80:
                    pos[i,j] = 80
                    z2 += 80 - first_pos
                elif pos[i,j] <= 7:
                    pos[i,j] = 7
                    ########################## 777777777777
                    if (test ==  41 or test == 42) and j == 3: # 3. faza je veca od 7 u datom test primeru
                        # #print('8',pos[i])
                        pos[i,j] = 8
                        # #print('8',pos[i])
                    z2 += pos[i,j] - first_pos

                else:
                    z2 += pos[i,j] - first_pos
            first_pos = 0
        
        # print('pos i',pos[i])
        if z1 > z2:
            
            subtraction = z1 - z2
            t = False
            for ii in range(1,dim):
                if 7<=pos[i,ii]+subtraction and pos[i,ii]+subtraction<=80:
                    # #print('z1 > z2, g' + str(subtraction))
                    pos[i,ii] += subtraction 
                    t = True
                    break
            if t == False:
                # #print('z1 > z2, C'+ str(subtraction))
                pos[i,0] -= subtraction 
            

        
        elif z2 > z1:
            
            subtraction = z2 - z1
            if 30<=pos[i,0]+subtraction and pos[i,0]+subtraction<=120:
                # #print('z2 > z1, C'+ str(subtraction))
                pos[i,0] += subtraction
            else:
                # #print('z2 > z1, g'+ str(subtraction))
                # g = max(pos[i][1:])
                # index = np.where(pos[i]==g)
                # pos[i][index[0]] -= subtraction
                # print(subtraction)
                
                for ii in range(1,dim):
                    if subtraction > pos[i][ii]-7:
                        
                        if (test == 41):
                            # print('pass')
                            if ii != 3:
                                r = pos[i][ii]-7
                                subtraction -= r
                                pos[i][ii] = 7
                        elif (test == 42):
                            if ii != 3:
                                subtraction -= (pos[i][ii]-7)
                                pos[i][ii] = 7
                        else:
                            subtraction -= (pos[i][ii]-7)
                            pos[i][ii] = 7
                    else:
                        if (test == 41):
                            # print('pass')
                            if ii != 3:
                                pos[i][ii] -= subtraction
                                subtraction = 0
                                break
                        elif (test == 42):
                            if ii != 3:
                                pos[i][ii] -= subtraction
                                subtraction = 0
                                break                            
                        else:
                            pos[i][ii] -= subtraction
                            subtraction = 0
                            break   

                        
                ####### ako se uslov1 ne ispuni
                if subtraction != 0:
                    pos[i][0] += subtraction
                    if pos[i][0]>120:
                        print('pass1--------------------------------------------------')

        # print(pos[i])

    return pos, vel
