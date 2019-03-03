import matplotlib.pyplot as plt
import numpy as np


def build_plot(data_dict, x_key, y_key, **kwargs):
    """
    This function builds one plot using 'pyplot'.
    :param data_dict: data dictionary with 'x' and 'y' keys
    :param x_key: an argument (for example 't')
    :param y_key: a function (for example 'L')
    :param kwargs: key arguments
    """
    x, y = [], []
    for data in data_dict:
        x.append(float(data[x_key]))
        y.append(float(data[y_key]))

    if 'win_name' in kwargs:
        plt.figure(kwargs['win_name'])
    else:
        plt.figure()
    if 'title' in kwargs:
        plt.title(kwargs['title'])
    if 'color' not in kwargs:
        plt.plot(x, y)
    else:
        plt.plot(x, y, color=kwargs['color'])
    if 'x_dim' in kwargs:
        plt.xlabel(f'${x_key}$, {kwargs["x_dim"]}')
    else:
        plt.xlabel(f'${x_key}$')
    if 'y_dim' in kwargs:
        plt.ylabel(f'${y_key}$, {kwargs["y_dim"]}')
    else:
        plt.ylabel(f'${y_key}$')
    plt.xlim(min(x))
    plt.ylim(min(y))
    plt.grid(True)

    plt.show()


def build_plots(data_dicts_list, x_key, y_key, *colors, **kwargs):
    """
    This function builds plots at common grid using 'pyplot'.
    Plots data is contained in list of dictionaries.
    :param data_dicts_list: list of data dictionaries
    :param x_key: an argument (for example 't')
    :param y_key: a function (for example 'L')
    :param colors: it is contained colors for all plots from data list
    :param kwargs: key arguments
    """
    if len(colors) != len(data_dicts_list):
        print('Warning: size of colors list != size of data list!')
        autocolors = True
    else:
        autocolors = False
    if 'win_name' in kwargs:
        plt.figure(kwargs['win_name'])
    else:
        plt.figure()
    if 'title' in kwargs:
        plt.title(kwargs['title'])

    for data_dict, color in zip(data_dicts_list, colors):
        x, y = [], []
        for data in data_dict:
            x.append(float(data[x_key]))
            y.append(float(data[y_key]))
        if autocolors is False:
            plt.plot(x, y, color=color)
        else:
            plt.plot(x, y)

    if 'x_dim' in kwargs:
        plt.xlabel(f'${x_key}$, {kwargs["x_dim"]}')
    else:
        plt.xlabel(f'${x_key}$')
    if 'y_dim' in kwargs:
        plt.ylabel(f'${y_key}$, {kwargs["y_dim"]}')
    else:
        plt.ylabel(f'${y_key}$')
    if 'right' in kwargs and 'left' in kwargs and 'x_step' in kwargs:
        plt.xlim(kwargs['left'], kwargs['right'])
        plt.xticks(np.arange(kwargs['left'], kwargs['right'] + kwargs['x_step'], kwargs['x_step']))
    elif 'left' in kwargs:
        plt.xlim(kwargs['left'])
    if 'bottom' in kwargs and 'top' in kwargs and 'y_step' in kwargs:
        plt.ylim(kwargs['bottom'], kwargs['top'])
        plt.yticks(np.arange(kwargs['bottom'], kwargs['top'] + kwargs['y_step'], kwargs['y_step']))
    elif 'bottom' in kwargs:
        plt.ylim(kwargs['bottom'])

    plt.grid()
    plt.show()


def build_plots_list(xy, xlab, ylab, *colors, **kwargs):
    """
    This function builds plots using 'pyplot' and the list as a data source.
    Every dimension of two-dimensional data list (X or Y) may be the list in its turn.
    :param xy: 2-dimensional [X; Y] list of data
    :param xlab: x-axes label text
    :param ylab: y-axes label text
    :param colors: colors of plots
    :param kwargs: key arguments
    """
    if len(xy[0]) != len(xy[1]):
        print('Error: size of X list != size of Y list!')
        exit(-1)

    if len(colors) != len(xy[0]):
        print(f'Warning: size of colors list ({len(colors)}) != size of data list ({len(xy[0])})!')
        autocolors = True
    else:
        autocolors = False
    if 'win_name' in kwargs:
        plt.figure(kwargs['win_name'])
    else:
        plt.figure()
    if 'title' in kwargs:
        plt.title(kwargs['title'])

    X, Y = xy[0], xy[1]
    for x_list, y_list, color in zip(X, Y, colors):
        if autocolors is False:
            plt.plot(x_list, y_list, color=color)
        else:
            plt.plot(x_list, y_list)

    if 'x_dim' in kwargs:
        plt.xlabel(f'${xlab}$, {kwargs["x_dim"]}')
    else:
        plt.xlabel(f'${xlab}$')
    if 'y_dim' in kwargs:
        plt.ylabel(f'${ylab}$, {kwargs["y_dim"]}')
    else:
        plt.ylabel(f'${ylab}$')
    if 'right' in kwargs and 'left' in kwargs and 'x_step' in kwargs:
        plt.xlim(kwargs['left'], kwargs['right'])
        plt.xticks(np.arange(kwargs['left'], kwargs['right'] + kwargs['x_step'], kwargs['x_step']))
    elif 'left' in kwargs:
        plt.xlim(kwargs['left'])
    if 'bottom' in kwargs and 'top' in kwargs and 'y_step' in kwargs:
        plt.ylim(kwargs['bottom'], kwargs['top'])
        plt.yticks(np.arange(kwargs['bottom'], kwargs['top'] + kwargs['y_step'], kwargs['y_step']))
    elif 'bottom' in kwargs:
        plt.ylim(kwargs['bottom'])

    plt.grid()
    plt.show()
