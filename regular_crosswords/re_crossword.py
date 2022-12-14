import sys
import sre_yield
import string


#fills the gaps in worddict with the characters of the chosen word  
def fillthegaps(w,worddict,numdict):
    #checks if the word is already filled
    if worddict[w].count(".")!=len(worddict[w]):
        #finds neighbors in order to fill the positions that are crossed
        neigh=numdict[w]
        for n in range(0,len(neigh),2):         
            herpos=neigh[n+1]          
            nowlist=numdict[neigh[n]]       
            for now in range(0,len(nowlist),2):
                if nowlist[now]==w:
                    mypos=nowlist[now+1]
                    herword=worddict[neigh[n]]           
                    tempword=list(herword)
                    myword=worddict[w]  
                    if myword[mypos]!=herword[herpos]:
                        change=myword[mypos]
                        tempword[herpos]=change
                        worddict[neigh[n]]="".join(tempword)
    return worddict

#finds the most suitable expressions to fill the word out
def findmatch(w,word,worddict,numdict,reguralList,reguralFlag):   
    match, mdict=[], {}
    for reg in reguralList:
        #checks if the expression is used
        if reguralFlag[reguralList.index(reg)]==False:
            match=[]
            #produces all the strings of the expression
            temp=set(sre_yield.AllStrings(reg,max_count=5,charset=string.ascii_uppercase))
            #keeps only the ones that have the same lengh with the word           
            filtered = [x for x in temp if len(x)==len(word)]
            #checks if the string matches the gaps or the filled characters of the word        
            for f in filtered:                  
                flag1=False             
                for i in range(len(word)):
                    if word[i]=='.' or f[i]==word[i]:
                        flag1=True
                    else :
                        flag1=False
                        break                
                if flag1:
                    match.append(f)
            if len(match)!=0:
                mdict.setdefault(reg,[])
                for m in match:  
                    mdict[reg].append(m)                                                                          
    return mdict

     
#finds the next word from a path that has the biggest ration: filled_gaps/word_lengh
def findnext(graph,position,path,worddict,flag):
    lengh, filled, ratio={}, {}, {}
    #calculates all ratios of the words in the path
    for vertex in path:
        lengh[vertex]=len(worddict[vertex])
        filled[vertex]=lengh[vertex] - worddict[vertex].count(".")
        ratio[vertex]=filled[vertex]/lengh[vertex]
    #if flag is true and we have more than one max ratios we choose the one that
    #is a neighbor to the word that we just filled
    if flag:        
        values=ratio.values()
        maxvalue=max(values)
        temp=list(graph[position])
        for vertex in ratio:
            if ratio==maxvalue and vertex in temp:
                return vertex
    return max(ratio,key=ratio.get)
    
#Depth-first search that backtracks when we reach a word that can't be filled with any expression
def solve_recursive(graph,position,worddict,intersect,reguralList,reguralFlag,path,result={}):
    #checks if there are remaining unfilled words
    if len(path)>0:
        vertex=findnext(graph,position,path,worddict,True)
        #all strings that match the word
        possible=findmatch(vertex,worddict[vertex],worddict,intersect,reguralList,reguralFlag)
        #if we found matches
        if bool(possible):
            path.remove(vertex)
        else:
            return result
        #save the previous state of the crossword
        before=worddict[vertex]
        #try different string to find a match that doesn't cause backtracking
        for key in possible:         
            for i in (possible[key]):
                worddict[vertex]=i
                #fill the gaps of the word with the string                          
                worddict=fillthegaps(vertex,worddict,intersect)
                #apply changes to the result dictionary
                result.pop(vertex,None)
                result.setdefault(vertex,[])
                result[vertex].append(key)
                result[vertex].append(i)
                reguralFlag[reguralList.index(key)]=True
                #recursion               
                solve_recursive(graph,vertex,worddict,intersect,reguralList,reguralFlag, path,result)
                if len(path)==0:
                    break
            if len(path)==0:
                break
            #if an expression causes backtracking
            reguralFlag[reguralList.index(key)]=False
        #when there isn't any expressions that can fill a word
        if len(path)>0:
            path.append(vertex)
            worddict[vertex]=before
            #return words to the previous state
            worddict=fillthegaps(vertex,worddict,intersect)
            #backtracks here
            return result
    return result


def main(argv):
    crossword_file=sys.argv[1]
    regural_expressions_file=sys.argv[2]
    #read crossword file
    with open(crossword_file, 'r') as file:
       cross = file.readlines()
       cross = [row.split(',') for row in cross]
    V, reguralList = [], []
    numdict, mydict,worddict = {}, {},{}
    #read regular expressions file    
    with open(regural_expressions_file, 'r') as l:
        reguralList=l.readlines()
    reguralList=[x.replace("\n","") for x in reguralList]
    #add mydict crossword data in two dictionaries
    for row in cross:
        #save path of words
        V.append(int(row[0]))
        #save every character in a dictionary            
        worddict[int(row[0])]=str(row[1])
        mydict.setdefault(int(row[0]),[])
        for i in range(2,len(row),2):
           mydict[int(row[0])].append(int(row[i]))
        #save the position where the words are crossed
        numdict.setdefault(int(row[0]),[])
        for j in range(2,len(row)):
            numdict[int(row[0])].append(int(row[j]))
    #create array to keep track of used expressions                                  
    reguralFlag=[False]*len(reguralList)
    #fill the gaps for the already completed words
    for w in worddict:
        worddict=fillthegaps(w,worddict,numdict)
    #finds the best word to start  
    start=findnext(mydict,0,V,worddict,False)
    #solves the crossword
    solution=solve_recursive(mydict,start,worddict,numdict,reguralList,reguralFlag,V)
    #print solution
    for key in sorted(solution):
        print(str(key) + " " + solution[key][0] + " " + solution[key][1])

    
if __name__ == "__main__":
   main(sys.argv[1:])