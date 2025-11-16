
class Lesson:
    def __init__(self, lesson_id: int, title: str, module_id: int):
        self.__lesson_id = lesson_id
        self.__title = title
        self.__module_id = module_id

    @property
    def lesson_id(self):
        return self.__lesson_id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str):
        if type(value) != str:
            raise ValueError('Lesson\'s title must be a string')
        self.__title = value

    @property
    def module_id(self):
        return self.__module_id

    @module_id.setter
    def module_id(self, value: int):
        if type(value) != int:
            raise ValueError('Module id must be an integer')
        self.__module_id = value

    def __repr__(self):
        return f'Lesson {self.lesson_id}: {self.title}'


class Module:
    def __init__(self, module_id: int, title: str, course_id: int, lessons: list[Lesson] | tuple[Lesson] = ()):
        self.__module_id = module_id
        self.__title = title
        self.__course_id = course_id
        self.__lessons = []
        for lesson in lessons:
            self.add_lesson(lesson)

    @property
    def module_id(self):
        return self.__module_id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str):
        if type(value) != str:
            raise ValueError('Module\'s title must be a string')
        self.__title = value

    @property
    def course_id(self):
        return self.__course_id

    @course_id.setter
    def course_id(self, value: int):
        if type(value) != int:
            raise ValueError('Course id must be an integer')
        self.__course_id = value

    @property
    def lessons(self):
        return self.__lessons

    def add_lesson(self, lesson: Lesson):
        if type(lesson) != Lesson:
            raise ValueError('Cannot add not a Lesson class object')
        if lesson in self.__lessons:
            raise ValueError('This lesson is already added')
        self.__lessons.append(lesson)

    def remove_lesson(self, lesson: Lesson):
        if not lesson in self.__lessons:
            raise ValueError('There are no such lessons')
        self.__lessons.append(lesson)

    def __len__(self):
        return len(self.__lessons)

    def __repr__(self):
        return f'Module {self.module_id}: {self.title}'


class Course:
    def __init__(self, course_id: int, title: str, description: str, instructor_id: int, modules: list[Module] | tuple[Module] = ()):
        self.__course_id = course_id
        self.__title = title
        self.__description = description
        self.__instructor_id = instructor_id
        self.__modules = []
        for module in modules:
            self.add_module(module)

    @property
    def course_id(self):
        return self.__course_id

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

    @property
    def instructor_id(self):
        return self.__instructor_id

    @instructor_id.setter
    def instructor_id(self, value: int):
        if type(value) != int:
            raise ValueError('Instructor id must be an integer')
        self.__instructor_id = value

    @property
    def modules(self):
        return self.__modules

    def add_module(self, module: Module):
        if type(module) != Module:
            raise ValueError('Cannon add not a Module class object')
        if module in self.__modules:
            raise ValueError('This module is already added')
        self.__modules.append(module)

    def remove_lesson(self, module: Module):
        if not module in self.__modules:
            raise ValueError('There are no such lessons')
        self.__modules.append(module)

    def __len__(self):
        return len(self.__modules)

    def __repr__(self):
        return f'Course {self.course_id}: {self.title}'