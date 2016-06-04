
class Group():
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID

groups = {
"Alfa_c" : Group("Character", 0),
"enemy" : Group("Abstract Enemy", 1)
}
relations_list = [
#   Alfa_C  enemy
    [0,      0], # Alfa_C
    [-1,    -1]  # Enemy
]
