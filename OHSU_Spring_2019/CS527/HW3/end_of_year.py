#!/usr/bin/env python3

import datetime
import sys

if len(sys.argv) != 2 or sys.argv[1] not in ['days','hours','minutes','seconds']:

    # usage
    print("USAGE ERROR: following the program name, \n")
    print("\t 'days' will return days.")
    print("\t 'hours' will return hours.")
    print("\t 'minutes' will return minutes.")
    print("\t 'seconds' will return seconds.\n")
    print("Example: python3 end_of_year.py hours")
    exit()


# get the current date and time
right_now = datetime.datetime.now()

# extract current year and calculate next year
this_year = right_now.year 
next_year = this_year + 1
end_of_this_year = datetime.datetime(next_year, 1, 1)

# get time delta now to
now_to_end = end_of_this_year - right_now

# convert to proper format
delta = 0.0
delta_in_seconds = float(now_to_end.total_seconds())

if sys.argv[1] == 'seconds':
    delta = delta_in_seconds
elif sys.argv[1] == 'minutes':
    delta = delta_in_seconds/60.0
elif sys.argv[1] == 'hours':
    delta = delta_in_seconds/(60.0*60.0)
elif sys.argv[1] == 'days':
    delta = delta_in_seconds/(60.0*60.0*24)


print("Current datetime is: ", right_now)
print("End of the year is:  ", end_of_this_year)
print("\nTime difference in %s:" % sys.argv[1], delta)
