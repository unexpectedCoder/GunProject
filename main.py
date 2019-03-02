import monoblock as mono
import multilay_barrel as multi

import os


def main():
    if os.path.isdir('src') is False:
        os.mkdir('src')

    choice = input('Design monobloc barrel? (+/-): ')
    if choice == '+':
        barr = mono.Monoblock('src/StartData.csv')
        barr.design()
        print(barr)
        del barr
    choice = input('Design multi-layered barrel? (+/-): ')
    if choice == '+':
        barr = multi.MultilayBarrel('src/StartData.csv')
        barr.design()
        print(barr)
        del barr

    return 0


if __name__ == '__main__':
    main()
else:
    print('Error: no entering point!')
