#!/usr/bin/env python3
import networkx as nx
import numpy as np
from math import sqrt
import pyprimes
from itertools import product

def euler_phi(n):
  rtv = n
  for p, _ in pyprimes.factorise(n):
    rtv *= ( 1 - 1/p )
  return round(rtv)

def cnt_circle(n):
  lines = set()
  for i,j,k in product(range(n),repeat=3):
    if all( ((a*i)%n,(a*j)%n,(a*k)%n) != (0,0,0) for a in range(1,n) ):
      lines.add((i,j,k))
  cnt = 0
  for (i,j,k) in lines:
    if (i**2+j**2+k**2)%n == 0:
      cnt+=1
  return round((cnt-1)/euler_phi(n))

def erdos_order(p,k):
  q = p**k
  return q**2 + q + 1

def erdos_degree(p,k):
  q = p**k
  return q + 1

def erdos_orders():
  rtv = []
  for p in pyprimes.primes_below(1000):
    for k in range(1,30):
      rtv.append(erdos_order(p,k))
  rtv.sort()
  return rtv
  
def order(n):
  rtv = n**2
  for (p,_) in pyprimes.factorise(n):
    rtv *= 1 + 1/p + 1/p**2
  return round(rtv)

def degree(n):
  rtv = n
  for (p,_) in pyprimes.factorise(n):
    rtv *=  1 + 1/p 
  return round(rtv)

def pair(n):
  return order(n),degree(n)

def is_ddp_new(o,d):
  for i in range(1,100):
    facts = pyprimes.factors(d - i)
    if len(set(facts)) == 1:
      p, k = facts[0], len(facts)
      eo, ed = erdos_order(p, k), erdos_degree(p, k)
      if p == 2:
        eo += 1
      if o - eo  > d - ed:
        print(eo,ed,p,k)
        return True
      else:
        return False
    
def get(p):
  lines = set()
  for i in range(p):
    for j in range(p):
      for k in range(p):
        if all(not ((a*i)%p,(a*j)%p,(a*k)%p) in lines for a in range(1,p)):
          lines.add((i,j,k)) 
  
  lines.remove((0,0,0))
  #print(lines)

  G = nx.Graph()

  for line1 in lines:
    for line2 in lines:
      if line1 != line2:
        norm = 0
        for i in range(3):
          norm += line1[i]*line2[i]
        if norm % p == 0:
          G.add_edge(line1,line2)

  return G

def show(p):
  G = get(p)
  deg_vals = list(G.degree().values())
  max_d = max(deg_vals)
  min_d = min(deg_vals)
  print("diameter:", nx.diameter(G))
  if max_d - min_d == 1 or max_d - min_d == 0:
    deg_ave = np.average(deg_vals)
    print("degree is safe:", deg_ave)
  print("node:", len(G.nodes()))
  print("root of nodes", int(sqrt(len(G.nodes()))),",",int(2*sqrt(len(G.nodes()))))
  if len(G.nodes()) in erdos_orders():
    print("order in erdos nums")
  erdos_bound = deg_ave**2-deg_ave+1
  print("erodos bound:", erdos_bound)
  print(int(100*len(G.nodes())/erdos_bound),"%")

