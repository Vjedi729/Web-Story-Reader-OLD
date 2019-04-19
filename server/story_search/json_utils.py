def list_to_json_list(list):
    myjson = '[\n'
    for item in list:
        myjson += "\n" + item.toJson() + ","
    myjson = myjson[:-1] + '\n]'
    return myjson
