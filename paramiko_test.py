import paramiko
import argparse
import os

# 1) Configurar argumentos
parser = argparse.ArgumentParser(
    description="📤 Transferencia de archivo y verificación por SSH",
    epilog="Ejemplo: python envio_ssh.py -ip 192.168.1.100 -u alumno -p clave123"
)
parser.add_argument("-ip", required=True, help="IP del servidor SSH")
parser.add_argument("-puerto", type=int, default=22, help="Puerto SSH (por defecto 22)")
parser.add_argument("-u", required=True, help="Usuario SSH")
parser.add_argument("-p", required=True, help="Contraseña SSH")
args = parser.parse_args()

# 2) Verificar que el archivo exista
archivo_local = "m_matricula.txt" #Sustituye matricula por tu matricula
if not os.path.exists(archivo_local):
    print("❌ No se encontró el archivo matricula.txt en esta carpeta.")
    exit()

# 3) Crear cliente SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"🔗 Conectando a {args.ip}:{args.puerto} como {args.u}...")
    ssh.connect(
        hostname=args.ip,
        port=args.puerto,
        username=args.u,
        password=args.p,
        timeout=5
    )

    # 4) Transferir archivo por SFTP
    print("Transfiriendo archivo matricula.txt...")
    sftp = ssh.open_sftp()
    archivo_remoto = f"/home/{args.u}/matricula.txt"
    sftp.put(archivo_local, archivo_remoto)
    sftp.close()
    print("Archivo transferido correctamente.")

    # 5) Ejecutar comando remoto para verificar
    print("Verificando contenido con 'cat matricula.txt'...")
    comando = f"cat {archivo_remoto}"
    stdin, stdout, stderr = ssh.exec_command(comando)

    salida = stdout.read().decode().strip()
    error = stderr.read().decode().strip()

    if salida:
        print("📄 Contenido del archivo en el servidor:")
        print("----------------------------------------")
        print(salida)
        print("----------------------------------------")
    if error:
        print("Error al ejecutar el comando:")
        print(error)

except paramiko.AuthenticationException:
    print("Error de autenticación. Verifica usuario y contraseña.")
except paramiko.SSHException as e:
    print(f"Error SSH: {e}")
except Exception as e:
    print(f"Error general: {e}")
finally:
    ssh.close()
    print("Sesión finalizada.")
