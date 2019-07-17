import collections
import pickle
import operations_gui as og


def load_profs():
    return pickle.load(open("profs_file", "rb"))


def save_profs(prof_list):
    pickle.dump(prof_list, open("profs_file", "wb"))


def remove_prof_by_name(prof_list, name):
    prof_dict_by_name = collections.defaultdict(list)
    for prof in prof_list:
        prof_dict_by_name[prof.name].append(prof)
    if name not in prof_dict_by_name:
        print("Prof not found")
        return
    if len(prof_dict_by_name[name]) > 1:  # to be continued
        print("Multiple profs found\nOperation did NOT finish")
        return
    else:
        for i in range(len(prof_list)):
            if prof_list[i].name == name:
                save_profs(prof_list)
                return prof_list.pop(i)


def all_profs_info():
    profs = load_profs()
    string = 'ID\tName\tTelephone\n'
    for prof in profs:
        string += prof.__str__()
        string += '\n'
    return string


def find_prof(name):
    profs = load_profs()
    for i in profs:
        if name == i.name:
            return i
    return None
