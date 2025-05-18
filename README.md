**Learning Progress Tracker**

**Description**

The Learning Progress Tracker is a command-line application written in Python that allows instructors to manage student records, track their progress across multiple courses, compute statistics, and send completion notifications. It supports the following courses:

* **Python** (600 points)
* **DSA** (Data Structures and Algorithms, 400 points)
* **Databases** (480 points)
* **Flask** (550 points)

**Features**

1. **Add Students**: Register students with unique email addresses and automatically assigned IDs.
2. **List Students**: Display all registered student IDs in the order they were added.
3. **Add Points**: Update student progress by adding points for each course.
4. **Find Student**: View total points per course for an individual student.
5. **Statistics**: Compute and display:

   * Most and least popular courses (by enrollment)
   * Highest and lowest activity courses (by number of submissions)
   * Easiest and hardest courses (by average points per submission)
   * Detailed course standings (sorted by points and ID)
6. **Notify**: Send a one-time congratulatory message to students who completed a course.
7. **Exit**: Gracefully terminate the application.

---

## Installation

1. Ensure you have **Python 3.8+** installed.

2. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/learning-progress-tracker.git
   cd learning-progress-tracker
   ```

3. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

4. Install any required dependencies (none beyond the standard library).

---

## Usage

Run the application:

```bash
python main/app.py
```

You will see the prompt:

```
Learning Progress Tracker
>
```

### Available Commands

| Command        | Description                                                                                    |
| -------------- | ---------------------------------------------------------------------------------------------- |
| `add_students` | Register new students (enter `back` to return to main menu).                                   |
| `list`         | List all student IDs.                                                                          |
| `add_points`   | Add or update points for each course (enter `back` to return).                                 |
| `find`         | Display a student’s total points per course (enter `back` to return).                          |
| `statistics`   | Show overall course stats and drill down into individual course standings.                     |
| `notify`       | Send one-time completion notifications to students who have met all requirements for a course. |
| `exit`         | Quit the application.                                                                          |

### Examples

**1. Add Students**

```
> add_students
Enter student credentials or 'back' to return
> John Doe johndoe@example.com
The student has been added
> back
Total 1 students have been added.
```

**2. Add Points & Find**

```
> add_points
Enter an id and points or 'back' to return
> 10000 600 400 0 0
Points updated.
> back
> find
Enter an id or 'back' to return
> 10000
10000 points: Python=600; DSA=400; Databases=0; Flask=0
```

**3. Statistics**

```
> statistics
Type the name of a course to see details or 'back' to quit
Most popular: Python
Least popular: Databases
Highest activity: Python
Lowest activity: Databases
Easiest course: DSA
Hardest course: Flask
> python
Python
id   points   completed
10000 600      100.0%
> back
```

**4. Notify**

```
> notify
To: johndoe@example.com
Re: Your Learning Progress
Hello, John Doe! You have accomplished our Python course!
To: johndoe@example.com
Re: Your Learning Progress
Hello, John Doe! You have accomplished our DSA course!
Total 1 students have been notified.
> notify
Total 0 students have been notified.
```


---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.


