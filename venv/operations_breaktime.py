import pickle


def load_breaktime():
    return pickle.load(open("breaktime_file", "rb"))


def save_breaktime(breaktime_file):
    pickle.dump(breaktime_file, open("breaktime_file", "wb"))

