from database.connection import DatabaseConnection

class UserDAO:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def authenticate(self, username, password):
        """Xác thực đăng nhập"""
        query = """
            SELECT UserID, Username, FullName, Role 
            FROM Users 
            WHERE Username = ? AND Password = ? AND IsActive = 1
        """
        rows = self.db.execute_query(query, (username, password))
        return rows[0] if rows else None
    
    def get_user_by_username(self, username):
        """Lấy user theo username"""
        query = "SELECT * FROM Users WHERE Username = ?"
        rows = self.db.execute_query(query, (username,))
        return rows[0] if rows else None
    
    def change_password(self, username, new_password):
        """Đổi mật khẩu"""
        query = "UPDATE Users SET Password = ? WHERE Username = ?"
        return self.db.execute_non_query(query, (new_password, username))