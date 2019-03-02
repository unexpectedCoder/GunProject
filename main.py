import monoblock as mono

import os


def main():
    if os.path.isdir('src') is False:
        os.mkdir('src')

    barr = mono.Monoblock('src/StartData.csv')
    barr.design()
    print(barr)

    return 0


if __name__ == '__main__':
    main()
else:
    print('Error: no entering point!')
