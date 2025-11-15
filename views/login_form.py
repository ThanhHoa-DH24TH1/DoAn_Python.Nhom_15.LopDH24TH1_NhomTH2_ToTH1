import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
from dao.user_dao import UserDAO
from dao.student_dao import StudentDAO

class LoginForm:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Đăng nhập - Quản lý Ký túc xá")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Căn giữa màn hình
        self.center_window()
        
        # DAO
        self.user_dao = UserDAO()
        self.student_dao = StudentDAO()
        
        # Biến lưu thông tin user
        self.current_user = None
        
        # Tạo giao diện
        self.create_widgets()
    
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Tạo các widget"""
        # Frame chính
        main_frame = tk.Frame(self.window, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tiêu đề
        title_label = tk.Label(
            main_frame,
            text="ĐĂNG NHẬP HỆ THỐNG",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg="#2387D9"
        )
        title_label.pack(pady=(0, 30))
        
        # Frame nhập liệu
        input_frame = tk.Frame(main_frame, bg='white')
        input_frame.pack(pady=10)
        
        # Username
        tk.Label(
            input_frame,
            text="Tên đăng nhập:",
            font=('Arial', 10),
            bg='white'
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        self.username_entry = tk.Entry(
            input_frame,
            font=('Arial', 10),
            width=25
        )
        self.username_entry.grid(row=0, column=1, pady=10, padx=(10, 0))
        self.username_entry.focus()
        
        # Password
        tk.Label(
            input_frame,
            text="Mật khẩu:",
            font=('Arial', 10),
            bg='white'
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        self.password_entry = tk.Entry(
            input_frame,
            font=('Arial', 10),
            width=25,
            show='●'
        )
        self.password_entry.grid(row=1, column=1, pady=10, padx=(10, 0))
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Frame buttons
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(pady=30)
        
        # Button Đăng nhập
        login_btn = tk.Button(
            button_frame,
            text="Đăng nhập",
            font=('Arial', 10, 'bold'),
            bg='#2196F3',
            fg='white',
            width=12,
            height=1,
            cursor='hand2',
            command=self.login
        )
        login_btn.grid(row=0, column=0, padx=5)
        
        # Button Thoát
        exit_btn = tk.Button(
            button_frame,
            text="Thoát",
            font=('Arial', 10),
            bg='#f44336',
            fg='white',
            width=12,
            height=1,
            cursor='hand2',
            command=self.window.quit
        )
        exit_btn.grid(row=0, column=1, padx=5)
        
        # Label hướng dẫn
        info_label = tk.Label(
            main_frame,
            text="Admin: admin/123456 | SV: sv2001/123456",
            font=('Arial', 8),
            bg='white',
            fg='gray'
        )
        info_label.pack(side='bottom', pady=10)
    
    def hash_password(self, password):
        """Mã hóa mật khẩu MD5"""
        return hashlib.md5(password.encode()).hexdigest()
    
    def login(self):
        """Xử lý đăng nhập"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validate (vẫn giữ nguyên)
        if not username:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên đăng nhập!")
            self.username_entry.focus()
            return
        if not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mật khẩu!")
            self.password_entry.focus()
            return
        
        # ==========================================================
        # BƯỚC 1: THỬ ĐĂNG NHẬP VỚI VAI TRÒ ADMIN (USER TỪ BẢNG USERS)
        # ==========================================================
        hashed_password = self.hash_password(password)
        user = self.user_dao.authenticate(username, hashed_password)
        
        if user:
            # Đăng nhập Admin/User thành công
            self.current_user = {
                'user_id': user[0],
                'username': user[1],
                'full_name': user[2],
                'role': user[3]
            }
            
            messagebox.showinfo(
                "Thành công", 
                f"Xin chào {self.current_user['full_name']}!"
            )
            
            self.window.destroy()
            self.open_main_form()
            return # Thoát hàm sau khi đăng nhập thành công

        # ==========================================================
        # BƯỚC 2: NẾU ADMIN THẤT BẠI, THỬ ĐĂNG NHẬP VỚI VAI TRÒ SINH VIÊN
        # ==========================================================
        
        # Mật khẩu cố định cho sinh viên (dựa theo gợi ý của bạn)
        STUDENT_FIXED_PASSWORD = '12345' 
        
        if password == STUDENT_FIXED_PASSWORD:
            # Mật khẩu SV đúng, kiểm tra xem username có phải là MSSV không
            # (Giả sử hàm này lấy SV bằng Mã SV)
            student_data = self.student_dao.get_student_by_code(username) 
            
            if student_data:
                # Đăng nhập Sinh viên thành công
                # (Hãy đảm bảo các chỉ số [0], [1], [2] khớp với CSDL của bạn)
                self.current_user = {
                    'user_id': student_data[0],   # ID chính (ví dụ: 1, 2, 3)
                    'username': student_data[1],  # Mã SV (ví dụ: 'sv2001')
                    'full_name': student_data[2], # Họ tên
                    'role': 'Student'             # Gán vai trò là 'Student'
                }
                
                messagebox.showinfo(
                    "Thành công", 
                    f"Xin chào sinh viên {self.current_user['full_name']}!"
                )
                
                self.window.destroy()
                self.open_main_form() # Hàm này sẽ tự động mở form sinh viên
                return # Thoát hàm

        # ==========================================================
        # BƯỚC 3: NẾU CẢ HAI ĐỀU THẤT BẠI
        # ==========================================================
        messagebox.showerror(
            "Lỗi", 
            "Tên đăng nhập hoặc mật khẩu không đúng!"
        )
        self.password_entry.delete(0, tk.END)
        self.password_entry.focus()
    
    def open_main_form(self):
        """Mở form chính theo role"""
        if self.current_user['role'] == 'Admin':
            from views.main_admin_form import MainAdminForm
            MainAdminForm(self.current_user)
        else:
            from views.main_student_form import MainStudentForm
            MainStudentForm(self.current_user)
    
    def run(self):
        """Chạy ứng dụng"""
        self.window.mainloop()