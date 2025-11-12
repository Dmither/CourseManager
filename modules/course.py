from user import User, Student, Instructor, Admin


class Lesson:
    def __init__(self, title: str):
        self.__title = title

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str):
        if type(value) != str:
            raise ValueError('Lesson\'s title must be a string')
        self.__title = value


class Module:
    def __init__(self, title: str, lessons: list[Lesson] | tuple[Lesson] = ()):
        self.__title = title
        self.__lessons = list(lessons)

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str):
        if type(value) != str:
            raise ValueError('Module\'s title must be a string')
        self.__title = value

    def add_lesson(self, lesson: Lesson):
        if type(lesson) != Lesson:
            raise ValueError('Cannon add not a Lesson class object')
        self.__lessons.append(lesson)


class Course:
    def __init__(self, title: str, description: str, instructor: Instructor, modules: list[Module] | tuple[Module] = ()):
        self.__title = title
        self.__description = description
        self.__instructor = instructor
        self.__modules: list[Module] = modules

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str):
        if type(value) != str:
            raise ValueError('Course\'s title must be a string')
        self.__title = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value: str):
        if type(value) != str:
            raise ValueError('Course\'s description must be a string')
        self.__description = value

    def add_module(self, module: Module):
        if type(module) != Module:
            raise ValueError('Cannon add not a Module class object')
        self.__modules.append(module)