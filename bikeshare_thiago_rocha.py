import time
import datetime as dt
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
    print('='*60, '[̲̅w̲̅є̲̅l̲̅c̲̅σ̲̅м̲̅є̲̅]','='*60, '\n', 'HELO! LET\'S EXPLORE SOME US BIKESHARE DATA!')
    
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    city = input("Enter a city (Chicago, New York or Washington):")
    while(city != "Chicago") and (city != "New York") and (city != "Washington"):
        city = input("Please, enter a valid city (Chicago, New York or Washington):")
    time_filter = input("Would you like to see a day, month, both or not at all time filter(type 'none' if you don't for all month/weekdays)?:")  
    while (time_filter != "month") and (time_filter != "day") and (time_filter != "both") and (time_filter != "none"):
        time_filter = input("Please, type one of valid options:")
    if time_filter == "day":
        day = input("Select a day (Monday, Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday): ")
        while (day !="Sunday") and (day !="Monday")and (day !="Tuesday") and (day !="Wednesday") and (day !="Thursday") and (day !="Friday") and (day !="Saturday"):
              day = input("Please, enter a valid value:")
        month = "all"
    elif time_filter == "month":
        month = input ("Select a month between January and June or type 'all' for all: ")
        while (month != "January") and (month != "February") and (month != "March") and (month != "April") and (month != "May") and (month != "June") and (month != "all"):
            month = input ("Select a month between January and June: ")
        day = "all"
    elif time_filter == "none":
        day = "all"
        month = "all"
    elif time_filter =="both":
        day = input("Select a day (Monday, Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday): ")
        while (day !="Sunday") and (day !="Monday")and (day !="Tuesday") and (day !="Wednesday") and (day !="Thursday") and (day !="Friday") and (day !="Saturday"):
              day = input("Please, enter a valid weekday name:")
        month = input ("Select a month between January and June: ")
        while (month != "January") and (month != "February") and (month != "March") and (month != "April") and (month != "May") and (month != "June") and (month != "all"):
            month = input ("Select a month between January and June or type 'all' for all: ")
    print('='*120)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # loading data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    """ 
    Another way to do this using conditions:
    def get_data(city, month, day):
        if city == "Chicago":
            file = open('project/chicago.csv')
        elif city == "New York":
            file = open('project/new_york_city.csv')
        elif city == "Washington":
            file = open('project/washington.csv')
        df = pd.read_csv(file)
        return df
    """
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

#to display the city name, we add the city variable as a entry parameter in this function
def time_stats(df,city):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    #calculating the process time
    start_time = time.time()
    #bring the "Start Time" field to datetime type (to extract hour, day, month)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    month = df['month'].mode()[0]
    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    day = df['day_of_week'].mode()[0]
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour = df['hour'].mode()[0]
    
    # display total count of trips
    total_trips = df['Start Station'].count()
    
    #total trips
    print("\nTotal of trips in " , city , " :" , total_trips)
    
    #print the day preference (or selected)
    print("\nPrefered Weekday: " , day)
        
    #print the month preference (or selected)
    print("\nPrefered Month: " , month)
    
    #print the hour preference
    print("\nPrefered Hour: " , hour , "hs")
    
    #total processing time message
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*120)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station (qty and station name)
    start = df['Start Station'].value_counts().max()
    start_name = df['Start Station'].mode()[0]

    
    # display most commonly used end station
    end = df['End Station'].value_counts().max()
    end_name = df['End Station'].mode()[0]
    
        
    # display most frequent combination of start station and end station trip
    start_end = df[['Start Station', 'End Station']].mode().loc[0]
    
    #printing the results
    print("\nBest start station:\n", start_name, " | ", start, " trips"  )
    print("\nBest end station:\n" ,end_name, " | ",end, " trips")
    print("\nBest combination station:\n" ,start_end)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*120)


def trip_duration_stats(df,city):
    """Displays statistics on the total and average trip duration.
       Unfortunately the 'washington' dataset doesn't have the gender & birth year columns
       To display the city name, we add the city variable as a entry parameter in this function.
       We add 2 if clauses (to calculate and print) the  'gender stats', using groupby function
    """
    #calculating the process time message
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    
    # display mean travel time (general, user type(using groupby function))
    duration = df['Trip Duration'].mean()
    duration_max = df['Trip Duration'].max()
    duration_min = df['Trip Duration'].min()
    duration_by_user_type = df.groupby(['User Type']).mean()['Trip Duration']
    
    
    # display mean travel time by gender (unfortunately the 'washington' dataset doesn't have the gender column)
    if city != "Washington":
        duration_by_gender = df.groupby(['Gender']).mean()['Trip Duration']
  
    #print al the results. As we said, we're using a if clause to print the "Gender Avg" data, for city washington
    print("\nTotal time trip" , total_time, "s")
    print("\nAverage time of trips (in seconds): ", duration, "s")
    print("\nAverage time of trips (in seconds) by user type: ", duration_by_user_type, "s")
    print("\nMax duration of trips (in seconds): ", duration_max, "s")
    print("\nMin duration of trips (in seconds): ", duration_min, "s")
    
   
    if city != "Washington":
        print("\nAverage time of trips (in seconds) by gender: ", duration_by_gender, "s")
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*120)


def user_stats(df,city):
    """Displays statistics on bikeshare users.
       Unfortunately the 'washington' dataset doesn't have the gender & birth year columns
       To display these stats, we add the 'city' variable as a entry parameter in this function.
       We add 2 if clauses (to calculate and print) the  'gender stats', using groupby function
    """
    
    #calculating the process time
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of gender (unfortunately the 'washington' dataset doesn't have the gender column)
    if city != "Washington":
        user_gender = df['Gender'].value_counts()

    # Display counts of user type
    user_types = df['User Type'].value_counts()
    
    # Display youngest user by Birth Year and AGE (except for washington)
    if city != "Washington":
        most_recent = df['Birth Year'].max()
        most_recent_age = 2020 - most_recent
    
    # Display oldest user by Birth Year and AGE, and most common year of birth/AGE (except for washington)
    if city != "Washington":
        most_old = df['Birth Year'].min()
        most_old_age = 2020 - most_old
        most_popular_year = df['Birth Year'].mode()[0]
        most_popular_age = 2020 - most_popular_year
    
    #priting the results
    if city != "Washington":
        print("\nUsers by gender:\n" , user_gender)
        print("\nYoungest User:\n", most_recent, " | ",  most_recent_age , "yrs old" )
        print("\nOldest User:\n", most_old, " | ",  most_old_age , "yrs old" )
        print("\nMost Popular Age:\n", most_popular_year, " | ", most_popular_age , "yrs old")
    print("\nUsers by type:\n", user_types)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

#this function provides the filter of 5 trips, if users want to
def filter_five_trips(df):
    #getting user option (yes/no)
    filter_five_trips = input("Would you like to see some trips?(yes or no)")
    
    #setting the initial/final location lines. They will be incremented on while loop
    initial_position = 0
    final_position = 5

    #lopping to give trips for users 
    #checking if the dataset doesn't ended
    while  final_position <= df.shape[0]: 
        #for valid users input
        if (filter_five_trips == "yes") or (filter_five_trips=="no"):
            #in case users want to see some trips
            if filter_five_trips == "yes": 
                #display the trips
                print (df.iloc[initial_position:final_position,:])
                """
                    we also could do this using a variable, like this:
                    trips = df.iloc[initial_position:final_position,:]
                    print (trips)
                """
                #incrementting the locations of iloc positions
                initial_position += 5
                final_position += 5
                #asking again
                filter_five_trips = input("Would you like to see more trips(yes or no):")
                
            #in case users dont want to see some trips
            else:
                print("Bye Bye!")
                break
            
        #forcing users to put a valid value (yes/no)       
        else:
            filter_five_trips = input("Please, input a valid value(yes or no):")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,city)
        station_stats(df)
        trip_duration_stats(df,city)
        user_stats(df,city)
        filter_five_trips(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

#commenting to testing git alterations