#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 18 01:10:35 2025

@author: Claire
"""
import numpy as np
import matplotlib.pyplot as plt

def voronoi_visuel(points):
    #  graphe
    x_min, x_max = min(points[:,0])-1, max(points[:,0])+1
    y_min, y_max = min(points[:,1])-1, max(points[:,1])+1
    
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 500),
                         np.linspace(y_min, y_max, 500))
    grid = np.c_[xx.ravel(), yy.ravel()]
    
    
    distances_aux_points = []
    
   
    for point in points:
        # Calcule les différence entre tous les points de la grille et le point 
        differences = grid - point
        
        
        carres_differences = differences ** 2
        distances_au_carre = np.sum(carres_differences, axis=1)#=1 somme selon les lignes
        
        distances_aux_points.append(distances_au_carre)
    
    
    tableau_distances = np.array(distances_aux_points)
    
    # Pour chaque point de la grille, trouve l'indice de la source la plus proche
    indices_voronoi = np.argmin(tableau_distances, axis=0)
    
    
    voronoi = indices_voronoi
    
    
    # Affichage 
    plt.figure(figsize=(8, 8))
    plt.imshow(voronoi.reshape(xx.shape), 
               extent=(x_min, x_max, y_min, y_max),
               cmap='tab10', origin='lower')
    plt.scatter(points[:,0], points[:,1], color='black', s=30)
    plt.axis('off')  # pas d'axes 
    plt.tight_layout()
    plt.show()


points = np.random.rand(10, 2)
voronoi_visuel(points)