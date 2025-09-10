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
        self.setWindowTitle("Parámetros del Script Identificar Dangles")

        layout = QFormLayout(self)

        # Campos de entrada
        self.esquema = QLineEdit()
        self.capa = QLineEdit()

        layout.addRow("🔹 Esquema:", self.esquema)
        layout.addRow("🔹 Capa:", self.capa)

        # Botones Aceptar / Cancelar
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addRow(botones)

    def get_values(self):
        return (
            self.esquema.text().strip(),
            self.capa.text().strip()
        )

try:
    # ========= ENTRADA DE DATOS =========
    dlg = EntradaDialog()
    if dlg.exec_() != QDialog.Accepted:
        raise Exception("⚠️ Entrada cancelada por el usuario.")

    esquema, capa = dlg.get_values()

    if not all([esquema, capa]):
        raise Exception("⚠️ Todos los campos son obligatorios.")

    # ========= CARGA DEL SCRIPT =========
    mostrar_mensaje("Descargando", "📥 Descargando el script desde GitHub...")
    url_sql = "https://raw.githubusercontent.com/JhoinnerM07/Geoprocesos-LATAM/refs/heads/main/identificar_dangles.sql"
    sql_crudo = requests.get(url_sql, verify=False).text

    # ========= ADAPTACIÓN =========
    sql_final = (sql_crudo
                 .replace("{esquema}", esquema)
                 .replace("{capa}", capa))

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
