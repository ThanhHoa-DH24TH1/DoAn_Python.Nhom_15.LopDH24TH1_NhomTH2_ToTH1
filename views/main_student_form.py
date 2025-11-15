import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
import io

# Import DAOs để lấy dữ liệu
from dao.student_dao import StudentDAO
from dao.contract_dao import ContractDAO
from dao.invoice_dao import InvoiceDAO
from dao.room_dao import RoomDAO

class MainStudentForm:
    def __init__(self, current_user):
        """
        current_user = {
            'user_id': 2,
            'username': 'sv2001',  # ← Đây là MSSV sinh viên dùng để đăng nhập
            'full_name': 'Nguyễn Văn A',
            'role': 'Student'
        }
        """
        self.current_user = current_user
        self.window = tk.Tk()
        self.window.title(f"Thông tin sinh viên - {current_user['full_name']}")
        self.window.geometry("1200x700")
        self.window.state('zoomed')
        
        # DAOs để lấy dữ liệu
        self.student_dao = StudentDAO()
        self.contract_dao = ContractDAO()
        self.invoice_dao = InvoiceDAO()
        self.room_dao = RoomDAO()
        
        # Biến lưu thông tin sinh viên
        self.student_data = None
        self.contract_data = None
        self.room_data = None
        
        # Tạo giao diện
        self.create_menu()
        self.create_widgets()
        self.load_student_data()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def create_menu(self):
        """Tạo menu bar"""
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        # Menu Tài khoản
        account_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tài khoản", menu=account_menu)
        account_menu.add_command(label="Đổi mật khẩu", command=self.change_password)
        account_menu.add_separator()
        account_menu.add_command(label="Đăng xuất", command=self.logout)
        account_menu.add_command(label="Thoát", command=self.on_closing)
        
        # Menu Trợ giúp
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        help_menu.add_command(label="Hướng dẫn sử dụng", command=self.show_help)
        help_menu.add_command(label="Liên hệ quản lý", command=self.contact_admin)
    
    def create_widgets(self):
        """Tạo giao diện chính"""
        # ===== HEADER =====
        header_frame = tk.Frame(self.window, bg='#2196F3', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title và thông tin user
        title_frame = tk.Frame(header_frame, bg='#2196F3')
        title_frame.pack(expand=True)
        
        tk.Label(
            title_frame,
            text="🏠 THÔNG TIN SINH VIÊN KÝ TÚC XÁ",
            font=('Arial', 18, 'bold'),
            bg='#2196F3',
            fg='white'
        ).pack(pady=(10, 5))
        
        tk.Label(
            title_frame,
            text=f"Xin chào, {self.current_user['full_name']}",
            font=('Arial', 11),
            bg='#2196F3',
            fg='white'
        ).pack()
        
        # ===== MAIN CONTENT =====
        main_frame = tk.Frame(self.window, bg='#f5f5f5')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Container với 2 cột
        left_container = tk.Frame(main_frame, bg='#f5f5f5')
        left_container.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        right_container = tk.Frame(main_frame, bg='#f5f5f5', width=400)
        right_container.pack(side='right', fill='both', padx=(10, 0))
        right_container.pack_propagate(False)
        
        # ===== CỘT TRÁI =====
        
        # 1. THÔNG TIN CÁ NHÂN
        self.create_personal_info_section(left_container)
        
        # 2. THÔNG TIN PHÒNG Ở
        self.create_room_info_section(left_container)
        
        # ===== CỘT PHẢI =====
        
        # 3. THÔNG TIN TÀI CHÍNH
        self.create_financial_info_section(right_container)
        
        # 4. HÓA ĐƠN GẦN NHẤT
        self.create_recent_invoices_section(right_container)
        
        # ===== STATUS BAR =====
        self.create_statusbar()
    
    def create_personal_info_section(self, parent):
        """Phần 1: Thông tin cá nhân"""
        section = tk.LabelFrame(
            parent,
            text="📋 THÔNG TIN CÁ NHÂN",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2196F3',
            relief='solid',
            bd=1
        )
        section.pack(fill='x', pady=(0, 15))
        
        content_frame = tk.Frame(section, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Container cho ảnh và thông tin
        info_container = tk.Frame(content_frame, bg='white')
        info_container.pack(fill='x')
        
        # Ảnh sinh viên (bên trái)
        avatar_frame = tk.Frame(info_container, bg='white', width=120, height=150)
        avatar_frame.pack(side='left', padx=(0, 20))
        avatar_frame.pack_propagate(False)
        
        # Placeholder avatar
        self.avatar_label = tk.Label(
            avatar_frame,
            text="👤",
            font=('Arial', 60),
            bg='#e3f2fd',
            fg='#2196F3',
            relief='solid',
            bd=1
        )
        self.avatar_label.pack(fill='both', expand=True)
        
        # Thông tin chi tiết (bên phải)
        details_frame = tk.Frame(info_container, bg='white')
        details_frame.pack(side='left', fill='both', expand=True)
        
        # Labels để hiển thị thông tin
        self.info_labels = {}
        
        info_fields = [
            ('MSSV:', 'mssv', '#1976D2'),
            ('Họ và tên:', 'fullname', '#000000'),
            ('Ngày sinh:', 'dob', '#555555'),
            ('Giới tính:', 'gender', '#555555'),
            ('Số điện thoại:', 'phone', '#555555'),
            ('Email:', 'email', '#555555'),
            ('Khoa:', 'faculty', '#555555'),
            ('Lớp:', 'class', '#555555'),
        ]
        
        for idx, (label_text, key, color) in enumerate(info_fields):
            row_frame = tk.Frame(details_frame, bg='white')
            row_frame.pack(fill='x', pady=3)
            
            tk.Label(
                row_frame,
                text=label_text,
                font=('Arial', 10, 'bold'),
                bg='white',
                fg='#666666',
                width=15,
                anchor='w'
            ).pack(side='left')
            
            self.info_labels[key] = tk.Label(
                row_frame,
                text="Đang tải...",
                font=('Arial', 10, 'bold' if key in ['mssv', 'fullname'] else 'normal'),
                bg='white',
                fg=color,
                anchor='w'
            )
            self.info_labels[key].pack(side='left', fill='x', expand=True)
    
    def create_room_info_section(self, parent):
        """Phần 2: Thông tin phòng ở"""
        section = tk.LabelFrame(
            parent,
            text="🏢 THÔNG TIN PHÒNG Ở",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#4CAF50',
            relief='solid',
            bd=1
        )
        section.pack(fill='x', pady=(0, 0))
        
        content_frame = tk.Frame(section, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0,15)) 

        # Cấu hình grid cho content_frame: 2 hàng, 1 cột
        content_frame.grid_rowconfigure(0, weight=0)    # Hàng 0 (status+grid) không giãn nhiều
        content_frame.grid_rowconfigure(1, weight=10, minsize=50)    # Hàng 1 (roommates) sẽ giãn chính
        content_frame.grid_columnconfigure(0, weight=1) # Cột 0 giãn ngang

        # --- Frame chứa status và grid thông tin ---
        top_info_frame = tk.Frame(content_frame, bg='white')
        top_info_frame.grid(row=0, column=0, sticky='ew') # Đặt vào hàng 0

        # Frame trạng thái phòng (đặt vào top_info_frame)
        status_frame = tk.Frame(top_info_frame, bg='#e8f5e9', relief='solid', bd=1)
        status_frame.pack(fill='x', pady=0) # Dùng pack trong frame con này

        self.room_status_label = tk.Label(
            status_frame,
            text="📍 Chưa được phân phòng",
            font=('Arial', 11, 'bold'),
            bg='#e8f5e9',
            fg='#2E7D32',
            pady=10
        )
        self.room_status_label.pack()

        # Grid 2 cột cho thông tin phòng (đặt vào top_info_frame)
        grid_frame = tk.Frame(top_info_frame, bg='white')
        grid_frame.pack(fill='x') # Chỉ fill ngang

        # Cấu hình cột cho grid_frame
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)

        # Cột trái (đặt vào grid_frame)
        left_col = tk.Frame(grid_frame, bg='white')
        left_col.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        # Cột phải (đặt vào grid_frame)
        right_col = tk.Frame(grid_frame, bg='white')
        right_col.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

        self.room_labels = {}
        left_fields = [('Số phòng:', 'room_number', '#4CAF50'), ('Tòa nhà:', 'building', '#555555'), ('Tầng:', 'floor', '#555555'), ('Loại phòng:', 'room_type', '#555555')]
        right_fields = [('Giá thuê/tháng:', 'price', '#FF9800'), ('Ngày bắt đầu:', 'start_date', '#555555'), ('Ngày kết thúc:', 'end_date', '#555555'), ('Tiền cọc:', 'deposit', '#555555')]

        for label_text, key, color in left_fields:
            self._create_info_row(left_col, label_text, key, color)
        for label_text, key, color in right_fields:
            self._create_info_row(right_col, label_text, key, color)

        roommates_frame = tk.Frame(
            content_frame, # Đặt vào content_frame
            bd=1,
            relief='solid',
            bg='white',
        )
        roommates_frame.grid(row=1, column=0, sticky='nsew', pady=(0,5))

        title_label = tk.Label(
            roommates_frame,
            text="👥 Bạn cùng phòng",
            font=('Arial', 10, 'bold'),
            bg='white', # Màu nền giống frame
            fg='#555555', # Màu chữ
            anchor='w' # Căn trái
        )
        title_label.pack(side='top', fill='x', padx=10, pady=0) # Đặt ở trên cùng

        # Listbox cho bạn cùng phòng
        self.roommates_listbox = tk.Listbox(
            roommates_frame, # Đặt vào roommates_frame
            font=('Arial', 10),
            bg='#fefefe', 
            relief='flat',
            height=6
        )
        
        self.roommates_listbox.pack(fill='x',expand=True, padx=5, pady=(0,2)) # Chiếm hết không gian còn lại
    
    def create_financial_info_section(self, parent):
        """Phần 3: Thông tin tài chính"""
        section = tk.LabelFrame(
            parent,
            text="💰 THÔNG TIN TÀI CHÍNH",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#FF9800',
            relief='solid',
            bd=1
        )
        section.pack(fill='x', pady=(0, 15))
        
        content_frame = tk.Frame(section, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Cards tài chính
        cards_frame = tk.Frame(content_frame, bg='white')
        cards_frame.pack(fill='x')
        
        # Card 1: Tổng nợ
        self.debt_card = self._create_finance_card(
            cards_frame,
            "Tổng nợ",
            "0 đ",
            '#f44336',
            0
        )
        
        # Card 2: Đã thanh toán
        self.paid_card = self._create_finance_card(
            cards_frame,
            "Đã thanh toán",
            "0 đ",
            '#4CAF50',
            1
        )
        
        # Card 3: Tháng này
        self.month_card = self._create_finance_card(
            cards_frame,
            "Hóa đơn tháng này",
            "0 đ",
            '#2196F3',
            2
        )
    
    def _create_finance_card(self, parent, title, value, color, col):
        """Tạo card tài chính"""
        card = tk.Frame(parent, bg=color, relief='solid', bd=1)
        card.grid(row=0, column=col, padx=5, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(
            card,
            text=title,
            font=('Arial', 9),
            bg=color,
            fg='white'
        ).pack(pady=(10, 2))
        
        value_label = tk.Label(
            card,
            text=value,
            font=('Arial', 14, 'bold'),
            bg=color,
            fg='white'
        )
        value_label.pack(pady=(2, 10))
        
        return value_label
    
    def create_recent_invoices_section(self, parent):
        """Phần 4: Hóa đơn gần nhất"""
        section = tk.LabelFrame(
            parent,
            text="📄 HÓA ĐƠN GẦN NHẤT",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#9C27B0',
            relief='solid',
            bd=1
        )
        section.pack(fill='both', expand=True)
        
        content_frame = tk.Frame(section, bg='white')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview hóa đơn
        columns = ('Tháng', 'Tổng tiền', 'Đã trả', 'Còn nợ', 'Trạng thái')
        
        self.invoice_tree = ttk.Treeview(
            content_frame,
            columns=columns,
            show='headings',
            height=8
        )
        
        # Define headings
        widths = [80, 100, 100, 100, 120]
        for col, width in zip(columns, widths):
            self.invoice_tree.heading(col, text=col)
            self.invoice_tree.column(col, width=width, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.invoice_tree.yview)
        self.invoice_tree.configure(yscrollcommand=scrollbar.set)
        
        self.invoice_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double click
        self.invoice_tree.bind('<Double-1>', self.view_invoice_detail)
        
        # Button xem tất cả
        tk.Button(
            section,
            text="📋 Xem tất cả hóa đơn",
            font=('Arial', 10),
            bg='#9C27B0',
            fg='white',
            cursor='hand2',
            command=self.view_all_invoices
        ).pack(pady=10)
    
    def _create_info_row(self, parent, label_text, key, color):
        """Helper: Tạo dòng thông tin"""
        row_frame = tk.Frame(parent, bg='white')
        row_frame.pack(fill='x', pady=4)
        
        tk.Label(
            row_frame,
            text=label_text,
            font=('Arial', 9, 'bold'),
            bg='white',
            fg='#666666',
            anchor='w'
        ).pack(fill='x')
        
        self.room_labels[key] = tk.Label(
            row_frame,
            text="---",
            font=('Arial', 10, 'bold' if 'price' in key or 'deposit' in key else 'normal'),
            bg='white',
            fg=color,
            anchor='w'
        )
        self.room_labels[key].pack(fill='x')
    
    def create_statusbar(self):
        """Tạo status bar"""
        statusbar = tk.Frame(self.window, bg='#34495e', height=30)
        statusbar.pack(side='bottom', fill='x')
        
        self.status_label = tk.Label(
            statusbar,
            text=f"👤 {self.current_user['username']} - Sinh viên",
            font=('Arial', 9),
            bg='#34495e',
            fg='white'
        )
        self.status_label.pack(side='left', padx=10, pady=5)
        
        self.time_label = tk.Label(
            statusbar,
            text="",
            font=('Arial', 9),
            bg='#34495e',
            fg='white'
        )
        self.time_label.pack(side='right', padx=10, pady=5)
        
        self.update_time()
    
    def update_time(self):
        """Cập nhật thời gian"""
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.time_label.config(text=f"🕐 {now}")
        self.window.after(1000, self.update_time)
    
    # ========================================
    # LOAD DỮ LIỆU
    # ========================================
    
    def load_student_data(self):
        """Load tất cả thông tin sinh viên"""
        try:
            # 🔍 BƯỚC 1: Lấy thông tin sinh viên theo MSSV
            # current_user['username'] chính là MSSV sinh viên
            mssv = self.current_user['username']  # VD: 'sv2001' hoặc '2001001'
            # TODO: Bạn cần sửa lại hàm này trong StudentDAO để lấy theo MSSV
            # Hiện tại: get_student_by_code(student_code)
            self.student_data = self.student_dao.get_student_by_code(mssv)
            
            if not self.student_data:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin sinh viên!")
                return
            
            # Load thông tin cá nhân
            self.load_personal_info()
            
            # 🔍 BƯỚC 2: Lấy hợp đồng của sinh viên
            student_id = self.student_data[0]  # StudentID
            
            # TODO: Bạn cần method này trong ContractDAO
            # get_contract_by_student(student_id) 
            # → Trả về hợp đồng đang hiệu lực
            self.contract_data = self.contract_dao.get_contract_by_student(student_id)
            
            # Load thông tin phòng
            self.load_room_info()
            
            # 🔍 BƯỚC 3: Lấy thông tin tài chính
            # TODO: Bạn cần các method này trong InvoiceDAO
            self.invoice_dao.get_total_debt(student_id)
            self.invoice_dao.get_total_paid(student_id)  
            self.invoice_dao.get_invoices_by_student(student_id, limit=5)
            self.load_financial_info()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu:\n{e}")
            import traceback
            traceback.print_exc()
    
    def load_personal_info(self):
        """Load thông tin cá nhân"""
        if not self.student_data:
            return
        
        # student_data structure từ database:
        # [0]=StudentID, [1]=StudentCode, [2]=FullName, [3]=DOB,
        # [4]=Gender, [5]=Phone, [6]=Email, [7]=IDCard, [8]=Address,
        # [9]=Faculty, [10]=Major, [11]=Class, [12]=Status
        
        self.info_labels['mssv'].config(text=self.student_data[1])
        self.info_labels['fullname'].config(text=self.student_data[2])
        self.info_labels['dob'].config(
            text=self.student_data[3].strftime('%d/%m/%Y') if self.student_data[3] else '---'
        )
        self.info_labels['gender'].config(text=self.student_data[4])
        self.info_labels['phone'].config(text=self.student_data[5] or 'Chưa cập nhật')
        self.info_labels['email'].config(text=self.student_data[6] or 'Chưa cập nhật')
        self.info_labels['faculty'].config(text=self.student_data[9])
        self.info_labels['class'].config(text=self.student_data[11])
    
    def load_room_info(self):
        """Load thông tin phòng ở"""
        
        # DEBUG: In thông tin contract
        print(f"\n{'='*50}")
        print(f"[DEBUG] Loading room info...")
        print(f"Contract data: {self.contract_data}")
        print(f"{'='*50}\n")
        
        if not self.contract_data:
            # Chưa có phòng
            self.room_status_label.config(
                text="⚠️ Bạn chưa được phân phòng",
                bg='#fff3e0',
                fg='#E65100'
            )
            
            for label in self.room_labels.values():
                label.config(text="---")
            
            self.roommates_listbox.delete(0, 'end')
            self.roommates_listbox.insert(0, "Chưa có phòng")
            return
        
        # Có hợp đồng
        # contract_data có thể có 2 dạng:
        # - Dạng đầy đủ (từ get_contract_by_student): 13+ cột
        # - Dạng cơ bản: ít hơn
        
        try:
            # Lấy thông tin cơ bản
            room_id = self.contract_data[2]  # RoomID
            
            # Kiểm tra có RoomNumber trong contract_data không
            if len(self.contract_data) > 10:
                room_number = self.contract_data[10]
            else:
                # Nếu không có, lấy từ RoomDAO
                room_data = self.room_dao.get_room_by_id(room_id)
                room_number = room_data[1] if room_data else "N/A"
            
            print(f"[DEBUG] Room ID: {room_id}, Room Number: {room_number}")
            
            self.room_status_label.config(
                text=f"✅ Đang ở phòng {room_number}",
                bg='#e8f5e9',
                fg='#2E7D32'
            )
            
            # Lấy chi tiết phòng
            self.room_data = self.room_dao.get_room_by_id(room_id)
            
            if self.room_data:
                print(f"[DEBUG] Room data loaded: {self.room_data[1]}")
                
                self.room_labels['room_number'].config(text=self.room_data[1])
                self.room_labels['building'].config(text=f"Tòa {self.room_data[2]}")
                self.room_labels['floor'].config(text=f"Tầng {self.room_data[3]}")
                self.room_labels['room_type'].config(text=self.room_data[4])
                self.room_labels['price'].config(text=f"{self.room_data[7]:,.0f} VNĐ")
            
            # Thông tin hợp đồng
            self.room_labels['start_date'].config(
                text=self.contract_data[3].strftime('%d/%m/%Y')
            )
            self.room_labels['end_date'].config(
                text=self.contract_data[4].strftime('%d/%m/%Y')
            )
            self.room_labels['deposit'].config(text=f"{self.contract_data[6]:,.0f} VNĐ")
            
            # ===== PHẦN QUAN TRỌNG: Load bạn cùng phòng =====
            print(f"\n[DEBUG] Loading roommates for room {room_id}...")
            
            # Clear listbox trước
            self.roommates_listbox.delete(0, 'end')
            
            # Lấy danh sách sinh viên trong phòng
            roommates = self.room_dao.get_students_in_room(room_id)
            
            print(f"[DEBUG] Total students in room: {len(roommates)}")
            
            if roommates and len(roommates) > 0:
                current_student_id = self.student_data[0]
                print(f"[DEBUG] Current student ID: {current_student_id}")
                
                added_count = 0
                
                for rm in roommates:
                    student_id = rm[0]
                    student_code = rm[1]
                    student_name = rm[2]
                    phone = rm[3] if len(rm) > 3 else ''
                    
                    print(f"[DEBUG] Checking: {student_id} vs {current_student_id}")
                    
                    # Không hiển thị chính mình
                    if student_id != current_student_id:
                        display_text = f"• {student_code} - {student_name}"
                        if phone:
                            display_text += f" ({phone})"
                        
                        self.roommates_listbox.insert('end', display_text)
                        added_count += 1
                        print(f"[DEBUG] Added: {display_text}")
                
                print(f"[DEBUG] Added {added_count} roommates")
                
                # Nếu không có ai khác (chỉ có mình)
                if added_count == 0:
                    self.roommates_listbox.insert(0, "Chỉ có bạn trong phòng")
                    print(f"[DEBUG] Only you in the room")
                self.roommates_listbox.update_idletasks()
            else:
                self.roommates_listbox.insert(0, "Không có dữ liệu bạn cùng phòng")
                print(f"[DEBUG] No roommates data")
        
        except Exception as e:
            print(f"[ERROR] load_room_info: {e}")
            import traceback
            traceback.print_exc()
            
            self.roommates_listbox.delete(0, 'end')
            self.roommates_listbox.insert(0, f"Lỗi: {str(e)}")
    
    def load_financial_info(self):
        """Load thông tin tài chính (Cập nhật Cards + Treeview)"""
        if not self.student_data:
            messagebox.showwarning("Thiếu dữ liệu", "Không có thông tin sinh viên để tải tài chính.")
            return
        
        student_id = self.student_data[0]
        
        try:
            # === CẬP NHẬT CÁC THẺ THỐNG KÊ (CARDS) ===
            
            # 1. Lấy Tổng nợ
            # (Bạn cần tạo hàm get_total_debt trong InvoiceDAO)
            total_debt = self.invoice_dao.get_total_debt(student_id) 
            self.debt_card.config(text=f"{total_debt or 0:,.0f} đ") # Thêm 'or 0' phòng trường hợp trả về None
            
            # 2. Lấy Tổng đã thanh toán
            # (Bạn cần tạo hàm get_total_paid trong InvoiceDAO)
            total_paid = self.invoice_dao.get_total_paid(student_id)
            self.paid_card.config(text=f"{total_paid or 0:,.0f} đ")

            # 3. Lấy Hóa đơn tháng này
            # (Bạn cần tạo hàm get_current_month_invoice_total trong InvoiceDAO)
            current_month_str = datetime.now().strftime('%Y-%m')
            # Hàm này cần trả về TotalAmount của hóa đơn tháng này, hoặc 0
            month_total = self.invoice_dao.get_current_month_invoice_total(student_id, current_month_str) 
            self.month_card.config(text=f"{month_total or 0:,.0f} đ")
            
            # === LOAD HÓA ĐƠN GẦN NHẤT VÀO BẢNG (TREEVIEW) ===
            
            # 1. Xóa dữ liệu cũ
            for item in self.invoice_tree.get_children():
                self.invoice_tree.delete(item)

            # 2. Lấy 5 hóa đơn gần nhất 
            # (Bạn cần tạo hàm get_invoices_by_student trong InvoiceDAO)
            # Hàm này nên trả về list các tuple/row, ví dụ:
            # [(InvoiceID, BillingMonth, TotalAmount, PaidAmount, RemainingAmount, Status), ...]
            invoices = self.invoice_dao.get_invoices_by_student(student_id, limit=5) 
            
            if invoices:
                # 3. Chèn dữ liệu mới
                for inv in invoices:
                    # Đảm bảo index khớp với dữ liệu trả về từ DAO
                    # Ví dụ: inv[0]=InvoiceID, inv[1]=BillingMonth, inv[2]=Total, inv[3]=Paid, inv[4]=Remaining, inv[5]=Status
                    values = (
                        inv[1],                       # Tháng (ví dụ: '2025-10')
                        f"{inv[2] or 0:,.0f}",       # Tổng tiền
                        f"{inv[3] or 0:,.0f}",       # Đã trả
                        f"{inv[4] or 0:,.0f}",       # Còn nợ
                        inv[5]                        # Trạng thái
                    )
                    
                    # Xác định tag màu sắc
                    status = inv[5]
                    if status == 'Đã thanh toán': 
                        tag = 'paid'
                    elif status == 'Chưa thanh toán': 
                        tag = 'unpaid'
                    else: # Mặc định cho 'Thanh toán 1 phần' hoặc trạng thái khác
                        tag = 'partial' 
                        
                    # Chèn vào treeview, lưu InvoiceID vào tag để double-click
                    self.invoice_tree.insert('', 'end', values=values, tags=(inv[0], tag))
                
                # 4. Cấu hình màu sắc (Nên đặt ở create_widgets để chỉ chạy 1 lần)
                # Chỉ cấu hình nếu chưa có để tránh lặp lại
                if not self.invoice_tree.tag_has('paid'): 
                    self.invoice_tree.tag_configure('paid', background='#DCEDC8', foreground='#33691E') # Xanh lá nhạt
                if not self.invoice_tree.tag_has('unpaid'):
                    self.invoice_tree.tag_configure('unpaid', background='#FFCDD2', foreground='#B71C1C') # Đỏ nhạt
                if not self.invoice_tree.tag_has('partial'):
                    self.invoice_tree.tag_configure('partial', background='#FFF9C4', foreground='#F57F17') # Vàng nhạt
            
            else:
                # Nếu không có hóa đơn nào
                self.invoice_tree.insert('', 'end', values=('---', 'Chưa có hóa đơn', '---', '---', '---'))
        
        except AttributeError as ae:
             # Bắt lỗi cụ thể nếu hàm DAO chưa có
             messagebox.showerror("Lỗi Lập Trình", f"Lỗi gọi hàm DAO: {ae}\n\nVui lòng kiểm tra lại file dao/invoice_dao.py.")
             # Có thể chèn dòng báo lỗi vào Treeview nếu muốn
             self.invoice_tree.insert('', 'end', values=('---', 'Lỗi tải DAO', '---', '---', '---'))
        except Exception as e:
            # Bắt các lỗi khác (ví dụ: lỗi CSDL)
            print(f"Lỗi không xác định khi load financial info: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải thông tin tài chính:\n{e}")
            import traceback
            traceback.print_exc() # In lỗi chi tiết ra terminal
            self.invoice_tree.insert('', 'end', values=('---', 'Lỗi tải dữ liệu', '---', '---', '---'))
    # ========================================
    # CÁC CHỨC NĂNG KHÁC
    # ========================================
    
    def view_invoice_detail(self, event):
        """Xem chi tiết hóa đơn khi double click"""
        selected = self.invoice_tree.selection()
        if not selected:
            return
        
        invoice_id = self.invoice_tree.item(selected[0])['tags'][0]
        
        try:
            # 🔍 TODO: Method get_invoice_by_id(invoice_id) trong InvoiceDAO
            invoice = self.invoice_dao.get_invoice_by_id(invoice_id)
            
            if invoice:
                # Hiển thị dialog chi tiết
                self.show_invoice_detail_dialog(invoice)
        except:
            messagebox.showerror("Lỗi", "Không thể tải chi tiết hóa đơn!")
    
    def show_invoice_detail_dialog(self, invoice):
        """Hiển thị dialog chi tiết hóa đơn"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Chi tiết hóa đơn")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg='#2196F3', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📄 CHI TIẾT HÓA ĐƠN",
            font=('Arial', 14, 'bold'),
            bg='#2196F3',
            fg='white'
        ).pack(pady=18)
        
        # Content
        content = tk.Frame(dialog, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # invoice structure từ get_invoice_by_id:
        # [0]=InvoiceID, [1]=ContractID, [2]=StudentID, [3]=BillingMonth,
        # [4]=RoomFee, [5]=ElectricityFee, [6]=WaterFee, [7]=InternetFee,
        # [8]=ServiceFee, [9]=TotalAmount, [10]=PaidAmount, [11]=RemainingAmount,
        # [12]=Status, [13]=DueDate, [14]=PaymentDate, [15]=CreatedDate,
        # [16]=StudentCode, [17]=FullName, [18]=RoomNumber
        
        detail_text = f"""
HÓA ĐƠN TIỀN PHÒNG KÝ TÚC XÁ
{'═' * 50}

Mã hóa đơn:     {invoice[0]}
Tháng:          {invoice[3]}
Sinh viên:      {invoice[16]} - {invoice[17]}
Phòng:          {invoice[18]}

{'─' * 50}
CHI TIẾT CÁC KHOẢN PHÍ
{'─' * 50}

1. Tiền phòng:              {invoice[4]:>15,.0f} đ
2. Tiền điện:               {invoice[5]:>15,.0f} đ
3. Tiền nước:               {invoice[6]:>15,.0f} đ
4. Phí internet:            {invoice[7]:>15,.0f} đ
5. Phí dịch vụ khác:        {invoice[8]:>15,.0f} đ

{'═' * 50}
TỔNG CỘNG:                  {invoice[9]:>15,.0f} đ
Đã thanh toán:              {invoice[10]:>15,.0f} đ
CÒN NỢ:                     {invoice[11]:>15,.0f} đ

{'─' * 50}
Trạng thái:     {invoice[12]}
Hạn thanh toán: {invoice[13].strftime('%d/%m/%Y') if invoice[13] else 'N/A'}
Ngày tạo:       {invoice[15].strftime('%d/%m/%Y') if invoice[15] else 'N/A'}

        """
        
        text_widget = tk.Text(
            content,
            font=('Courier New', 10),
            wrap='word',
            bg='#fafafa',
            relief='flat'
        )
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', detail_text)
        text_widget.config(state='disabled')
        
        # Button
        tk.Button(
            dialog,
            text="Đóng",
            font=('Arial', 10),
            bg='#2196F3',
            fg='white',
            width=15,
            command=dialog.destroy
        ).pack(pady=15)
    
    def view_all_invoices(self):
        """Xem tất cả hóa đơn"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Tất cả hóa đơn")
        dialog.geometry("900x600")
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg='#9C27B0', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📋 TẤT CẢ HÓA ĐƠN",
            font=('Arial', 14, 'bold'),
            bg='#9C27B0',
            fg='white'
        ).pack(pady=18)
        
        # Content
        content = tk.Frame(dialog)
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview
        columns = ('Mã HĐ', 'Tháng', 'Tổng tiền', 'Đã trả', 'Còn nợ', 'Trạng thái', 'Hạn TT')
        
        tree = ttk.Treeview(content, columns=columns, show='headings')
        
        widths = [80, 80, 120, 120, 120, 130, 100]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor='center')
        
        vsb = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        
        # Load tất cả hóa đơn
        if self.student_data:
            student_id = self.student_data[0]
            
            query = """
                SELECT 
                    InvoiceID, BillingMonth, TotalAmount, 
                    PaidAmount, RemainingAmount, Status, DueDate
                FROM Invoices 
                WHERE StudentID = ?
                ORDER BY BillingMonth DESC
            """
            
            try:
                invoices = self.invoice_dao.db.execute_query(query, (student_id,))
                
                for inv in invoices:
                    values = (
                        inv[0],
                        inv[1],
                        f"{inv[2]:,.0f}",
                        f"{inv[3]:,.0f}",
                        f"{inv[4]:,.0f}",
                        inv[5],
                        inv[6].strftime('%d/%m/%Y') if inv[6] else 'N/A'
                    )
                    tree.insert('', 'end', values=values)
            except:
                pass
        
        # Button
        tk.Button(
            dialog,
            text="Đóng",
            bg='#9C27B0',
            fg='white',
            width=15,
            command=dialog.destroy
        ).pack(pady=15)
    
    def change_password(self):
        """Đổi mật khẩu"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Đổi mật khẩu")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="ĐỔI MẬT KHẨU",
            font=('Arial', 14, 'bold'),
            fg='#2196F3'
        ).pack(pady=20)
        
        form_frame = tk.Frame(dialog)
        form_frame.pack(padx=40, pady=10)
        
        # Mật khẩu cũ
        tk.Label(form_frame, text="Mật khẩu cũ:", anchor='w').grid(row=0, column=0, sticky='w', pady=10)
        old_pass = tk.Entry(form_frame, show='●', width=25)
        old_pass.grid(row=0, column=1, pady=10)
        
        # Mật khẩu mới
        tk.Label(form_frame, text="Mật khẩu mới:", anchor='w').grid(row=1, column=0, sticky='w', pady=10)
        new_pass = tk.Entry(form_frame, show='●', width=25)
        new_pass.grid(row=1, column=1, pady=10)
        
        # Xác nhận
        tk.Label(form_frame, text="Xác nhận:", anchor='w').grid(row=2, column=0, sticky='w', pady=10)
        confirm_pass = tk.Entry(form_frame, show='●', width=25)
        confirm_pass.grid(row=2, column=1, pady=10)
        
        def do_change():
            # 🔍 TODO: Implement logic đổi mật khẩu
            # - Validate input
            # - Check mật khẩu cũ đúng không
            # - Hash mật khẩu mới
            # - Update vào database
            messagebox.showinfo("Thông báo", "Chức năng đổi mật khẩu đang phát triển!")
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Đổi mật khẩu",
            bg='#4CAF50',
            fg='white',
            width=12,
            command=do_change
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="Hủy",
            width=12,
            command=dialog.destroy
        ).pack(side='left', padx=5)
    
    def show_help(self):
        """Hiển thị hướng dẫn"""
        help_text = """
        HƯỚNG DẪN SỬ DỤNG
        
        📋 Thông tin cá nhân:
           Hiển thị thông tin sinh viên và phòng ở
        
        💰 Thông tin tài chính:
           - Tổng nợ: Số tiền còn phải trả
           - Đã thanh toán: Tổng đã đóng
           - Tháng này: Hóa đơn tháng hiện tại
        
        📄 Hóa đơn:
           - Double click để xem chi tiết
           - Click "Xem tất cả" để xem toàn bộ
        
        🔐 Đổi mật khẩu:
           Menu Tài khoản → Đổi mật khẩu
        
        ℹ️ Liên hệ hỗ trợ:
           Email: support@ktx.edu.vn
           Hotline: 1900-xxxx
        """
        messagebox.showinfo("Hướng dẫn", help_text)
    
    def contact_admin(self):
        """Liên hệ quản lý"""
        contact_text = """
        THÔNG TIN LIÊN HỆ
        
        📧 Email: ktx@university.edu.vn
        📞 Hotline: 1900-xxxx
        📍 Văn phòng: Tòa A, Tầng 1
        
        ⏰ Giờ làm việc:
           Thứ 2 - 6: 8:00 - 17:00
           Thứ 7: 8:00 - 12:00
           Chủ nhật: Nghỉ
        """
        messagebox.showinfo("Liên hệ", contact_text)
    
    def logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất?"):
            self.window.destroy()
            from views.login_form import LoginForm
            LoginForm().run()
    
    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        if messagebox.askyesno("Xác nhận", "Bạn có muốn thoát?"):
            self.window.destroy()
