import my_parser
import monoblock as mb

import os


def main():
    if os.path.isdir('src') is False:
        os.mkdir('src')

    barr = mb.Monoblock('src/StartData.csv')
    barr.start_solve()
    print(barr)
    # barr.show_indicator_lines('src/', 'L', 'p',
    #                           'green', 'red', 'blue',
    #                           x_dim='м', y_dim='МПа',
    #                           bottom=0, top=550, y_step=100,
    #                           left=0, right=4, x_step=0.5,
    #                           win_name='ILines')
    barr.show_pressures()

    return 0


if __name__ == '__main__':
    main()
else:
    print('Error: no entering point!')
