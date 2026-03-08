import pika
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


if not os.path.exists('pages'):
    os.makedirs('pages')


visited_urls = set()

def callback(ch, method, properties, body):
    url = body.decode()
    
    
    if url in visited_urls:
        print(f" [SKIP] Already visited: {url}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    print(f" [W] Fetching: {url}")
    
    try:
        
        response = requests.get(url, timeout=5)
        
        
        if response.status_code == 200:
            
            visited_urls.add(url)
            
            
            filename = url.split("//")[-1].replace(".", "_").replace("/", "_")[:50] + ".html"
            filepath = os.path.join('pages', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            
            soup = BeautifulSoup(response.text, 'html.parser')
            link_count = 0
            for link in soup.find_all('a', href=True):
                if link_count >=5:
                    break
                new_url = urljoin(url, link['href'])
                
                
                if urlparse(new_url).netloc == urlparse(url).netloc:
                    link_count +=1
                    
                    ch.basic_publish(
                        exchange='',
                        routing_key='url_queue',
                        body=new_url,
                        properties=pika.BasicProperties(delivery_mode=2)
                    )
            
            print(f" [OK] Processed and extracted links from: {url}")
        
        
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f" [!] Error: {e}")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='url_queue', durable=True)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='url_queue', on_message_callback=callback)

print(' [*] Worker started. Waiting for URLs. To exit press CTRL+C')
channel.start_consuming()

