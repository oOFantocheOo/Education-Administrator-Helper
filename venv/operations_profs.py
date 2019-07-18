import pickle


def load_profs():
    return pickle.load(open("profs_file", "rb"))


def save_profs(prof_list):
    pickle.dump(prof_list, open("profs_file", "wb"))


def all_profs_info(profs):
    string = 'ID\tName\tTelephone\n'
    for pid in profs.keys():
        string += profs[pid].__str__()
        string += '\n'
    return string


def find_prof(profs, name):
    for pid in profs.keys():
        if name == profs[pid].name:
            return profs[pid]
    return None
