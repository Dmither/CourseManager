import mysql.connector as connector
from validate_email_address import validate_email


class DBManager:
    def __init__(self, host:str='localhost', user:str='root', password:str='', database:str='course_manager', roles:list[str]=None):
        if not database.isidentifier():
            raise ValueError('Invalid database name')
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__roles = roles if roles else ['Student', 'Instructor', 'Admin']

        self.__check_db()
        self.__check_tables()


    def __execute(self, operation: str, params=None, commit=False, fetch=False, nodb=False):
        with connector.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            database=None if nodb else self.__database
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(
                operation, params
            )
            if commit:
                connection.commit()
                return cursor.lastrowid
            if fetch:
                return cursor.fetchall()
            return None

    def __executemany(self, operation: str, seq_params: list=None):
        with connector.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            database=self.__database
        ) as connection:
            cursor = connection.cursor()
            cursor.executemany(operation, seq_params)
            connection.commit()
            return cursor.lastrowid, cursor.rowcount

    def __check_db(self):
        self.__execute(f'create database if not exists {self.__database}', nodb=True)

    def drop_db(self):
        self.__execute(f'drop database {self.__database}', nodb=True)

    def __check_tables(self):
        self.__execute('''
            create table if not exists roles(
                Id int primary key auto_increment,
                `Name` varchar(31) not null unique
            );
        ''')
        roles = [role_data[1] for role_data in self.__execute('select * from roles', fetch=True)]
        roles = [role for role in self.__roles if not role in roles]
        # try:
        self.__executemany('''
            insert into roles(Name) values (%s);
            ''',[(role,) for role in roles]
        )
        # except connector.errors.IntegrityError as e:
        #     pass
        self.__execute('''
            create table if not exists users(
                Id int primary key auto_increment,
                `Name` varchar(63) not null,
                Email varchar(64) not null unique,
                Role_id int not null,
                foreign key (role_id) references roles(Id)
            );
        ''')
        if not self.__execute(
           'select 1 from users',
            fetch=True
        ):
            self.__execute(
                'insert into users (`Name`, Email, Role_id) values (\'Admin\', \'admin@admin.com\', 3)',
                commit=True
            )

        self.__execute('''
            create table if not exists courses(
                Id int primary key auto_increment,
                Title varchar(31) not null unique,
                `Description` varchar(255) not null,
                Instructor_id int not null,
                foreign key (Instructor_id) references users(Id)
            );
        ''')

        self.__execute('''
            create table if not exists modules(
                Id int primary key auto_increment,
                Title varchar(31) not null unique,
                Course_id int not null,
                foreign key (Course_id) references courses(Id)
            );
        ''')

        self.__execute('''
            create table if not exists lessons(
                Id int primary key auto_increment,
                Title varchar(31) not null unique,
                Module_id int not null,
                foreign key (Module_id) references modules(Id)
            );
        ''')

        self.__execute('''
            create table if not exists enrollments(
                Student_id int not null,
                Course_id int not null,
                foreign key (Student_id) references users(Id),
                foreign key (Course_id) references courses(Id),
                primary key (Student_id, Course_id)
            );
        ''')

    def add_role(self, name: str):
        roles = self.__execute('select Id, `Name` from roles', fetch=True)
        role_names = tuple(i[1].lower() for i in roles)
        if name.lower() in role_names:
            raise ValueError('There is such role already')
        self.__execute('insert into roles (`Name`) values (%s)', (name,), commit=True)

    def get_roles(self):
        roles = self.__execute(
            '''
            select * from roles order by Id
        ''', fetch=True
        )
        return roles

    def add_user(self, name: str, email: str, role_id: int):
        if not validate_email(email):
            raise ValueError('Invalid email')
        if self.__execute(
            'SELECT 1 FROM users where `Email` = %s',
            (email,),
            fetch=True
        ):
            raise ValueError('There is user with such email')
        roles = self.get_roles()
        roles_id = tuple(i[0] for i in roles)
        if not role_id in roles_id:
            raise ValueError('There is no such role id')
        result = self.__execute(
            'insert into users (`Name`, Email, Role_id) values (%s, %s, %s)',
            (name, email, role_id),
            commit=True
        )
        return result

    def get_users(self):
        users = self.__execute(
            '''
            select * from users order by Id
        ''', fetch=True
        )
        return users

    def get_users_by_role_id(self, role_id: int):
        users = self.__execute(
            '''
                select * from users where Role_id = %s order by Id
            ''',
            (role_id,),
            fetch=True
        )
        return users

    def get_user_by_id(self, user_id: int):
        res = self.__execute(
            'select * from users where Id = %s',
            (user_id,),
            fetch=True
        )
        if not res:
            raise ValueError('There is no user with such ID')
        return res[0]

    def get_user_by_email(self, email: str):
        res = self.__execute(
            'select * from users where Email = %s',
            (email,),
            fetch=True
        )
        if not res:
            raise ValueError('There is no user with such Email')
        return res[0]

    def add_course(self, title: str, description: str, instructor_id: int):
        if self.__execute(
            'SELECT 1 FROM courses where `Title` = %s',
            (title,),
            fetch=True
        ):
            raise ValueError('There is a course with such title')
        if self.get_user_by_id(instructor_id)[3] != 2:
            raise ValueError('Only Instructor can teach')
        res = self.__execute(
            'insert into courses(Title, Description, Instructor_id) values (%s, %s, %s)',
            (title, description, instructor_id),
            commit=True
        )
        return res

    def get_courses(self):
        return self.__execute(
            'select * from courses order by Id',
            fetch=True
        )

    def get_course_by_id(self, course_id: int):
        res = self.__execute(
            'select * from courses where Id = %s',
            (course_id,),
            fetch=True
        )
        if not res:
            raise ValueError('There is no course with such ID')
        return res[0]

    def add_module(self, title: str, course_id: int):
        if self.__execute(
                'SELECT 1 FROM modules where `Title` = %s',
                (title,),
                fetch=True
        ):
            raise ValueError('There is a module with such title')
        self.get_course_by_id(course_id)
        res = self.__execute(
            'insert into modules(Title, Course_id) values (%s, %s)',
            (title, course_id),
            commit=True
        )
        return res

    def get_modules(self):
        return self.__execute(
            'select * from modules order by Id',
            fetch=True
        )

    def get_module_by_id(self, module_id: int):
        res = self.__execute(
            'select * from modules where Id = %s',
            (module_id,),
            fetch=True
        )
        if not res:
            raise ValueError('There is no module with such ID')
        return res[0]

    def add_lesson(self, title: str, module_id: int):
        if self.__execute(
                'SELECT 1 FROM lessons where `Title` = %s',
                (title,),
                fetch=True
        ):
            raise ValueError('There is a lesson with such title')
        self.get_module_by_id(module_id)
        res = self.__execute(
            'insert into lessons(Title, Module_id) values (%s, %s)',
            (title, module_id),
            commit=True
        )
        return res

    def get_lessons(self):
        return self.__execute(
            'select * from lessons order by Id',
            fetch=True
        )

    def get_lesson_by_id(self, lesson_id: int):
        res = self.__execute(
            'select * from lessons where Id = %s',
            (lesson_id,),
            fetch=True
        )
        if not res:
            raise ValueError('There is no lesson with such ID')
        return res[0]

    def check_enrollment(self, student_id, course_id):
        return bool(self.__execute(
            'SELECT 1 FROM enrollments where Student_id = %s and Course_id = %s',
            (student_id, course_id),
            fetch=True
        ))

    def add_enrollment(self, student_id, course_id):
        if self.check_enrollment(student_id, course_id):
            raise ValueError('This student has already enrolled for this course')
        if self.get_user_by_id(student_id)[3] != 1:
            raise ValueError('Only Student can enroll')
        res = self.__execute(
            'insert into enrollments(Student_id, Course_id) values (%s, %s)',
            (student_id, course_id),
            commit=True
        )
        return res

    def get_enrollments(self):
        return self.__execute(
            'select * from enrollments order by Student_id',
            fetch=True
        )


if __name__ == '__main__':
    dbm = DBManager(password='111111')
    dbm.drop_db()

    dbm = DBManager(password='111111')

    dbm.add_user('Ethan', 'ethanator@gmail.com', 2)
    dbm.add_user('Sam', 'sam@example.com', 1)
    dbm.add_user('Carl', 'carl@example.com', 1)
    dbm.add_user('Carter', 'teacher1@gmail.com', 2)
    print(dbm.get_users())
    print(dbm.get_users_by_role_id(1))

    dbm.add_course('DA', 'Data analysis', 2)
    dbm.add_course('Web', 'Web Design', 5)
    print(dbm.get_courses())
    print(dbm.get_course_by_id(2))

    dbm.add_module('Intro to SQL', 1)
    dbm.add_module('Python for DA', 1)
    print(dbm.get_modules())

    dbm.add_lesson('Intro to Python', 2)
    dbm.add_lesson('Python variables', 2)
    print(dbm.get_lessons())

    dbm.add_enrollment(3, 1)
    dbm.add_enrollment(3, 2)
    dbm.add_enrollment(4, 2)
    print(dbm.get_enrollments())
    print(dbm.check_enrollment(3, 1))
    print(dbm.check_enrollment(2, 1))