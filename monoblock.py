import my_parser as mpar
import bore
import materials
import my_functions as mfuncs

import os
import numpy as np


class Monoblock:
    """
    This class implements the calculation of the monoblock barrel.
    """
    # Barrel material
    steel = materials.Steel([0, 0, 0])
    # Geometry
    r1 = []
    r2 = []

    # Public functions
    def __init__(self, data_path):
        self.barr_bore = bore.BarrelBore(data_path)

    def __str__(self):
        return 'MONOBLOCK BARREL:\n' + str(self.barr_bore)

    def design(self):
        """
        This is the main function of this class.
        :return: nothing
        """
        if os.path.isdir('monoblock') is False:
            os.mkdir('monoblock')

        self.barr_bore.build_graphs()
        choice = input('Show indicator lines? (+/-): ')
        if choice == '+':
            self.barr_bore.show_graphs()

        while True:
            self.steel = materials.Steel(self.__choose_material())
            self.__calc_thickness()
            choice = ''
            if self.__is_hardenability() is True:
                print('\tSelected steel is suitable.')
            else:
                print(f'\tSelected steel is not suitable. r2, m: {self.r2}')
            choice = input('>>> your choice (ok, new, exit): ')
            if choice == 'ok':
                break
            elif choice == 'new':
                continue
            else:
                self.steel = materials.Steel([0, 0, 0])
                break
        if self.steel.sigma != 0:
            print(f'Your selected steel: {self.steel}')
        else:
            print('It is impossible to design monoblock barrel.\n'
                  'You can use module for designing multi-layered barrel...')

    def __choose_material(self):
        print('Choosing of barrel material\n\tSteels list:')
        steels = self.__init_steels()
        for steel in steels:
            steel['sigma'] = float(steel['sigma'])
            steel['hardenability'] = float(steel['hardenability'])
            print('\t-', steel)
        print(f'\tCondition: p_chanel_max = {round(self.barr_bore.p_bore_max)} MPa <= (0.4...0.6)*sigma')
        print('\tFor this steels:')
        for steel in steels:
            ok = False
            if 0.6 * steel['sigma'] >= self.barr_bore.p_bore_max:
                ok = True
            print(f"\t- {steel['name']}: "
                  f"sigma = {0.4 * steel['sigma']}...{0.6 * steel['sigma']} MPa"
                  f" ({ok})")
        while True:
            name = input('\tChoose steel (by name): ')
            sigma = 0
            hard = 0
            ok = False
            for steel in steels:
                if name == steel['name']:
                    sigma = steel['sigma']
                    hard = steel['hardenability']
                    ok = True
                    break
            if ok is True:
                break
            print('Warning: no such steel in list! Please, try again...')
        while True:
            share = float(input('\tSet share of steel sigma: '))
            if 0.4 <= share <= 0.6:
                break
            print('Warning: invalid length value! Please, try again...')
        return name, share * sigma, hard

    def __init_steels(self):
        res = mpar.read_xml_tree('src/steels.xml')
        steels = res[::2]
        data = res[1::2]
        for s, d in zip(steels, data):
            s.update(d)
        return steels

    def __calc_thickness(self):
        self.r1 = [self.barr_bore.d_main / 2,
                   self.barr_bore.d / 2,
                   self.barr_bore.d / 2,
                   self.barr_bore.d / 2]
        indexes = [0,
                   mfuncs.find_index(self.barr_bore.L, 0),
                   mfuncs.find_index(self.barr_bore.L, self.barr_bore.L_bore_max),
                   len(self.barr_bore.L) - 1]
        self.r2 = []
        for r, i in zip(self.r1, indexes):
            if 3 * self.steel.sigma - 4 * self.barr_bore.p_des[i] > 0:
                self.r2.append(round(r * np.sqrt((3 * self.steel.sigma + 2 * self.barr_bore.p_des[i]) /
                                                 (3 * self.steel.sigma - 4 * self.barr_bore.p_des[i])), 3))
            else:
                self.r2.append(0)

    def __is_hardenability(self):
        for r1, r2 in zip(self.r1, self.r2):
            if r2 - r1 > self.steel.hardenability or r2 - r1 < 0:
                return False
        return True

    def __write_geometry_txt(self, path):
        with open(path, 'w') as file:
            file.write('Geometry of monoblock barrel:\n')
            file.write(f'd, mm: {self.barr_bore.d * 1e3}\n'
                       f'd_main, mm: {self.barr_bore.d_main * 1e3}\t'
                       f'l_main, mm: {self.barr_bore.l_main_cone * 1e3}\n'
                       f'd_trans, mm: {self.barr_bore.d_trans * 1e3}\t'
                       f'l_trans, mm: {self.barr_bore.l_trans_cone * 1e3}\n'
                       f'd_tail, mm: {self.barr_bore.d_tail * 1e3}\t'
                       f'l_tail, mm: {self.barr_bore.l_tail_cone * 1e3}\n'
                       f'd_thrust, mm: {self.barr_bore.d_thrust * 1e3}\t'
                       f'l_thrust, mm: {self.barr_bore.l_thrust_cone * 1e3}\n')
