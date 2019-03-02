import bore
import my_parser as mpar
import materials

import os
import scipy.optimize as sciopt
import numpy as np


class MultilayBarrel:
    steel = materials.Steel([0, 0, 0])
    r1, r2, r3 = 0, 0, 0

    # Public functions
    def __init__(self, data_path):
        self.barr_bore = bore.BarrelBore(data_path)

    def __str__(self):
        return 'MULTI-LAYERED BARREL:\n' + str(self.barr_bore)

    def design(self):
        if os.path.isdir('multi_layered') is False:
            os.mkdir('multi_layered')

        self.barr_bore.build_graphs()
        choice = input('Show indicator lines? (+/-): ')
        if choice == '+':
            self.barr_bore.show_graphs()
        self.steel = materials.Steel(self.__choose_material())

    def __choose_material(self):
        print('Choosing of barrel material\n\tSteels list:')
        steels = self.init_steels()
        for steel in steels:
            steel['sigma'] = float(steel['sigma'])
            steel['hardenability'] = float(steel['hardenability'])
            print('\t-', steel)
        print('\t*** Warning: for all steels E = 0.2 MPa by default ***')
        print('\tFor this steels:')
        for steel in steels:
            print(f"\t- {steel['name']}: sigma({steel['sigma']} MPa) "
                  f"hardenability({steel['hardenability']} mm)")
        while True:
            name = input('\tChoose steel (by name): ').upper()
            sigma = 0
            hard = 0
            is_exist = False
            for steel in steels:
                if name == steel['name']:
                    sigma = steel['sigma']
                    hard = steel['hardenability']
                    is_exist = True
                    break
            if is_exist is True:
                break
            print('Warning: no such steel in list! Please, try again...')
        return name, sigma, hard

    @staticmethod
    def init_steels():
        res = mpar.read_xml_tree('src/steels.xml')
        steels = res[::2]
        data = res[1::2]
        for s, d in zip(steels, data):
            s.update(d)
        return steels
