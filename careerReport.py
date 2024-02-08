'''
Description: This is the utility program that takes in a user's input of job title \
to compile a report with details on the title's visa sponsorship opportunities\
in 2021-2022, median annual wage in 2022, and 2022-2032 employment projection.
 

The program contains two main parts:
    1- Extract and display employment projection data (web-scraping with BeautifulSoup).
    2- Extract and display visa sponsorship data (text matching with textdistance library).

This program extracts visa data from .csv files included in the unzipped 'Career Outcome' folder.
Originally, the files for these visa data that we downloaded from the U.S. Department of Labor is in .xlsx format \
(see https://www.dol.gov/agencies/eta/foreign-labor/performance). 
However, pandas .read_excel function's processing time is signifincantly longer \
than .read_csv. Therefore, we manually use Excel to save the .xlsx files as \
.csv files and read these in instead for better processing.
    
'''

import pandas as pd
import textdistance as td 
import requests
from bs4 import BeautifulSoup

def main():
    
    int_title = input('Enter a job title of interest to you: ')
    
    #Part 1-
    
    #Check if the user has pre-extracted data. if not, extract the data. If so, load the data (reduce processing time).
    try:
        proj_data = pd.read_csv('employmentprojection.csv')
    except FileNotFoundError:
        print('\nScraping employment projection data for 2022-2023...')
        print('Do not delete \'employmentprojection.csv\' to save time on your next usage.')
        
        url = 'https://data.bls.gov/projections/occupationProj' 
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #find the table on the website and scrape it
        table = soup.find('table', {'id': 'mytable'})

        # Extract the HTML table into a Pandas DataFrame
        df_raw = pd.read_html(str(table))[0]

        # List of columns to keep for our utility
        columns_to_keep = [0, 2, 3, 5, 6, 7]
        
        # A new dataframe with the selected columns
        employment_projection = df_raw.iloc[:, columns_to_keep]
        
        # Replace Nan values with 'None Found'
        proj_data = employment_projection.fillna('None Found')

        #changing all column names from complicated tuples to the first str value in each tuple
        newCol = [proj_data.columns[i][0] for i in range(len(proj_data.columns))]
        proj_data.columns = newCol
        
        proj_data.to_csv('employmentprojection.csv', index = False)
        
        print('Scraped successfully.')
        print('-'*50+ '\n')
    else:
        print('\nEmployment projection data successfully loaded.')    
        print('-'*50+ '\n')
    
    #Matching user's input to the correct row

    rep_list_proj = proj_data['Occupation Title'].tolist() #create a list of occupation title rows

    #There are multiple titles, separated by a '*', in each row of the 'Occupation Title' column so we will split each row into a list of titles

    inter_list_proj = []
    inter_list_proj_exact = []
    for i in rep_list_proj:
        j = i.split('*') #spliting each str of a row into a list of titles
        temp_dict = {} 
        for k in j:
            k = k.replace(' Show/hide Example Job Titles','') #some str will have this unnessary part
            k = k.strip()
            #create a temp dict of each title and its similarity index (using textdistance) to the user's input 
            temp_dict[k] = td.jaccard(k.upper().split(),int_title.upper().split()) 
        m = max(temp_dict, key=temp_dict.get) # choose title with the most similarity
        if temp_dict[m] > 0.4: #if the title with the most similarity matches more than 40%
            inter_list_proj.append(i) #choose all titles in that row
            inter_list_proj_exact.append(m) #choose that specific matched title 
    
    #Employment projection display
    if inter_list_proj == []: #if there is no match
        print('Could not find data of employment projection for your job title.')
        print('-'*50+ '\n')
    else: #if there is a match
    
        #selecting the entire row in the dataframe that has the matched title into a new dataframe
        sel_rows = proj_data['Occupation Title'].isin(inter_list_proj) 
        sel_proj_data = proj_data[sel_rows] 
        
        #the scraped data is stored as str so we need to convert some columns into float but values might have NaN or are in weird formats ('>=23,000')
        try: 
            sel_proj_data = sel_proj_data.astype({'Employment Percent Change, 2022-2032': float, 'Occupational Openings, 2022-2032 Annual Average': float, 'Median Annual Wage 2022':float})
        except ValueError:
            print('The source data was coded in unsuported format. The program was unable to calculate the results.')
            print('We recommend running this option again and search with a general key word (\'data\' instead of \'data scientist\'.')
        else:
        #display the result
            print('2022-2032 EMPLOYMENT PROJECTION REPORT FOR: ',inter_list_proj_exact)
            print('\nAverage employment percent change between 2022 and 2032: %.1f' % sel_proj_data['Employment Percent Change, 2022-2032'].mean())
            print('Average occupational openings between 2022 and 2032: %.1f'% sel_proj_data['Occupational Openings, 2022-2032 Annual Average'].mean())
            print('Median wage in 2022: ${:<20,.2f}'. format(sel_proj_data['Median Annual Wage 2022'].mean()))
            print('\n\n')

    #Part 2- 
    
    #Check if the user has pre-extracted data. If not, extract the data. If so, load the data (reduce processing time).   
    try:
        visa_data = pd.read_csv('visa_data.csv',encoding='latin',index_col = False,usecols=['CASE_STATUS','VISA_CLASS','JOB_TITLE','EMPLOYER_NAME','FULL_TIME_POSITION','EMPLOYER_CITY','EMPLOYER_STATE'],low_memory=False)
    except FileNotFoundError:
        print('\nExtracting visa sponsorship data to your system.')
        print('Do not delete \'visa_data.csv\' to save time on your next usage.')
        print('-'*50+ '\n')
        #extract each .csv file
        visa_data_1 = pd.read_csv('LCA_Disclosure_Data_FY2021_Q1.csv',encoding='latin',index_col = False,usecols=['CASE_STATUS','VISA_CLASS','JOB_TITLE','EMPLOYER_NAME','FULL_TIME_POSITION','EMPLOYER_CITY','EMPLOYER_STATE'],low_memory=False)
        visa_data_2 = pd.read_csv('LCA_Disclosure_Data_FY2021_Q2.csv',encoding='latin',index_col = False,usecols=['CASE_STATUS','VISA_CLASS','JOB_TITLE','EMPLOYER_NAME','FULL_TIME_POSITION','EMPLOYER_CITY','EMPLOYER_STATE'],low_memory=False)
        visa_data_3 = pd.read_csv('LCA_Disclosure_Data_FY2021_Q3.csv',encoding='latin',index_col = False,usecols=['CASE_STATUS','VISA_CLASS','JOB_TITLE','EMPLOYER_NAME','FULL_TIME_POSITION','EMPLOYER_CITY','EMPLOYER_STATE'],low_memory=False)
        visa_data_4 = pd.read_csv('LCA_Disclosure_Data_FY2021_Q4.csv',encoding='latin',index_col = False,usecols=['CASE_STATUS','VISA_CLASS','JOB_TITLE','EMPLOYER_NAME','FULL_TIME_POSITION','EMPLOYER_CITY','EMPLOYER_STATE'],low_memory=False)
        visa_data_5 = pd.read_csv('LCA_Disclosure_Data_FY2022_Q1.csv',encoding='latin',index_col = False,usecols=['CASE_STATUS','VISA_CLASS','JOB_TITLE','EMPLOYER_NAME','FULL_TIME_POSITION','EMPLOYER_CITY','EMPLOYER_STATE'],low_memory=False)
        visa_data_6 = pd.read_csv('LCA_Disclosure_Data_FY2022_Q2.csv',encoding='latin',index_col = False,usecols=['CASE_STATUS','VISA_CLASS','JOB_TITLE','EMPLOYER_NAME','FULL_TIME_POSITION','EMPLOYER_CITY','EMPLOYER_STATE'],low_memory=False)
        visa_data_7 = pd.read_csv('LCA_Disclosure_Data_FY2022_Q3.csv',encoding='latin',index_col = False,usecols=['CASE_STATUS','VISA_CLASS','JOB_TITLE','EMPLOYER_NAME','FULL_TIME_POSITION','EMPLOYER_CITY','EMPLOYER_STATE'],low_memory=False)
        visa_data_8 = pd.read_csv('LCA_Disclosure_Data_FY2022_Q4.csv',encoding='latin',index_col = False,usecols=['CASE_STATUS','VISA_CLASS','JOB_TITLE','EMPLOYER_NAME','FULL_TIME_POSITION','EMPLOYER_CITY','EMPLOYER_STATE'],low_memory=False)

        #concatinate into one dataframe and save to .csv for future use
        visa_data = pd.concat([visa_data_1,visa_data_2,visa_data_3,visa_data_4,visa_data_5,visa_data_6,visa_data_7,visa_data_8],axis=1)
        visa_data.to_csv('visa_data.csv',index = False)
        print('Extracted successfully.')
        print('-'*50+ '\n')
    else:
        print('\nVisa data successfully loaded.')    
        print('-'*50+ '\n')
    
    
    rep_list_visa = visa_data['JOB_TITLE'].values.tolist() #a list of job title

    # Identifying titles in visa data that match user's input (similar process with textdistance as with projection data)
    
    inter_list_visa = set() #matched job title is a set so there are no repeated titles
    
    for i in rep_list_visa:
        i = str(i)
        if td.jaccard(i.upper().split(),int_title.upper().split()) > 0.4: #compare each job title to the user's input, add to set if match more than 40%
           i = i.upper().strip()
           inter_list_visa.add(i)

    # Report Summary Output For User
    
    if len(inter_list_visa) > 0: 
        print('These are the titles that match your input:\n',inter_list_visa) #prints all the titles that matched the input
        
        while True:
            sel_title = input('\nSelect title from above set to view detailed visa report for: ').upper() #allowing the user to choose the best fit title
            
            visa_data['JOB_TITLE'] = visa_data['JOB_TITLE'].apply(lambda x : str(x).upper())
            sel_visa_data = visa_data[visa_data['JOB_TITLE'] == sel_title] #selecting an entire row of data based on the user's input
            
            if len(sel_visa_data) > 0: #user chose a valid title from the list
                print('\n\n2021-2022 VISA SPONSORSHIP STATUS REPORT FOR %s' % sel_title)
                print('\nTotal visa cases for this title: ',sel_visa_data['JOB_TITLE'].count())
                print('Total visa cases certified: ',sel_visa_data[sel_visa_data['CASE_STATUS'] == 'Certified']['JOB_TITLE'].count())
                print('Total visa cases withdrawn: ',sel_visa_data[sel_visa_data['CASE_STATUS'] == 'Withdrawn']['JOB_TITLE'].count())
                print('Total visa cases denied: ',sel_visa_data[sel_visa_data['CASE_STATUS'] == 'Denied']['JOB_TITLE'].count())
                print('Top employers:')
                print('%-20s   %s' % ('# of visa sponsored', 'Employer'))
                emCount = sel_visa_data['EMPLOYER_NAME'].value_counts().nlargest(10) 
                #above is a Series of employers and total applications they filed, which is equal to how many times their name came up in the data
                for index, value in emCount.items():
                    print('{:^20d}   {:s}'.format(value, index))
                break
            else:
                print('Invalid input. Try a different title?') #user choice of title fails

    else: 
        print('Didn\'t find any titles that match the input in Visa Data. You may try this option again with a different input.')

if __name__ == '__main__':
    main()