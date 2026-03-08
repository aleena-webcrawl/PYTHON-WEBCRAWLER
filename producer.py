import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='url_queue', durable=True)


seeds = ["https://quotes.toscrape.com", "https://books.toscrape.com"]

for url in seeds:
    
    channel.basic_publish(
        exchange='',
        routing_key='url_queue',
        body=url,
        properties=pika.BasicProperties(delivery_mode=2) 
    )
    print(f" [P] Published to queue: {url}")


connection.close()

