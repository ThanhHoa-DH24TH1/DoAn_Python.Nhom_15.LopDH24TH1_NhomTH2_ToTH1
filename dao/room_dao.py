from database.connection import DatabaseConnection

class RoomDAO:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all_rooms(self):
        """Lấy tất cả phòng"""
        query = "SELECT * FROM Rooms ORDER BY Building, Floor, RoomNumber"
        room = self.db.execute_query(query)
        return room
    
    def get_room_by_id(self, room_id):
        """Lấy phòng theo ID"""
        query = "SELECT * FROM Rooms WHERE RoomID = ?"
        rows = self.db.execute_query(query, (room_id,))
        return rows[0] if rows else None
    
    def search_rooms(self, building=None, floor=None, status=None):
        """Tìm kiếm phòng theo điều kiện"""
        query = "SELECT * FROM Rooms WHERE 1=1"
        params = []
        
        if building and building != 'Tất cả':
            query += " AND Building = ?"
            params.append(building)
        
        if floor and floor != 'Tất cả':
            query += " AND Floor = ?"
            params.append(floor)
        
        if status and status != 'Tất cả':
            query += " AND Status = ?"
            params.append(status)
        
        query += " ORDER BY Building, Floor, RoomNumber"
        return self.db.execute_query(query, tuple(params)) if params else self.db.execute_query(query)
    
    def add_room(self, room):
        """Thêm phòng mới"""
        query = """
            INSERT INTO Rooms (RoomNumber, Building, Floor, RoomType, 
                             Capacity, PricePerMonth, Status, Description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            room.room_number, room.building, room.floor, room.room_type,
            room.capacity, room.price_per_month, room.status, room.description
        )
        return self.db.execute_non_query(query, params)
    
    def update_room(self, room):
        """Cập nhật phòng"""
        query = """
            UPDATE Rooms SET
                Building = ?, Floor = ?, RoomType = ?,
                Capacity = ?, PricePerMonth = ?, 
                Status = ?, Description = ?
            WHERE RoomID = ?
        """
        params = (
            room.building, room.floor, room.room_type,
            room.capacity, room.price_per_month,
            room.status, room.description, room.room_id
        )
        return self.db.execute_non_query(query, params)
    
    def delete_room(self, room_id):
        """Xóa phòng"""
        query = "DELETE FROM Rooms WHERE RoomID = ?"
        return self.db.execute_non_query(query, (room_id,))
    
    def get_available_rooms(self):
        """Lấy phòng còn chỗ"""
        query = """
            SELECT * FROM Rooms 
            WHERE CurrentOccupancy < Capacity AND Status IN (N'Trống', N'Còn chỗ')
            ORDER BY Building, Floor, RoomNumber
        """
        room = self.db.execute_query(query)
        return room
    
    def get_students_in_room(self, room_id):
        """Lấy danh sách sinh viên trong phòng"""
        query = """
            SELECT s.StudentID, s.StudentCode, s.FullName, s.PhoneNumber
            FROM Students s
            INNER JOIN Contracts c ON s.StudentID = c.StudentID
            WHERE c.RoomID = ? AND c.Status = N'Đang hiệu lực'
            ORDER BY s.StudentCode
        """
        try:
            result = self.db.execute_query(query, (room_id,))
            print(f"[DEBUG] Room {room_id}: Found {len(result)} students")
            for r in result:
                print(f"  - {r[1]}: {r[2]}")
            return result
        except Exception as e:
            print(f"[ERROR] get_students_in_room: {e}")
            return []

        
    def update_occupancy(self, room_id):
        """Cập nhật số người ở hiện tại"""
        query = """
            UPDATE Rooms
            SET CurrentOccupancy = (
                SELECT COUNT(*) FROM Contracts
                WHERE RoomID = ? AND Status = N'Đang hiệu lực'
            ),
            Status = CASE
                WHEN (SELECT COUNT(*) FROM Contracts WHERE RoomID = ? AND Status = N'Đang hiệu lực') = 0
                    THEN N'Trống'
                WHEN (SELECT COUNT(*) FROM Contracts WHERE RoomID = ? AND Status = N'Đang hiệu lực') < Capacity
                    THEN N'Còn chỗ'
                ELSE N'Đầy'
            END
            WHERE RoomID = ?
        """
        return self.db.execute_non_query(query, (room_id, room_id, room_id, room_id))
    
    def get_buildings(self):
        """Lấy danh sách tòa"""
        query = "SELECT DISTINCT Building FROM Rooms ORDER BY Building"
        rows = self.db.execute_query(query)
        return [row[0] for row in rows]