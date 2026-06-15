# Cliente SMTP avanzado: STARTTLS + AUTH LOGIN (Base64)
# RESTRICCIÓN: Prohibido usar smtplib. Se permite: socket, ssl, base64, os.

from socket import *
import ssl
import base64
import os

# DATOS DE CONEXIÓN

# Servidor de correo
MAIL_SERVER = 'smtp.gmail.com'

# Puerto con soporte STARTTLS
SMTP_PORT   = 587

# Cargar credenciales desde variables de entorno (más seguro)
FROM_ADDR = os.environ.get('SMTP_USER', '')
PASSWORD  = os.environ.get('SMTP_PASS', '')  

# Destinatario
TO_ADDR   = 'juanmgoyeneche@gmail.com'

# Verificar que la contraseña haya sido definida.
if not PASSWORD:
    raise EnvironmentError('Definir SMTP_PASS en variables de entorno.')

# Cabeceras y cuerpo del mensaje
msg_header = (
    f"From: {FROM_ADDR}\r\n"
    f"To: {TO_ADDR}\r\n"
    "Subject: TP Redes SMTP\r\n"
    "\r\n"
)

# Contenido del mensaje
msg_body   = (
    "Hola!\r\n"
    "Con el cifrado este mensaje no puede ser interceptado.\r\n"
)
msg_end = "\r\n.\r\n"

#  CREAR SOCKET TCP Y CONECTAR AL SERVIDOR
clientSocket = socket(AF_INET, SOCK_STREAM) 

# Conectarse al servidor SMTP
clientSocket.connect((MAIL_SERVER, SMTP_PORT))

# Leer respuesta de bienvenida — debe comenzar con '220'
recv = clientSocket.recv(1024).decode()
print('S:', recv, end='')
if recv[:3] != '220':
    raise Exception(f'Banner inesperado: {recv}')

# ───  EHLO (Extended HELO) ────────────────────────────────────────────
# Se usa EHLO (no HELO) para negociar extensiones como STARTTLS.
# COMPLETAR: Enviar 'EHLO localhost\r\n' y leer la respuesta ('250').

ehlo_cmd = 'EHLO localhost\r\n'
clientSocket.send(ehlo_cmd.encode())
print('C:', ehlo_cmd, end='')
recv1 = clientSocket.recv(1024).decode()
print('S:', recv1, end='')
if recv1[:3] != '250':
    raise Exception(f'Error EHLO: {recv1[:3]}')

# ───  STARTTLS ─────────────────────────────────────────────────────────
# Solicitar inicio de sesión cifrada ANTES de enviar credenciales.

starttls_cmd = 'STARTTLS\r\n'
clientSocket.send(starttls_cmd.encode())
print('C:', starttls_cmd, end='')
recv2 = clientSocket.recv(1024).decode()
print('S:', recv2, end='')
if recv2[:3] != '220':
    raise Exception(f'Error STARTTLS: {recv2[:3]}')

# ───  ENVOLVER SOCKET CON SSL/TLS ─────────────────────────────────────

context = ssl.create_default_context()

# Envolver el socket TCP original con TLS.
tlsSocket = context.wrap_socket(
    clientSocket,
    server_hostname=MAIL_SERVER
)

# ───  EHLO NUEVAMENTE (sobre canal cifrado) ───────────────────────────
# RFC 3207 exige re-enviar EHLO tras establecer TLS.

ehlo_cmd = 'EHLO localhost\r\n'
tlsSocket.send(ehlo_cmd.encode())
print('C:', ehlo_cmd, end='')
recv3 = tlsSocket.recv(1024).decode()
print('S:', recv3, end='')
if recv3[:3] != '250':
    raise Exception(f'Error cifrado: {recv3[:3]}')


# ───  AUTH LOGIN ──────────────────────────────────────────────────────
# Autenticación mediante usuario y contraseña codificados en Base64.

auth_login_cmd = 'AUTH LOGIN\r\n'
tlsSocket.send(auth_login_cmd.encode())
print('C:', auth_login_cmd, end='')

recv4 = tlsSocket.recv(1024).decode()
print('S:', recv4, end='')
if recv4[:3] != '334':
    raise Exception(f'Error AUTH LOGIN: {recv4[:3]}')

#       Codificar FROM_ADDR en Base64 y enviarlo.
usuariob64_cmd = base64.b64encode(FROM_ADDR.encode()).decode() + '\r\n'
tlsSocket.send(usuariob64_cmd.encode())
print('C:',usuariob64_cmd, end='')

# COMPLETAR: El servidor responde '334' solicitando la contraseña en Base64.
recv5 = tlsSocket.recv(1024).decode()
print('S:', recv5, end='')
if recv5[:3] != '334':
    raise Exception(f'Error USUARIO B64: {recv5[:3]}')

#       Codificar PASSWORD en Base64 y enviarlo.
contraseñab64_cmd = base64.b64encode(PASSWORD.encode()).decode() + '\r\n'
tlsSocket.send(contraseñab64_cmd.encode())
print('C:',contraseñab64_cmd, end='')


recv6 = tlsSocket.recv(1024).decode()
print('S:', recv6, end='')
if recv6[:3] != '235':
    raise Exception(f'Error PASSWORD B64: {recv6[:3]}')




# ───  COMPLETAR EL ENVIO DEL RESTO DE COMANDOS: MAIL FROM, RCPT TO, DATA, CUERPO, QUIT ───────────────────

mail_from_cmd = f'MAIL FROM:<{FROM_ADDR}>\r\n'  
tlsSocket.send(mail_from_cmd.encode())
print('C:', mail_from_cmd, end='')
recv7 = tlsSocket.recv(1024).decode()
print('S:', recv7, end='')
if recv7[:3] != '250':
    raise Exception(f'Error MAIL FROM: {recv7[:3]}')

### ────────────RCPT TO─────────────────────────────────
rcpt_to_cmd = f'RCPT TO:<{TO_ADDR}>\r\n'
tlsSocket.send(rcpt_to_cmd.encode())
print('C:', rcpt_to_cmd, end='')
recv8 = tlsSocket.recv(1024).decode()
print('S:', recv8, end='')
if recv8[:3] != '250':
    raise Exception(f'Error RCPT TO: {recv8[:3]}')

### ────────────DATA────────────────────────────────────
data_cmd = 'DATA\r\n'
tlsSocket.send(data_cmd.encode())
print('C:', data_cmd, end='')
recv9 = tlsSocket.recv(1024).decode()
print('S:', recv9, end='')
if recv9[:3] != '354':
    raise Exception(f'Error DATA: {recv9[:3]}')

### ────────────MAIL INFO───────────────────────────────
mail_info_cmd = msg_header + msg_body + msg_end
tlsSocket.send(mail_info_cmd.encode())
print('C:', mail_info_cmd, end='')
recv10 = tlsSocket.recv(1024).decode()
print('S:', recv10, end='')
if recv10[:3] != '250':
    raise Exception(f'Error MAIL INFO: {recv10[:3]}')

# ───  FINALIZAR CONEXIÓN SMTP ───────────────────────────────────────────────────
quit_cmd = 'QUIT\r\n'
tlsSocket.send(quit_cmd.encode())
print('C:', quit_cmd, end='')
recv11 = tlsSocket.recv(1024).decode()
print('S:', recv11, end='')
if recv11[:3] != '221':
    raise Exception(f'Error QUIT: {recv11[:3]}')

# ───  CERRAR CONEXIÓN TLS ───────────────────────────────────────────────────────

tlsSocket.close()
print('\n[OK] Correo enviado con cifrado TLS.')
