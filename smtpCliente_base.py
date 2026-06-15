# Cliente SMTP básico — construcción manual del diálogo SMTP
# RESTRICCIÓN: Prohibido usar la librería smtplib.

from socket import *

# DATOS DE CONEXIÓN

MAIL_SERVER = 'localhost'
SMTP_PORT   = 1025 #Elegimos este puerto de escucha para el servidor de prueba

# Remitente y destinatario
FROM_ADDR = 'remitente@ejemplo.com'
TO_ADDR   = 'destinatario@ejemplo.com'

# Cabeceras y cuerpo del mensaje
# Deben finalizar con una línea en blanco (\r\n\r\n)
# para indicar el comienzo del cuerpo del mail.
msg_header = (
    f"From: {FROM_ADDR}\r\n"
    f"To: {TO_ADDR}\r\n"
    "Subject: TP Redes SMTP\r\n"
    "\r\n"
)

#Contenido
msg_body   = (
    "Hola!\r\n"
    "Este es un mail enviado desde un cliente SMTP hecho con sockets.\r\n"
)
msg_end    = "\r\n.\r\n"


# 1. CREAR SOCKET TCP Y CONECTAR AL SERVIDOR
# SMTP usa TCP como protocolo de transporte
clientSocket = socket(AF_INET, SOCK_STREAM)

#  Establecer la conexión con el servidor SMTP
clientSocket.connect((MAIL_SERVER, SMTP_PORT))


# Leer respuesta de bienvenida — debe comenzar con '220'
recv = clientSocket.recv(1024).decode()
print('S:', recv, end='')
if recv[:3] != '220':
    raise Exception(f'Error: Se esperaba 220, se recibió: {recv[:3]}')

# ─── 2. HELO ───────────────────────────────────────────────────────────────
# Se identifica el cliente al servidor.
helo_cmd = 'HELO cliente.ejemplo.com\r\n'

clientSocket.send(helo_cmd.encode())
print('C:', helo_cmd, end='')

recv1 = clientSocket.recv(1024).decode()
print('S:', recv1, end='')

if recv1[:3] != '250':
    raise Exception(f'Error HELO: {recv1[:3]}')

# ─── 3. COMPLETAR EL ENVIO DEL RESTO DE COMANDOS ──────────────────────────────────────────────────────────

### 220 y HELO ya estan, completamos el resto
### ────────────MAIL FROM───────────────────────────────
mail_from_cmd = f'MAIL FROM:<{FROM_ADDR}>\r\n'  
clientSocket.send(mail_from_cmd.encode())
print('C:', mail_from_cmd, end='')
recv2 = clientSocket.recv(1024).decode()
print('S:', recv2, end='')
if recv2[:3] != '250':
    raise Exception(f'Error MAIL FROM: {recv2[:3]}')

### ────────────RCPT TO─────────────────────────────────
# Se especifica el destinatario del mensaje.
rcpt_to_cmd = f'RCPT TO:<{TO_ADDR}>\r\n'
clientSocket.send(rcpt_to_cmd.encode())
print('C:', rcpt_to_cmd, end='')
recv3 = clientSocket.recv(1024).decode()
print('S:', recv3, end='')
if recv3[:3] != '250':
    raise Exception(f'Error RCPT TO: {recv3[:3]}')

### ────────────DATA────────────────────────────────────
# Se solicita al servidor comenzar la transmisión
# del contenido completo del correo.
data_cmd = 'DATA\r\n'
clientSocket.send(data_cmd.encode())
print('C:', data_cmd, end='')
recv4 = clientSocket.recv(1024).decode()
print('S:', recv4, end='')

# El servidor debe responder con 354 indicando
# que está listo para recibir los datos.
if recv4[:3] != '354':
    raise Exception(f'Error DATA: {recv4[:3]}')

### ────────────MAIL INFO───────────────────────────────
# Se envían las cabeceras, luego el cuerpo y finalmente
# la secuencia <CRLF>.<CRLF> para indicar fin del mensaje.
clientSocket.send(msg_header.encode())
clientSocket.send(msg_body.encode())
clientSocket.send(msg_end.encode())

recv5 = clientSocket.recv(1024).decode()
print('S:', recv5, end='')
if recv5[:3] != '250':
    raise Exception(f'Error MAIL INFO: {recv5[:3]}')


# ─── 4. FINALIZAR CONEXIÓN SMTP ───────────────────────────────────────────────────────────────
quit_cmd = 'QUIT\r\n'
clientSocket.send(quit_cmd.encode())
print('C:', quit_cmd, end='')
recv6 = clientSocket.recv(1024).decode()
print('S:', recv6, end='')
if recv6[:3] != '221':
    raise Exception(f'Error QUIT: {recv4[:3]}')

# ─── 5. CERRAR CONEXIÓN TCP ───────────────────────────────────────────────────────
# Cerrar el socket.
clientSocket.close()
print('\n[OK] Sesión SMTP finalizada correctamente.')
