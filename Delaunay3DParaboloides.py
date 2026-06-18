#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 13 12:05:55 2025

@author: Claire
"""


import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from random import randint

# Initialisation
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Génération des points
Points = [(randint(-500, 500)/100, 
           randint(-500, 500)/100,
           randint(-500, 500)/100) for i in range(4)]

# Affichage des points
for p in Points:
    ax.scatter(*p, color='b', s=50)

def delaunay_paraboloid(points):
    """Calcul des paraboloïdes de Delaunay 3D"""
    paraboles = list(combinations(points, 4))
    paraDelo = []
    
    for para in paraboles:
        P1, P2, P3, P4 = para
        res = True
        
        # Calcul coefficients
        B1 = P2[0]**2 - P1[0]**2 + P2[1]**2 - P1[1]**2
        B2 = P3[0]**2 - P1[0]**2 + P3[1]**2 - P1[1]**2
        B3 = P4[0]**2 - P1[0]**2 + P4[1]**2 - P1[1]**2
        
        # Calcul matrices
        N1 = 2*((P3[1]-P1[1])*(P4[2]-P1[2]) - (P4[1]-P1[1])*(P3[2]-P1[2]))
        N2 = -2*((P3[0]-P1[0])*(P4[2]-P1[2]) - (P4[0]-P1[0])*(P3[2]-P1[2]))
        N3 = 4*((P3[0]-P1[0])*(P4[1]-P1[1]) - (P4[0]-P1[0])*(P3[1]-P1[1]))
        N4 = -2*((P2[1]-P1[1])*(P4[2]-P1[2]) - (P4[1]-P1[1])*(P2[2]-P1[2]))
        N5 = 2*((P2[0]-P1[0])*(P4[2]-P1[2]) - (P4[0]-P1[0])*(P2[2]-P1[2]))
        N6 = -4*((P2[0]-P1[0])*(P4[1]-P1[1]) - (P4[0]-P1[0])*(P2[1]-P1[1]))
        N7 = 2*((P2[1]-P1[1])*(P3[2]-P1[2]) - (P3[1]-P1[1])*(P2[2]-P1[2]))
        N8 = -2*((P2[0]-P1[0])*(P3[2]-P1[2]) - (P3[0]-P1[0])*(P2[2]-P1[2]))
        N9 = 4*((P2[0]-P1[0])*(P3[1]-P1[1]) - (P3[0]-P1[0])*(P2[1]-P1[1]))
        
        det = 4*(
            (P2[0]-P1[0])*(P3[1]-P1[1])*(P4[2]-P1[2]) +
            (P3[0]-P1[0])*(P4[1]-P1[1])*(P2[2]-P1[2]) +
            (P4[0]-P1[0])*(P2[1]-P1[1])*(P3[2]-P1[2]) -
            (P4[0]-P1[0])*(P3[1]-P1[1])*(P2[2]-P1[2]) -
            (P3[0]-P1[0])*(P2[1]-P1[1])*(P4[2]-P1[2]) -
            (P2[0]-P1[0])*(P4[1]-P1[1])*(P3[2]-P1[2])
        )
        
        try:
            a = (N1*B1 + N4*B2 + N7*B3)/det
            b = (N2*B1 + N5*B2 + N8*B3)/det
            d = (N3*B1 + N6*B2 + N9*B3)/det
            c = -(P1[0]**2 - 2*P1[0]*a + a**2 + P1[1]**2 - 2*P1[1]*b + b**2 - d*P1[2])/d
            
            # verifie condition Delaunay
            for P in points:
                if P in para:
                    continue
                    
                u = ((P[0]-a)**2 + (P[1]-b)**2)/d
                Z = P[2]-c
                
                if d > 0:#    \/
                    if Z > u:
                        res = False
                        break
                else:
                    if Z < u:#  /\
                        res = False
                        break
            
            if res:
                paraDelo.append((para, (a, b, c, d)))
                
        except ZeroDivisionError: # points alignés
            continue
            
    return paraDelo

# Calcul paraboloïdes
res = delaunay_paraboloid(Points)

# Affichage tétraèdres
for para, _ in res:
    
    aretes = [
        [para[0], para[1], para[2], para[0]],
        [para[0], para[1], para[3], para[0]],
        [para[0], para[2], para[3], para[0]],
        [para[1], para[2], para[3], para[1]]
    ]
    
    for a in aretes:
        x, y, z = zip(*a)
        ax.plot(x, y, z, 'b', linewidth=1)

# Affichage paraboloïdes
for _, (a, b, c, d) in res:
    x = np.linspace(-5, 5, 30)
    y = np.linspace(-5, 5, 30)
    x, y = np.meshgrid(x, y)
    z = ((x-a)**2 + (y-b)**2)/d + c
    
    ax.plot_surface(x, y, z, color=(1.0, 0.0, 0.0, 0.5), alpha=0.5, rstride=1, cstride=1)

# Configuration graphique
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)

plt.show()

# Affichage des résultats
print("Points générés:", Points)
print("Nbr paraboloïdes valides:", len(res))