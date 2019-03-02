class Steel:
    E = 0.2     # By default, MPa

    def __init__(self, data_list):
        self.name = data_list[0]
        self.sigma = data_list[1]
        self.hardenability = data_list[2]

    def __str__(self):
        return f'Steel {self.name}:\n'\
               + f'\tsigma, MPa: {self.sigma}'\
               + f'\thardenability, m: {self.hardenability}'\
               + f'\tE, MPa: {self.E}\n'
