import itertools
import sys
from operator import itemgetter

basket=[]
count=0
l1=[]
c1=set()
l={}
c={}
k=0
rules={}
dup=[]
sortedLists=[]
min_sup=0.0
min_conf=0.0


''' This is to get the one item candidate set , for each item in the row, 
we add it to the list c1 if it wasnt already there ( i.e creating a set of items ).'''
def getFirstCandidateSet():
    #print "get c1"
    global c1
    for i in basket: 
        for x in i:
            if x != '':
                c1.add(x.strip())
    c1=list(c1)
    c1 = [[x] for x in c1]
    getLargeItemSet()

'''for each item in first candidate set, we get its support and if the support is greated than min_sup, 
we add it to the first large itemset l1'''
def getLargeItemSet():
    #print "get l1"
    global c1,l1,min_sup
    for candidate in c1:
        #print candidate
        if getSupport(candidate) > float(min_sup):
            l1.append(candidate)
 
'''support(c)= number of rows in which c appears/ total number of rows in the csv,
c might contain multiple items, and hence we use a counter to check if all the items in c are present in each row, before incrementing its support value'''           
def getSupport(c):
    #print "get support"
    cnt=0
    length=len(c)
    for i in basket:
        d=0
        for j in c:
            if j in i:
                d+=1
        if d==length:
            cnt+=1
    a=float(cnt)/float(count)
    return (a)
    
'''the pruning check is done for all lists[k] whose k (k=number of items per row) values are greater than 2,
this is to check if all possible combinations of the set of items is present in the previous large itemset, 
and then only add it to ck ( candidate set for k)'''    
def prune(a,k):
    ct=0
    val=0
    for sub in itertools.combinations(a,k-1):
        ct+=1
        #print l[k-1]
        for i in range(len(l[k-1])):
            #print "a"+str(l[k-1][i])
            if list(sub) == l[k-1][i]:
                #print "sub="+str(sub)
                #print "l="+str(l[k-1][i])
                val+=1
    #print "ct="+str(ct)+"val="+str(val)
    if ct == val:
        return True
    else:
        return False
'''This is used to calculate the large itemsets and candidate sets for k values starting from 2, 
it stops when there are no more items in the previous list( l[k-1] ).
This function calls the pruning step, adds the succeeded values to candidate set c[k] and then calls getSupport to
add the succeeded values to large itemsets l[k]'''        
def getFrequentSets():
    global k
    l[1]=l1
    c[1]=c1
    k=2
    while(l[k-1]):
        l[k]=[]
        c[k]=[]
        for i in range(len(l[k-1])):
            for j in range(i+1,len(l[k-1])):
                a=[]
                x=l[k-1][i]
                #print x[:k-2]
                y=l[k-1][j]
                #print y
                if x[:k-2]== y[:k-2]:#k-2
                    a=list(set(x+y))
                    if k>2:
                        if(prune(a,k)):
                            c[k].append(a)
                    else:
                        c[k].append(a)
        #print c[k]
        for candidate in c[k]:
            if float(getSupport(candidate)) > float(min_sup):
                l[k].append(candidate)     
        k=k+1
        
'''Once we have all the large itemsets, we access each itemset from all the lists and permutate amongst them to calculate rules of the type A => B,
where A can have more than one elements but B has only one. 
We calculate (confidence of a rule A => B) = (support of A U B)/ (support of A) . 
If this value is greater than min_conf, we add it to the rules dictionary.
We remove duplicates of  type A,B => C & B,A => C by checking it in the dup list which create items of type (C,set(ABC))'''
def getConfidence():
  global k,min_conf
  for i in range(2,3):
    for j in l[i]:
        for a in itertools.permutations(j):
            if [a[-1],set(a)] in dup:
                continue
            dup.append([a[-1],set(a)])
            n=float(getSupport(j))
            #print list(a[:-1])
            m=float(getSupport(list(a[:-1])))
            conf=float(n)/float(m)
            if conf >= min_conf:
                rules[a]=(conf)
  #print rules          
  
'''This function prints the qualifying support and confidence values in sorted order to the file'''           
def printToFile(): 
    global min_sup,min_conf
    for i in range(1,k):
        for j in l[i]:
            sortedLists.append((getSupport(j)*100,j))
    sortedLists.sort(reverse=True)
    #sortedLists(sortedLists, key=itemgetter(1), reverse = True)       
    output = open("output.txt", 'w')
    print >>output,'== Frequent itemsets (min_sup=%.1f%%)' % (min_sup*100)
    for i in sortedLists:
        print >>output,str(i[1])+",%.1f %%" % i[0]
    print >>output,"\n"
    print >>output,'== High-confidence association rules (min_conf=%.1f%%)' % (min_conf*100)
    for w in sorted(rules, key=rules.get, reverse=True):
        print >>output,str([w[:-1]])+"==>"+str([w[-1]])+",(Conf: %.1f %%, Supp: %.1f%% )" % (rules[w]*100,getSupport(w)*100)
            
'''the variable basket is a list that contains each row of the csv with spaces removed, using , as the new line indicator point'''

def main():
    global count,min_sup,min_conf
    filename=sys.argv[1]                           
    min_sup=float(sys.argv[2])
    min_conf=float(sys.argv[3])
    with open(filename) as f:
        l=f.readlines()
        for i in l:
            basket.append(i.strip().split(','))
            count+=1
    #print basket
    getFirstCandidateSet()
    getFrequentSets()
    getConfidence()
    printToFile()        
 
 
main()
