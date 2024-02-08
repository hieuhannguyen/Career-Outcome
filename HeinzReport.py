'''
Description: This is the utility program that identifies employers that have hired a \
Heinz student recently (2021-2023) based on an input of job title. 

The program contains three main parts:
    1- Extracting all relevant career outcomes PDFs into a usable dataframe.
    2- Displaying all the employers that hired a Heinz student previously \
based on an inputted job title.
    3- Allowing the user to save the detailed output to a .csv

'''

import tabula # Download tabula through Anaconda: conda install -c conda-forge tabula-py
import pandas as pd
import re

def main():
    
    #Part 1-

    #Check if the user has pre-extracted data, if not extract the data (reduce processing time), if so load the data
    try:
        all_df = pd.read_csv('Heinz_Employment.csv') 
    
    except FileNotFoundError:  
        print('\nExtracting Heinz career outcome data to your system.')
        print('Do not delete \'Heinz_Employment.csv\' to save time on your next usage.')
        print('-'*50+ '\n')
        # Columns - Employer, Job Title, City, State, Degree, Year
        # Defining variables with links to Career Outcome Reports 
        mam_2022 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/mam_may2022.pdf'
        mam_2021 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/mam-2021-employment-report.pdf'

        meim_2022 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/meim_may2022.pdf'
        meim_2021 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/meim-2021-employment-report.pdf'

        msispm_2022 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/2023-one-pagers/msispm-may-2023-one-pager.pdf'
        msispm_2021 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/msispm-2022-may-graduates.pdf'
        msispm_2021_may = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/msispm-2021-graduates.pdf'

        mism_2023 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/2023-one-pagers/s23-final-one-pager-mism-bida.9-5-2023.pdf'
        mism_2022 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/2022-one-pagers/mism16-f22-final-one-pager-4-6-2023.pdf'
        mism_2021 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/mism-december-2021-graduates.pdf'

        bida_2022 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/2022-one-pagers/bida-f22-one-pager-data.pdf'
        bida_2021 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/mism-bida-december2021-graduates.pdf'

        msppm_2022 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/msppm-s22-outcome-reporting.pdf'
        msppm_2021 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/msppm-2021-employment-report.pdf'

        dc_2022 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/msppm-dc_may2022.pdf'
        dc_2021 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/msppm-dc-2021-employment-report.pdf'

        da_2022 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/msppm-da_may-2022.pdf'
        da_2021 = 'https://www.heinz.cmu.edu/heinz-shared/_files/img/career-services-pages/employment-reports/msppm-da-2021-employment-report.pdf'

        # Function to extract data from a PDF into a DataFrame using tabula library 
        # Columns 'Employer', 'Job Title', 'City', and 'State/Country'.
        def extract_data(url):
            table = tabula.read_pdf(url, pages = 'all', multiple_tables = True)
            df = table[0]
            
            #add a column for the degree program associated with the PDF (not available in the table)
            if re.search(r'mam', url) != None:
                df['Degree'] = ['MAM' for i in range(len(df))]
            elif re.search(r'meim', url) != None:
                df['Degree'] = ['MEIM' for i in range(len(df))]
            elif re.search(r'msispm', url) != None:
                df['Degree'] = ['MSISPM' for i in range(len(df))]
            elif re.search(r'bida', url) != None:
                 df['Degree'] = ['MISM BIDA' for i in range(len(df))]
            elif re.search(r'mism', url) != None:
                 df['Degree'] = ['MISM' for i in range(len(df))]
            elif re.search(r'msppm-da', url) != None:
                 df['Degree'] = ['MSPPM DA' for i in range(len(df))]
            elif re.search(r'msppm-dc', url) != None:
                 df['Degree'] = ['MSPPM DC' for i in range(len(df))]
            elif re.search(r'msdc', url) != None:
                 df['Degree'] = ['MSPPM DC' for i in range(len(df))]
            elif re.search(r'msppm', url) != None:
                 df['Degree'] = ['MSPPM' for i in range(len(df))]
            
            #add a column for the year associated with the PDF (not available in the table)
            if re.search(r'2022', url) != None:
                df['Year'] = ['2022' for i in range(len(df))]
            elif re.search(r'2021', url) != None:
                df['Year'] = ['2021' for i in range(len(df))]
            elif re.search(r'2023', url) != None:
                df['Year'] = ['2023' for i in range(len(df))]
                
            # Renaming columns for consistency
            df.rename(columns = {df.columns[0]: 'Employer', 
                                 df.columns[1]: 'Job Title', 
                                 df.columns[2]: 'City', 
                                 df.columns[3]: 'State/Country'}, 
                            inplace = True) 
            
            # Dropping first row containing column headers
            df = df.drop(0) 
            # Dropping missing values
            df.dropna(inplace = True) 
            # Resetting DataFrame index
            df = df.reset_index(drop=True) 
            return df

        # Putting the data in functions and creating DataFrames
        mam_2022_df = extract_data(mam_2022)
        mam_2021_df = extract_data(mam_2021)
        data = [mam_2022_df, mam_2021_df]
        # Concatenating DataFrames specific to a degree and resetting index
        mam_df = pd.concat(data, ignore_index=True)  

        meim_2022_df = extract_data(meim_2022)
        meim_2021_df = extract_data(meim_2021)
        data = [meim_2021_df, meim_2022_df]
        meim_df = pd.concat(data, ignore_index=True)  

        msispm_2022_df = extract_data(msispm_2022)
        msispm_2021_df = extract_data(msispm_2021)
        msispm_2012m_df = extract_data(msispm_2021_may)
        data = [msispm_2012m_df, msispm_2021_df, msispm_2022_df]
        msispm_df = pd.concat(data, ignore_index=True)

        mism_2023_df = extract_data(mism_2023)
        mism_2022_df = extract_data(mism_2022)
        mism_2021_df = extract_data(mism_2021)
        data = [mism_2021_df, mism_2022_df, mism_2023_df]
        mism_df = pd.concat(data, ignore_index=True)

        bida_2022_df = extract_data(bida_2022)
        bida_2021_df = extract_data(bida_2021)
        data = [bida_2021_df, bida_2022_df]
        bida_df = pd.concat(data, ignore_index=True)
        
        msppm_2022_df = extract_data(msppm_2022)
        msppm_2021_df = extract_data(msppm_2021)
        data = [msppm_2022_df, msppm_2021_df]
        msppm_df = pd.concat(data, ignore_index=True)

        dc_2022_df = extract_data(dc_2022)
        dc_2021_df = extract_data(dc_2021)
        data = [dc_2022_df, dc_2021_df]
        dc_df = pd.concat(data, ignore_index=True)

        da_2022_df = extract_data(da_2022)
        da_2021_df = extract_data(da_2021)
        data = [da_2022_df, da_2021_df]
        da_df = pd.concat(data, ignore_index=True)

        all_data = [mam_df, meim_df, msispm_df, mism_df, bida_df, msppm_df, da_df, dc_df]

        # Concatenating degree-wise DataFrames into one
        all_df = pd.concat(all_data, ignore_index=True) 
        # Dropping missing values
        all_df.dropna(inplace = True) 
        
        #read all data into a .csv 
        all_df.to_csv('Heinz_Employment.csv', index=False) 
    
    else:
        print('\nHeinz career outcome data successfully loaded.')
        print('-'*50+ '\n')
    
    #Part 2-

    # Get input from user for desired job title
    title = input("Enter a job title of interest to you: ") 
    
    # Filter rows based on job titles that match user input, ignoring case and missing values
    matches = all_df[all_df['Job Title'].str.contains(title, case=False, na=False)]
    
    #Finding the title in the data

    if matches.empty:
        print('\nNo matches found.')
        print('There may not be any employers on record that hired a Heinz student for the title of %s from 2021 to 2023.' %title)
        print('Navigating back to menu...')

    else:
        # Group records by Employer
        grouped = matches.groupby('Employer')[['Degree', 'Job Title']].agg(', '.join).reset_index()
        # Adding Year to grouped
        grouped['Year'] = matches.groupby('Employer')['Year'].apply(lambda x: ', '.join(x.astype(str))).reset_index()['Year']
        
        # Creating set to only include unique companies
        unique_companies = set()
        
        # Iterating through grouped DataFrame
        for index, row in grouped.iterrows():
            if row['Employer'] not in unique_companies:
                unique_companies.add(row['Employer'])
        
        # Calculating total number of students hired for user's job title
        total_students_hired = len(matches)
        print(f"\nTotal number of students hired for the given job title: {total_students_hired}")
        
        #Grouping by employers (avoid duplicated records)
        result_df = grouped[grouped['Employer'].isin(unique_companies)]
        
        #Printing the list of employers
        
        employers = result_df['Employer'].tolist()
        print('\nEmployers that have hired a Heinz students (employers with a \'*\' hired an international student): ')
        
        for i in employers:
            print(i)
        
        #Part 3-
    
        #if students want full details (degree associated with a particular employer, etc.), the program extract result into a .csv        
        print('\nDo you want detailed data of these employers (the hired students\' degree programs, years, and job titles)?')
        
        #while loop to ensure appropriate input
        choice = 0
        while choice == 0:
            choice = input('\nType \'Y\' to save details to a .csv or \'N\' to go back to menu: ').upper()
            if choice not in ('Y', 'N'):
                print('Only enter \'Y\' or \'N\'. Try again.')
                choice = 0
        
        #save a .csv file if user choose 'Y'
        #using excel, students can expand the columns and see everything instead of the columns being truncated if displayed in spyder
        if choice == 'Y':
            result_df.to_csv('Employers.csv', index=False)
            print('\nYour data has been saved as \'Employers.csv\'.')
            print('Navigate to your unzipped \'Career Outcome Program\' folder to find this file.')
        else:
            print('\nNavigating back to menu...') #main.py will automatically run the next menu loop

if __name__ == '__main__':
    main()