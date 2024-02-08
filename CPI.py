"""
Description: This is the utility program that converts cost of living between \
two inputted cities in the U.S. based on data within the last 3 years.

The program has two main parts:
    
    1- Extracting the necessary data
    
    *Notes:
        This utility query API from the U.S. Bureau of Labor Statistics (BLS):
        https://www.bls.gov/developers/home.htm 
        using "Series ID": https://www.bls.gov/help/hlpforma.htm#CU
        
        We are interested in the CPI data that is not seasonally adjusted \
        (more data), sampled/observed monthly, is more recent, and for all \
        items. The area code helps query the exact CPI for a specific area.
        
        In short, our "Series ID" format is 'CUUR%sSA0' % (areaCode).
        
        The BLS did not calculate CPI for all cities but grouped CPIs by \
        region division in the census (northeast, pacific, etc.). However, \
        some cities have their own CPI dataset, maybe because prices there \
        are significantly higher than other cities in the same state.
        
        For this utility, if the user input a city that has its own dataset,\
        the program will use that city's area code. If the user input a city \
        that does not have its own dataset or a city that does not exist,\
        the program default to the area code of the census region division \
        containing the state of the city.
        
        These are the area code: https://download.bls.gov/pub/time.series/cu/cu.area
        
        It is copied and pasted into a text document, called 'areacode_main.txt' \
        in the folder, which the program will use. We clean this text file \
        manually for easier text processing. Detailed notes on how it was edited \
        is included in 'areacode.txt'.
        
        To avoid manually creating a dictionary of census region divisions and \
        their corresponding states, the program will also use census.csv downloaded from GitHub
        https://github.com/cphalpert/census-regions/blob/master/us%20census%20bureau%20regions%20and%20divisions.csv
        

    2- Coding the input and comparison methods
    
    *Notes: The CPI is only one part of the "cost of living index." This index \
    is used in a simple formula of [(City B – City A)/City A] x 100 to give \
    the change in cost of living. With the purpose of simplifying this program \
    for this class, we will assume the CPI is the cost of living index and\
    apply it to the formula.
    
"""
import pandas as pd
import requests
import json
from datetime import datetime

def main():
    #Part 1-
    
    #getting current year so the program can run in perpetuity
    year = datetime.now().year
    
    #read each line in areacode_main.txt into a list of str
    areacode = []
    with open('areacode_main.txt', 'r') as file:
        for line in file:
            line = line[:-1].split('\t')
            areacode.append(line)

    #split main list into 2 lists, one for region and one for cities
    regionstr = areacode[1:10]
    citystr = areacode[10:] 

    #read list of region str into a dataframe of region and areacode
    regionDF = pd.DataFrame(regionstr, columns = areacode[0])

    #then clean the columns and set the region names as index for searching with .loc later
    regionDF.drop(['display_level','selectable','sort_sequence'], axis=1, inplace=True)
    regionDF.set_index('area_name', inplace=True)

    #create a dataframe for cities' name, their corresponding state, and areacode
    cities = [] 

    for i in citystr: #spliting each str item in the city list, i will have the format [area_code, area_name]
        i[1] = i[1].split(',') #results in a list like [area_code, [cities, state]]
        i[1][0] = i[1][0].split('-') #results in a list of list like [areacode, [[city1, city2], state]]
        i[1][1] = i[1][1].strip() #removing white spaces from state code (the white space in 'city, state' is splitted with the state)
        temp = i[1]  #taking the list of city & state out temporarily 
        if len(temp[0])>1: #if the list has more than 1 city, append each city with the state and area code to the list [[city1, state, area_code], [city2, state, area_code]]
            for c in temp[0]:
                cities.append([c,temp[1],i[0]]) 
        else:
            cities.append([temp[0][0],temp[1],i[0]]) #if the list has only 1 city, append the city, its state, and area_code

    citiesDF = pd.DataFrame(cities, columns = ['City', 'State', 'Area Code']) #convert list of list into dataframe of cities, their corresponding state, and their area_code

    #adding canonical city names data for search methods
    temp = pd.DataFrame(citiesDF['City'].apply(str.upper))
    temp.rename(columns = {'City':'CITY'}, inplace=True)
    citiesDF = pd.concat([citiesDF, temp], axis=1)
    citiesDF.set_index('CITY', inplace=True) #setting canonical city name as index for search 

    #read the census.csv file into a dataframe of region and states
    censusDF = pd.read_csv('census.csv')
    censusDF.set_index('State Code', inplace=True) #setting state code as index for search 

    #function to search for area code
    def CityorState(userCity, userState):    
        result = 0
        for index, row in citiesDF.iterrows():
            if (index == userCity) and (row['State'] == userState): #only matches if both city name and state code match
                result = row['Area Code']
        if result == 0: #if city doesn't match, use state code to get area code
            if userState in censusDF.index:
                searchKey = censusDF.loc[userState, 'Division']
                result = regionDF.loc[searchKey, 'area_code']
            else:
                print('Could not find your state in the census data.')
        return result

    #Part 2-

    #coding inputs and convert to area code
    print('\nYou will input your interested cities and their respective states below. ')
    print('Please do not abbreviate the city\'s name (type \'New York\' instead of \'NYC\').')
    print('Please only enter 2-character state codes (\'OH\' for \'Ohio\').')
    
    while True:
        cityFrom = input('\nWhich city are you converting from? ').strip()
        stateFrom = input('What is the state of this city? ').strip()
        if len(stateFrom) != 2: #state need to be a 2-character code
            print('You need to enter a 2-character state code. Please try again.')
            continue
        codeA = CityorState(cityFrom.upper(), stateFrom.upper())
        break

    while True:
        cityTo = input('\nWhich city are you converting to? ').strip()
        stateTo = input('What is the state of this city? ').strip()
        if len(stateTo) != 2:
            print('You need to enter a 2-character state code. Please try again.')
            continue
        codeB = CityorState(cityTo.upper(), stateTo.upper())
        if cityFrom.upper() == cityTo.upper() and stateFrom.upper() == stateTo.upper(): 
            #check if user enter the same place
            print('You have entered the exact same place... Please try again.')
            continue
        else:
            break

    #function to compare CPI, A is city to convert from, B is city to convert to
    def compare(CityA, CityB):
        delta = (CityB-CityA)/CityA
        if delta < 0:
            conclude = 'more'
        else:
            conclude = 'less'
        print('%s, %s is about %.2f percent %s expensive than %s, %s.' % (cityFrom.title(),stateFrom.upper(), abs(delta*100), conclude, cityTo.title(),stateTo.upper()))

    #if the two states are the same census division:
    if codeA == codeB:
        print('\nThere may not be a significant difference in cost of living between %s, %s and %s, %s.' %(cityFrom.title(), stateFrom.upper(), cityTo.title(), stateTo.upper()))
    else: #querying the data in the last three years
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"seriesid": ['CUUR%sSA0' % codeA,'CUUR%sSA0' % codeB],"startyear":str(year-3), "endyear":str(year)})
        response = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            
        results  = data['Results']['series']
        
        #handling no data results - the BLS may or may not collect recent data for a certain city
        newCodeA = 0
        newCodeB = 0
        print('')
        if len(results[0]['data']) == 0: #cityFrom has no data
            print('The Bureau of Labor Statistics did not collect cost of living data for %s, %s in the last three years.' % (cityFrom.title(), stateFrom.upper()))
            searchKey = censusDF.loc[stateFrom.upper(), 'Division'] #changing the areacode from its city to the areacode of the city's state
            newCodeA = regionDF.loc[searchKey, 'area_code']
        if len(results[1]['data']) == 0: #cityTo has no data
            print('The Bureau of Labor Statistics did not collect cost of living data for %s, %s in the last three years.' % (cityTo.title(), stateTo.upper()))
            searchKey = censusDF.loc[stateTo.upper(), 'Division']
            newCodeB = regionDF.loc[searchKey, 'area_code']
            
        if (newCodeA != 0) or (newCodeB != 0): #if one of the inputs do have result in data, search by state for that input
            print('\nBecause of missing data, the program will search by state instead of city, which will take more time.')
            print('Keep in mind that the result now may not be as accurate.\n')
            if newCodeA == 0: #keep the area code for input has data
                newCodeA = codeA
            if newCodeB == 0:
                newCodeB = codeB
            if newCodeA == newCodeB:
                print('There may not be a significant difference in cost of living between %s, %s and %s, %s.' %(cityFrom.title(), stateFrom.upper(), cityTo.title(), stateTo.upper()))
            else:
                headers = {'Content-type': 'application/json'}
                data = json.dumps({"seriesid": ['CUUR%sSA0' % newCodeA,'CUUR%sSA0' % newCodeB],"startyear":str(year-3), "endyear":str(year)})
                response = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
                if response.status_code == 200:
                    data = json.loads(response.content.decode('utf-8'))
                results  = data['Results']['series']
                
                #extracting cityA and cityB's CPIs for comparison
                CPIA = float(results[0]['data'][0]['value']) 
                CPIB = float(results[1]['data'][0]['value'])
                compare(CPIA, CPIB)
        else: 
            CPIA = float(results[0]['data'][0]['value'])
            CPIB = float(results[1]['data'][0]['value'])
            compare(CPIA, CPIB)

if __name__ == '__main__':
    main()