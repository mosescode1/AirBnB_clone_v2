#!/usr/bin/python3


def dict_converter(values):
    temp_dict = {}
    values = values[1:]
    # print(values)
    for val in values:
        dict_val = val.split('=')
        key = dict_val[0]
        value = dict_val[1]
        temp_dict.update({key: value})
    new = val_returner(temp_dict)
    return new


def val_returner(value):
    temp2 = {}
    for key, val in value.items():
        if val.startswith('"'):
            temp2[key] = val.rstrip('"').lstrip('"')
            if "_" in temp2[key]:
                temp2[key] = temp2[key].replace("_", " ")
        elif val.count("."):
            try:
                temp2[key] = float(val)
            except Exception:
                pass
        elif val.isdigit():
            temp2[key] = int(val)
        # print(temp2[key], '===>', type(temp2[key]))

    return temp2
