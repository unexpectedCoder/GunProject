import bore
import my_parser as mpar
import materials

import os
import scipy.optimize as sciopt
import numpy as np


class MultilayBarrel:
    steel = materials.Steel([0, 0, 0])
    a21, a31, a32 = 0, 0, 0
    Delta1 = 0
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

        choice = 'new'
        while choice != 'exit':
            self.steel = materials.Steel(self.__choose_material())
            self.__set_a31()
            self.__calc_abs_tension()
            self.__calc_r1()
            self.__calc_r2()
            self.__calc_r3()
            if self.__check_sigma_eTK() is True and self.__check_hardenability() is True:
                print('\tSelected steel is suitable (enter "new", "ok" or "exit").')
                choice = input('\t>>> ')
                if choice == 'ok':
                    break
            else:
                print('\tWarning: selected steel is NOT suitable!\n'
                      '\tPlease, select other steel or enter "exit"...')
                choice = input('\t>>> ')

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
                  f"hardenability({steel['hardenability'] * 1e3} mm)")
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

    def __set_a31(self):
        print('Choose a31 = r3 / r1:')
        if self.steel.sigma < 1000:
            bounds = [2.7, 3]
        else:
            bounds = [2.4, 2.7]
        while True:
            self.a31 = float(input(f'\tFor selected steel r3 / r1 = {bounds[0]}...{bounds[1]}: '))
            if self.a31 < bounds[0] or self.a31 > bounds[1]:
                print('\tWarning: invalid value!\n\tPlease, try again...')
                continue
            break

    def __calc_abs_tension(self):
        if self.barr_bore.d < 0.76:
            self.Delta1 = 0.4 * self.barr_bore.d
        if 0.076 <= self.barr_bore.d <= 0.152:
            self.Delta1 = 0.3 * self.barr_bore.d
        if self.barr_bore.d > 0.152:
            self.Delta1 = 0.2 * self.barr_bore.d

    def __calc_r1(self):
        self.r1 = self.barr_bore.d / 2
        print(f'\t- r1, mm: {self.r1 * 1e3}')

    def __calc_r2(self):
        if self.steel.sigma >= 1000:
            while True:
                mult = float(input('\tSet multiplier for tension (1.5...1.8): '))
                if mult < 1.5 or mult > 1.8:
                    print('\tWarning: invalid value!\n\tPlease, try again...')
                    continue
                break
        else:
            mult = 1
        self.r2 = self.r1 + mult * self.Delta1
        print(f'\t- r2, mm: {self.r2 * 1e3}')
        self.a21 = self.r2 / self.r1

    def __calc_r3(self):
        self.r3 = self.a31 * self.r1
        print(f'\t- r3, mm: {self.r3 * 1e3}')
        self.a32 = self.r3 / self.r2

    def __check_sigma_eTK(self):
        if self.steel.sigma > 2 / 3 * max(self.barr_bore.p_des) * (2 * self.a31 ** 2 + 1) / (self.a31 ** 2 - 1):
            print(self.steel.sigma)
            print(2 / 3 * max(self.barr_bore.p_des) * (2 * self.a31 ** 2 + 1) / (self.a31 ** 2 - 1))
            return True
        return False

    def __check_hardenability(self):
        if self.steel.hardenability > self.r2 - self.r1 and self.steel.hardenability > self.r3 - self.r2:
            return True
        return False
