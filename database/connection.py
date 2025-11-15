import pyodbc
from config import DB_CONFIG

class DatabaseConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def connect(self):
        """Tạo kết nối đến SQL Server"""
        try:
            conn_str = (
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"UID={DB_CONFIG['username']};"
                f"PWD={DB_CONFIG['password']}"
            )
            self._connection = pyodbc.connect(conn_str)
            print("✓ Kết nối database thành công!")
            return self._connection
        except Exception as e:
            print(f"✗ Lỗi kết nối database: {e}")
            return None
    
    def get_connection(self):
        """Lấy connection hiện tại"""
        if self._connection is None:
            return self.connect()
        return self._connection
    
    def close(self):
        """Đóng kết nối"""
        if self._connection:
            self._connection.close()
            print("✓ Đã đóng kết nối database")
    
    def execute_query(self, query, params=None):
        """Thực thi câu lệnh SELECT"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"✗ Lỗi execute_query: {e}")
            return []
    
    def execute_non_query(self, query, params=None):
        """Thực thi INSERT, UPDATE, DELETE"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return True
        except Exception as e:
            print(f"✗ Lỗi execute_non_query: {e}")
            conn.rollback()
            return False
    
    def execute_scalar(self, query, params=None):
        """Lấy giá trị đơn (COUNT, MAX, etc.)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"✗ Lỗi execute_scalar: {e}")
            return None