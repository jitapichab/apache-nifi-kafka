from apscheduler.schedulers.blocking import BlockingScheduler
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import logging
from config import Config
import json
from time import sleep


logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

class Worker:

    def __init__(self):
       self.bootstrap_server = Config.bootstrap_server
       self.topic = Config.topic

    def config_consumer(self):
       consumer = KafkaConsumer(
                                 self.topic,
                                 group_id='nifi_covid_overview_consumer',
                                 bootstrap_servers=self.bootstrap_server,
                                 auto_offset_reset='latest',
                                 )
       #consumer.subscribe(self.topic)
       return consumer

    def run_tasks(self):
       try:
          consumer = self.config_consumer()
          for data in consumer:
              logging.info(json.loads(data.value))
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
