import tkinter as tk
from tkinter import ttk, messagebox
from dao.room_dao import RoomDAO
from dao.student_dao import StudentDAO
from dao.contract_dao import ContractDAO
from models.room import Room

class RoomManagementForm:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Quản lý Phòng")
        self.window.geometry("1200x700")
        self.window.state('zoomed')
        
        self.room_dao = RoomDAO()
        self.student_dao = StudentDAO()
        self.contract_dao = ContractDAO()
        
        self.create_widgets()
        self.load_rooms()
    
    def create_widgets(self):
        """Tạo giao diện"""
        # Title
        title_frame = tk.Frame(self.window, bg='#4CAF50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="QUẢN LÝ PHÒNG",
            font=('Arial', 16, 'bold'),
            bg='#4CAF50',
            fg='white'
        ).pack(pady=15)
        
        # Filter frame
        filter_frame = tk.Frame(self.window, bg='white')
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        # Tòa
        tk.Label(filter_frame, text="Tòa:", bg='white').pack(side='left', padx=5)
        self.building_combo = ttk.Combobox(filter_frame, width=10, state='readonly')
        self.building_combo.pack(side='left', padx=5)
        
        # Tầng
        tk.Label(filter_frame, text="Tầng:", bg='white').pack(side='left', padx=5)
        self.floor_combo = ttk.Combobox(filter_frame, width=10, state='readonly')
        self.floor_combo['values'] = ['Tất cả'] + [str(i) for i in range(1, 11)]
        self.floor_combo.current(0)
        self.floor_combo.pack(side='left', padx=5)
        
        # Trạng thái
        tk.Label(filter_frame, text="Trạng thái:", bg='white').pack(side='left', padx=5)
        self.status_combo = ttk.Combobox(filter_frame, width=15, state='readonly')
        self.status_combo['values'] = ['Tất cả', 'Trống', 'Còn chỗ', 'Đầy', 'Bảo trì']
        self.status_combo.current(0)
        self.status_combo.pack(side='left', padx=5)
        
        tk.Button(
            filter_frame,
            text="🔍 Lọc",
            bg='#2196F3',
            fg='white',
            command=self.filter_rooms
        ).pack(side='left', padx=5)
        
        tk.Button(
            filter_frame,
            text="🔄 Làm mới",
            bg='#4CAF50',
            fg='white',
            command=self.load_rooms
        ).pack(side='left', padx=5)
        
        # Main content
        content_frame = tk.Frame(self.window)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview
        tree_frame = tk.Frame(content_frame)
        tree_frame.pack(side='left', fill='both', expand=True)
        
        columns = ('STT', 'Số phòng', 'Tòa', 'Tầng', 'Loại', 'Sức chứa', 
                  'Đang ở', 'Còn trống', 'Giá/tháng', 'Trạng thái')
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        widths = [50, 100, 80, 80, 100, 100, 100, 100, 120, 120]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        
        # Color tags
        self.tree.tag_configure('empty', background="#a8ffbf")
        self.tree.tag_configure('available', background="#ffffff")
        self.tree.tag_configure('full', background="#ff0000")
        self.tree.tag_configure('maintenance', background="#edff61")
        
        # Button frame
        btn_frame = tk.Frame(content_frame, width=150)
        btn_frame.pack(side='right', fill='y', padx=(10, 0))
        
        buttons = [
            ("➕ Thêm phòng", self.add_room, '#4CAF50'),
            ("✏️ Sửa", self.edit_room, '#2196F3'),
            ("🗑️ Xóa", self.delete_room, '#f44336'),
            ("👥 Xem SV", self.view_students, '#FF9800'),
            ("🏠 Phân bổ", self.assign_room, '#9C27B0')
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
            ).pack(pady=5, fill='x')
        
        # Load buildings
        self.load_buildings()
    
    def load_buildings(self):
        """Load danh sách tòa"""
        buildings = self.room_dao.get_buildings()
        self.building_combo['values'] = ['Tất cả'] + buildings
        self.building_combo.current(0)
    
    def load_rooms(self):
        """Load danh sách phòng"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        rooms = self.room_dao.get_all_rooms()
        
        for idx, room in enumerate(rooms, 1):
            remaining = room[5] - room[6]  # Capacity - CurrentOccupancy
            values = (
                idx,
                room[1],  # RoomNumber
                room[2],  # Building
                room[3],  # Floor
                room[4],  # RoomType
                room[5],  # Capacity
                room[6],  # CurrentOccupancy
                remaining,
                f"{room[7]:,.0f}",  # PricePerMonth
                room[8]   # Status
            )
            
            # Màu sắc theo trạng thái
            tag = ''
            if room[8] == 'Trống':
                tag = 'empty'
            elif room[8] == 'Còn chỗ':
                tag = 'available'
            elif room[8] == 'Đầy':
                tag = 'full'
            elif room[8] == 'Bảo trì':
                tag = 'maintenance'
            
            self.tree.insert('', 'end', values=values, tags=(room[0], tag))
    
    def filter_rooms(self):
        """Lọc phòng"""
        building = self.building_combo.get()
        building = None if building == 'Tất cả' else building
        
        floor = self.floor_combo.get()
        floor = None if floor == 'Tất cả' else floor
        
        status = self.status_combo.get()
        status = None if status == 'Tất cả' else status
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        rooms = self.room_dao.search_rooms(building, floor, status)
        
        for idx, room in enumerate(rooms, 1):
            remaining = room[5] - room[6]
            values = (
                idx, room[1], room[2], room[3], room[4],
                room[5], room[6], remaining,
                f"{room[7]:,.0f}", room[8]
            )
            
            tag = ''
            if room[8] == 'Trống':
                tag = 'empty'
            elif room[8] == 'Còn chỗ':
                tag = 'available'
            elif room[8] == 'Đầy':
                tag = 'full'
            
            self.tree.insert('', 'end', values=values, tags=(room[0], tag))
    
    def add_room(self):
        """Thêm phòng"""
        RoomFormDialog(self.window, None, self.load_rooms)
    
    def edit_room(self):
        """Sửa phòng"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng!")
            return
        
        room_id = self.tree.item(selected[0])['tags'][0]
        room_data = self.room_dao.get_room_by_id(room_id)
        
        if room_data:
            RoomFormDialog(self.window, room_data, self.load_rooms)
    
    def delete_room(self):
        """Xóa phòng"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng!")
            return
        
        room_id = self.tree.item(selected[0])['tags'][0]
        
        # Kiểm tra còn sinh viên không
        students = self.room_dao.get_students_in_room(room_id)
        if students:
            messagebox.showwarning("Cảnh báo", 
                                 "Không thể xóa phòng đang có sinh viên ở!")
            return
        
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phòng này?"):
            return
        
        if self.room_dao.delete_room(room_id):
            messagebox.showinfo("Thành công", "Đã xóa phòng!")
            self.load_rooms()
        else:
            messagebox.showerror("Lỗi", "Không thể xóa phòng!")
    
    def view_students(self):
        """Xem sinh viên trong phòng"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng!")
            return
        
        room_id = self.tree.item(selected[0])['tags'][0]
        RoomStudentsDialog(self.window, room_id, self.room_dao, self.contract_dao)
    
    def assign_room(self):
        """Phân bổ sinh viên vào phòng"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng!")
            return
        
        room_id = self.tree.item(selected[0])['tags'][0]
        room_data = self.room_dao.get_room_by_id(room_id)
        
        if room_data[6] >= room_data[5]:  # CurrentOccupancy >= Capacity
            messagebox.showwarning("Cảnh báo", "Phòng đã đầy!")
            return
        
        AssignRoomDialog(self.window, room_id, room_data, 
                        self.student_dao, self.room_dao, 
                        self.contract_dao, self.load_rooms)


# ============================================
# Dialog Form thêm/sửa phòng
# ============================================

class RoomFormDialog:
    def __init__(self, parent, room_data, callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Thông tin phòng")
        self.dialog.geometry("500x500")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        self.room_data = room_data
        self.callback = callback
        self.room_dao = RoomDAO()
        
        self.create_form()
        
        if room_data:
            self.load_data()
    
    def create_form(self):
        """Tạo form"""
        title = "CẬP NHẬT PHÒNG" if self.room_data else "THÊM PHÒNG MỚI"
        tk.Label(
            self.dialog,
            text=title,
            font=('Arial', 14, 'bold'),
            fg='#4CAF50'
        ).pack(pady=15)
        
        form_frame = tk.Frame(self.dialog)
        form_frame.pack(padx=20, fill='both', expand=True)
        
        # Số phòng
        tk.Label(form_frame, text="Số phòng (*):").grid(row=0, column=0, sticky='w', pady=10)
        self.room_number_entry = tk.Entry(form_frame, width=30)
        self.room_number_entry.grid(row=0, column=1, pady=10)
        
        # Tòa
        tk.Label(form_frame, text="Tòa (*):").grid(row=1, column=0, sticky='w', pady=10)
        self.building_combo = ttk.Combobox(form_frame, width=28, state='readonly')
        self.building_combo['values'] = ['A', 'B', 'C', 'D', 'E']
        self.building_combo.grid(row=1, column=1, pady=10)
        
        # Tầng
        tk.Label(form_frame, text="Tầng (*):").grid(row=2, column=0, sticky='w', pady=10)
        self.floor_spin = tk.Spinbox(form_frame, from_=1, to=10, width=28)
        self.floor_spin.grid(row=2, column=1, pady=10)
        
        # Loại phòng
        tk.Label(form_frame, text="Loại phòng (*):").grid(row=3, column=0, sticky='w', pady=10)
        self.type_combo = ttk.Combobox(form_frame, width=28, state='readonly')
        self.type_combo['values'] = ['2 người', '4 người', '6 người', '8 người']
        self.type_combo.grid(row=3, column=1, pady=10)
        
        # Sức chứa
        tk.Label(form_frame, text="Sức chứa (*):").grid(row=4, column=0, sticky='w', pady=10)
        self.capacity_spin = tk.Spinbox(form_frame, from_=2, to=8, width=28)
        self.capacity_spin.grid(row=4, column=1, pady=10)
        
        # Giá thuê
        tk.Label(form_frame, text="Giá/tháng (VNĐ) (*):").grid(row=5, column=0, sticky='w', pady=10)
        self.price_entry = tk.Entry(form_frame, width=30)
        self.price_entry.grid(row=5, column=1, pady=10)
        
        # Trạng thái
        tk.Label(form_frame, text="Trạng thái:").grid(row=6, column=0, sticky='w', pady=10)
        self.status_combo = ttk.Combobox(form_frame, width=28, state='readonly')
        self.status_combo['values'] = ['Trống', 'Còn chỗ', 'Đầy', 'Bảo trì']
        self.status_combo.grid(row=6, column=1, pady=10)
        
        # Mô tả
        tk.Label(form_frame, text="Mô tả:").grid(row=7, column=0, sticky='w', pady=10)
        self.desc_text = tk.Text(form_frame, width=30, height=4)
        self.desc_text.grid(row=7, column=1, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="💾 Lưu",
            font=('Arial', 10, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=12,
            command=self.save
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Hủy",
            font=('Arial', 10),
            bg='#f44336',
            fg='white',
            width=12,
            command=self.dialog.destroy
        ).pack(side='left', padx=5)
    
    def load_data(self):
        """Load dữ liệu phòng"""
        self.room_number_entry.insert(0, self.room_data[1])
        self.room_number_entry.config(state='disabled')
        
        self.building_combo.set(self.room_data[2])
        self.floor_spin.delete(0, 'end')
        self.floor_spin.insert(0, self.room_data[3])
        self.type_combo.set(self.room_data[4])
        self.capacity_spin.delete(0, 'end')
        self.capacity_spin.insert(0, self.room_data[5])
        self.price_entry.insert(0, int(self.room_data[7]))
        self.status_combo.set(self.room_data[8])
        if self.room_data[9]:
            self.desc_text.insert('1.0', self.room_data[9])
    
    def save(self):
        """Lưu phòng"""
        # Validate
        room_number = self.room_number_entry.get().strip()
        if not room_number:
            messagebox.showwarning("Cảnh báo", "Số phòng không được để trống!")
            return
        
        building = self.building_combo.get()
        if not building:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tòa!")
            return
        
        room_type = self.type_combo.get()
        if not room_type:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn loại phòng!")
            return
        
        try:
            floor = int(self.floor_spin.get())
            capacity = int(self.capacity_spin.get())
            price = float(self.price_entry.get())
        except:
            messagebox.showwarning("Cảnh báo", "Dữ liệu số không hợp lệ!")
            return
        
        # Tạo object Room
        room = Room()
        room.room_number = room_number
        room.building = building
        room.floor = floor
        room.room_type = room_type
        room.capacity = capacity
        room.price_per_month = price
        room.status = self.status_combo.get() or 'Trống'
        room.description = self.desc_text.get('1.0', 'end').strip()
        
        if self.room_data:
            room.room_id = self.room_data[0]
            if self.room_dao.update_room(room):
                messagebox.showinfo("Thành công", "Đã cập nhật phòng!")
                self.callback()
                self.dialog.destroy()
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật phòng!")
        else:
            if self.room_dao.add_room(room):
                messagebox.showinfo("Thành công", "Đã thêm phòng!")
                self.callback()
                self.dialog.destroy()
            else:
                messagebox.showerror("Lỗi", "Không thể thêm phòng! Số phòng có thể đã tồn tại.")


# ============================================
# Dialog xem sinh viên trong phòng
# ============================================

class RoomStudentsDialog:
    def __init__(self, parent, room_id, room_dao, contract_dao):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Sinh viên trong phòng")
        self.dialog.geometry("600x400")
        self.dialog.grab_set()
        
        self.room_id = room_id
        self.room_dao = room_dao
        self.contract_dao = contract_dao
        
        room_data = room_dao.get_room_by_id(room_id)
        
        # Title
        tk.Label(
            self.dialog,
            text=f"PHÒNG {room_data[1]} - TÒA {room_data[2]} TẦNG {room_data[3]}",
            font=('Arial', 12, 'bold'),
            fg='#2196F3'
        ).pack(pady=10)
        
        tk.Label(
            self.dialog,
            text=f"Đang ở: {room_data[5]}/{room_data[4]} người",
            font=('Arial', 10)
        ).pack()
        
        # Listbox
        list_frame = tk.Frame(self.dialog)
        list_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(list_frame, font=('Arial', 10), yscrollcommand=scrollbar.set)
        self.listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Load students
        students = room_dao.get_students_in_room(room_id)
        for s in students:
            self.listbox.insert('end', f"{s[1]} - {s[2]} - {s[3]}")
        
        # Buttons
        tk.Button(
            self.dialog,
            text="Đóng",
            width=15,
            command=self.dialog.destroy
        ).pack(pady=10)


# ============================================
# Dialog phân bổ sinh viên vào phòng
# ============================================

class AssignRoomDialog:
    def __init__(self, parent, room_id, room_data, student_dao, room_dao, contract_dao, callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Phân bổ phòng")
        self.dialog.geometry("700x500")
        self.dialog.grab_set()
        
        self.room_id = room_id
        self.room_data = room_data
        self.student_dao = student_dao
        self.room_dao = room_dao
        self.contract_dao = contract_dao
        self.callback = callback
        
        self.create_widgets()
        self.load_students()
    
    def create_widgets(self):
        """Tạo giao diện"""
        # Title
        tk.Label(
            self.dialog,
            text=f"PHÂN BỔ SINH VIÊN VÀO PHÒNG {self.room_data[1]}",
            font=('Arial', 12, 'bold'),
            fg='#2196F3'
        ).pack(pady=10)
        
        tk.Label(
            self.dialog,
            text=f"Còn {self.room_data[5] - self.room_data[6]} chỗ trống",
            font=('Arial', 10)
        ).pack()
        
        # Search
        search_frame = tk.Frame(self.dialog)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Tìm SV:").pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_students())
        
        # Listbox
        list_frame = tk.Frame(self.dialog)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(
            list_frame,
            font=('Arial', 10),
            yscrollcommand=scrollbar.set,
            selectmode='single'
        )
        self.listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="✅ Phân bổ",
            bg='#4CAF50',
            fg='white',
            width=12,
            command=self.assign
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Đóng",
            bg='#f44336',
            fg='white',
            width=12,
            command=self.dialog.destroy
        ).pack(side='left', padx=5)
    
    def load_students(self):
        """Load sinh viên chưa có phòng"""
        self.listbox.delete(0, 'end')
        self.students_data = []
        
        keyword = self.search_entry.get().strip()
        
        if keyword:
            all_students = self.student_dao.search_students(keyword)
            # Lọc những SV chưa có phòng
            for s in all_students:
                contract = self.contract_dao.get_contract_by_student(s[0])
                if not contract:
                    self.students_data.append(s)
                    self.listbox.insert('end', f"{s[1]} - {s[2]} - {s[9]} - {s[11]}")
        else:
            students = self.student_dao.get_students_without_room()
            self.students_data = students
            for s in students:
                self.listbox.insert('end', f"{s[1]} - {s[2]} - {s[3]} - {s[4]}")
    
    def assign(self):
        """Phân bổ sinh viên"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên!")
            return
        
        student = self.students_data[selection[0]]
        student_id = student[0]
        
        # Tạo hợp đồng
        from utils.date_utils import DateUtils
        
        start_date = DateUtils.get_current_date()
        end_date = DateUtils.add_months(start_date, 10)
        price = self.room_data[7]
        
        if self.contract_dao.add_contract(
            student_id, self.room_id, start_date, end_date,
            price, 500000, 'Phân bổ phòng'
        ):
            # Cập nhật số người ở
            self.room_dao.update_occupancy(self.room_id)
            
            messagebox.showinfo(
                "Thành công",
                f"Đã phân bổ phòng {self.room_data[1]} cho sinh viên {student[1]}!"
            )
            self.callback()
            self.dialog.destroy()
        else:
            messagebox.showerror("Lỗi", "Không thể phân bổ phòng!")