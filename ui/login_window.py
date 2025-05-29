from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout
from db.database import connect_db

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Establecemos el título y las dimensiones de la ventana de login
        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon("resources/el_escondite_ingles.bmp"))
        self.setGeometry(100, 100, 400, 300)

        # Creamos el layout vertical donde se ubicarán los elementos de la interfaz
        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(30, 30, 30, 30)  # Márgenes exteriores
        self.layout.setSpacing(15)  # Espaciado entre secciones

        # ---------- CABECERA VISUAL (Logo + Título) ----------
        header_layout = QHBoxLayout()

        self.logo = QLabel()
        self.logo.setPixmap("resources/el_escondite_ingles.jpg")  # Asegúrate de que la ruta es correcta
        self.logo.setFixedSize(60, 60)
        self.logo.setScaledContents(True)
        header_layout.addWidget(self.logo)

        title = QLabel("Gestión de Alumnos - El Escondite Inglés")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4B0082;")  # Morado elegante
        header_layout.addWidget(title)
        header_layout.addStretch()
        self.layout.addLayout(header_layout)
        # -----------------------------------------------------

        # Creamos el campo de texto para el nombre de usuario
        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Usuario')  # Texto de ejemplo que aparece en el campo
        self.layout.addWidget(self.username)

        # Creamos el campo de texto para la contraseña (con texto oculto)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)  # Configuramos para que se oculte el texto
        self.password.setPlaceholderText('Contraseña')  # Texto de ejemplo para la contraseña
        self.layout.addWidget(self.password)

        # Creamos el botón de login y lo conectamos al metodo 'authenticate'
        self.login_button = QPushButton('Iniciar sesión', self)
        self.login_button.clicked.connect(self.authenticate)  # Al hacer clic, ejecuta el metodo authenticate
        self.layout.addWidget(self.login_button)

        # Asignamos el layout al widget principal de la ventana
        self.setLayout(self.layout)

    def authenticate(self):
        """Este metodo se ejecuta cuando el usuario hace clic en el botón de login"""
        username = self.username.text()  # Obtenemos el texto del campo de nombre de usuario
        password = self.password.text()  # Obtenemos el texto del campo de contraseña

        # Verificamos las credenciales llamando a la base de datos
        if self.check_credentials(username, password):
            # Si las credenciales son correctas, mostramos la ventana principal
            from ui.main_window import MainWindow  # Importamos MainWindow solo cuando sea necesario para evitar importaciones circulares
            username, role = self.check_credentials(username, password)
            self.main_window = MainWindow(username, role)  # Creamos la ventana principal
            self.main_window.show()  # Mostramos la ventana principal
            self.close()  # Cerramos la ventana de login
        else:
            # Si las credenciales son incorrectas, mostramos un mensaje de error
            QMessageBox.warning(self, 'Error', 'Usuario o contraseña incorrectos')

    def check_credentials(self, username, password):
        """Verifica si el nombre de usuario y la contraseña existen en la base de datos"""
        conn = connect_db()  # Conectamos a la base de datos
        cursor = conn.cursor()

        # Realizamos una consulta para verificar si existe un usuario con el nombre y la contraseña proporcionados
        cursor.execute('SELECT username, role FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()  # Si encontramos un usuario, obtenemos los datos del mismo

        # Cerramos la conexión a la base de datos
        conn.close()

        # Devuelve (username, role) si existe, sino None
        return user