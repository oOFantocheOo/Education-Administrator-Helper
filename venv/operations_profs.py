import pickle

import Prof
import openpyxl as xl


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


# Extract info from the first worksheet in profs.xlsx
# column1: name; column2: ID
def update_profs(profs):
    workbook = xl.load_workbook('profs.xlsx')
    worksheet = workbook[workbook.sheetnames[0]]

    i = 1
    while worksheet['A' + str(i)].value:
        name = str(worksheet['A' + str(i)].value)
        id = str(worksheet['B' + str(i)].value)
        profs[id] = Prof.Prof(id, name)
        i += 1


def list_prof_ids_to_names(profs, ids):
    str = ''
    for i in ids:
        str += profs[i].name + ' '
    return str


def profs_are_available(profs, ids, weeks, period, date):
    for pid in ids:
        for w in range(30):
            if weeks[w] in ['1', 1]:
                if not profs[pid].schedule[w].is_available(period, date):
                    return False
    return True


def change(profs, prof_id, weeks, period, date, content):
    for w in range(30):
        if weeks[w] in [1, '1']:
            profs[prof_id].schedule[w].change_one_period(period, date, content)
