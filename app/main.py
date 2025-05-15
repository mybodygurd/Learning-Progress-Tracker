import sys
import re
from dataclasses import dataclass
# email.utils
@dataclass
class Student:
    first_name: str
    last_name: str
    email: str
    
class LearningProgressTracker:
    def __init__(self) -> None:
        self.students = []
        self.commands = {"exit": self.cmd_exit,
                        "add": self.cmd_add_stud,
                        "back": self.cmd_back
                        }

    def cmd_exit(self) -> None:
        print("Bye!")
        sys.exit(0)
    
    def cmd_add_stud(self) -> None:
        print("Enter student credentials or 'back' to return")
        while True:
            inp = input("> ").strip()
            if not inp:
                print("Incorrect credentials")
                continue
            tokens = inp.split()
            if tokens[0] == "back":
                self.cmd_back()
                break
            try:
                f_name = tokens[0]
                l_name = ' '.join(tokens[1: -1])
                email = tokens[-1]
            except IndexError:
                print("Incorrect credentials")
                continue
            if any(s.email == email for s in self.students):
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
            student = Student(f_name, l_name, email)
            self.students.append(student)
            print("The student has been added")
            
            
    def cmd_back(self) -> None:
        print(f"Total {len(self.students)} students have been added.")
        
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