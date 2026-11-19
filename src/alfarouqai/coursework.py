# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Classical AI coursework: real shortest-path search, not a robot controller."""
import heapq
from .core import Result,ValidationError

def search(*,grid,start,goal,config):
    if not isinstance(grid,list) or not grid or len(grid)>200 or not isinstance(grid[0],list) or not grid[0] or len(grid[0])>200 or any(not isinstance(r,list) or len(r)!=len(grid[0]) or any(type(v)is not int or v not in (0,1) for v in r) for r in grid):raise ValidationError('Rectangular binary grid <=200x200 required: 0 free, 1 blocked')
    h,w=len(grid),len(grid[0])
    def point(p):return isinstance(p,(tuple,list)) and len(p)==2 and all(type(v)is int for v in p) and 0<=p[0]<h and 0<=p[1]<w and grid[p[0]][p[1]]==0
    if not point(start) or not point(goal):raise ValidationError('Valid free start/goal [row,column] required')
    start,goal=tuple(start),tuple(goal);queue=[(0,0,start)];cost={start:0};parents={};expanded=0
    while queue:
        _,distance,node=heapq.heappop(queue)
        if distance!=cost[node]:continue
        expanded+=1
        if node==goal:
            path=[node]
            while path[-1]!=start:path.append(parents[path[-1]])
            path.reverse()
            return Result('ai.search',{'found':True,'cost':distance,'path':[list(p) for p in path],'expanded':expanded,'rows':[{'step':i,'row':r,'column':c} for i,(r,c) in enumerate(path)]},'stdlib.A-star-Manhattan',['Four-neighbor unit-cost grid exercise, not autonomous navigation or robot safety.'])
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nxt=node[0]+dr,node[1]+dc
            if point(nxt) and distance+1<cost.get(nxt,float('inf')):
                cost[nxt]=distance+1;parents[nxt]=node;heuristic=abs(nxt[0]-goal[0])+abs(nxt[1]-goal[1]);heapq.heappush(queue,(distance+1+heuristic,distance+1,nxt))
    return Result('ai.search',{'found':False,'cost':None,'path':[],'expanded':expanded,'rows':[]},'stdlib.A-star-Manhattan',['No path found in the provided static grid.'])
