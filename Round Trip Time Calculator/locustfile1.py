import base64

from locust import HttpLocust, TaskSet, task
from random import randint, choice
import numpy as np


class WebTasks(TaskSet):

    @task
    def load(self):
               self.client.get("/microservices/fibonacci")


class Web(HttpLocust):
    task_set = WebTasks
    min_wait = 1000
    max_wait = 3000
