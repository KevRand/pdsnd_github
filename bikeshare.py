import time
import pandas as pd
import numpy as np


CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n Hello! Let\'s explore some US bikeshare data!')
    time.sleep(.75)
    
    #Gets user input for city & handles invalid inputs
    city=""
    while True:
        city =(input("\n What city would you like to search by? Please enter one of the following cities - New York, Washington or Chicago \n"))
        if city.title() in ["New York" , "Washington" , "Chicago"]:
            city=city.title()
            break
        else:
            print("Sorry, that was an invalid input")
    
    # Gets user input for month and handles invalid inputs
    month=""
    while True:
        month= (input("\n Now, would you like to filter by month? \n If so, please type the full month from January-June \n or type 'All' to look at data from every month \n"))
        if month.title() in ["January" , "February" , "March" , "April" , "May" , "June" , "All"]:
            month=month.title()
            break
        else:
            print("Sorry, that was an invalid input")
   
    # Gets user input for day and handles invalid inputs
    day=""
    while True:
       day= (input(" \n Finally, would you like to filter by day? \n If so, please type the full day \n or type 'All' to look at data from every day \n"))
       if day.title() in ["Sunday" , "Monday" , "Tuesday" , "Wednesday" , "Thursday" , "Friday" , "Saturday" , "All"]:
           day=day.title()
           break
       else:
           print("Sorry, that was an invalid input")
            
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # loads data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converts the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extracts month and day from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day"] = df["Start Time"].dt.weekday_name

    # filters by month if applicable
    if month != "All":
        # use the index of the months list to get the corresponding int
        months = ["January" , "February" , "March" , "April" , "May" , "June"]
        month = months.index(month) + 1

        # filters by month to create the new dataframe
        df = df[df["month"] == month]

    # filters by day if applicable
    if day != "All":
        # filters by day to create the new dataframe
        df = df[df["day"] == day.title()]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculates and displays most common month (if filtering by month, will list that month as most common)
    month_count=df["month"].value_counts()
    month_di=month_count.to_dict()
    month_max=max(month_di, key=month_di.get)
    if month_max is 1:
        print ("The most common month is - January")
    elif month_max is 2:
        print ("The most common month is - February")
    elif month_max is 3:
        print ("The most common month is - March")
    elif month_max is 4:
        print ("The most common month is - April")
    elif month_max is 5:
        print ("The most common month is - May")
    elif month_max is 6:
        print ("The most common month is - June")

    # Calculates and displays most common day (if filtering by day, will list that day as most common)
    day_count=df["day"].value_counts()
    day_di=day_count.to_dict()
    day_max=max(day_di, key=day_di.get)
    print("The most common day is -",day_max)

    # Calculates and displays most common start hour
    df2=df
    df2["start_hour"] = df2["Start Time"].dt.strftime('%H')
    sthr_count=df2["start_hour"].value_counts()
    sthr_di=sthr_count.to_dict()
    sthr_max=max(sthr_di, key=sthr_di.get)
    print("The most common start hour is -",sthr_max)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calculates and displays most common start station
    start_count=df["Start Station"].value_counts()
    start_di=start_count.to_dict()
    start_max=max(start_di, key=start_di.get)
    print("The most common start station is -",start_max)

    # Calculates and displays most common end station
    end_count=df["End Station"].value_counts()
    end_di=end_count.to_dict()
    end_max=max(end_di, key=end_di.get)
    print("The most common end station is -",end_max)

    # Concats start & end stations to calculate & display most common trip from start to end
    df["trip_comb"]=df["Start Station"] + ' / ' + df["End Station"]
    comb_count=df["trip_comb"].value_counts()
    comb_di=comb_count.to_dict()
    comb_max=max(comb_di, key=comb_di.get)
    print("The most common trip from start to end station is -",comb_max)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculates & displays total travel time in hours and minutes
    total_tt =float(df["Trip Duration"].sum())
    hrtot=total_tt/3600
    mintot=round(hrtot%1,2)
    minutetot=int((mintot*100)*.60)
    hourtot=int(hrtot)
    print("The total travel time across every trip is - ",hourtot,"hrs &",minutetot,"mins")

    # Calculates average (by mean) travel time in hours and mintues
    mean_tt =float(df["Trip Duration"].mean())
    hrmean=mean_tt/3600
    minmean=round(hrmean%1,2)
    minutemean=int((minmean*100)*.60)
    hourmean=int(hrmean)
    print("The average travel time across every trip is - ",hourmean,"hrs &",minutemean,"mins")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculates and displays user type counts
    utypes_count=df["User Type"].value_counts()
    print(utypes_count, "\n")
    

    # Calculates and displays gender counts (Washington gender data not available)
    if city == "Washington":
        print("No gender data available \n")
    else:
        gen_count=df["Gender"].value_counts()
        print(gen_count, "\n")
        
    # Calculates and displays earliest, most recent & most common year of birth
    if city == "Washington":
        print("Birth year data not available")
    else:
        rec_birth= int(df["Birth Year"].max())
        earl_birth= int(df["Birth Year"].min())
        cb_count=df["Birth Year"].value_counts()
        cb_di=cb_count.to_dict()
        cb_max=int(max(cb_di, key=cb_di.get))
        print ("The most recent year of birth is - ",rec_birth)
        print ("The earliest year of birth is - ",earl_birth)
        print("The most common year of birth is -",cb_max)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Runs & restarts program if the user wishes too
def main();
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'yes':
            continue
        else:
            print("Ok, Good Bye")
            break
if __name__ == "__main__":
    main()        
