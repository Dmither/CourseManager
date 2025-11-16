from modules.user import *
from modules.course import *
from modules.db_manager import DBManager

class Session(ABC):
    def __init__(self, email, password):
        self.__email = email
        self.__dbm = DBManager(password=password)
        self.__lessons = self.get_lessons()
        self.__modules = self.get_modules()
        self.__courses = self.get_courses()
        self.__students = self.get_students()
        self.__instructors = self.get_instructors()
        self.__admins = self.get_admins()
        self.__object = None

    @property
    def email(self):
        return self.__email

    @property
    def dbm(self):
        return self.__dbm

    @property
    def lessons(self):
        return self.__lessons

    @property
    def modules(self):
        return self.__modules

    @property
    def courses(self):
        return self.__courses

    @property
    def students(self):
        return self.__students

    @property
    def instructors(self):
        return self.__instructors

    @property
    def admins(self):
        return self.__admins

    def get_lessons(self):
        lessons = []
        for lesson_id, title, module_id in self.__dbm.get_lessons():
            lessons.append(Lesson(lesson_id, title, module_id))
        return lessons

    def get_modules(self):
        modules = []
        for module_id, title, course_id in self.__dbm.get_modules():
            lessons = []
            for lesson in self.__lessons:
                if lesson.module_id == module_id:
                    lessons.append(lesson)
            modules.append(Module(module_id, title, course_id, lessons))
        return modules

    def get_courses(self):
        courses = []
        for course_id, title, description, instructor_id in self.__dbm.get_courses():
            modules = []
            for module in self.__modules:
                if module.course_id == course_id:
                    modules.append(module)
            courses.append(Course(course_id, title, description, instructor_id, modules))
        return courses

    def get_students(self):
        students = []

        for user_id, name, email, role in self.__dbm.get_users_by_role_id(1):
            courses = []
            for student_id, course_id in self.__dbm.get_enrollments():
                if student_id == user_id:
                    course = self.__dbm.get_course_by_id(course_id)[1]
                    courses.append(course)
            students.append(Student(user_id, name, email, courses))
        return students

    def get_instructors(self):
        instructors = []

        for user_id, name, email, role in self.__dbm.get_users_by_role_id(2):
            courses = []
            for course_id, title, desc, instr_id in self.__dbm.get_courses():
                if instr_id == user_id:
                    courses.append(title)
            instructors.append(Instructor(user_id, name, email, courses))
        return instructors

    def get_admins(self):
        admins = []
        for user_id, name, email, role in self.__dbm.get_users_by_role_id(3):
            admins.append(Admin(user_id, name, email))
        return admins


class StudentSession(Session):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.__account: Student = self.get_self()

    @property
    def account(self):
        return self.__account

    def get_self(self):
        for student in self.students:
            if student.email == self.email:
                return student
        raise ValueError('There are no students with such email')

    def add_course(self, course_title: str):
        if not course_title in [course.title for course in self.courses]:
            raise ValueError('There is no course with such title')
        self.__account.courses.append(course_title)
        for course in self.courses:
            if course.title == course_title:
                self.dbm.add_enrollment(self.__account.user_id, course.course_id)


class InstructorSession(Session):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.__account: Instructor = self.get_self()

    @property
    def account(self):
        return self.__account

    def get_self(self):
        for instructor in self.instructors:
            if instructor.email == self.email:
                return instructor
        raise ValueError('There are no instructors with such email')

    def create_module(self, title, course_id):
        for course in self.courses:
            if course.course_id == course_id and course.instructor_id == self.account.user_id:
                module_id = self.dbm.add_module(title, course_id)
                module = Module(module_id, title, course_id, [])
                self.modules.append(module)
                return
        raise ValueError('You can add modules only for courses you teach')

    def create_lesson(self, title, module_id):
        for course in self.courses:
            if course.instructor_id == self.account.user_id:
                for module in course.modules:
                    if module.module_id == module_id:
                        lesson_id = self.dbm.add_lesson(title, module_id)
                        lesson = Lesson(lesson_id, title, module_id)
                        self.lessons.append(lesson)
                        return
        raise ValueError('You can add lessons only for courses you teach')

class AdminSession(Session):
    def create_course(self, title, description, instructor_id):
        course_id = self.dbm.add_course(title, description, instructor_id)
        course = Course(course_id, title, description, instructor_id)
        self.courses.append(course)

    def create_user(self, name, email, role_id):
        user_id = self.dbm.add_user(name, email, role_id)
        match role_id:
            case 1:
                student = Student(user_id, name, email, [])
                self.students.append(student)
            case 2:
                instructor = Instructor(user_id, name, email, [])
                self.instructors.append(instructor)
            case 3:
                admin = Admin(user_id, name, email)
                self.admins.append(admin)
            case _:
                raise ValueError('There are no roles with such ID')
