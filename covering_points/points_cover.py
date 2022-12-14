import sys
from itertools import combinations
from itertools import chain

                    
#calculate the slop of two points
def slop(dx,dy):
    g = gcd(abs(dy), abs(dx))   
    if (dy < 0) or (dx < 0) :
        return (-abs(dy) // g, abs(dx) // g)
    else:
        return (abs(dy) // g, abs(dx) // g)
  
#calculates the greatest common divisor
def gcd(x, y):
    if (y == 0):
        return x
    return gcd(y, x % y)

#generate all lines that cover the points
def findAllLines(mydict,comb,flag):    
    lines={}
    paralines={}
    current={}
    alllines={}
    #unitialize all points as not used
    usedpoints=[False for x in range (len(mydict))]
    #calculate slop for all lines that generate from the combinations
    for c in comb:
        point1=c[0]
        point2=c[1]
        x1=mydict[point1][0]
        y1=mydict[point1][1]
        x2=mydict[point2][0]
        y2=mydict[point2][1]
        temp=slop(x2-x1, y2-y1)
        #check if a line with that slop already exists
        if temp not in lines.keys():
            lines.setdefault(temp,[])
            lines[temp].append(c)
        else:
            lines[temp].append(c)
    #if grid argument exists
    if flag :
        for line in lines.keys():
            #keeps only the lines that are horizontal or vertical
            if line[0]==0 or line[1]==0:
                paralines.setdefault(line,[])
                for i in range(len(lines[line])):
                    paralines[line].append(lines[line][i])
        current=paralines
    #if grid argument doesn't exist we keep all the lines
    else:
        current=lines
    counter=0
    #generate the lines from the slops and the points
    for c in current.keys():
        #keeps track of the used points
        used=[]
        for i in range (0,len(current[c])):         
            position=current[c]
            temp=position[i]  
            point=temp[0]
            if point not in used and temp[1] not in used:
                #updates used points list
                used.append(point)
                used.append(temp[1])
                #add points to the line with the specific slop
                alllines.setdefault(counter,[])
                alllines[counter].append(temp[0])
                alllines[counter].append(temp[1])
                for j in range (i+1,len(current[c])):                  
                    position=current[c]
                    temp=position[j]               
                    pointnow=temp[0]
                    #check if point belogs to the specific line and add it                  
                    if point==pointnow:
                        alllines[counter].append(temp[1])
                counter=counter+1
    #find unused points
    for v in alllines.values():
        for point in v:
            usedpoints[point]=True  
    j=len(alllines)
    #create a line for every unused point
    for u in range (len(usedpoints)):
        if usedpoints[u]==False:
            alllines.setdefault(j,[])
            alllines[j].append(u)
            j=j+1
    return alllines


#finds set of lines with the smallest cost by checking all the possible lines
def set_cover(u, lines, costs):
    tempset = powerset(lines.keys())  
    best_cost = float("inf")
    for subset in tempset:
        used= set()
        cost = 0
        for s in subset:
            used.update(lines[s])
            cost =cost + costs[s]
        #checks if all points are covered and if the cost is less than the best cost
        if len(used) == len(u) and cost < best_cost:
            final_set = subset
            best_cost = cost
    return final_set


#generates all subsets of a set
def powerset(i):
    s = list(i)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


#finds line that covers the most points
def findMax(u,lines):
    eff={}
    for l in lines.keys():
        sum=0
        for point in lines[l]:
            #counts the number of points from the universe that the line covers
            if point in u:
                sum=sum+1    
        eff[l] =sum
    values=eff.values()
    maxvalue=max(values)
    min=1000
    #finds the line that covers the most points
    for l in lines.keys():        
        if eff[l]==maxvalue and lines[l][0]<min:
            pos=l
            min=lines[l][0]
    return pos

#finds the best lines in the greedy way
def greedy(u,lines):
    temp=u
    result=[]
    #while not all the points are covered
    while len(temp)!=0:
        #every time it finds the line that covers the most ucovered points   
        line=findMax(temp,lines)
        result.append(lines[line])  
        for l in lines[line]:  
            if l in temp:
                temp.remove(l)
        #remove the line so I don't have to check it again
        del lines[line]
    return result


def main(argv):
    mydict={}    
    comb=[]    
    par1,par2=None,None
    #read arguments  
    if len(sys.argv)==2:
        file=sys.argv[1]
    elif len(sys.argv)==3:
        par1=sys.argv[1]
        file=sys.argv[2]
    elif len(sys.argv)==4:
        file=sys.argv[3]
        par1=sys.argv[1]
        par2=sys.argv[2]
    #read points file
    with open(file, 'r') as file:
       points = file.readlines()
       points = [row.split(' ') for row in points]
    temppoints=[]
    #save points in a temporary dictionary
    for i in range (0,len(points)):
        points[i][1]=points[i][1].replace("\n","") 
        temp=[]
        temp.append(int(points[i][0]))
        temp.append(int(points[i][1]))
        temppoints.append(temp)
    temppoints.sort()
    #save sorted points in a dictionary
    for i in range (0,len(points)):
        mydict.setdefault(i,[])    
        mydict[i].append(int(temppoints[i][0]))
        mydict[i].append(int(temppoints[i][1]))
    #find all combinations of two points
    for i in combinations(mydict.keys(),2):
        comb.append(i)
    flag=False
    #check if argument is grid
    if par1=="-g" or par2=="-g":
        flag=True
    lines=findAllLines(mydict, comb,flag)
    u=set([x for x in mydict.keys()])
    un=[x for x in mydict.keys()]
    cost={}
    #counts the points every line has 
    for l in lines.keys():
        cost[l]=len(lines[l])
    result=[]
    #check for full exploration argument
    if par1=="-f" or par2=="-f":
        result=set_cover(u, lines, cost)
        sol=[]
        #preperation for printing format
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
        #print result
        for s in sol:
            for r in s:
                print("("+ str(r[0]) + ", " + str(r[1]) +")", end=" ")
            print()
    #if exploration argument doesn't exist
    else:
        result=greedy(un, lines)
        s=[]
        #preperation for printing format
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
        ##print result      
        for result in s:
            for r in result:
                print("("+ str(r[0]) + ", " + str(r[1]) +")", end=" ")
            print()



if __name__ == "__main__":
   main(sys.argv[1:])
