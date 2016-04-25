
class Group():
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID

groups = {
"cher" : Group("Character", 0),
"enemy" : Group("Abstract Enemy", 1)
}
relations_list = [
#   Char enemy
    [0,   0], # Char
    [-1, -1]  # Enemy
]
