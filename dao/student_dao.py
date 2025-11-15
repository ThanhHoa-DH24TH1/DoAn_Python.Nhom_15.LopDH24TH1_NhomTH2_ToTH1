from database.connection import DatabaseConnection
from models.student import Student

class StudentDAO:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all_students(self):
        """Lấy tất cả sinh viên"""
        query = """
            SELECT s.*, r.RoomNumber
            FROM Students s
            LEFT JOIN Contracts c ON s.StudentID = c.StudentID AND c.Status = N'Đang hiệu lực'
            LEFT JOIN Rooms r ON c.RoomID = r.RoomID
            ORDER BY s.StudentCode
        """
        rows = self.db.execute_query(query)
        return rows
    
    def get_student_by_id(self, student_id):
        """Lấy sinh viên theo ID"""
        query = "SELECT * FROM Students WHERE StudentID = ?"
        rows = self.db.execute_query(query, (student_id,))
        return rows[0] if rows else None
    
    def get_student_by_code(self, student_code):
        """Lấy sinh viên theo MSSV"""
        query = "SELECT * FROM Students WHERE StudentCode = ?"
        rows = self.db.execute_query(query, (student_code,))
        return rows[0] if rows else None
    
    def search_students(self, keyword, faculty=None):
        """Tìm kiếm sinh viên"""
        query = """
            SELECT s.*, r.RoomNumber
            FROM Students s
            LEFT JOIN Contracts c ON s.StudentID = c.StudentID AND c.Status = N'Đang hiệu lực'
            LEFT JOIN Rooms r ON c.RoomID = r.RoomID
            WHERE (s.StudentCode LIKE ? OR s.FullName LIKE ? OR s.PhoneNumber LIKE ?)
        """
        params = [f'%{keyword}%', f'%{keyword}%', f'%{keyword}%']
        
        if faculty and faculty != 'Tất cả':
            query += " AND s.Faculty = ?"
            params.append(faculty)
        query += " ORDER BY s.StudentCode"
        return self.db.execute_query(query, tuple(params))
    
    def add_student(self, student):
        """Thêm sinh viên mới"""
        query = """
            INSERT INTO Students (StudentCode, FullName, DateOfBirth, Gender, 
                                PhoneNumber, Email, IDCard, Address, Faculty, 
                                Major, Class, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            student.student_code, student.full_name, student.date_of_birth,
            student.gender, student.phone, student.email, student.id_card,
            student.address, student.faculty, student.major, 
            student.class_name, student.status
        )
        return self.db.execute_non_query(query, params)
    
    def update_student(self, student):
        """Cập nhật thông tin sinh viên"""
        query = """
            UPDATE Students SET
                FullName = ?, DateOfBirth = ?, Gender = ?,
                PhoneNumber = ?, Email = ?, Address = ?,
                Faculty = ?, Major = ?, Class = ?, Status = ?
            WHERE StudentID = ?
        """
        params = (
            student.full_name, student.date_of_birth, student.gender,
            student.phone, student.email, student.address,
            student.faculty, student.major, student.class_name,
            student.status, student.student_id
        )
        return self.db.execute_non_query(query, params)
    
    def delete_student(self, student_id):
        """Xóa sinh viên"""
        query = "DELETE FROM Students WHERE StudentID = ?"
        return self.db.execute_non_query(query, (student_id,))
    
    def get_students_without_room(self):
        """Lấy danh sách SV chưa có phòng"""
        query = """
            SELECT StudentID, StudentCode, FullName, Faculty, Class
            FROM Students
            WHERE StudentID NOT IN (
                SELECT StudentID FROM Contracts WHERE Status = N'Đang hiệu lực'
            )
            AND Status = N'Đang ở'
            ORDER BY StudentCode
        """
        return self.db.execute_query(query)
    
    def get_faculties(self):
        """Lấy danh sách các khoa"""
        query = "SELECT DISTINCT Faculty FROM Students ORDER BY Faculty"
        rows = self.db.execute_query(query)
        return [row[0] for row in rows]