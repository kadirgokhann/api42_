from src.api42 import API42
from src.api42.all_moduls import *


def print_json(json_):
    print(json.dumps(json_, indent=4))


api = API42(49)
# print(api.get_accreditations(range="created_at=2022-10-03T06:42:00.000Z,2023-01-03T06:42:00.000Z")[0].cursus_id)

# How to request simply
response = api.request("get", "/v2/users", params={})

quit(1)


class th(Thread):
    def __init__(self, id, min, max, ):
        Thread.__init__(self)
        self.id = id
        self.min = min
        self.max = max

    def run(self):
        with tqdm(total=100) as pbar:
            while self.min < self.max:
                self.min += 1
                time.sleep(0.1)
                pbar.update(1)
                pbar.set_description("Processing th")


ths = []
for i in range(10):
    ths.append(th(i, 0, 100))
for i in ths:
    i.start()
for i in ths:
    i.join()
