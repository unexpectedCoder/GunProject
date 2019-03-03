import csv
import my_parser


def txt_to_csv(path, **kwargs):
    """
    This function creates CSV file from TXT file having similar structure.
    :param path: source text file's path (without resolution)
    """
    with open(path + '.txt', 'r') as ftxt:
        if 'skip_first' in kwargs:
            first_str = ftxt.readline()
        else:
            first_str = ''
        if 'show_first' in kwargs:
            print(first_str)
        if 'delim' in kwargs:
            delim = kwargs['delim']
        else:
            delim = '\t'
        data, fieldnames = my_parser.read_txt_with_fieldnames(ftxt, delim)
    write_csv_dict(path + '.csv', fieldnames, data, delim)


def write_csv_dict(path, fieldnames, data, delim):
    """
    Auxiliary function. Used from other functions of the module.
    For example, from txt_to_csv().
    """
    with open(path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delim)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
