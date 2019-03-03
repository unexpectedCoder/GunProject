from xml.etree import ElementTree
import csv


def read_txt_with_fieldnames(file, delim):
    """
    This function reads data from TXT file with forming field of names
    for further converting to CSV file.
    :param path: TXT file path
    :param delim: delimiter between data elements
    :return: data and field of names
    """
    data = []
    fieldnames = file.readline().split(delim)
    fieldnames[-1] = fieldnames[-1][:-1]
    for line in file:
        new_line = line.split(delim)
        new_line[-1] = new_line[-1][:-1]
        buf = []
        for x in new_line:
            buf.append(float(x))
        data.append(dict(zip(fieldnames, buf)))
    return data, fieldnames


def read_csv_dict(path, delim):
    """
    This function reads data from CSV file to RAM in dictionary view.
    :param path: CSV file path
    :param delim: delimiter between data elements in CSV file
    :return: list of dictionaries
    """
    dicts_list = []
    with open(path, 'r') as file:
        reader = csv.DictReader(file, delimiter=delim)
        for dict in reader:
            dicts_list.append(dict)
    return dicts_list


def read_csv_light(path, delim):
    """
    This function is the light version of read_csv_dict() function.
    It reads CSV data to RAM in dictionary view
    and uses update() function to combine dictionaries
    from this function and from CSV DictReader.
    :param path: CSV file path
    :param delim: delimiter between data elements in CSV file
    :return: dictionary
    """
    dic = {}
    with open(path, 'r') as file:
        reader = csv.DictReader(file, delimiter=delim)
        for d in reader:
            dic.update(d)
    return dic


def write_csv(path, data, delim='\t'):
    with open(path, 'w') as file:
        writer = csv.writer(file, delimiter=delim)
        for row in data:
            writer.writerow(row)


def write_csv_dict(path, fieldnames, data, delim='\t'):
    with open(path, 'w') as file:
        writer = csv.DictWriter(file, delimiter=delim, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def read_xml_tree(path):
    """
    This function reads XML file to RAM in ElementTree view.
    :param path: XML file path
    :return: list of dictionaries of XML node objects (attributes)
    """
    tree = ElementTree.parse(path)
    root = tree.getroot()
    return traverse_nodes(root)


def traverse_nodes(node, i=0, dicts=[], **kwargs):
    """
    Recursive function to read all XML nodes to RAM.
    :param node: current node
    :param i: starting multiplier of tabulation
    :param dicts: current list of dictionaries
    :return: list of dictionaries of XML node objects (attributes)
    """
    space = 4 * ' '
    if 'space' in kwargs:
        space = kwargs['space'] * ' '
    if 'print' in kwargs:
        for child in node:
            print(i*space, child.tag, child.attrib)
            dicts.append(child.attrib)
            traverse_nodes(child, i + 1, dicts)
    else:
        for child in node:
            dicts.append(child.attrib)
            traverse_nodes(child, i + 1, dicts)
    return dicts
