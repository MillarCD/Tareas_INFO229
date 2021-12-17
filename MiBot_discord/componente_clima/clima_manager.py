import os, time
import pika
import requests
from dotenv import load_dotenv

print("start clima manager...")

########### KEY DE LA API WEATHERMAP ###################
load_dotenv()
KEY = os.getenv('API_KEY')

########### CONNEXIÓN A RABBIT MQ #######################
HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

EXCHANGE = 'cartero'
QUEUE = 'weather'

#El consumidor utiliza el exchange 'mensajero'
channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic', durable=True)

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue=QUEUE, exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=QUEUE)

##########################################################


########## ESPERA Y HACE ALGO CUANDO RECIBE UN MENSAJE ####

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(body.decode("UTF-8"))
    arguments = body.decode("UTF-8").split(" ")
    arguments.append('santiago')
    city = arguments[1].replace('-',' ')

    if (arguments[0]!="!clima"):
        return
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}")
    res = r.json()
    if(len(res.values())==2):
       channel.basic_publish(exchange='cartero',routing_key="discord_writer",body="Ciudad no encontrada")
       return
       
    print(res)
    clima = res['weather'][0]['main']
    url = ''
    if(clima.lower()=='clear'):
        clima = 'Soleado'
        url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F1.bp.blogspot.com%2F-t0L80CdG0e8%2FUA2SqzwmVFI%2FAAAAAAAAkmA%2FqqnHKQHT0as%2Fs1600%2Feltiempoparaimprimir.gif&f=1&nofb=1'
    elif(clima.lower()=='mist'):
        clima = 'Ligeras precipitaciones' 
        url = 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.acn.cu%2Fimages%2F2018%2Ffebrero%2Fnublados_y_chubascos.jpg&f=1&nofb=1'
    elif(clima.lower()=='clouds'):
        clima = 'Nublado'
        url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwebstockreview.net%2Fimages%2Fcloudy-clipart-19.jpg&f=1&nofb=1'
    elif(clima.lower()=='rain'):
        clima = 'Lluvia'
        url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2F474x%2F96%2Fd6%2F5d%2F96d65dbbde977d8f4da81e1d0da6ea49--preschool-classroom-preschool-crafts.jpg&f=1&nofb=1'

    temperatura = str(res['main']['temp']-273)+'°C'
    humedad = str(res['main']['humidity'])+"%"
    result = f'''CIUDAD: {city}\nCLIMA: {clima}\nTEMPERATURA: {temperatura}\nHUMEDAD: {humedad}'''
    print(result)
    ########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
    print("send a new message to rabbitmq...")
    channel.basic_publish(exchange=EXCHANGE,routing_key="discord_writer",body=result)
    if(url!=''):
        channel.basic_publish(exchange=EXCHANGE,routing_key="discord_writer",body=url)



channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
