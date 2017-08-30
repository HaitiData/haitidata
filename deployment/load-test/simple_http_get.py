from locust import HttpLocust, TaskSet, task


class HaitiData(TaskSet):
    def on_start(self):
        response = self.client.get("/account/login")
        csrftoken = response.cookies['csrftoken']
        self.client.post("/account/login/",
                         {"username": "admin",
                          "password": "admin"},
                         headers={"X-CSRFToken": csrftoken})

    @task
    def index(self):
        self.client.get("/layers/geonode:madagascar_earthquake_cqmtpiu_tif_2017_08_23_08_59_10")


class HaitiUser(HttpLocust):
    task_set = HaitiData
    min_wait = 5000
    max_wait = 15000