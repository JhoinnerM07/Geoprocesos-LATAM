from PyQt5.QtWidgets import QInputDialog, QMessageBox
import psycopg2
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def mostrar_mensaje(titulo, texto, icono=QMessageBox.Information):
    msg = QMessageBox()
    msg.setIcon(icono)
    msg.setWindowTitle(titulo)
    msg.setText(texto)
    msg.exec_()

def pedir_texto(titulo, etiqueta, default=""):
    valor, ok = QInputDialog.getText(None, titulo, etiqueta, text=default)
    if not ok or valor.strip() == "":
        raise Exception(f"⚠️ Entrada cancelada o vacía: {etiqueta}")
    return valor.strip()

try:
    # ========= ENTRADA DE DATOS =========
    usuario = pedir_texto("Usuario", "🔹 Ingrese su usuario de la base de datos:","latam_jhoinner_manrique")
    contraseña = pedir_texto("Contraseña", "🔹 Ingrese su contraseña:","ServiLatam*2024")
    base_datos = pedir_texto("Base de datos", "🔹 Ingrese el nombre de la base de datos:","Latam_Brasil")
    ip = pedir_texto("Servidor", "🔹 Ingrese la IP o nombre del servidor:", "192.168.1.179")
    puerto = pedir_texto("Puerto", "🔹 Ingrese el puerto (por defecto 5432):", "5432")
    esquema = pedir_texto("Esquema", "🔹 Ingrese el nombre del esquema:")
    capa = pedir_texto("Capa", "🔹 Ingrese el nombre de la capa:")

    # ========= CARGA DEL SCRIPT =========
    mostrar_mensaje("Descargando", "📥 Descargando el script desde GitHub...")
    url_sql = "https://raw.githubusercontent.com/JhoinnerM07/validaciones/refs/heads/main/identificar_dangles.sql"
    sql_crudo = requests.get(url_sql, verify=False).text

    # ========= ADAPTACIÓN =========
    sql_final = sql_crudo.replace("{esquema}", esquema).replace("{capa}", capa)
    mostrar_mensaje("Adaptación", "✅ Script adaptado con los valores ingresados.")

    # ========= CONEXIÓN A LA BD =========
    mostrar_mensaje("Conexión", "🔌 Intentando conexión a la base de datos...")
    conn = psycopg2.connect(
        host=ip,
        port=puerto,
        database=base_datos,
        user=usuario,
        password=contraseña
    )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    mostrar_mensaje("Conexión exitosa", "✅ Conexión establecida con la base de datos.")

    # ========= EJECUCIÓN =========
    cur.execute(sql_final)

    mensaje = f"✅ Script ejecutado correctamente.\nFilas afectadas: {cur.rowcount}"
    if conn.notices:
        mensaje += "\n\n📢 Notificaciones:\n" + "\n".join([n.strip() for n in conn.notices])

    mostrar_mensaje("Ejecución completada", mensaje)

    cur.close()
    conn.close()

except Exception as e:
    mostrar_mensaje("❌ Error", str(e), icono=QMessageBox.Critical)
