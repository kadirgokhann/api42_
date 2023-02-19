from src.api42.all_moduls import *


class API42:
    "This is the doc"

    def __init__(self, campus_id: int):
        self.results = []
        self.campus_id = campus_id
        self.dir_path = os.path.dirname(os.path.realpath(__file__))+"/../../"
        self.token = self.get_token()
        self.adress = ""
        self.whole_data = []

    def get_token(self):
        t1 = datetime.now()
        date_str = cfg.getTokenTime(self.campus_id)
        date_ob = strptime(date_str, '%y/%m/%d %H:%M:%S')
        dt = datetime.fromtimestamp(mktime(date_ob))
        if (t1-dt).total_seconds() >= 7000:
            year, month, day = t1.strftime("%y"), t1.strftime("%m"), t1.strftime("%d")
            hour, min, sec = t1.strftime("%H"), t1.strftime("%M"), t1.strftime("%S")
            response = requests.post(
                cfg.getUri(),
                data={"grant_type": "client_credentials",
                      "scope": "public projects profile tig forum elearning"},
                auth=(cfg.getPublicKey(self.campus_id), cfg.getPrivateKey(self.campus_id))
            )
            response = response.json()
            self.token = response["access_token"]
            self._update_json(self.token)
            with open(cfg.keys_path, "r+") as keysfile:
                file_data = json.load(keysfile)
                file_data["tokentime"] = year+"/" + \
                    month+"/"+day+" "+hour+":"+min+":"+sec
                keysfile.seek(0)
                json.dump(file_data, keysfile, indent=4)
            return self.token
        else:
            return cfg.getToken(self.campus_id)

    class Thread_Class(Thread):
        def __init__(self, adress, current_page, max, parametre, id, campus_id):
            Thread.__init__(self)
            self.id = id
            self.current_page = current_page
            self.max = max
            self.adress = adress
            self.params = parametre
            self.campus = campus_id
            self.api = API42(campus_id)
            self.whole_response = []
            self.pages = ""

        def run(self):
            params = dict()
            while self.current_page <= self.max:
                self.pages += str(self.current_page)+","
                params.update(self.params)
                params.update({"page[number]": self.current_page})
                # print(f"get: {self.adress} {params}")
                response = self.api._request(type="get", adress=self.adress, params=params)
                time.sleep(1)
                # response = self.api._request(type="get", adress=self.adress, params={'filter[primary_campus_id]': 49, 'page[size]': '100', 'page[number]': self.current_page})

                self.whole_response = self.api._response(response=response, whole_response=self.whole_response, key=1)
                # print("Thread["+str(self.id)+"], "+str(self.current_page)+" is done.")
                self.current_page += 1

    from src.api42.request import (
        _request,
        request,
        _response
    )
    from src.api42.utilities import (
        _check,
        _range_to_kv,
        _write_json,
        _update_json)

    from src.api42.accreditations import (
        get_accreditations,
        post_accreditations,
        put_accreditations,
        delete_accreditations,
        ACCREDITATIONS
    )
