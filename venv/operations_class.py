import pickle


def load_classes():
    return pickle.load(open("classes_file", "rb"))


def save_classes(class_list):
    pickle.dump(class_list, open("classes_file", "wb"))

