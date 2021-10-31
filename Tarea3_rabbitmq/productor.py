import pika
import uuid
import sys

def on_response(ch,method,props,body):
    global response
    if corr_id==props.correlation_id:
        response=body.decode()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Creamos el exchange 'wiki' de tipo 'fanout'
channel.exchange_declare(exchange='wiki',exchange_type='fanout')

# Se crea una cola temporal exclusiva para este consumidor
result = channel.queue_declare(queue='',exclusive=True)
callback_queue = result.method.queue

channel.basic_consume(queue=callback_queue,
                      on_message_callback=on_response,
                      auto_ack=True
                     )

message = ' '.join(sys.argv[1:]) or '"Hello World!" program'
corr_id = str(uuid.uuid4())

channel.basic_publish(exchange='wiki',
                      routing_key='',
                      properties=pika.BasicProperties(reply_to=callback_queue,
                                                      correlation_id=corr_id
                                                     ),
                      body=message)

print(" [X] Sent %r" % message)
response = None

while response is None:
    connection.process_data_events()

respuesta1 = response
response = None
while response is None:
    connection.process_data_events()

if respuesta1[0]==1:
    print("Visitias en los ultimos 10 años: ",response[1:])
    print("Pagina:")
    print(respuesta1[1:])
else:
    print("Visitias en los ultimos 10 años: ",respuesta1[1:])
    print("Pagina:")
    print(response[1:])
    
connection.close()
