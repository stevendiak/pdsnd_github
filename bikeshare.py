import time
import pandas as pd
import numpy as np

#File provides information on bikeshare data in major US cities

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input("Which city would you like to explore (chicago, new york city, washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter one of the following cities: chicago, new york city, washington.")

    # Get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? (all, january, february, march, april, may, june): ").lower()
        if month in months:
            break
        else:
            print("Invalid input. Please enter a valid month or 'all'.")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please enter a valid day or 'all'.")

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day]
    
    return df

def display_raw_data(df):
    """Displays raw data upon request by the user in increments of 5 rows."""
    row_index = 0
    view_data = input("\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n").lower()
    while view_data == 'yes' and row_index + 5 <= len(df):
        print(df.iloc[row_index:row_index+5])
        row_index += 5
        view_data = input("\nWould you like to view 5 more rows of individual trip data? Enter yes or no.\n").lower()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print(f"Most Common Month: {common_month}")

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {common_day_of_week}")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {common_start_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"Most Commonly Used Start Station: {common_start_station}")

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most Commonly Used End Station: {common_end_station}")

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['trip'].mode()[0]
    print(f"Most Frequent Trip: {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time} seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"User Types:\n{user_types}")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"\nGender Counts:\n{gender_counts}")
    else:
        print("\nGender Counts: No data available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest Year of Birth: {earliest_year}")
        print(f"Most Recent Year of Birth: {most_recent_year}")
        print(f"Most Common Year of Birth: {most_common_year}")
    else:
        print("Year of Birth: No data available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()