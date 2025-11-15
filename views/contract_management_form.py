import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from dao.contract_dao import ContractDAO
from dao.student_dao import StudentDAO
from dao.room_dao import RoomDAO
from utils.date_utils import DateUtils

class ContractManagementForm:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Quản lý Hợp đồng")
        self.window.geometry("1200x700")
        self.window.state('zoomed')
        
        self.contract_dao = ContractDAO()
        self.student_dao = StudentDAO()
        self.room_dao = RoomDAO()
        
        self.create_widgets()
        self.load_contracts()
    
    def create_widgets(self):
        """Tạo giao diện"""
        # Title
        title_frame = tk.Frame(self.window, bg='#3F51B5', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="QUẢN LÝ HỢP ĐỒNG",
            font=('Arial', 16, 'bold'),
            bg='#3F51B5',
            fg='white'
        ).pack(pady=15)
        
        # Search frame
        search_frame = tk.Frame(self.window, bg='white')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Tìm kiếm:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
    
        tk.Label(search_frame, text="Trạng thái:", bg='white').grid(row=0, column=2, sticky='w', padx=(20, 5), pady=5)
        self.status_combo = ttk.Combobox(search_frame, width=15, state='readonly')
        self.status_combo['values'] = ['Tất cả', 'Đang hiệu lực', 'Hết hạn', 'Thanh lý']
        self.status_combo.current(0)
        self.status_combo.grid(row=0, column=3, sticky='w', padx=5, pady=5)

        # Hàng 1 (cho các nút)
        button_frame = tk.Frame(search_frame, bg='white')
        button_frame.grid(row=1, column=0, columnspan=4, pady=(5,0)) # Đặt frame này ở hàng 1, kéo dài 4 cột

        tk.Button(
            button_frame, # Đặt nút vào frame mới
            text="🔍 Tìm",
            bg='#2196F3', fg='white',
            command=self.search_contracts
        ).pack(side='left', padx=5) # Dùng pack() trong frame con này
        
        tk.Button(
            button_frame, # Đặt nút vào frame mới
            text="🔄 Làm mới",
            bg='#4CAF50', fg='white',
            command=self.load_contracts
        ).pack(side='left', padx=5)
        
        # Main content
        content_frame = tk.Frame(self.window)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview
        tree_frame = tk.Frame(content_frame)
        tree_frame.pack(side='left', fill='both', expand=True)
        
        columns = ('STT', 'Mã HĐ', 'MSSV', 'Họ tên', 'Phòng', 
                  'Ngày BĐ', 'Ngày KT', 'Giá thuê', 'Tiền cọc', 'Trạng thái')
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        widths = [50, 80, 100, 180, 80, 100, 100, 120, 120, 120]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        
        # Button frame
        btn_frame = tk.Frame(content_frame, width=150)
        btn_frame.pack(side='right', fill='y', padx=(10, 0))
        
        buttons = [
            ("➕ Tạo HĐ", self.create_contract, '#4CAF50'),
            ("🔄 Gia hạn", self.renew_contract, '#2196F3'),
            ("❌ Thanh lý", self.terminate_contract, '#f44336'),
            ("👁️ Chi tiết", self.view_details, '#FF9800')
        ]
        
        for text, cmd, color in buttons:
            tk.Button(
                btn_frame,
                text=text,
                font=('Arial', 10),
                bg=color,
                fg='white',
                width=15,
                command=cmd
            ).pack(pady=5,fill='x', padx=5)

    def load_contracts(self):
        """
        Hàm này lấy dữ liệu từ DAO và nạp vào Treeview
        """
        try:
            # 1. Xóa tất cả dữ liệu cũ trong bảng
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # 2. Lấy dữ liệu mới từ CSDL
            # (Giả sử bạn có hàm get_all_contracts trong DAO)
            contracts = self.contract_dao.get_all_contracts() 
            
            # 3. Dùng print để kiểm tra xem có lấy được dữ liệu không
            print("Dữ liệu hợp đồng lấy về:", contracts) 
            
            # 4. Lặp qua dữ liệu và chèn vào bảng
            for idx, contract in enumerate(contracts, 1):
                
                # Cột của bạn: ('STT', 'Mã HĐ', 'MSSV', 'Họ tên', 'Phòng', 
                #               'Ngày BĐ', 'Ngày KT', 'Giá thuê', 'Tiền cọc', 'Trạng thái')
                
                values = (
                   idx,
                contract[0],  # ContractID
                contract[10],  # StudentCode
                contract[11],  # FullName
                contract[12],  # RoomNumber
                contract[3].strftime('%d/%m/%Y'),  # StartDate
                contract[4].strftime('%d/%m/%Y'),  # EndDate
                f"{contract[5]:,.0f}",  # MonthlyFee
                f"{contract[6]:,.0f}",  # Deposit
                contract[7]   # Status            
                )
                
                # Chèn hàng mới vào Treeview
                self.tree.insert('', 'end', values=values, tags=(contract[0],))
                
        except Exception as e:
            messagebox.showerror("Lỗi tải dữ liệu", f"Không thể tải danh sách hợp đồng: {e}")

    # Bạn cũng cần tạo các hàm này (dù là để trống)
    # nếu không code sẽ báo lỗi khi gán 'command'
    def search_contracts(self):
        """Tìm kiếm hợp đồng"""
        keyword = self.search_entry.get().strip()
        status = self.status_combo.get()
        status = None if status == 'Tất cả' else status
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        contracts = self.contract_dao.search_contracts(keyword, status)
        
        for idx, contract in enumerate(contracts, 1):
            values = (
                idx, contract[0], contract[10], contract[11], contract[12],
                contract[3].strftime('%d/%m/%Y'), contract[4].strftime('%d/%m/%Y'),
                f"{contract[5]:,.0f}", f"{contract[6]:,.0f}", contract[8]
            )
            self.tree.insert('', 'end', values=values, tags=(contract[0],))
    
    def create_contract(self):
        """Tạo hợp đồng mới"""
        CreateContractDialog(self.window, self.student_dao, self.room_dao, 
                           self.contract_dao, self.load_contracts)
    
    def renew_contract(self):
        """Gia hạn hợp đồng"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hợp đồng!")
            return
        
        contract_id = self.tree.item(selected[0])['tags'][0]
        RenewContractDialog(self.window, contract_id, self.contract_dao, self.load_contracts)
    
    def terminate_contract(self):
        """Thanh lý hợp đồng"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hợp đồng!")
            return
        
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thanh lý hợp đồng này?"):
            return
        
        contract_id = self.tree.item(selected[0])['tags'][0]
        
        if self.contract_dao.terminate_contract(contract_id):
            messagebox.showinfo("Thành công", "Đã thanh lý hợp đồng!")
            self.load_contracts()
        else:
            messagebox.showerror("Lỗi", "Không thể thanh lý hợp đồng!")
    
    def view_details(self):
        """Xem chi tiết"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hợp đồng!")
            return
        
        values = self.tree.item(selected[0])['values']
        
        detail = f"""
        THÔNG TIN CHI TIẾT HỢP ĐỒNG
        
        Mã hợp đồng: {values[1]}
        MSSV: {values[2]}
        Họ tên: {values[3]}
        Phòng: {values[4]}
        
        Ngày bắt đầu: {values[5]}
        Ngày kết thúc: {values[6]}
        
        Giá thuê/tháng: {values[7]} VNĐ
        Tiền cọc: {values[8]} VNĐ
        
        Trạng thái: {values[9]}
        """
        
        messagebox.showinfo("Chi tiết hợp đồng", detail)


# ============================================
# Dialog tạo hợp đồng
# ============================================

class CreateContractDialog:
    def __init__(self, parent, student_dao, room_dao, contract_dao, callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Tạo hợp đồng mới")
        self.dialog.geometry("500x500")
        self.dialog.grab_set()
        
        self.student_dao = student_dao
        self.room_dao = room_dao
        self.contract_dao = contract_dao
        self.callback = callback
        
        self.selected_student = None
        self.selected_room = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Tạo form"""
        tk.Label(
            self.dialog,
            text="TẠO HỢP ĐỒNG MỚI",
            font=('Arial', 14, 'bold'),
            fg='#3F51B5'
        ).pack(pady=15)
        
        form_frame = tk.Frame(self.dialog)
        form_frame.pack(padx=20, fill='both', expand=True)
        
        # Sinh viên
        tk.Label(form_frame, text="Sinh viên (*):").grid(row=0, column=0, sticky='w', pady=10)
        
        student_frame = tk.Frame(form_frame)
        student_frame.grid(row=0, column=1, pady=10, sticky='w')
        
        self.student_entry = tk.Entry(student_frame, width=20, state='readonly')
        self.student_entry.pack(side='left')
        
        tk.Button(
            student_frame,
            text="Chọn",
            width=8,
            command=self.select_student
        ).pack(side='left', padx=5)
        
        # Phòng
        tk.Label(form_frame, text="Phòng (*):").grid(row=1, column=0, sticky='w', pady=10)
        
        room_frame = tk.Frame(form_frame)
        room_frame.grid(row=1, column=1, pady=10, sticky='w')
        
        self.room_entry = tk.Entry(room_frame, width=20, state='readonly')
        self.room_entry.pack(side='left')
        
        tk.Button(
            room_frame,
            text="Chọn",
            width=8,
            command=self.select_room
        ).pack(side='left', padx=5)
        
        # Ngày bắt đầu
        tk.Label(form_frame, text="Ngày bắt đầu (*):").grid(row=2, column=0, sticky='w', pady=10)
        self.start_date = DateEntry(form_frame, width=27, date_pattern='dd/mm/yyyy')
        self.start_date.grid(row=2, column=1, pady=10, sticky='w')
        
        # Ngày kết thúc
        tk.Label(form_frame, text="Ngày kết thúc (*):").grid(row=3, column=0, sticky='w', pady=10)
        self.end_date = DateEntry(form_frame, width=27, date_pattern='dd/mm/yyyy')
        self.end_date.set_date(DateUtils.add_months(DateUtils.get_current_date(), 10))
        self.end_date.grid(row=3, column=1, pady=10, sticky='w')
        
        # Giá thuê
        tk.Label(form_frame, text="Giá thuê/tháng (*):").grid(row=4, column=0, sticky='w', pady=10)
        self.price_entry = tk.Entry(form_frame, width=30)
        self.price_entry.grid(row=4, column=1, pady=10, sticky='w')
        
        # Tiền cọc
        tk.Label(form_frame, text="Tiền cọc (*):").grid(row=5, column=0, sticky='w', pady=10)
        self.deposit_entry = tk.Entry(form_frame, width=30)
        self.deposit_entry.insert(0, "500000")
        self.deposit_entry.grid(row=5, column=1, pady=10, sticky='w')
        
        # Ghi chú
        tk.Label(form_frame, text="Ghi chú:").grid(row=6, column=0, sticky='w', pady=10)
        self.notes_text = tk.Text(form_frame, width=30, height=3)
        self.notes_text.grid(row=6, column=1, pady=10, sticky='w')
        
        # Buttons
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="✅ Tạo hợp đồng",
            bg='#4CAF50',
            fg='white',
            width=15,
            command=self.create
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Hủy",
            bg='#f44336',
            fg='white',
            width=15,
            command=self.dialog.destroy
        ).pack(side='left', padx=5)
    
    def select_student(self):
        """Chọn sinh viên"""
        SelectStudentDialog(self.dialog, self.student_dao, self.on_student_selected)
    
    def on_student_selected(self, student_id, student_code, student_name):
        """Callback khi chọn sinh viên"""
        self.selected_student = student_id
        self.student_entry.config(state='normal')
        self.student_entry.delete(0, 'end')
        self.student_entry.insert(0, f"{student_code} - {student_name}")
        self.student_entry.config(state='readonly')
    
    def select_room(self):
        """Chọn phòng"""
        SelectRoomDialog(self.dialog, self.room_dao, self.on_room_selected)
    
    def on_room_selected(self, room_id, room_number, price):
        """Callback khi chọn phòng"""
        self.selected_room = room_id
        self.room_entry.config(state='normal')
        self.room_entry.delete(0, 'end')
        self.room_entry.insert(0, room_number)
        self.room_entry.config(state='readonly')
        
        self.price_entry.delete(0, 'end')
        self.price_entry.insert(0, int(price))
    
    def create(self):
        """Tạo hợp đồng"""
        if not self.selected_student:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên!")
            return
        
        if not self.selected_room:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng!")
            return
        
        try:
            price = float(self.price_entry.get())
            deposit = float(self.deposit_entry.get())
        except:
            messagebox.showwarning("Cảnh báo", "Giá thuê và tiền cọc không hợp lệ!")
            return
        
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        notes = self.notes_text.get('1.0', 'end').strip()
        
        if self.contract_dao.add_contract(
            self.selected_student, self.selected_room,
            start_date, end_date, price, deposit, notes
        ):
            # Cập nhật số người ở
            self.room_dao.update_occupancy(self.selected_room)
            
            messagebox.showinfo("Thành công", "Đã tạo hợp đồng!")
            self.callback()
            self.dialog.destroy()
        else:
            messagebox.showerror("Lỗi", "Không thể tạo hợp đồng!")


# ============================================
# Dialog chọn sinh viên
# ============================================

class SelectStudentDialog:
    def __init__(self, parent, student_dao, callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Chọn sinh viên")
        self.dialog.geometry("600x400")
        self.dialog.grab_set()
        
        self.student_dao = student_dao
        self.callback = callback
        
        # Search
        search_frame = tk.Frame(self.dialog)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Tìm:").pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_students())
        
        # Listbox
        list_frame = tk.Frame(self.dialog)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(list_frame, font=('Arial', 10), yscrollcommand=scrollbar.set)
        self.listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        self.listbox.bind('<Double-1>', lambda e: self.select())
        
        # Buttons
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="Chọn",
            bg='#4CAF50',
            fg='white',
            width=12,
            command=self.select
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="Đóng",
            width=12,
            command=self.dialog.destroy
        ).pack(side='left', padx=5)
        
        self.load_students()
    
    def load_students(self):
        """Load sinh viên chưa có phòng"""
        self.listbox.delete(0, 'end')
        self.students_data = []
        
        keyword = self.search_entry.get().strip()
        
        if keyword:
            all_students = self.student_dao.search_students(keyword)
            for s in all_students:
                from dao.contract_dao import ContractDAO
                contract_dao = ContractDAO()
                contract = contract_dao.get_contract_by_student(s[0])
                if not contract:
                    self.students_data.append(s)
                    self.listbox.insert('end', f"{s[1]} - {s[2]} - {s[9]} - {s[11]}")
        else:
            students = self.student_dao.get_students_without_room()
            self.students_data = students
            for s in students:
                self.listbox.insert('end', f"{s[1]} - {s[2]} - {s[3]} - {s[4]}")
    
    def select(self):
        """Chọn sinh viên"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên!")
            return
        
        student = self.students_data[selection[0]]
        self.callback(student[0], student[1], student[2])
        self.dialog.destroy()


# ============================================
# Dialog chọn phòng
# ============================================

class SelectRoomDialog:
    def __init__(self, parent, room_dao, callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Chọn phòng")
        self.dialog.geometry("600x400")
        self.dialog.grab_set()
        
        self.room_dao = room_dao
        self.callback = callback
        
        tk.Label(
            self.dialog,
            text="Danh sách phòng còn chỗ",
            font=('Arial', 12, 'bold')
        ).pack(pady=10)
        
        # Listbox
        list_frame = tk.Frame(self.dialog)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(list_frame, font=('Arial', 10), yscrollcommand=scrollbar.set)
        self.listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        self.listbox.bind('<Double-1>', lambda e: self.select())
        
        # Buttons
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="Chọn",
            bg='#4CAF50',
            fg='white',
            width=12,
            command=self.select
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="Đóng",
            width=12,
            command=self.dialog.destroy
        ).pack(side='left', padx=5)
        
        self.load_rooms()
    
    def load_rooms(self):
        """Load phòng còn chỗ"""
        self.rooms_data = self.room_dao.get_available_rooms()
        
        for r in self.rooms_data:
            remaining = r[5] - r[6]
            self.listbox.insert('end', 
                f"{r[1]} - Tòa {r[2]} Tầng {r[3]} - Còn {remaining} chỗ - {r[7]:,.0f}đ/tháng")
    
    def select(self):
        """Chọn phòng"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng!")
            return
        
        room = self.rooms_data[selection[0]]
        self.callback(room[0], room[1], room[7])
        self.dialog.destroy()


# ============================================
# Dialog gia hạn hợp đồng
# ============================================

class RenewContractDialog:
    def __init__(self, parent, contract_id, contract_dao, callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Gia hạn hợp đồng")
        self.dialog.geometry("400x200")
        self.dialog.grab_set()
        
        self.contract_id = contract_id
        self.contract_dao = contract_dao
        self.callback = callback
        
        tk.Label(
            self.dialog,
            text="GIA HẠN HỢP ĐỒNG",
            font=('Arial', 14, 'bold'),
            fg='#2196F3'
        ).pack(pady=15)
        
        form_frame = tk.Frame(self.dialog)
        form_frame.pack(padx=20)
        
        tk.Label(form_frame, text="Ngày kết thúc mới (*):").grid(row=0, column=0, sticky='w', pady=10)
        self.new_end_date = DateEntry(form_frame, width=25, date_pattern='dd/mm/yyyy')
        self.new_end_date.set_date(DateUtils.add_months(DateUtils.get_current_date(), 10))
        self.new_end_date.grid(row=0, column=1, pady=10)
        
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="✅ Gia hạn",
            bg='#4CAF50',
            fg='white',
            width=12,
            command=self.renew
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Hủy",
            bg='#f44336',
            fg='white',
            width=12,
            command=self.dialog.destroy
        ).pack(side='left', padx=5)
    
    def renew(self):
        """Gia hạn"""
        new_end_date = self.new_end_date.get_date()
        
        if self.contract_dao.renew_contract(self.contract_id, new_end_date):
            messagebox.showinfo("Thành công", "Đã gia hạn hợp đồng!")
            self.callback()
            self.dialog.destroy()
        else:
            messagebox.showerror("Lỗi", "Không thể gia hạn hợp đồng!")