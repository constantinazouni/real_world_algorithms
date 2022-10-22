import sys
from itertools import combinations
from itertools import chain

def main(argv):
    mydict={}    
    comb=[]    
    par1,par2=None,None  
    if len(sys.argv)==2:
        file=sys.argv[1]
    elif len(sys.argv)==3:
        par1=sys.argv[1]
        file=sys.argv[2]
    elif len(sys.argv)==4:
        file=sys.argv[3]
        par1=sys.argv[1]
        par2=sys.argv[2]
    with open(file, 'r') as file:
       points = file.readlines()
       points = [row.split(' ') for row in points]    
    temppoints=[]
    for i in range (0,len(points)):
        points[i][1]=points[i][1].replace("\n","")        
        temp=[]
        temp.append(int(points[i][0]))
        temp.append(int(points[i][1]))
        temppoints.append(temp)    
    temppoints.sort()
    for i in range (0,len(points)):
        mydict.setdefault(i,[])        
        mydict[i].append(int(temppoints[i][0]))
        mydict[i].append(int(temppoints[i][1]))        
    for i in combinations(mydict.keys(),2):        
        comb.append(i)   
    flag=False
    if par1=="-g" or par2=="-g":
        flag=True
    lines=findAllLines(mydict, comb,flag)
    u=set([x for x in mydict.keys()])
    un=[x for x in mydict.keys()]
    cost={}    
    for l in lines.keys():
        cost[l]=len(lines[l]) 
    result=[]
    if par1=="-f" or par2=="-f":
        result=set_cover(u, lines, cost) 
        sol=[]
        for s in result:
            pr=[]
            if len(lines[s])==1:
                pointnow=temppoints[lines[s][0]]
                pr.append(pointnow)
                newpoint=[]
                newpoint.append(int(pointnow[0])+1)
                newpoint.append(pointnow[1])
                pr.append(newpoint)
            else:
                for point in lines[s]:
                    pr.append(temppoints[point])          
            sol.append(pr)
        for s in sol:
            for r in s:
                print("("+ str(r[0]) + ", " + str(r[1]) +")", end=" ")
            print()
                
        
        
    else:
        result=greedy(un, lines)
        s=[]
        for r in result:
            pr=[]
            if len(r)==1:
                pointnow=temppoints[r[0]]
                pr.append(pointnow)
                newpoint=[]
                newpoint.append(int(pointnow[0])+1)
                newpoint.append(pointnow[1])
                pr.append(newpoint)
            else:
                for point in r:
                    pr.append(temppoints[point])
            s.append(pr)       
        for result in s:
            for r in result:
                print("("+ str(r[0]) + ", " + str(r[1]) +")", end=" ")
            print()
                    
 
def slop(dx,dy):
    g = gcd(abs(dy), abs(dx))     
    if (dy < 0) or (dx < 0) :
        return (-abs(dy) // g, abs(dx) // g)
    else:
        return (abs(dy) // g, abs(dx) // g)   
  
 
def gcd(x, y):
    if (y == 0):
        return x
    return gcd(y, x % y)

    
def findAllLines(mydict,comb,flag):    
    lines={}
    paralines={}
    current={}
    alllines={}
    usedpoints=[False for x in range (len(mydict))]
    for c in comb:
        point1=c[0]
        point2=c[1]
        x1=mydict[point1][0]
        y1=mydict[point1][1]
        x2=mydict[point2][0]
        y2=mydict[point2][1]
        temp=slop(x2-x1, y2-y1)  
        if temp not in lines.keys():
            lines.setdefault(temp,[])
            lines[temp].append(c)
        else:
            lines[temp].append(c)
    if flag :
        for line in lines.keys():
            if line[0]==0 or line[1]==0:
                paralines.setdefault(line,[]) 
                for i in range(len(lines[line])):
                    paralines[line].append(lines[line][i])
        current=paralines
    else:
        current=lines
    counter=0 
    
    for c in current.keys(): 
        used=[]       
        for i in range (0,len(current[c])):           
            position=current[c]
            temp=position[i]            
            point=temp[0]
            if point not in used and temp[1] not in used:
                used.append(point)
                used.append(temp[1])
                alllines.setdefault(counter,[])
                alllines[counter].append(temp[0])
                alllines[counter].append(temp[1])
                for j in range (i+1,len(current[c])):                    
                    position=current[c]
                    temp=position[j]                    
                    pointnow=temp[0]                    
                    if point==pointnow:                        
                        alllines[counter].append(temp[1])
                counter=counter+1
    for v in alllines.values():
        for point in v:
            usedpoints[point]=True    
    j=len(alllines)  
    for u in range (len(usedpoints)):
        if usedpoints[u]==False:
            alllines.setdefault(j,[])
            alllines[j].append(u)
            j=j+1      
    return alllines
              


def set_cover(u, lines, costs):    
    tempset = powerset(lines.keys())    
    best_cost = float("inf")
    for subset in tempset:
        used= set()
        cost = 0
        for s in subset:
            used.update(lines[s])
            cost =cost + costs[s]
        if len(used) == len(u) and cost < best_cost:
            final_set = subset
            best_cost = cost
    return final_set


 
def powerset(i):   
    s = list(i)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))



def findMax(u,lines):   
    eff={}           
    for l in lines.keys() :
        sum=0
        for point in lines[l]:
            if point in u:
                sum=sum+1        
        eff[l] =sum
    values=eff.values()
    maxvalue=max(values)
    min=1000
    for l in lines.keys():            
        if eff[l]==maxvalue and lines[l][0]<min:
            pos=l
            min=lines[l][0]                
    return pos


def greedy(u,lines):
    temp=u
    result=[]
    while len(temp)!=0:        
        line=findMax(temp,lines)
        result.append(lines[line])       
        for l in lines[line]:           
            if l in temp:
                temp.remove(l)
        del lines[line]        
    return result

    
if __name__ == "__main__":
   main(sys.argv[1:])
