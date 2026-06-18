#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 13 11:56:52 2025

@author: Claire
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from random import randint

# rgraphique
plt.figure(figsize=(10, 8))
ax = plt.gca()
ax.set_xlim(-10, 10)
ax.set_ylim(-8, 8)


Points = [(randint(-500, 500)/100, randint(-500, 500)/100) for i in range(4)]

# dessin points
for p in Points:
    ax.scatter(p[0], p[1], color='blue', s=100)

def delaunay_parabole(points):
    Parabole_liste = list(combinations(points, 3))
    ParabolesDelo = []
    
    for p in Parabole_liste:
        p0, p1, p2 = p
        detP = (p0[0] - p1[0]) * (p0[0] - p2[0]) * (p1[0] - p2[0])
        
        # Calcul coeff de la parabole
        A = (p2[0]*(p1[1]-p0[1]) + p1[0]*(p0[1]-p2[1]) + p0[0]*(p2[1]-p1[1])) / detP
        B = (p2[0]**2*(p0[1]-p1[1]) + p1[0]**2*(p2[1]-p0[1]) + p0[0]**2*(p1[1]-p2[1])) / detP
        C = (p1[0]*p2[0]*(p1[0]-p2[0])*p0[1] + 
             p0[0]*p2[0]*(p2[0]-p0[0])*p1[1] + 
             p1[0]*p0[0]*(p0[0]-p1[0])*p2[1]) / detP
        
        # Vérif condition Delaunay
        res = True
        for P in points:
            if P in p:
                continue
                
            ab = A*P[0]**2 + B*P[0] + C #ordonné de la para au point P[0]=x
            if A < 0: #(concave)
                if P[1] < ab:#P est en dessous
                    res = False
                    break
            else: #(convexe)
                if P[1] > ab:#P est au dessus
                    res = False
                    break
        
        if res:
            ParabolesDelo.append((p, (A, B, C)))
    
    return ParabolesDelo

# affichage paraboles
results = delaunay_parabole(Points)
for p, coeffs in results:
    A, B, C = coeffs
    x = np.linspace(-10, 10, 400) #pour 400 valeurs de x on calcule la valeur de y correspondant pour la para
    y = A*x**2 + B*x + C  #plus rapide?
    ax.plot(x, y, color='b', linewidth=1)
    
    # triangle
    triangle = list(p)
    triangle.append(triangle[0])  #  fermer le triangle
    x_coords, y_coords = zip(*triangle) #((x1,y1),(x2,y2),...)-> (x1,x2,...),(y1,y2,...)
    ax.plot(x_coords, y_coords, 'r-')



plt.grid(True)
plt.show()


print("Points générés :", Points)
print("Nbr paraboles valides :", len(results))