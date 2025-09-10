from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QFileDialog
)
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

class EntradaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parámetros del Script Creador Araña")

        layout = QFormLayout(self)

        # Campos de entrada
        self.esquema_placa = QLineEdit()
        self.esquema_mavvial = QLineEdit()
        self.capa_placa = QLineEdit()
        self.capa_mavvial = QLineEdit()
        self.campo_llave_placa = QLineEdit()
        self.campo_llave_mavvial = QLineEdit()

        layout.addRow("🔹 Esquema Placa:", self.esquema_placa)
        layout.addRow("🔹 Esquema Mavvial:", self.esquema_mavvial)
        layout.addRow("🔹 Capa Placa:", self.capa_placa)
        layout.addRow("🔹 Capa Mavvial:", self.capa_mavvial)
        layout.addRow("🔹 Campo Llave Placa:", self.campo_llave_placa)
        layout.addRow("🔹 Campo Llave Mavvial:", self.campo_llave_mavvial)

        # Botones
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addRow(botones)

    def get_values(self):
        return (
            self.esquema_placa.text().strip(),
            self.esquema_mavvial.text().strip(),
            self.capa_placa.text().strip(),
            self.capa_mavvial.text().strip(),
            self.campo_llave_placa.text().strip(),
            self.campo_llave_mavvial.text().strip()
        )

try:
    # ========= ENTRADA DE DATOS =========
    dlg = EntradaDialog()
    if dlg.exec_() != QDialog.Accepted:
        raise Exception("⚠️ Entrada cancelada por el usuario.")

    esquema_placa, esquema_mavvial, capa_placa, capa_mavvial, campo_llave_placa, campo_llave_mavvial = dlg.get_values()

    if not all([esquema_placa, esquema_mavvial, capa_placa, capa_mavvial, campo_llave_placa, campo_llave_mavvial]):
        raise Exception("⚠️ Todos los campos son obligatorios.")

    # ========= CARGA DEL SCRIPT =========
    mostrar_mensaje("Descargando", "📥 Descargando el script desde GitHub...")
    url_sql = "https://raw.githubusercontent.com/JhoinnerM07/Geoprocesos-LATAM/refs/heads/main/creador_ara%C3%B1a.sql"
    sql_crudo = requests.get(url_sql, verify=False).text

    # ========= ADAPTACIÓN =========
    sql_final = (sql_crudo
                 .replace("{esquema_placa}", esquema_placa)
                 .replace("{esquema_mavvial}", esquema_mavvial)
                 .replace("{capa_placa}", capa_placa)
                 .replace("{capa_mavvial}", capa_mavvial)
                 .replace("{campo_llave_placa}", campo_llave_placa)
                 .replace("{campo_llave_mavvial}", campo_llave_mavvial))

    mostrar_mensaje("Adaptación", "✅ Script adaptado con los valores ingresados.")

    # ========= GUARDADO =========
    mostrar_mensaje("Guardar", "📂 Seleccione dónde guardar el SQL adaptado.")
    ruta_salida, _ = QFileDialog.getSaveFileName(
        None,
        "Guardar script adaptado",
        os.path.expanduser("~"),
        "SQL Files (*.sql)"
    )
    if not ruta_salida:
        raise Exception("⚠️ No se seleccionó ninguna ruta de salida.")

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(sql_final)

    mostrar_mensaje("Completado", f"✅ Script guardado correctamente en:\n{ruta_salida}")

except Exception as e:
    mostrar_mensaje("❌ Error", str(e), icono=QMessageBox.Critical)
