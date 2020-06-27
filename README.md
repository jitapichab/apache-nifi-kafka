# **Apache-Nifi-Kafka**

This project is an example that shows how it's possible to connect Apache Nifi with Kafka to consume messages from Kafka and produce messages to Kafka. A COVID-19 API was used for this example. 

## **Architecture of the project**


![Architecture Image](media/apache-nifi-kafka.png)

## **Prerequisites**

* Docker
* Docker Compose

## **Implementation**

1. Clone the repository and export your IP private as a variable; Eg:

```
export IP=$(ipconfig getifaddr en0)
```

2. Run the Docker Compose:
```
docker-compose up
```

3. Visit the apache nifi web site in http://localhost:8080

![Nifi website Image](media/apache-nifi-website.png)

4. Upload *nifi-templates/nifi-covid-kafka.xml*  in the section **operate**  in the bottom on the page, once the template was uploaded you should  drag the template in the toolbar on the top on the page and select the template uploaded.

![Nifi Template Image](media/nifi-template-uploaded.png)

5. Start the project and check if the  __*PublishKafka*__ procesor has received messages.

<p align="center">
<img width="395" height="254" src="media/publishkafka_processor.png">
</p>

## **Checking**

You can check the logs on the *consumer*  and see that the *consumer* only show the messages with countries that have more than 1000 cases of COVID-19 confirmed.

```
docker-compose logs -f consumer
```

![Consumer Logs](media/logs-by-consumer.png)

## *Explication*

https://medium.com/@jitapichab/apache-nifi-integrate-kafka-to-consume-and-produce-387968b8bd6b