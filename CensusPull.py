API_KEY='75f5755a25d265ecf2a0a5165f4d9e0a1b379433' #requested from api.census.gov

from us import states #python wrapper for census api that had fids utils
import requests, pandas, os
#year of acs data
year=2013
#string to specify geo region
geoLimit='&for=county:*&in=state:' + states.CA.fips + '&key=' + API_KEY
api_url_base = 'http://api.census.gov/data/'+str(year)+'/acs5?get=NAME,'

#-------- Set up income brackets to pull from census
#Look at data for number of households in each income bracket
#vars in http://api.census.gov/data/2013/acs5/variables.html
#---------

#edges of brackets in thousands (from vars above)
brackets=[0]+range(10,50,5)+[50, 60, 75, 100, 125, 150, 200, 300] #in thousands
#compute median income of each bracket for computation later
medianIncomes=[(brackets[b]+brackets[b+1])/2. for b in range(len(brackets)-1)]

#key for income db vars
valKeys=['B19001_0%02dE'%i for i in range(2, 18)]
#key for income db margin of error vars (not currently used)
errKeys=['B19001_0%02dM'%i for i in range(2, 18)]


def computeGini(dist):
	#first calculate average as median*n/(sum(n)) where n is households in each bracket
	avgIncome=sum([m*n for m,n in zip(medianIncomes, dist)])/sum(dist)
	#now calculate abs difference by looping over all pairs of brackets
	sumAbsDiff=0.

	for i in range(len(medianIncomes)):
		for j in range(len(medianIncomes)):
			sumAbsDiff+=dist[i]*dist[j]*(abs(medianIncomes[i]-medianIncomes[j]))
	#divide sum by number of pairs
	avgAbsDiff=sumAbsDiff/(sum(dist)**2)
	return avgAbsDiff/(2.*avgIncome)

def getIncomeDist(geoLoc):
	api_url=api_url_base+','.join(valKeys)+geoLimit+'&key='+API_KEY
	r=requests.get(api_url)
	data=r.json()
	incomeDict=dict()
	for d in data[1:]:
		incomeDict[d[0]]=[float(x) for x in d[1:1+len(valKeys)]]
	return incomeDict


#test here
incomeDist=getIncomeDist(geoLimit)
for k in incomeDist.keys():
	gini=computeGini(incomeDist[k])
	print k,gini







