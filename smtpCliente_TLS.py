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
PASSWORD  = os.environ.get('SMTP_PASS', '')   
TO_ADDR   = 'juanmartingoyeneche@gmail.com'

if not PASSWORD:
    raise EnvironmentError('Definir SMTP_PASS en variables de entorno.')

# Cabeceras y cuerpo del mensaje
msg_header = 
msg_body   = 
msg_end    = 

# 1. CREAR SOCKET TCP Y CONECTAR AL SERVIDOR
# COMPLETAR

# Leer respuesta de bienvenida — debe comenzar con '220'
recv = clientSocket.recv(1024).decode()
print('S:', recv, end='')
if recv[:3] != '220':
    raise Exception(f'Banner inesperado: {recv}')

# ─── 2. EHLO (Extended HELO) ────────────────────────────────────────────
# Se usa EHLO (no HELO) para negociar extensiones como STARTTLS.
# COMPLETAR: Enviar 'EHLO localhost\r\n' y leer la respuesta ('250').


# ─── 3. STARTTLS ─────────────────────────────────────────────────────────
# Solicitar inicio de sesión cifrada ANTES de enviar credenciales.
# COMPLETAR: Enviar el comando 'STARTTLS\r\n' y leer la respuesta ('220 Ready to start TLS').


# ─── 4. ENVOLVER SOCKET CON SSL/TLS ─────────────────────────────────────
# COMPLETAR: Crear un ssl.SSLContext con protocolo TLS cliente.
# COMPLETAR: Usar context.wrap_socket() sobre clientSocket,
#       indicando server_hostname=MAIL_SERVER.
#       Asignar el resultado a tlsSocket.


# ─── 5. EHLO NUEVAMENTE (sobre canal cifrado) ───────────────────────────
# RFC 3207 exige re-enviar EHLO tras establecer TLS.
# COMPLETAR: Enviar EHLO nuevamente usando tlsSocket.


# ─── 6. AUTH LOGIN ──────────────────────────────────────────────────────
# Autenticación mediante usuario y contraseña codificados en Base64.
# COMPLETAR: Enviar 'AUTH LOGIN\r\n' por tlsSocket.
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
