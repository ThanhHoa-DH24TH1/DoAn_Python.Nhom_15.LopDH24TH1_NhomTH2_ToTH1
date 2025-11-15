from database.connection import DatabaseConnection
from datetime import datetime

class InvoiceDAO:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_invoice(self, contract_id, student_id, billing_month, 
                   room_fee, electricity_fee, water_fee, 
                   internet_fee, service_fee):
        """Tạo hóa đơn mới"""
        try:
            total = room_fee + electricity_fee + water_fee + internet_fee + service_fee
            
            # Sửa câu lệnh INSERT (bỏ BillingYear)
            query = """
                INSERT INTO Invoices (
                    ContractID, StudentID, BillingMonth,
                    RoomFee, ElectricityFee, WaterFee, 
                    InternetFee, ServiceFee, TotalAmount, 
                    RemainingAmount, Status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, N'Chưa thanh toán')
            """
            
            # Sửa bộ tham số (params) (bỏ billing_year)
            params = (
                contract_id, student_id, billing_month,  # billing_month giờ là "2025-10"
                room_fee, electricity_fee, water_fee, 
                internet_fee, service_fee, 
                total, total
            )
            
            return self.db.execute_non_query(query, params)
        
        except Exception as e:
            print(f"Lỗi create_invoice: {e}")
            return False
    
    def get_all_invoices(self, month=None, status=None):
        """Lấy danh sách hóa đơn"""
        query = """
            SELECT i.*, s.StudentCode, s.FullName, r.RoomNumber
            FROM Invoices i
            INNER JOIN Students s ON i.StudentID = s.StudentID
            INNER JOIN Contracts c ON i.ContractID = c.ContractID
            INNER JOIN Rooms r ON c.RoomID = r.RoomID
            WHERE 1=1
        """
        params = []
        
        if month:
            query += " AND i.BillingMonth = ?"
            params.append(month)
        
        if status and status != 'Tất cả':
            query += " AND i.Status = ?"
            params.append(status)
        
        query += " ORDER BY i.BillingMonth DESC, s.StudentCode"
        
        if params:
            return self.db.execute_query(query, tuple(params))
        return self.db.execute_query(query)
    
    def get_invoice_by_id(self, invoice_id):
        """Lấy chi tiết hóa đơn"""
        query = """
            SELECT i.*, s.StudentCode, s.FullName, r.RoomNumber
            FROM Invoices i
            INNER JOIN Students s ON i.StudentID = s.StudentID
            INNER JOIN Contracts c ON i.ContractID = c.ContractID
            INNER JOIN Rooms r ON c.RoomID = r.RoomID
            WHERE i.InvoiceID = ?
        """
        rows = self.db.execute_query(query, (invoice_id,))
        return rows[0] if rows else None
    
    def record_payment(self, invoice_id, amount, payment_method, notes=''):
        """Ghi nhận thanh toán"""
        # Lấy thông tin hóa đơn hiện tại
        query = "SELECT TotalAmount, PaidAmount FROM Invoices WHERE InvoiceID = ?"
        result = self.db.execute_query(query, (invoice_id,))
        if not result:
            return False
        
        total_amount, paid_amount = result[0]
        new_paid = paid_amount + amount
        remaining = total_amount - new_paid
        
        # Xác định trạng thái
        if remaining <= 0:
            status = 'Đã thanh toán'
        elif new_paid > 0:
            status = 'Thanh toán 1 phần'
        else:
            status = 'Chưa thanh toán'
        
        # Cập nhật hóa đơn
        update_query = """
            UPDATE Invoices SET
                PaidAmount = ?,
                RemainingAmount = ?,
                Status = ?,
                PaymentDate = GETDATE()
            WHERE InvoiceID = ?
        """
        success = self.db.execute_non_query(update_query, 
                                           (new_paid, remaining, status, invoice_id))
        
        if success:
            # Ghi vào bảng Payments
            payment_query = """
                INSERT INTO Payments (InvoiceID, Amount, PaymentMethod, Notes)
                VALUES (?, ?, ?, ?)
            """
            self.db.execute_non_query(payment_query, 
                                     (invoice_id, amount, payment_method, notes))
        
        return success
    
    def get_payment_history(self, invoice_id):
        """Lấy lịch sử thanh toán"""
        query = """
            SELECT * FROM Payments 
            WHERE InvoiceID = ? 
            ORDER BY PaymentDate DESC
        """
        return self.db.execute_query(query, (invoice_id,))
    def check_invoice_exists(self, student_id, billing_month, billing_year):
        query = """
            SELECT 1 FROM Invoices 
            WHERE StudentID = ? AND BillingMonth = ? AND BillingYear = ?
        """
        params = (student_id, billing_month, billing_year)
        result = self.db.execute_query(query, params)
        return True if result else False
    
    def get_total_debt(self, student_id):
        """Tính tổng nợ"""
        query = "SELECT SUM(RemainingAmount) FROM Invoices WHERE StudentID = ? AND RemainingAmount > 0"
        result = self.db.execute_scalar(query, (student_id,))
        return result if result else 0

    def get_total_paid(self, student_id):
        """Tổng đã thanh toán"""
        query = "SELECT SUM(PaidAmount) FROM Invoices WHERE StudentID = ?"
        result = self.db.execute_scalar(query, (student_id,))
        return result if result else 0

    def get_current_month_invoice_total(self, student_id, month):
        """Hóa đơn tháng hiện tại"""
        query = "SELECT TotalAmount FROM Invoices WHERE StudentID = ? AND BillingMonth = ?"
        result = self.db.execute_scalar(query, (student_id, month))
        return result if result else 0

    def get_invoices_by_student(self, student_id, limit=5):
        """Danh sách hóa đơn của SV"""
        query = f"""
            SELECT TOP {limit} InvoiceID, BillingMonth, TotalAmount, 
                PaidAmount, RemainingAmount, Status
            FROM Invoices WHERE StudentID = ?
            ORDER BY BillingMonth DESC
        """
        return self.db.execute_query(query, (student_id,))
    def delete_invovice_by_student(self, student_id):
        '''Xóa hóa đơn của sinh viên'''
        query = '''
            DELETE FROM Invoices 
            WHERE ContractID IN (
                SELECT ContractID FROM Contracts WHERE StudentID = ?
            )
        '''
        return self.db.execute_non_query(query, (student_id,))
    
    def delete_payments_by_student(self, student_id):
        """Xóa TẤT CẢ các bản ghi thanh toán liên quan đến hóa đơn của một sinh viên"""
        # Xóa các Payments mà InvoiceID của nó thuộc về StudentID cần xóa
        query = """
            DELETE FROM Payments 
            WHERE InvoiceID IN (SELECT InvoiceID FROM Invoices WHERE StudentID = ?)
        """
        return self.db.execute_non_query(query, (student_id,))