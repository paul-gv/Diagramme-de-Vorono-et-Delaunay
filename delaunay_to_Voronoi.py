#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 18 19:29:23 2025

@author: Claire
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

def circumcenter(a, b, c):
    """Centre du cercle circonscrit au triangle ABC"""
    A = b - a
    B = c - a
    Asq = np.dot(A, A)
    Bsq = np.dot(B, B)
    cross = A[0]*B[1] - A[1]*B[0]
    if abs(cross) < 1e-10:
        return None  # Alignés
    center = a + (Bsq * np.array([-A[1], A[0]]) - Asq * np.array([-B[1], B[0]])) / (2 * cross)
    return center

# Générer les points

points = np.random.rand(15, 2)

# Triangulation de Delaunay
tri = Delaunay(points)

# Calcul des centres des cercles circonscrits
centers = []
for simplex in tri.simplices:
    a, b, c = points[simplex]
    center = circumcenter(a, b, c)
    centers.append(center)
centers = np.array(centers)

# Construction des arêtes du diagramme de Voronoi
edges = []

for t_index, neighbors in enumerate(tri.neighbors):
    for i, neighbor in enumerate(neighbors):
        if neighbor == -1:
            # Bord : prolonger
            # Obtenir l'arête opposée
            verts = tri.simplices[t_index]
            a = points[verts[i]]
            b = points[verts[(i + 1) % 3]]
            edge_dir = b - a
            edge_dir = np.array([-edge_dir[1], edge_dir[0]])  # normale

            edge_dir = edge_dir / np.linalg.norm(edge_dir)
            mid = (a + b) / 2

            center = centers[t_index]
            if center is None:
                continue

            # Vérifier direction correcte (doit pointer "dehors")
            to_center = center - mid
            if np.dot(to_center, edge_dir) < 0:
                edge_dir = -edge_dir

            # Créer un segment long vers l'extérieur
            far_point = center + edge_dir * 10  # Long segment

            edges.append((center, far_point))
        elif neighbor > t_index:
            # Arête intérieure
            c1 = centers[t_index]
            c2 = centers[neighbor]
            if c1 is not None and c2 is not None:
                edges.append((c1, c2))

# Tracé
fig, ax = plt.subplots(figsize=(8, 8))

# Triangulation
ax.triplot(points[:, 0], points[:, 1], tri.simplices, color="blue", label="Delaunay")
ax.plot(points[:, 0], points[:, 1], 'o', color="black")

# Arêtes du diagramme de Voronoï
for p1, p2 in edges:
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="red")

ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.1)
ax.set_aspect('equal')
plt.grid(True)
plt.show()
