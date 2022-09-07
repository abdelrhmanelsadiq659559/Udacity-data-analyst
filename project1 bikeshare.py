import time
import pandas as pd
from  datetime import timedelta

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
Months = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6}
Days = {"sa": "Saturday", "su": "Sunday", "mo": "Monday", "tu": "Tuesday", "we": "Wednesday", "th": "Thursday",
        "fr": "Friday"}


def handle_error(string, arr):
    ''' ask user to input data and handle any error
    Returns
    - (str) choice.lower()  is data which user enter in lower case   '''
    while True:
        choice = input(string) # take input from user
        if choice.lower() in arr: # check validity od input
            return choice.lower()
        else:
            print("invalid input ,please try again ")

def Month():
    '''
    ask user to enter month
    Returns:
        (str)  get_month_to_filter_on   string of month which user write in lower case in all times with handle_error function help
    '''
    get_month_to_filter_on=handle_error(
        "which month ? January, February, March, April, May, or June? please type the full name month\n",
        ["january", "february", "march", "april", "may", "june"])
    return get_month_to_filter_on


def Day():
    '''
     ask user to enter day
     Returns:
         str (get_day_to_filter_on)  string of month which user write in lower case in all times with handle_error function help
     '''
    get_day_to_filter_on=handle_error("Which day? please type your respnse as integer(Sa, Su, Mo, Tu, We, Th, Fr)\n",
                        ['sa', 'su', 'mo', 'tu', 'we', 'th', 'fr'])
    return get_day_to_filter_on


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = handle_error("Would you like to see data for Chicago, New York, or Washington?\n",
                        ["chicago", "new york", "washington"])

    # get from user how to filter data ["month", "day", "both", "none"]
    filter_on = handle_error(
        "Would you like to filter the data by month, day, or not at all? if not at all type none\n",
        ["month", "day", "both", "none"])
    # get user input for month (january, february, ..., june) if he choose filter by month only and make day none(meaning all days)

    if filter_on == "month":
        month = Month()
        day = None

    # get user input for day ([sa,su,mo...fr]   if he choose filter by day  and make month none(meaning all months)
    elif filter_on == "day":
        day = Day()
        month = None

    # get user input for day ([sa,su,mo...fr]  and  input for month (january, february, ..., june) if he choos to filter by both(month-day)
    elif filter_on == "both":
        month = Month()
        day = Day()

    # if user input for filter_on makes filter by all days and all months in a simple way no filter by month nor day
    elif filter_on=="none":
        month = None
        day = None

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month  and day
    """
    # load specfic city data
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])# change datatype of column Start time to datetime
    df['day_of_week'] = df["Start Time"].dt.day_name() # get day name depend on date of start  date
    filtering = "No-time filter" # makeing variable and store in it default value  filter No-time filter to use it in analysis later

    # get dataframe analysised by specfic month from user and modfiying filtering value
    if month != None and day == None:
        df = df[df["Start Time"].dt.month.astype(int) == Months[month]]
        filtering = "Month"

    # get dataframe analysised by specfic day from user and modfiying filtering value
    elif month == None and day != None:
        df = df[df['day_of_week'] == Days[day]]
        filtering = "Day"

    # get dataframe analysised by specfic day from user and by specfic month from user and modfiying filtering value
    elif month != None and day != None:
        df = df[(df["Start Time"].dt.month.astype(int)) & (df['day_of_week'] == Days[day])]
        filtering = "Both"
    # if filterinf was entered from user none return spec ficdata frame without filtering
    return df , filtering


def time_stats(df,filtering):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # to get,count and display the most common month if fitering by day only
    if filtering!="Both" and filtering!="Month":
        common_count_month=df["Start Time"].dt.month.value_counts()[0:1]
        print(f"the most common month is:{common_count_month.index[0]} , count:{common_count_month.values[0]}\n")
    # to get,count and display the most common month if fitering by day month
    if filtering!="Both" and filtering!="Day":
        common_count_day = df["day_of_week"].value_counts()[0:1]
        print(f"the most common day of week is (\'{common_count_day.index[0]}\') , count:{common_count_day.values[0]}\n")

    #  get ,count and display the most common start hour
    common_count_hour = df["Start Time"].dt.hour.value_counts()[0:1]
    print(f"the most common start hour is {common_count_hour.index[0]} , count:{common_count_hour.values[0]}")
    print(f"filter: {filtering}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df,filtering):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # to get ,count and display most commonly used  of start station and End station separatly
    for i in ['Start Station','End Station']:
        common_count_station=df[i].value_counts()[0:1]
        print(f"most commonly used {i} is (\'{common_count_station.index[0]}\') , count:{common_count_station.values[0]}\n")

    # to get ,count and display most  frequent combination of start station and end station trip
    df["Start&End"]=df['Start Station']+"--->>"+df['End Station']  # make a combinted  station by start and end for every row
    stations_comb =df["Start&End"].value_counts().index[0]
    count_station_comb=df["Start&End"].value_counts().values[0]
    print(f"most frequent combination of start station and end station trip are (\'{stations_comb}\') alternatively , count{count_station_comb}")

    print(f"filter: {filtering}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df,filtering):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # to calculate total travel time  in days hours:mintues:seconds
    tot_travel_time=round(df["Trip Duration"].sum()) 
    tot_travel_time=timedelta(seconds=tot_travel_time)
    
    # to calculate average travel time  in days hours:mintues:seconds
    avg_travel_time =round( df["Trip Duration"].mean())
    avg_travel_time= timedelta(seconds=avg_travel_time)

    ##  display most commonly total travel time and average time   in days hours:mintues:seconds and count for data
    print(f"total travel time: {tot_travel_time} ,  average time: {avg_travel_time} , count:{df.shape[0]}")

    print(f"filter: {filtering}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df,filtering,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # get and Display counts of user types
    user_types=df["User Type"].value_counts()
    print(f"{user_types}\n")
    # if for prevent errors because Washington does'nt have gender and birth day data
    if city !="Washington":
        # get and Display counts of gender
        Gender= df["Gender"].value_counts()
        print(f"{Gender}\n")

        # get earliest, most recent, and most common year of birth and count for most common year of birth
        earliest=int(df["Birth Year"].min())
        most_recent=int(df["Birth Year"].max())
        most_common=int(df["Birth Year"].mode()[0])
        most_common_count= df["Birth Year"].value_counts().values[0]

        #to display earliest, most recent, and most common year of birth and count for most common year of birth
        print(f"earliest, most recent year of birth are: (\'{earliest},{most_recent}\') , most common year of birth:(\'{most_common}\'),count:{most_common_count}")
    else :
        print("No-data for Gender and Birth Year  for Washington")
    print(f"filter: {filtering}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df ,filtering= load_data(city, month, day,)
        time_stats(df,filtering)
        station_stats(df,filtering)
        trip_duration_stats(df,filtering)
        user_stats(df,filtering,city)

        i = -1
        df=df.reset_index(drop=True) # to use df.loc  by right way
        while True : # this loop for if user want to display five rows  from data

            i += 1
            how_five_rows = handle_error('\nWould you like to see five row or see more from your data ? Enter yes or no.\n', ["yes", "no"])
            if how_five_rows!= 'yes': # to stop loop if user want
                break
            # get and display five rows from data
            data_to_display=df.loc[i * 5:(i + 1) * 5]
            print(data_to_display)
            if data_to_display.shape[0]<5: # to avoid printing without any values
                print("there is no more data ")
                break



        restart = handle_error('\nWould you like to restart? Enter yes or no.\n',["yes","no"])
        if restart!= 'yes':
            break



if __name__ == "__main__":

    main()


