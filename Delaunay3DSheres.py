#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 22:30:47 2025

@author: Claire
"""



import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from math import sqrt
from random import randint




#   NBR POINTS 
n_points = 4
coord_range = (-5, 5)

# 3D
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')


# genere des points 
Points = [(randint(-500, 500)/100, randint(-500, 500)/100, randint(-500, 500)/100) for i in range(9)]

# calcul du centre + rayon de la sphère circonscrite a un tetraedre
def sphere(tetra):
    A, B, C, D = tetra
    # 
    M = np.array([
        [2*(B[0]-A[0]), 2*(B[1]-A[1]), 2*(B[2]-A[2])],
        [2*(C[0]-A[0]), 2*(C[1]-A[1]), 2*(C[2]-A[2])],
        [2*(D[0]-A[0]), 2*(D[1]-A[1]), 2*(D[2]-A[2])]
    ])
    
    # second membre
    L = np.array([
        B[0]**2 + B[1]**2 + B[2]**2 - (A[0]**2 + A[1]**2 + A[2]**2),
        C[0]**2 + C[1]**2 + C[2]**2 - (A[0]**2 + A[1]**2 + A[2]**2),
        D[0]**2 + D[1]**2 + D[2]**2 - (A[0]**2 + A[1]**2 + A[2]**2)
    ])
    
    
    centre = np.linalg.solve(M, L)  #MX=L -> revoie X
    r = sqrt(sum((np.array(A) - centre)**2))
    return centre, r




# triangulation Delaunay 3D
def delaunay_3d(points):
    tetraedres = list(combinations(points, 4))
    tetraDelo = []
    
    for tetra in tetraedres:
        centre, r = sphere(tetra)
        if centre is None:
            continue
            
        # verif condition Delaunay
        Delo = True
        for point in points:
            if point in tetra:  # mtn  fonctionne car tuples
                continue
            if sum((np.array(point) - centre)**2) < r**2 :
                Delo = False
                break
                
        if Delo:
            tetraDelo.append((tetra, centre, r))
    
    return tetraDelo


res = delaunay_3d(Points)

# affiche points
ax.scatter(*zip(*Points), 
           color='blue', s=100, depthshade=False)

# affiche tétraèdres + sphères
for tetra, centre, r in res:
    # Arêtes du tétraèdre
    aretes = combinations(tetra, 2)
    for a in aretes:
        ax.plot([a[0][0], a[1][0]],
                [a[0][1], a[1][1]],
                [a[0][2], a[1][2]], 
                'r-', linewidth=1, alpha=0.5)
    
    # sphère circonscrite
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
    x = centre[0] + r * np.cos(u) * np.sin(v)
    y = centre[1] + r * np.sin(u) * np.sin(v)
    z = centre[2] + r * np.cos(v)
    ax.plot_wireframe(x, y, z, color='green', alpha=0.5, linewidth=0.5)
    
    

# graphique
ax.set_xlim(*coord_range)
ax.set_ylim(*coord_range)
ax.set_zlim(*coord_range)


plt.tight_layout()
plt.show()


