import pickle


def load_classes():
    return pickle.load(open("classes_file", "rb"))


def save_classes(class_list):
    pickle.dump(class_list, open("classes_file", "wb"))


def classes_are_available(class_list, ids, weeks, period, date):
    for cid in ids:
        for w in range(30):
            if weeks[w] in ['1', 1]:
                if not class_list[cid].schedule[w].is_available(period, date):
                    return False
    return True


def change(class_list, class_id, weeks, period, date, content):
    for w in range(30):
        if weeks[w] in [1, '1']:
            class_list[class_id].schedule[w].change_one_period(period, date, content)
