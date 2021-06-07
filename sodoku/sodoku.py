class Board:
    # The backtracking approach is to generate all possible numbers (1-9)
    # into the empty cells.
    # Try every row, column one by one until the correct solution is found.
    INIT_STAGE = [
        [3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]
    selected = None

    def __init__(self, input=None):
        self.init_area()
        self.refesh_stage()

    def init_area(self):
        self.areas = []
        for i in range(9):
            row = [Area(self.INIT_STAGE[i][j], i, j) for j in range(9)]
            self.areas.append(row)

    def update_stage(self, value, pos):
        self.stage[pos[0]][pos[1]] = value

    def refesh_stage(self):
        self.stage = \
            [[self.areas[i][j].value for j in range(9)] for i in range(9)]

    def refresh(self):
        self.init_area()
        self.refesh_stage()

    def select(self, pos):
        if pos is not None:
            # Unselect old area
            if self.selected is not None:
                self.areas[self.selected[0]][self.selected[1]].unselect()
            # Select new area
            self.areas[pos[0]][pos[1]].select()
            self.selected = pos

    def sketch(self, value):
        if self.selected is not None:
            self.areas[self.selected[0]][self.selected[1]].sketch(value)

    def commit(self):
        if self.selected is not None:
            x, y = self.selected
            area = self.areas[x][y]
            if self.is_safe_state(area.temp, (x, y)):
                self.update_stage(area.temp, (x, y))
                if self.solve():
                    self.areas[x][y].save()
                    self.selected = None
                self.refesh_stage()

    def is_safe_state(self, num, pos):
        for x in range(9):
            # Validate if the same 'num' in the same row
            if num == self.stage[pos[0]][x]:
                return False
            # Validate if the same 'num' in the same column
            if num == self.stage[x][pos[1]]:
                return False
        # Validate if the same 'num' in the same block 3x3
        start_x = pos[0] - pos[0] % 3
        start_y = pos[1] - pos[1] % 3
        for x in range(3):
            for y in range(3):
                if (num == self.stage[start_x + x][start_y + y]):
                    return False
        return True

    # Find the next empty location in the stafe from current position
    def find_next_location(self, pos=(0, 0)):
        for x in range(pos[0], 9):
            for y in range(pos[1], 9):
                if self.stage[x][y] == 0:
                    return (x, y)
        return None

    def solve(self):
        loc = self.find_next_location()

        if not loc:
            return True
        else:
            x, y = loc
        # Try all number cases
        for num in range(1, 10):
            # Check if it is safe to place number from (1-9)
            if self.is_safe_state(num, loc):
                self.stage[x][y] = num
                if self.solve():
                    return True
            # Assumption is incorrect, reset to 0
            self.stage[x][y] = 0
        # Backtracking
        return False

    def log(self):
        for row in self.stage:
            print(row, end="\n")
        print("------------------")


class Area:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.temp = 0
        self.selected = False
        self.default = bool(value)

    def sketch(self, temp):
        self.temp = temp

    def save(self):
        self.value = self.temp

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False
