import csv 
import pandas as pd 

f=open("opfile.csv","w")
writer=csv.writer(f)
writer.writerow(("type","year","month","hour","arrest","domestic","loc","beat","district","ward","CommunityArea"))
with open ('ipfile.csv','r') as csvfile:
	sr= csv.reader(csvfile)
	count=0
	sr.next();
	for row in sr:
		#print row[7]
		a=row[0].split('/')
		Month= a[0]
		b= a[2].split()
		Year= b[0]
		c=b[1].split(':')
		Hour=int(c[0])
		if b[2] == 'AM':
			Hour=Hour
		else:
			Hour=Hour+12
		Type= row[1]
		LocationDescription = row[2]
		writer.writerow((Type,Hour,LocationDescription))