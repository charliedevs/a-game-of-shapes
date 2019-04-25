#Test file for functions
from src.unit import Unit

cols = 9
rows = 6

grid = [[[0, 0] for j in range(cols)] for i in range(rows)]

# col 3 row 4
grid[1][7] = [0,1]

my_unit = Unit(1)
my_unit.pos = [7, 1]
range_list = my_unit.get_move_range(cols, rows)

print(range_list)