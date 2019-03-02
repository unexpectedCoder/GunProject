import my_parser as mpar
import plot_builder as pltb
import materials

import os
from math import *
import scipy.optimize as sciopt
import numpy as np


class MultilayBarrel:
    # Variables
    Wk = 0
    l_main_cone = 0
    l_trans_cone = 0
    l_tail_cone = 0
    l_thrust_cone = 0
    d_main = 0
    d_trans = 0
    d_tail = 0
    d_thrust = 0
    # Pressure at the bottom of the projectile...
    pb15 = []
    pb50 = []
    pb_50 = []
    pb_max = 0
    # ...and projectile path
    L15 = []
    L50 = []
    L_50 = []

    p_cham_max = 0
    L_cham_max = 0
    # For envelope curve
    p_env = []
    L = []
    # For desired resistance
    p_des = []
    L_res = []
    # Barrel material
    steel = materials.Steel([0, 0, 0])
    # Geometry
    r1 = []
    r2 = []

    # Public functions
    def __init__(self, path_start_data):
        data = mpar.read_csv_light(path_start_data, '\t')

        self.d = float(data['d'])
        self.q = float(data['q'])
        self.Vd = float(data['Vd'])
        self.omega = float(data['w'])
        self.W0 = float(data['W0'])
        self.Ld = float(data['Ld'])
        self.hi = float(data['hi'])
        self.phi1 = float(data['phi1'])
        self.ns = float(data['ns'])
        self.lmd = float(data['lambda'])  # lambda - rollback length
        self.Delta = float(data['Delta'])

        self.K = self.phi1
        self.S = 0.25 * pi * self.d ** 2 * self.ns
        self.L0 = self.W0 / self.S
        self.Lk = self.L0 / self.hi

        self.h = 0
        self.d1 = self.d
        self.W_main_cone = self.Wk

        self.K_main_cone = 0
        self.K_trans_cone = 0
        self.K_tail_cone = 0
        self.K_thrust_cone = 0

    def __str__(self):
        return 'Monoblock barrel:\n' \
               + f'\td = {self.d} mm\n\tq = {self.q} kg\n' \
               + f'\tVd = {self.Vd} m/s\n\tLd = {self.Ld} m\n' \
               + f'\tomega = {self.omega} kg\n\tDelta = {self.Delta} kg/m^3\n' \
               + f'\tW0 = {self.W0} m^3\n\tlambda = {self.lmd} m\n' \
               + f'\tL0 = {round(self.L0, 3)} m\n\tLk = {round(self.Lk, 3)} m\n' \
               + f'\tK = {self.K}\n\tns = {self.ns}\n\thi = {self.hi}\n' \
               + f'\th = {self.h * 1e3} mm\n' \
               + f'\tCalculated geometry:\n' \
               + f'\td_main, m: {self.d_main}\tl_main, m: {self.l_main_cone}\n' \
               + f'\td_trans, m: {self.d_trans}\tl_trans, m: {self.l_trans_cone}\n' \
               + f'\td_tail, m: {self.d_tail}\tl_tail, m: {self.l_tail_cone}\n' \
               + f'\td_thrust, m: {self.d_thrust}\tl_thrust, m: {self.l_thrust_cone}'

    def solve(self):
        pass

    @staticmethod
    def show_ballist_avrg_press(folder='', x_key='t', y_key='p',
                                *colors, **kwargs):
        dicts = []
        path = folder + 'ILine15.csv'
        dicts.append(mpar.read_csv_dict(path, '\t'))
        path = folder + 'ILine50.csv'
        dicts.append(mpar.read_csv_dict(path, '\t'))
        path = folder + 'ILine_50.csv'
        dicts.append(mpar.read_csv_dict(path, '\t'))
        pltb.build_plots(dicts, x_key, y_key, *colors, **kwargs)

    def show_pressures(self):
        p_list = []
        p_list.append(self.pb15)
        p_list.append(self.pb50)
        p_list.append(self.pb_50)
        p_list.append(self.p_env)
        p_list.append(self.p_des)

        L_list = []
        L_list.append(self.L15)
        L_list.append(self.L50)
        L_list.append(self.L_50)
        L_list.append(self.L)
        L_list.append(self.L)

        pltb.build_plots_list([L_list, p_list], 'L', 'p',
                              'green', 'red', 'blue', 'gray', 'orange',
                              x_dim='м', y_dim='МПа',
                              x_step=0.5, y_step=50,
                              win_name='ILines')

    def __set_depth_cut(self):
        if self.Vd > 800:
            hmin = 0.02 * self.d
            hmax = 0.04 * self.d
        else:
            hmin = 0.01 * self.d
            hmax = 0.015 * self.d
        print(f'Depth of cut is {round(hmin * 1e3, 3)}...{round(hmax * 1e3, 3)} mm')
        while True:
            self.h = float(input('\t- set final value: ')) * 0.001
            if hmin <= self.h <= hmax:
                break
            print('Error: invalid value (< or > than boundaries)!\nPlease, try again...')

    def __set_cones(self):
        print('Set cones for smooth tank barrel:')
        while True:
            self.K_main_cone = float(input('\t- main cone (1:50...1:100): 1/')) ** (-1)
            if 1 / 100 <= self.K_main_cone <= 1 / 50:
                break
            print('Warning: invalid cone value! Please, try again...')
        print('\t- transition cone will be calculated automatically')
        print('\t- tail cone is set by default: 1/200')
        self.K_tail_cone = 1 / 200
        while True:
            self.K_thrust_cone = float(input('\t- thrust cone (1:20...1:40): 1/')) ** (-1)
            if 1 / 40 <= self.K_thrust_cone <= 1 / 20:
                break
            print('Warning: invalid cone value! Please, try again...')

    def __set_lengths(self):
        print('Chamber\'s parts lenghts:')
        choice = input('\t- set by default (for MT-12)? (+/-): ')
        if choice == '+':
            self.l_main_cone = 0.605  # From guide book "MT-12"
            self.l_trans_cone = 0.045  # ...
            self.l_tail_cone = 0.315  # ...
            self.l_thrust_cone = 0.026  # ...
        else:
            while True:
                self.l_main_cone = float(input('\t- length of main cone, m: '))
                if self.l_main_cone <= 0:
                    print('Warning: invalid length value! Please, try again...')
                    continue
                break
            while True:
                self.l_trans_cone = float(input('\t- length of transition cone, m: '))
                if self.l_trans_cone <= 0:
                    print('Warning: invalid length value! Please, try again...')
                    continue
                break
            while True:
                self.l_tail_cone = float(input('\t- length of tail cone, m: '))
                if self.l_tail_cone <= 0:
                    print('Warning: invalid length value! Please, try again...')
                    continue
                break
            while True:
                self.l_thrust_cone = float(input('\t- length of thrust cone, m: '))
                if self.l_thrust_cone <= 0:
                    print('Warning: invalid length value! Please, try again...')
                    continue
                break

    def __calc_diameters(self):
        self.d_thrust = round(self.d + self.K_thrust_cone * self.l_thrust_cone, 3)
        self.d_tail = round(self.d_thrust + self.K_tail_cone * self.l_tail_cone, 3)
        W_sleeve_wall = 0.2 * 0.005 * 2 * pi * self.d  # Approximation
        self.Wk = self.W0 + W_sleeve_wall
        W = self.Wk
        L = self.l_main_cone
        K = self.K_main_cone

        def eq_sys(x):
            return [x[1] + 0.5 * x[0] - np.sqrt(-0.75 * x[0] ** 2 + 12 * W / (pi * L)),
                    x[1] - x[0] - K * L]

        diams = sciopt.root(eq_sys, np.array([0.12, 0.15]))
        self.d_trans = round(diams.x[0], 3)
        self.d_main = round(diams.x[1], 3)

    def _calc_bottom_press(self):
        path = 'src/ILine15.csv'
        data = mpar.read_csv_dict(path, '\t')
        for d in data:
            d['p'] = float(d['p'])
            d['p'] /= (1 + 1 / 3 * self.omega / (self.phi1 * self.q))
            d['p'] = round(d['p'], 3)
            self.pb15.append(d['p'])
        path = 'src/ILine50.csv'
        data = mpar.read_csv_dict(path, '\t')
        for d in data:
            d['p'] = float(d['p'])
            d['p'] /= (1 + 1 / 3 * self.omega / (self.phi1 * self.q))
            d['p'] = round(d['p'], 3)
            self.pb50.append(d['p'])
        path = 'src/ILine_50.csv'
        data = mpar.read_csv_dict(path, '\t')
        for d in data:
            d['p'] = float(d['p'])
            d['p'] /= (1 + 1 / 3 * self.omega / (self.phi1 * self.q))
            d['p'] = round(d['p'], 3)
            self.pb_50.append(d['p'])

    def __make_length_list(self):
        path = 'src/ILine15.csv'
        data = mpar.read_csv_dict(path, '\t')
        for d in data:
            d['L'] = round(float(d['L']), 3)
            self.L15.append(d['L'])
        path = 'src/ILine50.csv'
        data = mpar.read_csv_dict(path, '\t')
        for d in data:
            d['L'] = round(float(d['L']), 3)
            self.L50.append(d['L'])
        path = 'src/ILine_50.csv'
        data = mpar.read_csv_dict(path, '\t')
        for d in data:
            d['L'] = round(float(d['L']), 3)
            self.L_50.append(d['L'])

    def __calc_max_chamber_p_L(self):
        self.pb_max, index = self.find_max(self.pb50)
        p_max = self.pb_max
        L_max = self.L50[index]
        self.p_cham_max = p_max * (1 + 0.5 * self.omega / (self.phi1 * self.q))
        self.L_cham_max = L_max + 2 * self.d

    @staticmethod
    def find_max(data):
        index = 0
        res = data[index]
        for i in range(1, len(data)):
            if data[i] > res:
                res = float(data[i])
                index = i
            else:
                break
        return res, index

    def __calc_envelope_curve(self):
        dp = self.pb_max * self.omega / (self.phi1 * self.q)
        a = self.l_main_cone + self.l_trans_cone + self.l_tail_cone + self.l_thrust_cone
        x = 0
        x_end = self.L_cham_max + a
        while x < x_end:
            self.p_env.append(self.p_cham_max - (self.p_cham_max - self.pb_max) * x ** 2 / x_end ** 2)
            self.L.append(x - a)
            x += 0.001
        x -= a
        i = 0
        while self.L50[i] < x:
            i += 1
        adder = 0
        while i < len(self.pb50):
            self.p_env.append((1.02 + adder) * self.pb50[i])
            self.L.append(self.L50[i])
            adder += 0.0003
            i += 1

    def __calc_desired_resistance(self):
        for x, p in zip(self.L, self.p_env):
            self.p_des.append(p * self.n(x))

    # Safety factor
    def n(self, x):
        """
        Safety factor function for smooth tank barrel.
        :param x: current coordinate in barrel chanel
        :return: safety factor
        """
        if x < 0:
            return 1
        if 0 <= x <= self.L_cham_max:
            return 1.2
        if x > self.L_cham_max:
            return 1.2 + 0.7 * (x - self.L_cham_max) / (self.L[-1] - self.L_cham_max)

    def __choose_material(self):
        print('Choosing of barrel material\n\tSteels list:')
        steels = self.__init_steels()
        for steel in steels:
            steel['sigma'] = float(steel['sigma'])
            steel['hardenability'] = float(steel['hardenability'])
            print('\t-', steel)

        print(f'\tCondition: p_chanel_max = {round(self.p_cham_max)} MPa <= (0.4...0.6)*sigma')
        print('\tFor this steels:')
        for steel in steels:
            ok = False
            if 0.6 * steel['sigma'] >= self.p_cham_max:
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