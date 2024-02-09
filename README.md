#  Career Outcome Program
## A collaborative final project for Python II

### Abstract
This is a program that leverages web scraping and text mining techniques to compile relevant data from diverse sources into a comprehensive career report for job titles of interest to Heinz students.

The program gives the user three options:
1.	List employers that hired from Heinz from 2021 to 2023 based on a student’s interested job title.
2.	Report employment projection estimate and visa sponsorship approval rates for a job title. 
3.	Compare cost of living between 2 cities in the U.S. (to help students estimate relocation differences).

I exclusively coded main.py and CPI.py


### Data Sources
1.	***Heinz Career Report:*** Heinz publishes report of career outcomes for each degree program as PDFs on their [website](https://www.heinz.cmu.edu/current-students/career-services/employment-information-salary-statistics#msppm). 
2.	**Employment Projection & Visa Sponsorship Data:** Employment projection is scraped from the Bureau of Labor Statistics [website](https://data.bls.gov/projections/occupationProj) using BeautifulSoup. Visa sponsorship data are LCA applications (.xlxs) downloaded from the U.S. Department of Labor’s [website](https://www.dol.gov/agencies/eta/foreign-labor/performance) then converted to (.csv) using Excel. 
3.	**Consumer Price Index (Cost of Living data):** We query the public API of the Bureau of Labor Statistics, following their explicit instructions on their [website](https://www.bls.gov/developers/home.htm). 

### Additional Notes
1.	What are the CSVs and text files?
-	2 years’ quarter-wise visa H1B visa data (LCA_Disclosure_Data_FYYYY_QN)
-	census.csv and areacode_main.txt: state-region-division master files which are referenced in the cost-of-living utility to match input city-state choice to extracted CPI data
-	areacode.txt: the full area code available to query with notes on how it was manually cleaned for the program

2.	What are the .py files not executed?
These files contain the codes for each menu option; all are imported to main.py.
Each of these files has explanatory comments. Summary overview below:
-	‘CPI.py’: Extracts CPI data, and matches user input to show cost-of-living comparison
-	‘HeinzReport.py’: Extracts Heinz career reports for career outcome analysis and summarization
-	‘careerReport.py’: Use H1B visa information and extracts employment projection data to present information relevant to user
