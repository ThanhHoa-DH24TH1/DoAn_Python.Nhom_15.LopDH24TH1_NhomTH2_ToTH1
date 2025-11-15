class Student:
    def __init__(self, student_id=None, student_code='', full_name='', 
                 date_of_birth=None, gender='', phone='', email='', 
                 id_card='', address='', faculty='', major='', 
                 class_name='', status='Đang ở', user_id=None):
        self.student_id = student_id
        self.student_code = student_code
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone = phone
        self.email = email
        self.id_card = id_card
        self.address = address
        self.faculty = faculty
        self.major = major
        self.class_name = class_name
        self.status = status
        self.user_id = user_id
