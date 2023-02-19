from src.api42.all_moduls import *


class Response:
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.content = response.content
        self.text = response.text
        self.json = response.json()
        self.headers = response.headers


def _request(self, type, adress, params):
    if type == "get":
        response = requests.get(cfg.getEndpoint() + adress, headers={"Authorization": f"Bearer {self.token}"}, params=params)
    elif type == "post":
        response = requests.post(cfg.getEndpoint() + adress, headers={"Authorization": f"Bearer {self.token}"}, params=params)
    elif type == "patch":
        print("You have to use 'put', try again please..")
        quit()
    elif type == "put":
        response = requests.put(cfg.getEndpoint() + adress, headers={"Authorization": f"Bearer {self.token}"}, params=params)
    elif type == "delete":
        response = requests.delete(cfg.getEndpoint() + adress, headers={"Authorization": f"Bearer {self.token}"}, params=params)
    return response


def _response(self, response, whole_response: list = [], key=0):
    if response.status_code == 200:
        response_j = response.json()
        if key == 1:
            for i in response_j:
                whole_response.append(i)
            return whole_response
        return Response(response)
    elif response.status_code == 201 or response.status_code == 204:
        return Response(response)
    elif response.status_code == 401:
        print("401: The access token expired")
        return False
    elif response.status_code == 403:
        print("403: Access to the requested source is forbidden!!!")
        return False
    elif response.status_code == 404:
        print("404: Page or resource is not found, check your URL!!!!")
        return False
    elif response.status_code == 429:
        print("429: Rate Limit Exceeded")
        return False
    elif str(response.status_code)[0] == '5':
        print(response.status_code+": We have a problem with our server. Please try again later.")
        return False
    else:
        print("Request returned with {} status code, with the text \"{}\". \n".format(response.status_code, response.text))
        return False


def request(self, type: str = "get", adress: str = "", params: str = {}) -> tuple:
    with open(str(self.dir_path)+"/logs.txt", "a") as a:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        a.write(now + " : Requesting: "+type+":"+str(adress)+"  "+"Parametres:"+str(params) + "\n")
    self.adress = adress
    response = self._request(type, adress, params)
    data_size = response.headers["X-Total"] if "x-Total" in response.headers else 0
    numofPages = math.ceil(int(data_size)/100)
    thread_num = int(cfg.getThreads())
    work = math.ceil(int(numofPages)/int(thread_num))
    # If page property does not exist call the embedded request function. Params should be updated.
    if (not "x-Page" in response.headers) or (int(response.headers["X-Total"]) <= 30) or (("page[number]" in params) or ("page[size]" in params)) or (type == "post") or (type == "put") or (type == "delete"):
        self.results = self._response(response=response)
        self._write_json(self.results.json)
        return self.results
    params["page[size]"] = str(100)
    current_page = 1
    alldata = []
    threads = []
    id = 0
    max = current_page+work-1
    booleean = (numofPages != 1 and work != 1)
    print("--> Total Work: "+str(numofPages), ", Work on a thread: "+str(work), ", Total Thread: ", str(thread_num))
    while current_page <= numofPages and max <= numofPages:
        c, m, p, i, ca, a = current_page, max, params, id, self.campus_id, adress
        # print("Thread "+str(id)+" is working on "+str(c)+"-"+str(m))
        thread = CustomThread(adress=a, current_page=c, max=m, parametre=p, id=i, campus_id=ca)
        threads.append(thread)
        current_page += work
        max = current_page+work-1
        if max > numofPages:
            max = numofPages
        id += 1
    for thread in threads:
        thread.start()
    for k in range(len(threads)):
        threads[k].join()
        if booleean:
            print("--> Thread["+str(k)+"] is done with the pages "+threads[k].pages[:-1]+".")
        for i in threads[k].whole_response:
            alldata.append(i)
    self.__write_json(data=alldata)
    r = Response(response)
    r.json = alldata
    return r
