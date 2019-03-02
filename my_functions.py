def find_max(data):
    """
    This function searches max element with it's index in input list.
    :param data: input list (array)
    :return: max element and it's index
    """
    index = 0
    res = data[index]
    for i in range(1, len(data)):
        if data[i] > res:
            res = float(data[i])
            index = i
        else:
            break
    return res, index


def find_index(arr, val):
    """
    This function searches index of element in input array (list) that is the nearest to input value.
    :param arr: input list (array)
    :param val: the search target value
    :return: index of the nearest value in list
    """
    index = 0
    min_differ = abs(arr[0] - val)
    for i in range(1, len(arr)):
        if abs(arr[i] - val) < min_differ:
            min_differ = abs(arr[i] - val)
            index = i
    return index
