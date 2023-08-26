# Angela's Course Scheduler
### Main Problem: How do I schedule my courses so that I walk the least amount of distance between the buildings?

Each of my university "courses" have several "sections": each "section" is taught by a professor, at a specific time, and at a specific building. I know which "courses" I want to take. To take a "course", I need to take 1 and only 1 of its "sections." I would like to find the way(s) to take all my desired "courses" without scheduling conflicts, while minimizing the walking distance from one "section" building to another.

```json
{
  "course": "intro databases",
  "sections": {
    "A": {
      "professor": "Prof. Appleseed",
      "time": "MW 12:10-14:00",
      "location": "123 Sesame St, NYC, NY"
    },
    "B": {
      "professor": "Prof. Not Appleseed",
      "time": "MW 15:30-17:00",
      "location": "321 Sesame St, NYC, NY"
    }
  }
}
```

This is a __weighted shortest path problem__ where I have to traverse 1 section (node) from each course.

I break this shortest path problem down into several sub-problems:

#### Problem 0: How do I represent my sections / courses as a graph?

Let each section be represented by a node `Ai`, where `A` is the name of the course, and `i` the non-negative integer identifier for the specific section.

Let `c` be the number of courses and `s` be the number of sections.

Section `Ax` has an edge to Section `By` iff `Ax` ends before `By` starts. The weight of the edge from `Ax` to `By` is the distance of travel from the former section to the latter. Note that:
- `A` != `B`, as I cannot take multiple sections of the same course.
- An edge between two sections is never bidirectional, since if `Ax` finishes before `By` starts, `By` cannot finish before `Ax` starts.

Since I always start and end my day at my residential dorm, I will have a start node `S` that represents my starting at my dorm and node `E` that represents my ending at my dorm at the end of the day. Node `S` will have an edge into every other node, and node `E` will have an edge running into itself from all other nodes. 
We seek to find a shortest path from node `S` to `E` s.t. the length of the path is `c` + 2 (we've taken all courses).

#### Problem 1: How do I determine whether there is an edge from one section to another?

Each section may have multiple timeslots. For example, section `Ax` takes place Mondays 3:20-5pm; Wednesdays 9-11am.

Section `Ax` does NOT have an edge to Section `By` iff there exists a matching day from their timeslots in which `By` starts before `Ax` ends. 

We represent a section's timeslots as a dictionary, where the key is the day of the week (string), and the value is a tuple where index 0 holds start time (float) and index 1 holds end time (float).

Our example section `Ax`'s timeslots would be:

```python
# This represents a section's timeslot that take place Mondays 3:20-5pm; Wednesdays 9-11am.
Ax_timeslots = {
    "M": (15.33, 17),
    "Tu": None,
    "W": (9, 11),
    "Th": None,
    "F": None,
    "S": None
}
````

#### Problem 2: How do I determine the distance between two buildings?

If there is an edge from `Ax` to `By`, we need to assign the edge with a weight, which is the time taken to walk from the former to the latter.

I chose to use time instead of distance, since time taken is more representative of effort needed to get from one place to another. Distance does not account for uphill or downhill.

I will use [Google Map's Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/overview) to find associated time taken.


#### Problem 3: How do I find the best course schedule that minimizes travel time?

Here we use Dijkstra's Algorithm with a few changes.

First, we consider that each day has its own path.
- we want to minimize the TOTAL TIME traveled between classes from Monday to Sunday.
- if `Ax` was included in Monday's path, and `Ax` also takes place Wednesday, it needs to be included in Wednesday's path as well.

Second, we need to have exactly 1 section from each course.
- in total, the number of UNIQUE sections traversed throughout the week should be `c` + 2 (1 section from each course + start and end nodes).



#### Additional points to consider:
- professor rating / likeability
- do I have to rush from point A to point B?
- what floor is this building on? I don't like walking up stairs.
- how do I account for breakfast / lunch / snack / dinner?


csv format:
COURSE,COURSE NAME,SECTION,PROFESSOR,DAYS,TIME,LOCATION
COMS4111,INTRODUCTION TO DATABASES,001,Luis Gravano,Tu Th,1:10pm-2:25pm,301 PUPIN