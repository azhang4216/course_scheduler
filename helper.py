DAYS_OF_WEEK = {
    "M": 0,
    "Tu": 1,
    "W": 2,
    "Th": 3,
    "F": 4
}


# acceptable input: XX:XX[pm|PM|am|AM]
# output: input time as a float in 24h format
def _hour_to_float(time_string):
    time_period = time_string[-2:]  # pm or am
    hour, minute = time_string[:-2].split(":")
    hour, minute = int(hour), int(minute)

    # convert to 24h time
    if (time_period == "PM" or time_period == "pm") and hour != 12:
        hour += 12
    if (time_period == "AM" or time_period == "am") and hour == 12:
        hour -= 12

    return hour + (minute / 60)


# acceptable input: XX:XX[pm|PM|am|AM]-XX:XX[pm|PM|am|AM]
# output: a tuple of input times as floats in 24h format
def _convert_time_period(time_string):
    start, end = time_string.split("-")
    return _hour_to_float(start), _hour_to_float(end)


# acceptable input: file path to a .csv where:
    # - every row has: CALL NUMBER,COURSE,COURSE NAME,SECTION,PROFESSOR,DAYS,TIME,LOCATION
    # - CALL NUMBER is unique
    # - DAYS is a combination of " " separated keys from DAYS_OF_WEEK
    # - TIME is formatted XX:XX[pm|PM|am|AM]-XX:XX[pm|PM|am|AM]
    # - LOCATION is an address
# output: a dictionary where:
    # - every key is a course
    # - each course's associated value is a dictionary with information about each of its sections (key = call number)
    # - each section's dictionary contains info about section #, professor, and times where times[x] gives a tuple of
    #     24h format with start and end time of lecture for day x + 1.
def read_sections_csv(filename):
    courses = {}

    with open(filename, "r") as f:
        is_first_line = True

        for line in f:

            if is_first_line:
                is_first_line = not is_first_line
                continue

            line = line.strip("\n").split(",")
            call_num, course, course_name, section, prof, days, time, location = line

            if course not in courses:
                courses[course] = {}

            # format the days / time
            times = [None] * len(DAYS_OF_WEEK)
            time_floats = _convert_time_period(time)

            for day in days.split(" "):
                times[DAYS_OF_WEEK[day]] = time_floats

            courses[course][call_num] = {
                "section": section,
                "prof": prof,
                "times": times,
                "location": location,
            }

    return courses


# acceptable input: two arrays where each times[i] has a
#   start time, end time tuple in 24h float. If no lectures that day, None.
# output: a boolean indicating whether the two sessions conflict throughout the week.
def sections_conflict(times1, times2):
    for i in range(len(DAYS_OF_WEEK)):
        if times1[i] is not None and times2[i] is not None:
            # both sections have lectures on this day
            start1, end1 = times1[i]
            start2, end2 = times2[i]

            if (start1 <= end2 and end1 >= start2) or (start2 <= end1 and end2 >= start1):
                # there is a time conflict on this day
                return True

    return False

# Function Tests

# print(_hourToFloat("3:30pm"))
# print(_hourToFloat("12:10pm"))
# print(_hourToFloat("12:45am"))

# print(_convert_time_period("1:10pm-2:25pm"))
# print(_convert_time_period("10:10AM-12:40PM"))

# d = read_sections_csv("/Users/ange/PycharmProjects/course_scheduler/course_scheduler/sections.csv")
# print(d)

# print(sections_conflict(d["COMS4111"]["11218"], d["PSYC1001"]["00393"]))
# print(sections_conflict(d["COMS4111"]["11218"], d["PSYC1001"]["00447"]))
