from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

PIECES = [
    '100.100.111',
    '111.110',
    '101.111',
    '0001.1111',
    '0111.1100',
    '010.010.111',
    '1111.0100',
    '110.011.010',
    '110.010.011',
    '11111'
]

MONTHS = [
    (0,0), # Jan
    (0,1), # Feb
    (0,2), # Mar
    (0,3), # Apr
    (1,0), # May
    (2,0), # Jun
    (3,0), # Jul
    (4,0), # Aug
    (5,0), # Sep
    (5,1), # Oct
    (5,2), # Nov
    (5,3), # Dec
]

DAYS = [
    (0,4),
    (0,5),
    (0,6),
    (1,1),
    (1,2),
    (1,3),
    (1,4),
    (1,5),
    (1,6),
    (2,1),
    (2,2),
    (2,3),
    (2,4),
    (5,7), # 31
    (2,6),
    (3,1),
    (3,2),
    (3,3),
    (3,4),
    (3,5),
    (3,6),
    (4,1),
    (4,2),
    (4,3),
    (4,4),
    (4,5),
    (4,6),
    (5,4),
    (5,5),
    (5,6),
    (2,5), # 14
]

WEEKDAYS = [
    (0, 7), # Mon
    (0, 8), # Tue
    (1, 7), # Wed
    (2, 7), # Thu
    (3, 7), # Fri
    (3, 8), # Sat
    (4, 8), # Sun
]

def create_pieces() -> list[np.ndarray]:
    return [(i+1) * np.array([[int(char) for char in row] for row in s.split('.')]) for i, s in enumerate(PIECES)]

def rot90(p: np.ndarray) -> np.ndarray:
    sh = p.shape
    new_p = np.zeros(sh[1], sh[0])


class Board:
    def __init__(self, exceptions: list[tuple[int,int]]):
        self.b = np.zeros((6,9), dtype=np.int16)
        self.b[-1,-1] = -1
        for x, y in exceptions:
            self.b[x, y] = -1
        self.used = [False for _ in range(10)]
        self.flipable = [False for _ in range(10)]
        self.flipable[7] = True

    def place(self, x: int, y: int, p: np.array) -> bool:
        sh = p.shape
        if x < 0 or x + sh[0] > self.b.shape[0]:
            return False
        if y < 0 or y + sh[1] > self.b.shape[1]:
            return False
        for dx in range(sh[0]):
            for dy in range(sh[1]):
                if p[dx,dy] > 0 and self.b[x+dx, y+dy] != 0:
                    return False
        # Actually place stuff
        for dx in range(sh[0]):
            for dy in range(sh[1]):
                if p[dx, dy] > 0:
                    self.b[x+dx, y+dy] = p[dx, dy]
        return True

    def remove(self, x: int, y: int, p: np.array):
        sh = p.shape
        if x < 0 or x + sh[0] > self.b.shape[0]:
            return False
        if y < 0 or y + sh[1] > self.b.shape[1]:
            return False
        for dx in range(sh[0]):
            for dy in range(sh[1]):
                if p[dx,dy] == self.b[x+dx, y+dy]:
                    self.b[x+dx, y+dy] = 0
        return True

    def find_next_spot(self, x, y) -> tuple[int,int]:
        while x < self.b.shape[0]:
            while y < self.b.shape[1]:
                if self.b[x, y] == 0:
                    return x, y
                y += 1
            y = 0
            x += 1
        return x, y

    def test_placement(self, pieces, piece, i, x, y) -> bool:
        p_i = piece.copy()
        # Add to limit retries with same piece
        tried = []
        for _ in range(4):
            p_i = rot90(p_i)
            for t in tried:
                if t.shape == p_i.shape and (t == p_i).all():
                    return False
            tried.append(p_i.copy())
            off = 0
            while p_i[0, off] == 0:
                off += 1
            if self.place(x, y-off, p_i):
                self.used[i] = True
                nx, ny = self.find_next_spot(x, y)
                if self.solve(pieces, nx, ny):
                    return True
                self.remove(x, y-off, p_i)
                self.used[i] = False
        return False

    def Solve(self, pieces) -> bool:
        x, y = self.find_next_spot(0, 0)
        return self.solve(pieces, x, y)

    def solve(self, pieces, x ,y) -> bool:
        if all(self.used):
            return True
        for i, p in enumerate(pieces):
            if self.used[i]:
                continue
            if self.test_placement(pieces, p, i, x, y):
                return True
            if self.flipable[i]:
                if self.test_placement(pieces, flip(p), i, x, y):
                    return True
        return False

def rot90(p: np.ndarray) -> np.ndarray:
    new_p = np.zeros((p.shape[1], p.shape[0]), dtype=np.int16)
    for x in range(p.shape[0]):
        for y in range(p.shape[1]):
            new_p[p.shape[1]-1-y,x] = p[x,y]
    return new_p

def flip(p: np.ndarray) -> np.ndarray:
    new_p = p.copy()
    shape = p.shape
    for x in range(shape[0]):
        for y in range(shape[1]):
            new_p[x, y] = p[x, shape[1]-1-y]
    return new_p

def run(date: datetime, month=-1, day=-1, weekday=-1, plot=True) -> bool:
    pieces = create_pieces()

    use_month = date.month-1 if month == -1 else month
    use_day = date.day-1 if day == -1 else day
    use_weekday = date.weekday() if weekday == -1 else weekday

    board = Board([MONTHS[use_month], DAYS[use_day], WEEKDAYS[use_weekday]])
    solved = board.Solve(pieces)
    if not plot:
        return solved

    plt.imshow(board.b)
    plt.title(date.strftime('%Y-%m-%d'))
    plt.savefig(date.strftime('%Y-%m-%d'))
    plt.show()
    return solved

if __name__ == '__main__':
    today = datetime.today()
    run(today)
