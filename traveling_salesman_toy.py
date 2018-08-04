# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 19:42:00 2018

@author: yuwan
"""

'''
TODO: For each traveling salesman, print the path
'''
import numpy as np
from sympy.utilities.iterables import multiset_permutations

def travelingSalesman_naive(dist_array):
    #naive, should work for small cases
    #pretty bad though, O(n!)
    l = len(dist_array)
    min_dist = np.inf
    for p in multiset_permutations(range(1, l)):
        test = 0
        for i,j in zip([0] + p, p + [0]):
            test += dist_array[i][j]
        if test < min_dist:
            min_dist = test
    return min_dist


def travelingSalesman_dp(dist_array):
    #dp approach
    #use a bitmask
    #O(n*2^n)
    
    n = len(dist_array)
    dp = [[np.inf for i in range(n-1)] for j in range(2**(n-1))]
    dp[0] = [0 for i in range(n-1)]
    for i in range(n-1):
        dp[2**i][i] = dist_array[0][i+1]
    
    subsets = range(1,2**(n-1))
    for subset in sorted(subsets, key = lambda x: bin(x).count('1')):
        for i in range(n-1):
            if not  (1 << (i)) & subset:
                continue
            for k in range(n-1):
                if k == i or not (1 << (k)) & subset:
                    continue
                dp[subset][i] = min(dp[subset][i],dp[subset - (1 << i)][k]
                                + dist_array[k+1][i+1])
    out = [path + dist_array[i+1][0] 
                for i, path in zip(range(n-1),dp[2**(n-1)-1])]
    return min(out)

def travelingSalesman_nearest(dist_array):
    #greedy algo from each node
    #O(n^3), but not always correct
    n = len(dist_array)
    out = np.inf
    for i in range(n):
        curr = i
        unvisited = set(range(n))
        unvisited.remove(i)
        total_dist = 0
        while unvisited:
            min_dist = np.inf
            next_node = -1
            for s in unvisited:
                if dist_array[curr][s] < min_dist:
                    min_dist = dist_array[curr][s]
                    next_node = s
            total_dist += min_dist
            curr = next_node
            unvisited.remove(curr)
        total_dist += dist_array[curr][i]
        if total_dist < out:
            out = total_dist
    return out
        
                
    