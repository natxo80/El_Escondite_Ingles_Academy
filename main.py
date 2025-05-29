import sys
from PySide2.QtWidgets import QApplication
from ui.login_window import LoginWindow
from db.database import create_tables, init_levels

if __name__ == "__main__":
    # Crear las tablas si no existen
    create_tables()

    # Llmamos a la función para insertar los niveles
    init_levels()

    app = QApplication(sys.argv)
    with open("resources/styles.qss", "r") as f:app.setStyleSheet(f.read()) # Cargar y aplicar estilo desde models/style.qss
    login_window = LoginWindow() # Inicializamos la ventana de login
    login_window.show()
    sys.exit(app.exec_())