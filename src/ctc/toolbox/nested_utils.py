import typing


K = typing.TypeVar('K')
V = typing.TypeVar('V')


def list_of_dicts_to_dict_of_lists(
    list_of_dicts: list[dict[K, V]],
) -> dict[K, list[V]]:
    """convert list of dicts into dict of lists

    uses union of all keys across all dicts
    - any dicts that have missing values will use a fill value (e.g. 0 for ints)
    """

    # gather all keys
    all_keys = {
        each_key for each_dict in list_of_dicts for each_key in each_dict.keys()
    }

    # get dtype for fill value
    found = False
    for each_dict in list_of_dicts:
        for value in each_dict.values():
            dtype = type(value)
            found = True
            break
        if found:
            break

    # initialize lists
    dict_of_lists: dict[K, list[V]] = {}
    for key in all_keys:
        dict_of_lists[key] = []

    # build lists
    for each_dict in list_of_dicts:
        for key in all_keys:
            dict_of_lists[key].append(each_dict.get(key, dtype()))

    return dict_of_lists
