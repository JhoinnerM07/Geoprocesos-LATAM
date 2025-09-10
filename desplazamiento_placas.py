from PyQt5.QtWidgets import QInputDialog, QMessageBox, QFileDialog
import requests
import urllib3
import os

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
    esquema_mavvial = pedir_texto("Esquema MAVVIAL", "🔹 Ingrese el nombre del esquema MAVVIAL:")
    esquema_manzana = pedir_texto("Esquema MANZANA", "🔹 Ingrese el nombre del esquema MANZANA:")
    esquema_placa = pedir_texto("Esquema PLACA", "🔹 Ingrese el nombre del esquema PLACA:")
    capa_mavvial = pedir_texto("Capa MAVVIAL", "🔹 Ingrese el nombre de la capa MAVVIAL:")
    capa_placa = pedir_texto("Capa PLACA", "🔹 Ingrese el nombre de la capa PLACA:")
    capa_manzana = pedir_texto("Capa MANZANA", "🔹 Ingrese el nombre de la capa MANZANA:")

    # ========= CARGA DEL SCRIPT =========
    mostrar_mensaje("Descargando", "📥 Descargando el script desde GitHub...")
    url_sql = "https://raw.githubusercontent.com/JhoinnerM07/herramientas_automatizacion/refs/heads/main/desplazamiento_placas.sql"
    sql_crudo = requests.get(url_sql, verify=False).text

    # ========= ADAPTACIÓN =========
    sql_final = (sql_crudo
                 .replace("{esquema_mavvial}", esquema_mavvial)
                 .replace("{esquema_manzana}", esquema_manzana)
                 .replace("{esquema_placa}", esquema_placa)
                 .replace("{capa_mavvial}", capa_mavvial)
                 .replace("{capa_placa}", capa_placa)
                 .replace("{capa_manzana}", capa_manzana))

    mostrar_mensaje("Adaptación", "✅ Script adaptado con los valores ingresados.")

    # ========= GUARDADO =========
    mostrar_mensaje("Guardar", "📂 Seleccione dónde guardar el SQL adaptado.")
    ruta_salida, _ = QFileDialog.getSaveFileName(None, "Guardar script adaptado", os.path.expanduser("~"), "SQL Files (*.sql)")
    if not ruta_salida:
        raise Exception("⚠️ No se seleccionó ninguna ruta de salida.")

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(sql_final)

    mostrar_mensaje("Completado", f"✅ Script guardado correctamente en:\n{ruta_salida}")

except Exception as e:
    mostrar_mensaje("❌ Error", str(e), icono=QMessageBox.Critical)
