from modules.user import User, Student, Instructor, Admin



class Session:
    def __init__(self, user):
        self.__user = user

    def add_user(self, name: str, role: int):
        if type(self.__user) != Admin:
            raise PermissionError('Only Admin can create other users')
        if type(name) != str:
            raise ValueError('User name must be a string')
        if type(role) != int or not role in [1, 2, 3]:
            raise ValueError('Role must be a number (1/2/3)')
        match role:
            case 1:
                return Student(name)
            case 2:
                return Instructor(name)
            case 3:
                return Admin(name)

if __name__ == '__main__':
    print('Hello, CourseManager!')
