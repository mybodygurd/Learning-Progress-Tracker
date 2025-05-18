import sys
import re
from dataclasses import dataclass, field
# email.utils
@dataclass
class Student:
    id: str
    first_name: str
    last_name: str
    email: str
    courses: dict = field(default_factory=lambda: {
        "Python": 0,
        "DSA": 0,
        "Databases": 0,
        "Flask": 0
    })
    
class Course:
    def __init__(self, name: str) -> None:
        self.name = name
        self.studentsID = []
        self.activity = 0
        self.sum_points = 0
        self.max_point = 0
        max_points = {"Python": 600,
                      "DSA": 400,
                      "Databases": 480,
                      "Flask": 550
                      }
        self.max_point = max_points[self.name]
        
    def count_number_of_students(self) -> int:
        return len(self.studentsID)
    
    def calculate_avg_points(self):
        try:
            return self.sum_points / self.activity
        except ZeroDivisionError:
            return None
     
class LearningProgressTracker:
    def __init__(self) -> None:
        self.next_id = 10000
        self.students = {}
        self.commands = {"exit": self.cmd_exit,
                        "add_students": self.cmd_add_std,
                        "list": self.list_std,
                        "add_points": self.add_points,
                        "find": self.find_std,
                        "statistics": self.stats
                        }
        self.categories = {"Most popular": "n/a",
                           "Least popular": "n/a",
                           "Highest activity": "n/a",
                           "Lowest activity": "n/a",
                           "Easiest course": "n/a",
                           "Hardest course": "n/a"
                           }
        course_names = ["Python", "DSA", "Databases", "Flask"]
        self.courses = {name: Course(name) for name in course_names}             

    def cmd_exit(self) -> None:
        print("Bye!")
        sys.exit(0)
        
    def generate_id(self) -> str:
        current_id = self.next_id
        self.next_id += 1
        return str(current_id)
    
    def cmd_add_std(self) -> None:
        print("Enter student credentials or 'back' to return")
        while True:
            inp = input("> ").strip()
            if not inp:
                print("Incorrect credentials")
                continue
            tokens = inp.split()
            if tokens[0] == "back":
                n_std = len(self.students)
                if n_std >= 1:
                    print(f"Total {len(self.students)} student(s) have been added.")
                else:
                    print("Nobody have been added.")
                break
            try:
                f_name = tokens[0]
                l_name = ' '.join(tokens[1: -1])
                email = tokens[-1]
            except IndexError:
                print("Incorrect credentials")
                continue
            if any(std.email == email for std in self.students.values()):
                print("This email is already taken.")
                continue    
            if not validate_name(f_name):
                print("Incorrect first name")
                continue
            if not validate_name(l_name):
                print("Incorrect last name")
                continue
            if not validate_email(email):
                print("Incorrect email.")
                continue
            id = self.generate_id()
            student = Student(id, f_name, l_name, email)
            self.students[id] = student
            print("The student has been added")        
        
    def list_std(self) -> None:
        if not self.students:
            print("No students found")
        else:
            print("Students:")
            for id in self.students:
                print(id)
                
    def add_points(self) -> None:
        print("Enter an id and points or 'back' to return")
        while True:
            entry = input("> ").strip()
            if not entry:
                print("No input.")
                continue
            if entry == "back":
                break
            id, *points = entry.split()
            if len(points) != 4:
                print("Incorrect points format")
                continue
            if not all(p.isdigit() for p in points):
                print("Incorrect points format")
                continue
            points = list(map(int, points))
            if id in self.students:
                std = self.students[id]
                for idx, course in enumerate(std.courses):
                    std.courses[course] += points[idx]
                    if points[idx] != 0:
                        crs = self.courses[course]
                        if id not in crs.studentsID:
                            crs.studentsID.append(id)
                        crs.activity += 1 
                        crs.sum_points += points[idx]
                print("Points updated.")
            else:
                print(f"No student is found for id={id}.")            
            
    def find_std(self):
        print("Enter an id or 'back' to return")
        while True:
            id = input("> ").strip()
            if not id:
                print("No input.")
                continue
            if id == "back":
                break
            if id in self.students:
                courses = self.students[id].courses
                crs = "; ".join(f"{course}={point}" for course, point in courses.items())
                print(f"{id} points: " + crs)                    
            else:
                print(f"No student is found for id={id}.")
                
    def _calc_max_min_ctg(self, counts: dict) -> tuple[list | None, list | None]:
        if not any(val != 0 for val in counts.values()):
            return None, None
        max_val = max(counts.values())
        min_val = min(counts.values())
        most = [name for name, val in counts.items() if val == max_val]
        least = [name for name, val in counts.items() if val == min_val and name not in most]
        most = most if most else None
        least = least if least else None
        return most, least
  
    def stats(self):
        pop_counts = {}
        act_counts = {}
        diff_counts = {}
        counters = [pop_counts, act_counts, diff_counts]
        print("Type the name of a course to see details or 'back' to quit")
        for name, crs in self.courses.items():
            pop_counts[name] = crs.count_number_of_students()
            act_counts[name] = crs.activity
            avg_point = crs.calculate_avg_points()
            if avg_point is not None:
                diff_counts[name] = avg_point
        for counter in counters:
            most, least = self._calc_max_min_ctg(counter)
            if most and least:
                if counter == pop_counts:
                    self.categories["Most popular"] = ", ".join(most)
                    self.categories["Least popular"] = ", ".join(least)
                elif counter == act_counts:
                    self.categories["Highest activity"] = ", ".join(most)
                    self.categories["Lowest activity"] = ", ".join(least)
                else:
                    self.categories["Easiest course"] = ", ".join(most)
                    self.categories["Hardest course"] = ", ".join(least)
            elif most:
                if counter == pop_counts:
                    self.categories["Most popular"] = ", ".join(most)
                elif counter == act_counts:
                    self.categories["Highest activity"] = ", ".join(most)
                else:
                    self.categories["Easiest course"] = ", ".join(most)
        for ctg, course in self.categories.items():
            print(f"{ctg}: {course}")
        self.handle_course_details()
        
    def handle_course_details(self):
        while True:
            course = input("> ").strip().title()
            if not course:
                print("No input.")
                continue
            if course == "Back":
                break
            if course in self.courses:
                if course == "Dsa":
                    course = course.capitalize()
                print(course)
                print("id   points  completed")
                course_students = []
                for std in self.students.values():
                    point = std.courses[course]
                    if point != 0:
                        max_point = self.courses[course].max_point
                        completion = round((point / max_point) * 100, 1)
                        course_students.append((std.id, point, completion))
                if course_students:
                    sorted_std = sorted(course_students, key=lambda x: (-x[1], x[0]))
                    for std in sorted_std:
                        print(f"{std[0]}   {std[1]}  {std[2]}%")                   
            else:
                print("Unknown course")
                
    def run(self) -> None:
        try:
            print("Learning Progress Tracker")
            while True:
                inp = input("> ").strip().lower()
                if not inp:
                    print("No input.")
                    continue
                cmd, *parts = inp.split()

                if cmd in self.commands:
                    self.commands[cmd]()                              
                else:
                    print("Error: unknown command!")
        except (KeyboardInterrupt, EOFError):
            print()
            print("Bye!")
            sys.exit()
                    
def validate_name(name: str) -> bool:
    pattern = r"^[A-Za-z]([A-Za-z'-]*[A-Za-z])?$"
    if len(name) < 2:
        return False
    if not re.fullmatch(pattern, name):
        return False
    if "--" in name or "''" in name \
    or "-'" in name or "'-" in name:
        return False
    return True

def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.fullmatch(pattern, email))


if __name__ == "__main__":
    app = LearningProgressTracker()
    app.run()