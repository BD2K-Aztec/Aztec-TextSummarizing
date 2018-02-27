from collections import defaultdict
def parse_entry(line):
    line = line.strip().split(" ")
    key = line[0]
    values = [float(x) for x in line[1:]]
    return key, values


def load_pretrain(file_name):
    dic = defaultdict(list)
    with open(file_name, "r") as fin:
        lines = fin.readlines()

    for line in lines:
        key, value = parse_entry(line)
        dic[key] = value
    del lines
    return dic


if __name__ == "__main__":
    name = "../glove_pre_train/glove.6B.50d.txt"

    print("Loading dictionary from the file ...")
    dic = load_pretrain(name)

    i = 0
    for key, value in dic.items():
        if i > 10:
            break
        print(key, value)
        i += 1
