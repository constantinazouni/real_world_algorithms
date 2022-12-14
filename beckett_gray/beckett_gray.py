import sys

all_codes=[]

#show each code with a tabular representation    
def makeArray(code,bits):
    array=[]
    for i in range(bits-1,-1,-1):
        temp=[]
        for c in code:
            temp.append(c[i])
        array.append(temp)
    return array
        
#find the the reversed isomorphism of every code  
def reverse(delta,bits):
    result=[]
    for d in delta: 
        result.append(d[::-1])
    return result
        
#find the isomorphism of every code
def isomo(delta,reverse): 
    result=[]
    for j in range(0,len(delta)):
        for i in range(0,len(delta)):
            flag=False
            for p in range(0,len(delta[j])):
                positions_delta=[k for k, e in enumerate(delta[j]) if e == delta[j][p]]
                positions_reverse=[a for a, e in enumerate(reverse[i]) if e == reverse[i][p]]                
                if positions_delta!=positions_reverse:     
                    flag=True
                    break
            if not flag and not [i,j] in result and not [j,i] in result:
                temp=[]
                temp.append(j)
                temp.append(i)
                result.append(temp)    
    final=[]
    for r in result:
        temp=[]
        str1 = ''.join(str(x) for x in delta[r[0]])
        str2 = ''.join(str(x) for x in delta[r[1]])
        temp.append(str1)
        temp.append(str2)
        final.append(temp)              
    return final
                 
#algorithm that builds all gray and beckett gray codes
def GC_DFS(d,x,max_coord,bits,gc,visited,power,q,beckett):
    #if we visited all the nodes we stop recursion 
    if d==power:
        all_codes.extend(gc)    
        return
    #for every bit of that code
    for i in range (0,min(bits-1,max_coord)+1):
        #if we want to find beckett gray codes
        if beckett:
            x,flag,q=beckettFlip(x, i, bits, q, False,visited)
            #if I can't flip the bit
            if flag:
                #continue with the next bit
                continue
        #if we want to find just gray codes
        else:
            x=Flip(x,i,bits)
        if not visited[x]:
            visited[x]=True
            gc.append(x)
            #generate the next code
            GC_DFS(d+1,x,max(i+1,max_coord),bits,gc,visited,power,q,beckett)
            #if the flip of that code cause backtracking
            visited[x]=False
            gc.pop()
        #unflip the code that caused the backtracking
        if beckett:
            if not flag:
                x,flag,q=beckettFlip(x,i,bits,q,True,visited)
        else:
            x=Flip(x,i,bits)

#flip the bit that has remained the most time from 1 to 0
def beckettFlip(x,i,bits,q,undo,visited):
    flag=False
    temp=list(x)
    #if bit is 0 turn it to 1
    if temp[bits-i-1]=='0': 
        temp[bits-i-1]='1'
        x="".join(temp)
        if undo:
            q.insert(0, i)
        else:
            q.append(i)
    #if bit is 1
    else:
        #check if the bit is the older in the queue and if I haven't visited that code
        if len(q)>0 and q[0]==i and not visited[Flip(x,q[0],bits)]:
            #flips bit to 0
            temp[bits-i-1]='0'
            x="".join(temp)
            q.pop(0)
        #check if the move is undo caused from the backtrack
        elif undo and len(q)>0:
            temp[bits-i-1]='0'
            x="".join(temp)
            q.pop()
        #doesn't meet the requirements to flip it          
        else:
            x="".join(temp)
            flag=True
    return x,flag,q
    
 

def Flip(x,i,bits):
    #turns bit into a list of characters
    temp=list(x)
    #changes character from 0 to 1
    if temp[bits-i-1]=='0':
        temp[bits-i-1]='1'
        x="".join(temp)
    #changes character from 1 to 0 
    else:
        temp[bits-i-1]='0'
        x="".join(temp)
    return x


#count the bits of one number
def count_bits(number):
   counter = 0
   while number:
      counter= counter + (number & 1)
      number >>= 1
   return counter


#checks if two codes differ by one bit
def diff_one_bit(x, y):
   return count_bits(x ^ y) == 1


#find the differences in bits between two codes
def finddiff(x,y):
    r=[]
    for i in range(len(x)):
        if x[i] != y[i]:
           r.append(i)
    if len(r)==1:
        return r[0]
    else:
        return None
   

def main(argv):    
    bits=0
    choose=[]
    #read arguments and save them in a list
    for i in range(1,len(sys.argv)):
        temp=sys.argv[i]
        #read bits
        if temp.isdigit():
            bits=int(temp)
        else:
            choose.append(str(temp))
    #if we don't have any argument -a is implied
    if not '-a' in choose and not '-u' in choose and not '-c' in choose and not '-b' in choose and not '-p' in choose:
        choose.append('-a')
    gc=[]
    #generate as many zeros as the number of bits
    zero='0'*bits
    gc.append(zero)
    #number of codes that we need to create based on given bits
    power=pow(2,bits)
    visited={}
    #generate all codes with zeros
    nodes = [bin(x)[2:].rjust(bits, '0') for x in range(2**bits)]
    #mark all nodes as unvisited
    for i in range(power):
        visited[nodes[i]]=False
    #start from the first node
    visited[zero]=True
    x=zero
    max_coord=0
    d=1
    #find all codes (cycles and paths)
    if ('-a' in choose) or ('-c' in choose) or ('-p' in choose):
        GC_DFS(d,x,max_coord,bits,gc,visited,power,[],False)
    #find all codes (only paths)      
    if ('-u' in choose) or ('-b' in choose):
        q=[]
        GC_DFS(d,x,max_coord,bits,gc,visited,power,q,True)
    new_codes=[]
    temp=[]
    temp.append(zero)
    #put zero code in the beginning of the codes found
    for i in range(len(all_codes)):
        if all_codes[i]==zero:
            if len(temp)>1:
                new_codes.append(temp)
                temp=[]
                temp.append(zero)
        else:
            temp.append(all_codes[i])
        #if I am at the last code save all the codes to new_codes
        if i==(len(all_codes)-1):
            new_codes.append(temp)
    circles=[]
    paths=[]
    delta=[]
    #identify which codes are circles and which paths
    for c in new_codes:
        flag=diff_one_bit(int(c[0],2),int(c[len(c)-1],2))
        if flag:
            circles.append(c)
        else:
            paths.append(c)  
    c_delta=[]
    p_delta=[]
    #generate delta for cicles, paths and all codes
    for c in new_codes:
        temp=[]
        for e in range(0,len(c)-1):
            diff=finddiff(c[e], c[e+1])
            temp.append(bits-1-diff)
        final=finddiff(c[0], c[len(c)-1])
        if final!=None:
            temp.append(bits-1-final)
        if c in circles:
            c_delta.append(temp)
        else:
            p_delta.append(temp)
        delta.append(temp)
    #convert delta to strings
    str_delta=[]
    str_c_delta=[]
    str_p_delta=[]
    for i in range(len(delta)):
        str1 = ''.join(str(x) for x in delta[i])
        str_delta.append(str1)
        if delta[i] in c_delta:
            str_c_delta.append(str1)
        else:
            str_p_delta.append(str1)
    table=[]
    if '-a' in choose or '-u' in choose:
        table=delta
        full=new_codes
        str_table=str_delta
    elif '-c' in choose or '-b' in choose:
        if '-b' in choose and len(circles)==0:
            table=delta
            full=new_codes
            str_table=str_delta
        else:
            table=c_delta
            str_table=str_c_delta
            full=circles
    else:
        table=p_delta
        str_table=str_p_delta
        full=paths
    #prepering for printing and print solution for every case
    for i in range(len(table)):
        if table[i] in c_delta:
            if '-a' in choose or '-c' in choose:
                output='C '
            else:
                output='B '
        else:
            if '-a' in choose or '-p' in choose:
                output='P '
            else:
                output='U '    
        print(output,end="")
        print(str_table[i])
        if '-f' in choose:
            print(output,end="")
            for f in range(len(full[i])):
                if f==len(full[i])-1:
                    print(full[i][f])
                else:
                    print(full[i][f] + " ", end='')
        if '-m' in choose:
            #generate an array for every code   
            array=makeArray(full[i], bits)       
            for a in array:
                for i in range(len(a)):
                    if i<(len(a)-1):
                        print(a[i] + " ",end="")
                    else:
                        print(a[i])
    if '-r' in choose:
        #generate delta isomorfism
        delta_isomorf=isomo(c_delta,reverse(c_delta, bits))
        for d in delta_isomorf:
            print(str(d[0]) + " <=> ",end="")
            print(d[1])


if __name__ == "__main__":
   main(sys.argv[1:])
