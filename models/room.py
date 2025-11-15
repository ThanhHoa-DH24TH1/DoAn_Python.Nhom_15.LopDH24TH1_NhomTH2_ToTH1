class Room:
    def __init__(self, room_id=None, room_number='', building='', floor=0,
                 room_type='', capacity=0, current_occupancy=0, 
                 price_per_month=0, status='Trống', description=''):
        self.room_id = room_id
        self.room_number = room_number
        self.building = building
        self.floor = floor
        self.room_type = room_type
        self.capacity = capacity
        self.current_occupancy = current_occupancy
        self.price_per_month = price_per_month
        self.status = status
        self.description = description