from database.connection import DatabaseConnection

class ContractDAO:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def add_contract(self, student_id, room_id, start_date, end_date, 
                    monthly_fee, deposit, notes=''):
        """Tạo hợp đồng mới"""
        query = """
            INSERT INTO Contracts (StudentID, RoomID, StartDate, EndDate, 
                                 MonthlyFee, Deposit, Status, Notes)
            VALUES (?, ?, ?, ?, ?, ?, N'Đang hiệu lực', ?)
        """
        params = (student_id, room_id, start_date, end_date, 
                 monthly_fee, deposit, notes)
        return self.db.execute_non_query(query, params)
    
    def get_all_contracts(self):
        """Lấy tất cả hợp đồng"""
        query = """
            SELECT c.*, s.StudentCode, s.FullName, r.RoomNumber
            FROM Contracts c
            INNER JOIN Students s ON c.StudentID = s.StudentID
            INNER JOIN Rooms r ON c.RoomID = r.RoomID
            ORDER BY c.ContractID DESC
        """
        c = self.db.execute_query(query)
        return c
    
    def get_contract_by_student(self, student_id):
        """Lấy hợp đồng của sinh viên"""
        query = """
            SELECT c.*, r.RoomNumber, r.Building, r.Floor
            FROM Contracts c
            INNER JOIN Rooms r ON c.RoomID = r.RoomID
            WHERE c.StudentID = ? AND c.Status = N'Đang hiệu lực'
        """
        rows = self.db.execute_query(query, (student_id,))
        return rows[0] if rows else None
    
    def terminate_contract(self, contract_id):
        """Thanh lý hợp đồng"""
        query = "UPDATE Contracts SET Status = N'Thanh lý' WHERE ContractID = ?"
        return self.db.execute_non_query(query, (contract_id,))
    def search_contracts(self, keyword=None, status=None):
        '''Tìm kiếm hợp đồng'''
        query = '''
            SELECT c.*, s.StudentCode, s.FullName, r.RoomNumber
            FROM Contracts c
            INNER JOIN Students s ON c.StudentID = s.StudentID
            INNER JOIN Rooms r ON c.RoomID = r.RoomID
            WHERE 1=1
        '''
        params = []
        
        if keyword:
            query += " AND (s.StudentCode LIKE ? OR s.FullName LIKE ?)"
            params.extend([f'%{keyword}%', f'%{keyword}%'])
        
        if status and status != 'Tất cả':
            query += " AND c.Status = ?"
            params.append(status)
        
        query += " ORDER BY c.ContractID DESC"
        
        if params:
            return self.db.execute_query(query, tuple(params))
        return self.db.execute_query(query)
    
    def renew_contract(self, contract_id, new_end_date):
        '''Gia hạn hợp đồng'''
        query = "UPDATE Contracts SET EndDate = ? WHERE ContractID = ?"
        return self.db.execute_non_query(query, (new_end_date, contract_id))
    
    def delete_student_contracts(self, student_id):
        '''Xóa hợp đồng của sinh viên'''
        query = "DELETE FROM Contracts WHERE StudentID = ?"
        return self.db.execute_non_query(query, (student_id,))
    
    
    