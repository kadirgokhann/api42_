from src.api42.all_moduls import *


class Response:
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.content = response.content
        self.text = response.text
        self.json = response.json()


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
        if key == 1:  # if key == 1, it means that the response is a list to threads.
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


def request(self, type: str = "get", adress: str = "", params: str = {}) -> Response:
    self.adress = adress
    with open(str(self.dir_path)+"/logs.txt", "a") as a:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        a.write(now + " : Requesting: "+type+":"+str(adress)+"  "+"Parametres:"+str(params) + "\n")
    # Request the first page
    response = self._request(type, adress, params)
    data_size = response.headers["X-Total"] if "x-Total" in response.headers else 0
    num_of_pages = math.ceil(int(data_size)/100)
    num_of_thread = int(cfg.getThreads())
    work = math.ceil(int(num_of_pages)/int(num_of_thread))
    # If the number of pages is 1 or the work is 1, we don't need to use threads
    if (not "x-Page" in response.headers) or (int(response.headers["X-Total"]) <= 30) or (("page[number]" in params) or ("page[size]" in params)) or (type == "post") or (type == "put") or (type == "delete"):
        self.results = self._response(response=response)
        self._write_json(self.results.json)
        return self.results

    # If the number of pages is more than 1 and the work is more than 1, we need to use threads
    if "page[size]" not in params.keys():
        params["page[size]"] = str(100)
    current_page, alldata, threads, id = 1, [], [], 0
    max = current_page+work-1
    print("--> Total Work: "+str(num_of_pages), ", Work on a thread: "+str(work), ", Total Thread: ", str(num_of_thread))
    while current_page <= num_of_pages and max <= num_of_pages:
        threads.append(self.Thread_Class(adress=adress, current_page=current_page, max=max, parametre=params, id=id, campus_id=self.campus_id))
        current_page += work
        max = current_page+work-1
        if max > num_of_pages:
            max = num_of_pages
        id += 1
    for thread in threads:
        thread.start()
    for k in range(len(threads)):
        threads[k].join()
        print("--> Thread["+str(k)+"] is done with the pages "+threads[k].pages[:-1]+".")
        for i in threads[k].whole_response:
            alldata.append(i)
    # Since we are using threads, we need to collect the data and create a response class with
    # the data we collected. We also need to write the data to a json file.
    self._write_json(data=alldata)
    r = Response(response)
    r.json = alldata
    return r
