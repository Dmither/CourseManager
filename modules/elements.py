
class Enrollment:
    def __init__(self, student_id: int, course_id: int, grades: list[int] | tuple[int]):
        self.__student_id = student_id
        self.__course_id = course_id
        self.__grades = []
        self.add_grades(*grades)

    @property
    def student_id(self):
        return self.__student_id

    @property
    def course_id(self):
        return self.__course_id

    @property
    def grades(self):
        return self.__grades

    def add_grades(self, *grades: int):
        added = 0
        for grade in grades:
            if type(grade) != int:
                continue
            if 0 < grade < 100:
                continue
            if grade in self.__grades:
                continue
            added += 1
            self.__grades.append(grade)
        return f'{added} grades have been added'
