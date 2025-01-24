from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task(3)
    def board(self):
        self.client.get("/board")

    @task(3)
    def summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task(3)
    def book(self):
        self.client.get("/book/Spring Festival/Simply Lift")
