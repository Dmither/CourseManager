from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, name: str):
        self.__name = name

    def __repr__(self):
        return f'{self.__class__.__name__} {self.__name}'


class Student(User):
    def __init__(self, name: str):
        super().__init__(name)

    def enroll(self, course):
        pass


class Instructor(User):
    def __init__(self, name: str):
        super().__init__(name)

    def add_module(self):
        pass

    def add_lesson(self):
        pass

    def add_assignment(self):
        pass

    def add_grade(self):
        pass


class Admin(User):
    def __init__(self, name: str):
        super().__init__(name)

    def add_user(self):
        pass

    def add_course(self):
        pass

    def __repr__(self):
        return f'{super().__repr__()}, and I\'m cool!'



if __name__ == '__main__':
    student = Student('Sam')
    print(student)
    instructor = Instructor('John Doe')
    print(instructor)
    admin = Admin('Bill Gates')
    print(admin)