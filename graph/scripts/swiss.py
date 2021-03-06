#!/usr/bin/env python3
import numpy as np
from collections import defaultdict
import random, sys
import networkx as nx
from matplotlib import pyplot as plt

def round(A,M,r):
  print("ROUND", r)
  
  scores = M.sum(axis=0)
  groups = defaultdict(list)
  
  for player, score in enumerate(scores):
    groups[score].append(player)
  
  print(groups)
  if r == 1:
    players_a = groups[1].copy()
    print(players_a)
    players_b = groups[-1].copy()
    print(players_b)
    random.shuffle(players_a)
    print(players_a)
    random.shuffle(players_b)
    print(players_b)
    for p_a, p_b in zip(players_a,players_b):
      print("MATCH:", p_a, p_b)
      result = random.choice([-1,1])
      M[p_a][p_b] += result
      M[p_b][p_a] += -result
      A[p_a][p_b] += 1
      A[p_b][p_a] += 1 
  else:
    for score, players in groups.items():
      random.shuffle(players)
      iter_players = iter(players)
      for p_a, p_b in zip(iter_players,iter_players):
        print("MATCH:", p_a, p_b)
        result = random.choice([-1,1])
        M[p_a][p_b] += result
        M[p_b][p_a] += -result
        A[p_a][p_b] += 1
        A[p_b][p_a] += 1  

  print(M)

def fight(k):
  n = 2**k
  A = np.zeros((n,n))
  M = np.zeros((n,n))
  for r in range(k):
    round(A,M,r)
    print("")
  
  print("RESULT")
  print(M)
  print(M.sum(axis=0))
  print(M.sum(axis=0).max())
  print("ADJANCEY MATRIX")
  print(A)
  print("DEGREES")
  print(A.sum(axis=0))
  G=nx.from_numpy_matrix(A)
  print("ECCENTRICITY")
  
  try:
    ec = nx.eccentricity(G)
    print(ec)
    np_ec = np.array(list(ec.values()))
    print("average:", np.average(np_ec))
    print("varience:", np.var(np_ec))
    print("DIAMETER:", nx.diameter(G))
  except nx.exception.NetworkXError:
    print("diameter is infinite")
  
if __name__ == "__main__":
  k = int(sys.argv[1])
  fight(k)