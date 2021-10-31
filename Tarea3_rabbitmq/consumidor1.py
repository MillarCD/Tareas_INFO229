import pika
import wikipedia

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# el consumidor utiliza el exchange 'wiki'
channel.exchange_declare(exchange='wiki',exchange_type='fanout')

# Se crea una cola temporal exclusiva para el consumidor
result = channel.queue_declare(queue='',exclusive=True)
queue_name = result.method.queue

#Se le asigna un 'exchange'
channel.queue_bind(exchange='wiki',queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch,method,props,body):
    wikipedia.set_lang('es')
    pagina = wikipedia.page(body.decode())
    respuesta = f"1{pagina.title}\nURL: {pagina.url}\n{pagina.content}"
    print(respuesta[1:])
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=\
                                                         props.correlation_id),
                     body=respuesta
                    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("envie respuesta")
    
channel.basic_consume(queue=queue_name,on_message_callback=callback)

channel.start_consuming()
