from abc import ABC


class User(ABC):
    def __init__(self, user_id: int, name: str):
        self.__user_id = user_id
        self.__name = name

    @property
    def user_id(self):
        return self.__user_id

    @property
    def user_name(self):
        return self.__name

    def __repr__(self):
        return f'{self.__class__.__name__} {self.__name}'


class Student(User):
    def __init__(self, user_id: int, name: str, courses: list[str] | tuple[str] = (), grades: list[int] | tuple[int] = ()):
        super().__init__(user_id, name)
        self.__courses = []
        self.add_courses(*courses)

    @property
    def courses(self):
        return self.__courses

    def add_courses(self, *courses: str):
        added = 0
        for course in courses:
            if type(course) != str or course in self.__courses:
                continue
            added += 1
            self.__courses.append(course)
        return f'{added} courses have been added'

    def remove_courses(self, *courses: str):
        removed = 0
        for course in courses:
            if type(course) != str or not course in self.__courses:
                continue
            removed += 1
            self.__courses.remove(course)
        return f'{removed} courses have been removed'

    def __repr__(self):
        return f'{super().__repr__()}, learn: {', '.join(self.__courses)}'


class Instructor(User):
    def __init__(self, user_id: int, name: str, courses: list[str] | tuple[str] = ()):
        super().__init__(user_id, name)
        self.__courses = []
        self.add_courses(*courses)

    @property
    def courses(self):
        return self.__courses

    def add_courses(self, *courses: str):
        added = 0
        for course in courses:
            if type(course) != str or course in self.__courses:
                continue
            added += 1
            self.__courses.append(course)
        return f'{added} courses have been added'

    def remove_courses(self, *courses: str):
        removed = 0
        for course in courses:
            if type(course) != str or not course in self.__courses:
                continue
            removed += 1
            self.__courses.remove(course)
        return f'{removed} courses have been removed'

    def __repr__(self):
        return f'{super().__repr__()}, teach: {', '.join(self.__courses)}'


class Admin(User):
    def __init__(self, user_id: int, name: str):
        super().__init__(user_id, name)

    def __repr__(self):
        return f'{super().__repr__()}, and I\'m cool!'



if __name__ == '__main__':
    student = Student(1,'Sam')
    print(student)
    instructor = Instructor(2,'John Doe')
    print(instructor)
    admin = Admin(3,'Bill Gates')
    print(admin)