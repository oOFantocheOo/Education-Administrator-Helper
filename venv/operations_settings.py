import pickle


def load_settings():
    return pickle.load(open("settings_file", "rb"))


def save_settings(settings):
    pickle.dump(settings, open("settings_file", "wb"))

