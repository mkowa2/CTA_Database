#
# header comment! Overview, name, etc.
#

import sqlite3
import matplotlib.pyplot as plt

def command9(dbConn):
    dbCursor = dbConn.cursor()

# This command allows you to compare total ridership for two stations based on a year
# The result only prints out the first and last 5 days of the entered year,
# but the graph plots all the dates
def command8(dbConn):
    
    dbCursor = dbConn.cursor()

    year = input("\nYear to compare against? ")

    ## Finds the station and sees if there are multiple or no stations matching 
    station1 = input("\nEnter station 1 (wildcards _ and %): ")

    sql_station1 = """
        Select Station_ID, Station_Name
        From Stations
        Where Station_Name Like ?
        Order By Station_Name ASC
    """
    dbCursor.execute(sql_station1, [station1])
    result_station1 = dbCursor.fetchall()
    
    if not result_station1:
        print("**No station found...")
    elif len(result_station1) > 1:
        print("**Multiple stations found...")
    
    ## This will find the next station and will either say that there aren't any
    ## or there are mutiple matches
    else:
        station2 = input("\nEnter station 2 (wildcards _ and %): ")
        sql_station2 = """
        Select Station_ID, Station_Name
        From Stations
        Where Station_Name Like ?
        Order By Station_Name ASC
        """
        dbCursor.execute(sql_station2, [station2])
        result_station2 = dbCursor.fetchall()
        if not result_station2:
            print("**No station found...")
        elif len(result_station2) > 1:
            print("**Multiple stations found...")
        
        else:
            # Returns all the dates that are relevant to the selected year
            sql_dates = """
                Select Distinct strftime('%Y-%m-%d', Ride_Date) as Ride_Date
                From Ridership
                Where strftime('%Y', Ride_Date) = ?
                Order By Ride_Date ASC
            """
            dbCursor.execute(sql_dates, [year])
            all_dates = [row[0] for row in dbCursor.fetchall()]

            # Fetch data for the first 5 and last 5 days
            sql_main = """
                Select
                    strftime('%Y-%m-%d', Ride_Date) as Ride_Date,
                    SUM(CASE WHEN Station_ID = ? THEN Num_Riders ELSE 0 END) as Riders_Station1,
                    SUM(CASE WHEN Station_ID = ? THEN Num_Riders ELSE 0 END) as Riders_Station2
                From Ridership
                Where strftime('%Y', Ride_Date) = ?
                Group By Ride_Date
                Order By Ride_Date ASC
            """

            # Display the results for the first 5 days for Station 1
            print(f"Station 1: {result_station1[0][0]} {result_station1[0][1]}")
            for row in dbCursor.execute(sql_main, [result_station1[0][0], result_station2[0][0], year]):
                ride_date, riders_station1, riders_station2 = row
                print(f"{ride_date} {riders_station1}")
                if all_dates.index(ride_date) == 4:  # Stop after the first 5 days
                    break

            # Display the results for the last 5 days for Station 1
            for row in dbCursor.execute(sql_main, [result_station1[0][0], result_station2[0][0], year]):
                ride_date, riders_station1, riders_station2 = row
                if all_dates.index(ride_date) >= len(all_dates) - 5:  # Print last 5 days
                    print(f"{ride_date} {riders_station1}")

            # Display the results for the first 5 days for Station 2
            print(f"Station 2: {result_station2[0][0]} {result_station2[0][1]}")
            for row in dbCursor.execute(sql_main, [result_station2[0][0], result_station2[0][0], year]):
                ride_date, riders_station1, riders_station2 = row
                print(f"{ride_date} {riders_station2}")
                if all_dates.index(ride_date) == 4:  # Stop after the first 5 days
                    break

            # Display the results for the last 5 days for Station 2   
            for row in dbCursor.execute(sql_main, [result_station2[0][0], result_station2[0][0], year]):
                ride_date, riders_station1, riders_station2 = row
                if all_dates.index(ride_date) >= len(all_dates) - 5:  # Print last 5 days
                    print(f"{ride_date} {riders_station2}")


            # Ask if they want to plot the data
            plot_choice = input("\nPlot? (y/n) ").lower()

            if plot_choice == 'y':
                # Extract data for plotting
                days_of_year = range(0, len(all_dates), 1)


                riders_station1_data = []
                riders_station2_data = []

                for row in dbCursor.execute(sql_main, [result_station1[0][0], result_station2[0][0], year]):
                    ride_date, riders_station1, riders_station2 = row
                    if ride_date in all_dates:    
                        riders_station1_data.append(riders_station1)
                        riders_station2_data.append(riders_station2)

                # Plotting
                plt.figure(figsize=(10, 6))
                plt.plot(days_of_year, riders_station1_data, label=f"{result_station1[0][0]} {result_station1[0][1]}")
                plt.plot(days_of_year, riders_station2_data, label=f"{result_station2[0][0]} {result_station2[0][1]}")
                plt.title(f"Ridership Data for {year}")
                plt.xlabel("Day of the Year")
                plt.ylabel("Number of Riders")
                plt.legend()
                plt.grid(True)
                plt.show()

# The user enters the station name and year, and it will output the total ridership
# per month for that year
def command7(dbConn):
    # Finds if the station exists and if there is on or multiple 
    dbCursor = dbConn.cursor()

    x = input("\nEnter a station name (wildcards _ and %): ")

    sql = """
            Select Station_ID, Station_Name From Stations
            Where Stations.Station_Name LIKE ?
            Order By Station_Name ASC
            """

    dbCursor.execute(sql, [x])
    result = dbCursor.fetchall()
    
    if not result:
        print("**No station found...")
    elif len(result) > 1:
        print("**Multiple stations found...")
    else:
        #Gets the dates with the matching year
        year = input("Enter a year: ")
        sql_monthly_totals = """
        Select strftime('%m/%Y', Ride_Date) as Month,SUM(Num_Riders) as Total_Ridership
        From Ridership
        Where Station_ID = ? AND strftime('%Y', Ride_Date) = ?
        Group By Month
        Order By Month ASC
    """
        dbCursor.execute(sql_monthly_totals, [result[0][0], year])
        monthly_totals = dbCursor.fetchall()

        
            
        print("Monthly Ridership at",result[0][1],"for",year)
        for row in monthly_totals:
            print(f"{row[0]} : {format(row[1], ',')}")
        
        plot_choice = input("\nPlot? (y/n) ").lower()

        if plot_choice == 'y' and len(monthly_totals) > 1:
            months = [row[0] for row in monthly_totals]
            total_ridership = [row[1] for row in monthly_totals]

            # Plotting
            plt.figure(figsize=(10, 6))
            plt.plot(months, total_ridership, label=f"{result[0][0]} {result[0][1]}")
            plt.title(f"Monthly Ridership for {result[0][1]} in {year}")
            plt.xlabel("Months")
            plt.ylabel("Total Ridership")
            plt.xticks(months, [f"{m:02d}" for m in range(1, 13)]) 
            plt.legend()
            plt.show()

###################################################################

# The user enters a station and if it exits, it will output all the ridership per year
def command6(dbConn):
    #Gets the stations that match the name
    dbCursor = dbConn.cursor()
    x = input("\nEnter a station name (wildcards _ and %): ")
    
    sql = """
            Select Station_ID, Station_Name From Stations
            Where Stations.Station_Name LIKE ?
            Order By Station_Name ASC
            """

    
    dbCursor.execute(sql, [x])
    result = dbCursor.fetchall()
    
    if not result:
        print("**No station found...")
    elif len(result) > 1:
        print("**Multiple stations found...")
    else:
        #Gets the ridership for each month
        name = result[0][1]
        id = result[0][0]

        sql_rider = """ Select strftime('%Y', Ride_Date) as Year, SUM(Num_Riders)
        As TotalRiders
        From Ridership
        Where Station_ID = ?
        Group By Year
        Order By Year ASC;
        """
        dbCursor.execute(sql_rider, [id])
        ridership_result = dbCursor.fetchall()

        print(f"Yearly Ridership at {name}")

        for row in ridership_result:
            year, total = row
            print(f"{year} : {total:,}")

        yes = input("\nPlot? (y/n) ").lower()

        #Ploting 
        if yes == 'y':
            years = [row[0] for row in ridership_result]
            numRiders = [row[1] for row in ridership_result]
            plt.plot(years, numRiders, marker='o')
            plt.title(f"Yearly Ridership at {name} Station")
            plt.xlabel("Year")
            plt.ylabel("Number of Riders")
            plt.show()        

###################################################################

#Gives the percentages for directions for each line color
def command5(dbConn):
    dbCursor = dbConn.cursor()

    #Gets the total count of stop
    dbCursor.execute("SELECT COUNT(*) FROM Stops;")
    total_num_stops_row = dbCursor.fetchone()
    total_num_stops = total_num_stops_row[0]

    sql = """
        Select Lines.Color, Stops.Direction, COUNT(Stops.Stop_ID) as Num_Stops
        From Stops
        Inner Join StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID
        Inner Join Lines ON StopDetails.Line_ID = Lines.Line_ID
        Group By Lines.Color, Stops.Direction
        Order By Lines.Color ASC, Stops.Direction ASC;
    """
    dbCursor.execute(sql)
    result = dbCursor.fetchall()

    #Prints out all the information grouped by color in ascending order and direction
    print("Number of Stops For Each Color By Direction")
    for row in result:
        color, direction, num_stops = row
        total_num_stops_for_color_direction = sum(row[2] for row in result if row[0] == color and row[1] == direction)
        percentage = (total_num_stops_for_color_direction / total_num_stops) * 100 if total_num_stops > 0 else 0
        print(f"{color} going {direction} : {num_stops} ({percentage:.2f}%)")

###################################################################

# The user enters a line color and a direction, and it checks what stops are on it
# and if theyre handicap accessible
def command4(dbConn):
    #Get color of the line
    dbCursor = dbConn.cursor()
    color = input("\nEnter a line color (e.g. Red or Yellow): ")
    sql = """
        Select Color 
        From Lines
        Where Upper(Lines.Color) = Upper(?)
        """
    
    dbCursor.execute(sql, [color])
    result = dbCursor.fetchone()

    #Check if it exits 
    if result:
        direction = input("Enter a direction (N/S/W/E): ")
        sql_get_stops = """
            SELECT Stop_Name, ADA
            FROM Stops
            WHERE Stop_ID IN (
                SELECT Stop_ID
                FROM StopDetails
                WHERE Line_ID IN (
                    SELECT Line_ID
                    FROM Lines
                    WHERE UPPER(Color) = UPPER(?)
                )
            ) AND UPPER(Direction) = UPPER(?)
            ORDER BY Stop_Name ASC
        """
        dbCursor.execute(sql_get_stops, [color, direction])
        stops_result = dbCursor.fetchall()  

        #Checks if there are any stops 
        if stops_result:
            for stop in stops_result:
                stop_name, ada = stop
                handicap = "(handicap accessible)" if ada else "(not handicap accessible)"
                direction = direction.upper()
                print(f"{stop_name} : direction = {direction} {handicap}")
            
        else:
            print("**That line does not run in the direction chosen...")
        
    else:
        print("**No such line...\n")

###################################################################

#Checks there total ridership on weekdays for each station
def command3(dbConn):
    dbCursor = dbConn.cursor()

    sql = """
        Select Stations.Station_Name, SUM(Ridership.Num_Riders) AS TotalRiders
        From Ridership
        Join Stations ON Ridership.Station_ID = Stations.Station_ID
        Where Ridership.Type_of_Day = 'W'
        Group By Stations.Station_Name
        Order By TotalRiders DESC;
    """

    dbCursor.execute(sql)
    result = dbCursor.fetchall()

    totalWeekdayRidership = sum(row[1] 
                                for row in result)
    
    if result:
        print("Ridership on Weekdays for Each Station")
        for row in result:
            station_name, count = row
            percentage = (count / totalWeekdayRidership) * 100
            print(f"{station_name} : {count:,} ({percentage:.2f}%)")
        
    else:
        print("**No data found...\n")
    
###################################################################

# Gives a breakdown each station including the Weekday, Sat., and Sun/Holiday breakdown.
def command2(dbConn):
    #Get the station
    x = input("\nEnter the name of the station you would like to analyze: ")
    dbCursor = dbConn.cursor()

    sql = """
        Select Type_of_Day, SUM(Num_Riders) AS TotalRiders
        From Ridership
        Where Station_ID = (SELECT Station_ID FROM Stations WHERE Station_Name = ?)
        Group By Type_of_Day
        Order By
            CASE Type_of_Day
                WHEN 'W' THEN 1
                WHEN 'A' THEN 2
                WHEN 'U' THEN 3
            END;
    """
    dbCursor.execute(sql, [x])
    result = dbCursor.fetchall()
    total_riders = sum(row[1] for row in result)
    #Print out if there is any data
    if result:
        print(f"Percentage of ridership for the {x} station: ")
        for row in result:
            type_of_day, count = row
            if type_of_day == 'W':
                day_label = 'Weekday'
            elif type_of_day == 'A':
                day_label = 'Saturday'
            elif type_of_day == 'U':
                day_label = 'Sunday/holiday'

            percentage = (count / total_riders) * 100
            print(f" {day_label} ridership: {count:,} ({percentage:.2f}%)")
        print(f" Total ridership: {total_riders:,}")
    else:
        print("**No data found...")

###################################################################    
def command1(dbConn):
    x = input("\nEnter partial station name (wildcards _ and %): ")
    dbCursor = dbConn.cursor()
    
    sql = """
            Select Station_ID, Station_Name From Stations
            Where Stations.Station_Name LIKE ?
            Order By Station_Name ASC
            """

    
    dbCursor.execute(sql, [x])
    result = dbCursor.fetchall()

    if result:
        for row in result:
            print(row[0], ":", row[1])
        
    else:
        print("**No stations found...")

###################################################################
def chosingCommand(dbConn):
    while True:
        x = input("\nPlease enter a command (1-9, x to exit): ")
        if x == 'x':
            break
        elif x == '1':
            command1(dbConn)
        elif x == '2':
            command2(dbConn)
        elif x == '3':
            command3(dbConn)
        elif x == '4':
            command4(dbConn)
        elif x == '5':
            command5(dbConn)
        elif x == '6':
            command6(dbConn)
        elif x == '7':
            command7(dbConn)
        elif x == '8':
            command8(dbConn)
        else:
            print("**Error, unknown command, try again...")
##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General Statistics:")
    
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Stops; ")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")
    
    dbCursor.execute("Select count(*) From  Ridership;")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")

    dbCursor.execute("SELECT MIN(strftime('%Y-%m-%d', Ride_Date)) AS min_Date, MAX(strftime('%Y-%m-%d', Ride_Date)) AS max_Date FROM Ridership;")
    row = dbCursor.fetchone();
    min_Date, max_Date = row
    print("  date range:", f"{min_Date} - {max_Date}")

    dbCursor.execute("SELECT SUM(Num_Riders) FROM Ridership;")
    row = dbCursor.fetchone()
    total_ridership = row[0]
    print("  Total ridership:", f"{total_ridership:,}")

    chosingCommand(dbConn)

    

    


##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

#
# done
#
