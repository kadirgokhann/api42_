from src.api42.all_moduls import *


def _write_json(self, data, filename=""):
    if filename == "":
        filename = self.adress[3:]+".json"
    filename = re.sub(r"[/]", "_", filename)
    filename = str(self.dir_path)+"/fetched_data/" + filename
    with open(filename, "w") as outfile:
        data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
        outfile.write(data)


def _update_json(self, data):
    with open(cfg.keys_path, "r+") as keysfile:
        file_data = json.load(keysfile)
        file_data["token"] = data
        keysfile.seek(0)
        json.dump(file_data, keysfile, indent=4)


def _check(self, string: str):
    if string[-1] == "\n":
        string = string[:-1]
    return string


def _range_to_kv(self, string: str):
    # check key value from time=min,max
    # return key, min, max
    if string.count(",") != 1 or string.count("=") != 1 or string.count(" ") != 0:
        return "range must be in time=min,max format", None
    key = ""
    min = ""
    max = ""
    count = 0
    for i in range(len(string)):
        if string[i] == "=":
            key = string[:i]
            count = i
            break
    for i in range(count, len(string)):
        if string[i] == ",":
            min = string[count+1:i]
            count = i
            break
    max = string[count+1:len(string)]
    return key, f"{min},{max}"
