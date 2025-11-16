from modules.session import *


if __name__ == '__main__':
    session = AdminSession('admin@admin.com', '111111')
    for course in session.get_courses():
        print(course.title)
        for module in course.modules:
            print(f'\t{module.title}')
            for lesson in module.lessons:
                print(f'\t\t{lesson.title}')
    for student in session.students:
        print(student)
    for instructor in session.instructors:
        print(instructor)
    for admin in session.admins:
        print(admin)
    # print(session.account)
    print(session.courses)
    print(session.modules)
    print(session.lessons)
    # session.create_user('Ingvar', 'viking12@gmail.com', 2)
    # session.create_course('Viking arts', 'Axe battle and Rune magic', 6)