import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from dao.student_dao import StudentDAO
from dao.room_dao import RoomDAO
from dao.invoice_dao import InvoiceDAO

class MainAdminForm:
    def __init__(self, current_user):
        self.current_user = current_user
        self.window = tk.Tk()
        self.window.title(f"Quản lý Ký túc xá - {current_user['full_name']}")
        self.window.geometry("1200x700")
        self.window.state('zoomed')  # Maximize
        
        # DAOs
        self.student_dao = StudentDAO()
        self.room_dao = RoomDAO()
        self.invoice_dao = InvoiceDAO()
        
        # Tạo giao diện
        self.create_menu()
        self.create_widgets()
        self.load_dashboard_data()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def create_menu(self):
        """Tạo menu bar"""
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        # Menu Hệ thống
        system_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hệ thống", menu=system_menu)
        system_menu.add_command(label="Đổi mật khẩu", command=self.change_password)
        system_menu.add_separator()
        system_menu.add_command(label="Đăng xuất", command=self.logout)
        system_menu.add_command(label="Thoát", command=self.on_closing)
        
        # Menu Quản lý
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Quản lý", menu=manage_menu)
        manage_menu.add_command(label="Quản lý sinh viên", command=self.open_student_management)
        manage_menu.add_command(label="Quản lý phòng", command=self.open_room_management)
        manage_menu.add_command(label="Quản lý hợp đồng", command=self.open_contract_management)
        manage_menu.add_command(label="Quản lý thanh toán", command=self.open_payment_management)
        
        # Menu Báo cáo
        report_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Báo cáo", menu=report_menu)
        report_menu.add_command(label="Thống kê & Báo cáo", command=self.open_report)
        
        # Menu Trợ giúp
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        help_menu.add_command(label="Hướng dẫn", command=self.show_help)
        help_menu.add_command(label="Giới thiệu", command=self.show_about)
    
    def create_widgets(self):
        """Tạo giao diện chính"""
        # Container chính
        main_container = tk.Frame(self.window)
        main_container.pack(fill='both', expand=True)
        
        # Sidebar
        self.create_sidebar(main_container)
        
        # Main content area
        self.content_frame = tk.Frame(main_container, bg='#f5f5f5')
        self.content_frame.pack(side='left', fill='both', expand=True)
        
        # Dashboard
        self.create_dashboard()
        
        # Status bar
        self.create_statusbar()
    
    def create_sidebar(self, parent):
        """Tạo sidebar"""
        sidebar = tk.Frame(parent, bg='#2c3e50', width=200)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(sidebar, bg='#34495e', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="KÝ TÚC XÁ",
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(pady=25)
        
        # Menu buttons
        buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("👨‍🎓 Sinh viên", self.open_student_management),
            ("🏢 Phòng", self.open_room_management),
            ("📄 Hợp đồng", self.open_contract_management),
            ("💰 Thanh toán", self.open_payment_management),
            ("📊 Báo cáo", self.open_report)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                sidebar,
                text=text,
                font=('Arial', 10),
                bg='#2c3e50',
                fg='white',
                activebackground='#34495e',
                activeforeground='white',
                bd=0,
                cursor='hand2',
                anchor='w',
                padx=20,
                command=command
            )
            btn.pack(fill='x', pady=2)
            
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#34495e'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#2c3e50'))
    
    def create_dashboard(self):
        """Tạo dashboard"""
        # Title
        title_frame = tk.Frame(self.content_frame, bg='white', height=60)
        title_frame.pack(fill='x', padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="DASHBOARD - TỔNG QUAN",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=20, pady=15)
        
        # Stats cards frame
        self.stats_frame = tk.Frame(self.content_frame, bg='#f5f5f5')
        self.stats_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create 4 stat cards
        self.card_total_students = self.create_stat_card(
            self.stats_frame, "Tổng sinh viên", "0", "#3498db", 0
        )
        self.card_total_rooms = self.create_stat_card(
            self.stats_frame, "Tổng số phòng", "0", "#2ecc71", 1
        )
        self.card_empty_rooms = self.create_stat_card(
            self.stats_frame, "Phòng trống", "0", "#f39c12", 2
        )
        self.card_revenue = self.create_stat_card(
            self.stats_frame, "Doanh thu tháng", "0 đ", "#e74c3c", 3
        )
        
    
    def create_stat_card(self, parent, title, value, color, col):
        """Tạo card thống kê"""
        card = tk.Frame(parent, bg=color, relief='raised', bd=2)
        card.grid(row=0, column=col, padx=10, pady=10, sticky='nsew')
        
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(
            card,
            text=title,
            font=('Arial', 12),
            bg=color,
            fg='white'
        ).pack(pady=(20, 5))
        
        value_label = tk.Label(
            card,
            text=value,
            font=('Arial', 24, 'bold'),
            bg=color,
            fg='white'
        )
        value_label.pack(pady=(5, 20))
        
        return value_label
    
    def create_statusbar(self):
        """Tạo status bar"""
        statusbar = tk.Frame(self.window, bg='#34495e', height=25)
        statusbar.pack(side='bottom', fill='x')
        
        self.status_user = tk.Label(
            statusbar,
            text=f"👤 {self.current_user['full_name']} ({self.current_user['role']})",
            font=('Arial', 9),
            bg='#34495e',
            fg='white'
        )
        self.status_user.pack(side='left', padx=10)
        
        self.status_time = tk.Label(
            statusbar,
            text="",
            font=('Arial', 9),
            bg='#34495e',
            fg='white'
        )
        self.status_time.pack(side='right', padx=10)
        
        self.update_time()
    
    def update_time(self):
        """Cập nhật thời gian"""
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.status_time.config(text=f"🕐 {now}")
        self.window.after(1000, self.update_time)
    
    def load_dashboard_data(self):
        """Load dữ liệu dashboard"""
        try:
            # Tổng sinh viên
            students = self.student_dao.get_all_students()
            self.card_total_students.config(text=str(len(students)))
            
            # Tổng phòng
            rooms = self.room_dao.get_all_rooms()
            self.card_total_rooms.config(text=str(len(rooms)))
            
            # Phòng trống
            empty_rooms = [r for r in rooms if r[6] == 0]  # CurrentOccupancy = 0
            self.card_empty_rooms.config(text=str(len(empty_rooms)))
            
            # Doanh thu tháng hiện tại
            # 1. Lấy chuỗi "YYYY-MM" (ví dụ: "2025-10")
            current_month_str = datetime.now().strftime('%Y-%m') 

            # 2. Lấy hóa đơn "ĐÃ THANH TOÁN" của tháng này
            # (Vì hàm get_all_invoices của bạn chỉ nhận 'month' và 'status')
            invoices = self.invoice_dao.get_all_invoices(
                month=current_month_str, 
                status='Đã thanh toán' 
            )

            # 3. Tính tổng số tiền ĐÃ TRẢ (PaidAmount - giả sử là inv[10])
            total_revenue = sum(inv[10] for inv in invoices if inv[10] is not None) 
            self.card_revenue.config(text=f"{total_revenue:,.0f} đ")
            
        except Exception as e:
            print(f"Lỗi load dashboard: {e}")
    
    def show_dashboard(self):
        """Hiển thị dashboard"""
        self.load_dashboard_data()
        messagebox.showinfo("Thông tin", "Dashboard đã được làm mới!")
    
    def open_student_management(self):
        """Mở form quản lý sinh viên"""
        from views.student_management_form import StudentManagementForm
        StudentManagementForm(self.window)
    
    def open_room_management(self):
        """Mở form quản lý phòng"""
        from views.room_management_form import RoomManagementForm
        RoomManagementForm(self.window)
    
    def open_contract_management(self):
        """Mở form quản lý hợp đồng"""
        from views.contract_management_form import ContractManagementForm
        ContractManagementForm(self.window)
    
    def open_payment_management(self):
        """Mở form thanh toán"""
        from views.payment_management_form import PaymentManagementForm
        PaymentManagementForm(self.window)
    
    def open_report(self):
        """Mở form báo cáo"""
        from views.report_form import ReportForm
        ReportForm(self.window)
    
    def change_password(self):
        """Đổi mật khẩu"""
        messagebox.showinfo("Thông báo", "Chức năng đổi mật khẩu đang phát triển!")
    
    def logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất?"):
            self.window.destroy()
            from views.login_form import LoginForm
            LoginForm().run()
    
    def show_help(self):
        """Hiển thị hướng dẫn"""
        help_text = """
        HƯỚNG DẪN SỬ DỤNG
        
        1. Dashboard: Xem tổng quan hệ thống
        2. Quản lý sinh viên: Thêm, sửa, xóa sinh viên
        3. Quản lý phòng: Quản lý phòng và phân bổ
        4. Quản lý hợp đồng: Tạo và quản lý hợp đồng
        5. Thanh toán: Tạo hóa đơn và ghi nhận thanh toán
        6. Báo cáo: Xem thống kê và xuất báo cáo
        
        Liên hệ hỗ trợ: support@dormitory.com
        """
        messagebox.showinfo("Hướng dẫn sử dụng", help_text)
    
    def show_about(self):
        """Hiển thị thông tin"""
        about_text = """
        ỨNG DỤNG QUẢN LÝ KÝ TÚC XÁ
        Phiên bản: 1.0.0
        
        Sinh viên thực hiện: [Tên sinh viên]
        MSSV: [Mã số sinh viên]
        Lớp: [Tên lớp]
        
        Giảng viên hướng dẫn: [Tên giảng viên]
        
        © 2024 - Đồ án môn Lập trình Python
        """
        messagebox.showinfo("Giới thiệu", about_text)
    
    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        if messagebox.askyesno("Xác nhận", "Bạn có muốn thoát ứng dụng?"):
            self.window.destroy()