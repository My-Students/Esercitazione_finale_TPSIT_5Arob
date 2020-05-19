import socket

Server_ip = socket.gethostbyname(socket.gethostname())      # determino l'ip della macchina(per comodità)

MY_ID = '14'    # nel registro sono il numero 14 e i test quindi verranno effeuttati con quest'ultimo

# gli url a cui passo i pareametri

send_url = 'http://%s:5000/api/v1/send?sender_id=%s&text=%s&receiver_id=%s'

recv_url = 'http://%s:5000/api/v1/receive?receiver_id=%s'

users_list_url = 'http://%s:5000/api/v1/user_list'

download_url = 'http://%s:5000/api/v1/download_photo?photo_name=%s'     # non rischesto, aggiunto da me per permettere lo scaricamento delle foto