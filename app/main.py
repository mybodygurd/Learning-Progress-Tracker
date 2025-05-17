import sys
import re
from dataclasses import dataclass, field
# email.utils
@dataclass
class Student:
    id: int
    first_name: str
    last_name: str
    email: str
    courses: dict = field(default_factory=lambda: {
        "Python": 0,
        "DSA": 0,
        "Databases": 0,
        "Flask": 0
    })
    
class LearningProgressTracker:
    def __init__(self) -> None:
        self.students = {}
        self.commands = {"exit": self.cmd_exit,
                        "add_students": self.cmd_add_std,
                        "list": self.list_std,
                        "add_points": self.add_points,
                        "find": self.find_std
                        }
        self.next_id = 1000

    def cmd_exit(self) -> None:
        print("Bye!")
        sys.exit(0)
        
    def generate_id(self):
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
            else:
                print(f"No student is found for id={id}")
                continue
            print("Points updated.")
            
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
                print(f"No student is found for id={id}")
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