import tkinter as tk
from tkinter import messagebox
from database.connection import DatabaseConnection
from views.login_form import LoginForm

def main():
    """Hàm main - Entry point"""
    try:
        # Kiểm tra kết nối database
        print("=" * 50)
        print("KHỞI ĐỘNG ỨNG DỤNG QUẢN LÝ KÝ TÚC XÁ")
        print("=" * 50)
        
        db = DatabaseConnection()
        conn = db.connect()
        
        if conn is None:
            messagebox.showerror(
                "Lỗi kết nối",
                "Không thể kết nối đến cơ sở dữ liệu!\n\n"
                "Vui lòng kiểm tra:\n"
                "1. SQL Server đã được khởi động\n"
                "2. Thông tin kết nối trong config.py\n"
                "3. Database 'DormitoryDB' đã được tạo"
            )
            return
        
        print("\n✓ Kết nối database thành công!")
        print("✓ Đang khởi động giao diện đăng nhập...\n")
        
        # Mở form đăng nhập
        login_form = LoginForm()
        login_form.run()
        
    except Exception as e:
        print(f"\n✗ Lỗi khởi động ứng dụng: {e}")
        messagebox.showerror("Lỗi", f"Lỗi khởi động ứng dụng:\n{e}")

if __name__ == "__main__":
    main()