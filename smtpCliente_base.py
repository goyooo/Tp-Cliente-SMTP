# Cliente SMTP básico — construcción manual del diálogo SMTP
# RESTRICCIÓN: Prohibido usar la librería smtplib.

from socket import *

# DATOS DE CONEXIÓN
# COMPLETAR
# Completar con el servidor de correo real (p.ej. smtp.dominio.edu.ar) o 'localhost' para pruebas locales.
MAIL_SERVER = 'localhost'
SMTP_PORT   = 1025

# Remitente y destinatario
FROM_ADDR = 'remitente@ejemplo.com'
TO_ADDR   = 'destinatario@ejemplo.com'

# Cabeceras y cuerpo del mensaje
msg_header = (
    f"From: {FROM_ADDR}\r\n"
    f"To: {TO_ADDR}\r\n"
    "Subject: TP Redes SMTP\r\n"
    "\r\n"
)
msg_body   = (
    "Hola!\r\n"
    "Este es un mail enviado desde un cliente SMTP hecho con sockets.\r\n"
)
msg_end    = "."


# 1. CREAR SOCKET TCP Y CONECTAR AL SERVIDOR
clientSocket = socket(AF_INET, SOCK_STREAM)

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
# COMPLETAR: Construir y enviar los comandos típicos. Leer y verificar la respuesta de cada comando.
# Pista: Sigan el gráfico del enunciado y presten atención a como se envia las lineas de header y el cuerpo del mail.

### 220 y HELO ya estan, voy por el resto



# ─── 4. FINALIZAR CONEXIÓN SMTP ───────────────────────────────────────────────────────────────
# COMPLETAR


# ─── 5. CERRAR CONEXIÓN TCP ───────────────────────────────────────────────────────
# COMPLETAR: Cerrar el socket.
print('\n[OK] Sesión SMTP finalizada correctamente.')
