#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 11 15:53:00 2025

@author: Claire
"""


import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from math import sqrt



#  points de S  

Points = [(np.random.randint(-800, 800)/100, np.random.randint(-700, 700)/100) for i in range(4)]


# graphe
plt.figure(figsize=(10, 8))
ax = plt.gca()
ax.set_xlim(-10, 10)
ax.set_ylim(-8, 8)

# Dessin points
for p in Points:
    ax.scatter(p[0], p[1], color='blue', s=60)

def Delaunay(ListePoints):
    ListeTriangle = list(combinations(ListePoints, 3))
    TriangleDelo = []
    Cercles = []
    
    for Triangle in ListeTriangle:
        Triangle = list(Triangle)
        res = True
        
        # calcul ceff mediatrices
        A1 = 2 * (Triangle[1][0] - Triangle[0][0])
        B1 = 2 * (Triangle[1][1] - Triangle[0][1])
        C1 = (Triangle[0][0]**2 + Triangle[0][1]**2) - (Triangle[1][0]**2 + Triangle[1][1]**2)
        
        A2 = 2 * (Triangle[2][0] - Triangle[1][0])
        B2 = 2 * (Triangle[2][1] - Triangle[1][1])
        C2 = (Triangle[1][0]**2 + Triangle[1][1]**2) - (Triangle[2][0]**2 + Triangle[2][1]**2)
        
        # calcul centre du cercle circonscrit = intersection des deux mediatrices 
        try:
            X = (C1 * B2 - C2 * B1) / (A2 * B1 - A1 * B2)
            Y = (C1 * A2 - A1 * C2) / (A1 * B2 - B1 * A2)
        except ZeroDivisionError:
            continue  # les points sont colinéaires
        
        Rayon_carre = (Triangle[1][0] - X)**2 + (Triangle[1][1] - Y)**2
        
        # verifie condition de Delaunay
        for P in ListePoints:
            if P not in Triangle:
                Distance_carre = (P[0] - X)**2 + (P[1] - Y)**2
                if Distance_carre <= Rayon_carre:
                    res = False
                    break
        
        if res:
            TriangleDelo.append(Triangle)
            Cercles.append(((X, Y), sqrt(Rayon_carre)))
    
    return TriangleDelo, Cercles



# tracé
triangles,Cercles = Delaunay(Points)


for triangle in triangles:
    triangle = list(triangle)
    triangle.append(triangle[0])  #  fermer le triangle
    x_coords, y_coords = zip(*triangle)
    ax.plot(x_coords, y_coords, 'k-')


for cercle in Cercles:
    centre, rayon = cercle
    circle = plt.Circle(centre, rayon, fill=False, color='green', linestyle='--')
    ax.add_patch(circle)

plt.grid(True)
plt.show()


print("Points :", Points)
print("Triangles Delaunay :", triangles)
