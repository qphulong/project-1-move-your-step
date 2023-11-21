class Room:
    def __init__(self):
        self.tags = []
        self.connectedRooms = []
        self.doors = []

    def appendTag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
    
    def removeTag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def addConnectedRoom(self, room):
        if room not in self.connectedRooms:
            self.connectedRooms.append(room)

    def removeConnectedRoom(self, room):
        if room in self.connectedRooms:
            self.connectedRooms.remove(room)

    def addDoor(self, door):
        if door not in self.doors:
            self.doors.append(door)

    def removeDoor(self, door):
        if door in self.doors:
            self.doors.remove(door)
    