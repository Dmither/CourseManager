from user import User, Student, Instructor, Admin
from course import Course, Lesson


class Assignment:
    def __init__(self, title: str, lesson: Lesson):
        self.__title = title
        self.__lesson = lesson


class Enrollment:
    def __init__(self, student: Student, course: Course):
        self.__student = student
        self.__course = course
        self.__grades: list[Grade] = []


class Grade:
    def __init__(self, enrollment: Enrollment, score: float):
        self.__enrollment = enrollment
        self.__score = score