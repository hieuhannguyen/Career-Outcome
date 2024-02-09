#  Career Outcome Program
## A collaborative final project for Python II

### Abstract
This is a program that leverages web scraping and text mining techniques to compile relevant data from diverse sources into a comprehensive career report for job titles of interest to Heinz students.

The program gives the user three options:
1.	List employers that hired from Heinz from 2021 to 2023 based on a student’s interested job title.
2.	Report employment projection estimate and visa sponsorship approval rates for a job title. 
3.	Compare cost of living between 2 cities in the U.S. (to help students estimate relocation differences).

All data extracted are cleaned and stored as pandas DataFrames in the program. For data sources that require long extraction time, we only need the user to extract the data once as their results will be saved as a .csv in the user’s laptop.

The program used two special Python libraries:
1.	Tabula: Used to extract tabular data from PDFs. 
2.	Textdistance: Used to match the user’s inputted job titles with titles in the employment projection and visa sponsorship data if they are 40% similar (do not need to be exact).

We also use common libraries such as pandas, regex, json, beautiful soup, and requests. 

***I exclusively coded main.py and CPI.py.***

### User Instruction
1. Due to github's limits on file size, the code and the data must be downloaded separately. Please use this [link](https://drive.google.com/file/d/1dPc7BhG2KewUXLcJMNntwmmum2ZLm3A9/view?usp=sharing) to access our data.
2. Extract all .csv files in career_data.zip into the same folder as all files in this repo.
3. Install tabula for Python following [these](https://pypi.org/project/tabula-py/) instructions.
4. Run main.py in any Python interpreter. Do not execute other .py files.
   - Example of an input to enter when prompted for a Job title: ‘DATA ENGINEER’
   - Example of an input to enter when prompted for a city: ‘Pittsburgh’
   - Example of an input to enter when prompt for the city’s state: ‘PA’

### Data Sources
1.	**Heinz Career Report:** Heinz publishes report of career outcomes for each degree program as PDFs on their [website](https://www.heinz.cmu.edu/current-students/career-services/employment-information-salary-statistics#msppm). 
2.	**Employment Projection & Visa Sponsorship Data:** Employment projection is scraped from the Bureau of Labor Statistics [website](https://data.bls.gov/projections/occupationProj) using BeautifulSoup. Visa sponsorship data are LCA applications (.xlxs) downloaded from the U.S. Department of Labor’s [website](https://www.dol.gov/agencies/eta/foreign-labor/performance) then converted to (.csv) using Excel. 
3.	**Consumer Price Index (Cost of Living data):** We query the public API of the Bureau of Labor Statistics, following their explicit instructions on their [website](https://www.bls.gov/developers/home.htm). 

### Additional Notes
1.	What are the CSVs and text files?
   - 2 years' quarter-wise visa H1B visa data (LCA_Disclosure_Data_FYYYY_QN)
   - census.csv and areacode_main.txt: state-region-division master files which are referenced in the cost-of-living utility to match input city-state choice to extracted CPI data
   - areacode.txt: the full area code available to query with notes on how it was manually cleaned for the program
     
2.	What are the .py files not executed? These files contain the codes for each menu option; all are imported to main.py.
   - 'CPI.py': Extracts CPI data, and matches user input to show cost-of-living comparison
   - 'HeinzReport.py': Extracts Heinz career reports for career outcome analysis and summarization
   - 'careerReport.py': Use H1B visa information and extracts employment projection data to present information relevant to user
