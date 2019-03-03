class BarrPoint:
    r1, r2, r3 = 0, 0, 0
    x = 0
    num = 0

    def __init__(self, num, r1, r2, r3, x):
        self.num = num
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.x = x

    def __str__(self):
        return f'{int(self.num)}: r1 = {round(self.r1, 3)}, '\
            f'r2 = {round(self.r2, 3)}, '\
            f'r3 = {round(self.r3, 3)}, '\
            f'x = {round(self.x, 3)}'
