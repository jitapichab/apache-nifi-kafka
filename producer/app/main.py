from apscheduler.schedulers.blocking import BlockingScheduler
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging
from config import Config
from requests.exceptions import HTTPError
import requests
import json
from time import sleep


logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

class Worker:

    def __init__(self):
        self.covid_api = Config.covid_api
        self.bootstrap_server = Config.bootstrap_server
        self.topic = Config.topic

    def get_covid_info(self):
        overview_data = requests.get(self.covid_api)
        overview_data.raise_for_status()
        return overview_data.json()

    def config_producer(self):
        producer = KafkaProducer(bootstrap_servers=self.bootstrap_server, value_serializer=lambda m: json.dumps(m).encode('utf-8'),retries=3)
        return producer

    def send_producer_data(self,producer,data):
        producer.send(self.topic,data)
        logging.info("Successfully send message!")

    def run_tasks(self):
        try:
            data_covid = self.get_covid_info()
            producer = self.config_producer()
            for data in data_covid['Countries']:
                self.send_producer_data(producer,data)
                sleep(1)
        except KafkaError as err:
            logging.info(err)
        except Exception as err:
            logging.info(err)

    def run_worker(self):
         scheduler = BlockingScheduler()
         scheduler.add_job(self.run_tasks, 'cron', minute='*/1')
         logging.info('initializing worker cron task')
         scheduler.start()
         logging.info('finish worker cron task, wait for the next execution!')

if __name__ == '__main__':
    worker = Worker()
    worker.run_worker()
