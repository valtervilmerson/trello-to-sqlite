import json


class WriteJson:
    @staticmethod
    def write(arq_name, data):
        for i in data:
            item = json.dumps(i, indent=4)
            print('i: ', i)
            with open(arq_name + ".json", "a") as outfile:
                outfile.write(item + ',')
