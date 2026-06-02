# Cliente SMTP avanzado: STARTTLS + AUTH LOGIN (Base64)
# RESTRICCIÓN: Prohibido usar smtplib. Se permite: socket, ssl, base64, os.

from socket import *
import ssl
import base64
import os

# DATOS DE CONEXIÓN
# COMPLETAR
# Completar con el servidor de correo real (p.ej. smtp.dominio.edu.ar)
MAIL_SERVER = 'smpt.gmail.com'
SMTP_PORT   = 587

# Cargar credenciales desde variables de entorno (más seguro)
FROM_ADDR = os.environ.get('SMTP_USER', 'juanmartingoyeneche@gmail.com')
PASSWORD  = os.environ.get('SMTP_PASS', 'tuviejaconmipingoseahoga!')   
TO_ADDR   = 'juanmartingoyeneche@gmail.com'

if not PASSWORD:
    raise EnvironmentError('Definir SMTP_PASS en variables de entorno.')

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
msg_end = "\r\n.\r\n"

# 1. CREAR SOCKET TCP Y CONECTAR AL SERVIDOR
clientSocket = socket(AF_INET, SOCK_STREAM) 

clientSocket.connect((MAIL_SERVER, SMTP_PORT))

# Leer respuesta de bienvenida — debe comenzar con '220'
recv = clientSocket.recv(1024).decode()
print('S:', recv, end='')
if recv[:3] != '220':
    raise Exception(f'Banner inesperado: {recv}')

# ─── 2. EHLO (Extended HELO) ────────────────────────────────────────────
# Se usa EHLO (no HELO) para negociar extensiones como STARTTLS.
# COMPLETAR: Enviar 'EHLO localhost\r\n' y leer la respuesta ('250').
ehlo_cmd = 'EHLO localhost\r\n'
clientSocket.send(ehlo_cmd.encode())
print('C:', ehlo_cmd, end='')
recv1 = clientSocket.recv(1024).decode()
print('S:', recv1, end='')
if recv1[:3] != '250':
    raise Exception(f'Error EHLO: {recv1[:3]}')

# ─── 3. STARTTLS ─────────────────────────────────────────────────────────
# Solicitar inicio de sesión cifrada ANTES de enviar credenciales.
# COMPLETAR: Enviar el comando 'STARTTLS\r\n' y leer la respuesta ('220 Ready to start TLS').
starttls_cmd = 'STARTTLS\r\n'
clientSocket.send(starttls_cmd.encode())
print('C:', starttls_cmd, end='')
recv2 = clientSocket.recv(1024).decode()
print('S:', recv2, end='')
if recv2[:3] != '220':
    raise Exception(f'Error STARTTLS: {recv2[:3]}')

# ─── 4. ENVOLVER SOCKET CON SSL/TLS ─────────────────────────────────────
# COMPLETAR: Crear un ssl.SSLContext con protocolo TLS cliente.
# COMPLETAR: Usar context.wrap_socket() sobre clientSocket,
#       indicando server_hostname=MAIL_SERVER.
#       Asignar el resultado a tlsSocket.
context = ssl.create_default_context()

tlsSocket = context.wrap_socket(
    clientSocket,
    server_hostname=MAIL_SERVER
)

# ─── 5. EHLO NUEVAMENTE (sobre canal cifrado) ───────────────────────────
# RFC 3207 exige re-enviar EHLO tras establecer TLS.
# COMPLETAR: Enviar EHLO nuevamente usando tlsSocket.
ehlo_cmd = 'EHLO localhost\r\n'
tlsSocket.send(ehlo_cmd.encode())
print('C:', ehlo_cmd, end='')
recv3 = tlsSocket.recv(1024).decode()
print('S:', recv3, end='')
if recv3[:3] != '250':
    raise Exception(f'Error cifrado: {recv3[:3]}')


# ─── 6. AUTH LOGIN ──────────────────────────────────────────────────────
# Autenticación mediante usuario y contraseña codificados en Base64.
# COMPLETAR: Enviar 'AUTH LOGIN\r\n' por tlsSocket.
auth_login_cmd = 'AUTH LOGIN\r\n'
tlsSocket.send(auth_login_cmd.encode())
print('C:', auth_login_cmd, end='')
recv4 = tlsSocket.recv(1024).decode()
print('S:', recv4, end='')
if recv4[:3] != '250':
    raise Exception(f'Error AUTH LOGIN: {recv4[:3]}')
# COMPLETAR: El servidor responde '334' solicitando el usuario en Base64.
#       Codificar FROM_ADDR en Base64 y enviarlo.


# COMPLETAR: El servidor responde '334' solicitando la contraseña en Base64.
#       Codificar PASSWORD en Base64 y enviarlo.
# COMPLETAR: Verificar respuesta '235' (autenticación exitosa).

# Pista: base64.b64encode(string.encode()).decode() + '\r\n'


# ─── 7. COMPLETAR EL ENVIO DEL RESTO DE COMANDOS: MAIL FROM, RCPT TO, DATA, CUERPO, QUIT ───────────────────
# COMPLETAR: Completar igual que en SMTPClient_base.py,
#       pero usando tlsSocket en lugar de clientSocket.


# ─── 8. CERRAR CONEXIÓN TLS ───────────────────────────────────────────────────────
# COMPLETAR: Cerrar el socket.
print('\n[OK] Correo enviado con cifrado TLS.')
