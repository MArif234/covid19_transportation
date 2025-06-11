from datetime import datetime, timedelta
import pandas as pd
# this is the simple structure that I want to follow

date1 = datetime(2024, 10, 14)  # Year, Month, Day
date2 = datetime(2024, 9, 30)

# Subtract the dates
difference = date1 - date2

# The result is a timedelta object
print("Difference in days:", difference.days)

#Examples that we need to test: Autauga County, Alabama (1001)
# First Covid Case: 3/24/2020	
# 14 days before: 3/10/2020
# 14 days after: 4/07/2020
countyFirsts = "C:\\Users\\myral\\countyFirsts.csv"  # Double backslashes
first_covid = pd.read_csv(countyFirsts)
first_covid.head()  # Use 'first_covid' instead of 'df'
diff_dates = "C:\\Users\\myral\\Downloads\\diff_in_diff_data_use.csv" #not necessary for this
diff_covid_dates = pd.read_csv(diff_dates)
diff_covid_dates.head()
dates = "C:\\Users\\myral\\Downloads\\Trips_by_Distance_20241018 (1).csv"
dates_to_subtract = pd.read_csv(dates)
dates_to_subtract.head()
fips_firstCase_dict = dict(zip(first_covid['fips'],first_covid['firstCase']))
# created dictionary with first case of covid for each county in county_Firsts
print(fips_firstCase_dict)

import numpy as np
from datetime import datetime, timedelta
def calculate_difference(fips, mobility):
    county_event = fips_firstCase_dict.get(fips) #ex: date of first covid date is 3/12/2020
    
    date_split = county_event.split('/') # spliting on the / to separate month, date, and year
    if len(date_split) == 3: # making sure the date actually has a month, year, and day
        month, day, year = date_split # assigning the string numbers to month, year, and day
    # converting month, day, and year to integers so we can use them in datetime function
    month = int(month)
    day = int(day)
    year = int(year)
    
    start_after_covid = datetime(year=year,month=month,day=day) + timedelta(days=1) # date to use to start after 1st covid case
    fourteen_days_before = datetime(year=year, month=month, day=day) - timedelta(days=14) # 14 days before was 2/27/2020
    fourteen_days_after = datetime(year=year, month=month, day=day)  + timedelta(days=14) # 14 days after was 3/26/2020
    days_to_subtract = 14 # days for 2 week radius
    fourteen_days_before_list = []
    fourteen_days_after_list = []

    # putting all dates 2 weeks before first covid case into a list
    for i in range(days_to_subtract):
        current_date_before = fourteen_days_before + timedelta(days=i)
        fourteen_days_before_list.append(current_date_before.strftime('%m/%d/%Y'))

    # putting all dates 2 weeks after first covid case into a list
    for i in range(days_to_subtract):
        current_date_before = start_after_covid + timedelta(days=i)
        fourteen_days_after_list.append(current_date_before.strftime('%m/%d/%Y'))

    mobility_values_before = [] # mobility values two weeks before covid
    mobility_values_after = [] # mobility values two weeks after covid

    for index, row in dates_to_subtract.iterrows():
        if row['fips'] == fips: # making sure we are looking at right county
            relevant_date = row['Date']

            month1, day1, year1 = relevant_date.split('/') # taking dates and creating month, day, and year variables
            month1, day1, year1 = int(month1), int(day1), int(year1)

            # taking the date and formatting it so it can be recognized
            date_csv = datetime(year=year1, month=month1, day=day1)
            date_formatted = date_csv.strftime('%m/%d/%Y')

            # gathering the right values for 14 days before the covid date
            if date_formatted in fourteen_days_before_list:
                mobility_values_before.append(row[mobility])
               
            # gathering the right values for 14 days after the covid date
            if date_formatted in fourteen_days_after_list:
                mobility_values_after.append(row[mobility])

    # calculating the means and then taking the difference
    mean_two_weeks_before = np.nanmean(mobility_values_before)
    mean_two_weeks_after = np.nanmean(mobility_values_after)
    difference = mean_two_weeks_after - mean_two_weeks_before
    return difference

# Main body of the program
results_list = [] #going to gather all of the results for the counties
mobility_columns = ['Population_Staying_at_Home','Population_Not_Staying_at_Home', 'Number_of_Trips', 'Number_of_Trips_<1', 
                    'Number_of_Trips_1-3', 'Number_of_Trips_3-5', 'Number_of_Trips_5-10', 'Number_of_Trips_10-25',
                    'Number_of_Trips_25-50', 'Number_of_Trips_50-100', 'Number_of_Trips_100-250', 'Number_of_Trips_250-500',
                    'Number_of_Trips_>=500'] # all of the types of mobility
for fips in dates_to_subtract['fips'].unique():
    results_dict = {"fips": fips}

    for mobility_column in mobility_columns:
        result = calculate_difference(fips, mobility_column) # calculates the difference 
        results_dict[mobility_column] = result # labels the difference with the correct type of mobility
    results_list.append(results_dict)
    
two_week_covid_span_df = pd.DataFrame(results_list) # putting all the results into a data frame
two_week_covid_span_df.to_csv('two_week_covid_span_df.csv', index=False)  # turns the data frame into a csv file 