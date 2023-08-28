from helper import read_sections_csv, sections_conflict
from itertools import product
from mapsapirequest import walk_distance_time

# GLOBAL VARIABLES
d = read_sections_csv("/Users/ange/PycharmProjects/course_scheduler/course_scheduler/sections.csv")

call_nums_by_courses = {course_num: {call_num for call_num in d[course_num]} for course_num in d}
times_by_call_num = {call_num: d[course_num][call_num]["times"] for course_num in d for call_num in d[course_num]}
buildings_by_call_num = {call_num: d[course_num][call_num]["location"] for course_num in d for call_num in d[course_num]}

# section_conflict[smaller call #_larger call #] = whether the two sections conflict (boolean)
section_conflict = {}


# FUNCTIONS
# input: a tuple combination where each element is a section's call number from a different course.
def sections_have_conflict(sections_combo):
    for i in range(len(sections_combo)):
        for j in range(i + 1, len(sections_combo)):
            smaller_call_num, bigger_call_num = \
                min(sections_combo[i], sections_combo[j]), max(sections_combo[i], sections_combo[j])
            section_conflict_id = smaller_call_num + "_" + bigger_call_num

            if section_conflict_id not in section_conflict:
                section_conflict[section_conflict_id] = \
                    sections_conflict(times_by_call_num[smaller_call_num], times_by_call_num[bigger_call_num])

            if section_conflict[section_conflict_id]:
                return True

    return False


# make a cartesian product with 1 section (call number) from each course,
#   AND no conflicting lecture times
cp = {sections_combo for sections_combo in product(*call_nums_by_courses.values())
      if not sections_have_conflict(sections_combo)}
# print(cp)

# figure out distance between each building
for schedule in cp:
    building1, building2 = buildings_by_call_num[schedule[0]].split(None, 1)[1], \
                           buildings_by_call_num[schedule[1]].split(None, 1)[1]
    distance, time = walk_distance_time(building1, building2)
    # print("It takes", time, "to walk from", schedule[0], "at", building1, "to", schedule[1], "at", building2 + ".\n")


#
#
