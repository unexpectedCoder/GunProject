import bore
import my_parser as mpar
import materials
import my_file_converter as fconv
import my_types as mtype

import os
import numpy as np


class MultilayBarrel:
    steel = materials.Steel([0, 0, 0])
    a21, a31, a32 = [], [], []
    Delta1 = 0
    r1, r2, r3 = 0, 0, 0
    eta = 0
    points = []
    T1 = []
    p_act = []
    x = []
    p_c2add = []

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
            a31 = self.__set_a31()
            self.__calc_barr_thick()
            self.__calc_r1()
            self.__calc_r2()
            self.__calc_r3(a31)
            if self.__check_sigma_eTK(a31) is True and self.__check_hardenability() is True:
                print('\tSelected steel is suitable (enter "new", "ok" or "exit").')
                self.__calc_r_end()
                choice = input('\t>>> ')
                if choice == 'ok':
                    break
            else:
                print('\tWarning: selected steel is NOT suitable!\n'
                      '\tPlease, select other steel or enter "exit"...')
                choice = input('\t>>> ')
        if choice == 'ok':
            self.__read_geometry()
            self.__set_ref_tension()
            self.__calc_T1()
            self.__calc_possible_resist()
            self.__calc_casing()
            self.barr_bore.show_graphs([[self.p_act, self.x], [self.p_c2add, self.x[:-5]]])

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
            a31 = float(input(f'\tFor selected steel r3 / r1 = {bounds[0]}...{bounds[1]}: '))
            if a31 < bounds[0] or a31 > bounds[1]:
                print('\tWarning: invalid value!\n\tPlease, try again...')
                continue
            break
        return a31

    def __calc_barr_thick(self):
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

    def __calc_r3(self, a31):
        self.r3 = a31 * self.r1
        print(f'\t- r3, mm: {self.r3 * 1e3}')

    def __check_sigma_eTK(self, a31):
        if self.steel.sigma > 2 / 3 * max(self.barr_bore.p_des) * (2 * a31 ** 2 + 1) / (a31 ** 2 - 1):
            print(self.steel.sigma)
            print(2 / 3 * max(self.barr_bore.p_des) * (2 * a31 ** 2 + 1) / (a31 ** 2 - 1))
            return True
        return False

    def __check_hardenability(self):
        if self.steel.hardenability > self.r2 - self.r1 and self.steel.hardenability > self.r3 - self.r2:
            return True
        return False

    def __calc_r_end(self):
        r_end = self.barr_bore.d / 2 * np.sqrt((3 * self.steel.sigma + 2 * self.barr_bore.p_des[-1])\
                                               / (3 * self.steel.sigma - 4 * self.barr_bore.p_des[-1]))
        print(f'\tRadius at "l" point, mm: {round(r_end * 1e3, 0)}')

    def __read_geometry(self):
        fconv.txt_to_csv('multi_layered/geometry')
        data = mpar.read_csv_dict('multi_layered/geometry.csv', '\t')
        print(f'data = {data}')
        for d in data:
            point = mtype.BarrPoint(round(float(d['num']), 0),
                                    float(d['d1']) * 1e-3 / 2,
                                    float(d['d2']) * 1e-3 / 2,
                                    float(d['d3']) * 1e-3 / 2,
                                    float(d['x']) * 1e-3)
            self.a21.append(point.r2 / point.r1)
            self.a31.append(point.r3 / point.r1)
            self.a32.append(point.r3 / point.r2)
            self.x.append(point.x)
            self.points.append(point)

    def __set_ref_tension(self):
        while True:
            self.eta = float(input('\tSet relative tension (0.001...0.002): '))
            if self.eta < 0.001 or self.eta > 0.002:
                print('\tWarning: invalid value!\n\tPlease, try again...')
                continue
            break

    def __calc_T1(self):
        for i in range(len(self.points)):
            T1 = self.steel.E * self.eta\
                 * (self.a31[i] ** 2 - self.a21[i] ** 2) / (self.a31[i] ** 2 - 1)
            self.T1.append(T1)

    def __calc_possible_resist(self):
        for i in range(len(self.points)):
            p_1tau = 1.5 * (self.steel.sigma + self.T1[i])\
                     * (self.a31[i] ** 2 - 1) / (2 * self.a31[i] ** 2 + 1)
            p_1r = 1.5 * (self.steel.sigma + self.T1[i] / 3)\
                   * (self.a31[i] ** 2 - 1) / (2 * self.a31[i] ** 2 - 1)
            self.p_act.append(min(p_1tau, p_1r))

    def __calc_casing(self):
        for i in range(len(self.points) - 5):
            p_c2tau = 1.5 * self.steel.sigma\
                      * (self.a32[i] ** 2 - 1) / (2 * self.a32[i] ** 2 + 1)
            p_2 = 1.5 * (self.eta * self.steel.E * (self.a21[i] ** 2 - 1) * (self.a32[i] ** 2 - 1))\
                  / (3 * (self.a31[i] ** 2 - 1))
            p__2add = p_c2tau - p_2
            self.p_c2add.append(p__2add * (self.a31[i] ** 2 - 1) / (self.a32[i] ** 2 - 1))
