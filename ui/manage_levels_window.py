from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
                               QLineEdit,
                               QMessageBox, QHeaderView, QAbstractScrollArea, QAbstractItemView, QLabel)
from db.database import fetch_levels, insert_level, delete_level, update_level

class ManageLevelsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionar Niveles")  # Título de la ventana
        self.setWindowIcon(QIcon("resources/el_escondite_ingles.bmp"))
        self.setGeometry(100, 100, 400, 600)  # Posición y tamaño de la ventana
        self.init_ui()  # Inicializar la interfaz de usuario

    def init_ui(self):
        """Configura los elementos visuales de la ventana"""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 30, 30, 30)  # Márgenes exteriores
        self.layout.setSpacing(15)  # Espaciado entre bloques

        # ---------- CABECERA VISUAL (Logo + Título) ----------
        header_layout = QHBoxLayout()

        self.logo = QLabel()
        self.logo.setPixmap("resources/el_escondite_ingles.jpg")  # Asegúrate de que el archivo exista
        self.logo.setFixedSize(60, 60)
        self.logo.setScaledContents(True)
        header_layout.addWidget(self.logo)

        title = QLabel("Gestión de Niveles - El Escondite Inglés")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4B0082;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.layout.addLayout(header_layout)
        # -----------------------------------------------------

        # ---------- TABLA DE NIVELES ----------
        self.table = QTableWidget()
        self.table.setColumnCount(1)  # Solo una columna: nombre del nivel
        self.table.setHorizontalHeaderLabels(["Nivel"])
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setStretchLastSection(True)

        self.layout.addWidget(self.table)
        # --------------------------------------

        # ---------- FORMULARIO + BOTONES ----------
        button_layout = QHBoxLayout()

        self.level_input = QLineEdit()
        self.level_input.setPlaceholderText("Introduce el nivel (ej: A1, B2_Ad)")
        button_layout.addWidget(self.level_input)

        self.add_button = QPushButton("Añadir Nivel")
        self.add_button.clicked.connect(self.add_level)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Editar Nivel")
        self.edit_button.clicked.connect(self.edit_level)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Borrar Nivel")
        self.delete_button.clicked.connect(self.delete_level)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        # ---------- CARGA INICIAL DE DATOS ----------
        self.load_levels()

    def load_levels(self):
        """Carga los niveles desde la base de datos y los muestra en la tabla"""
        self.table.setRowCount(0)  # Limpiamos la tabla antes de llenarla
        levels = fetch_levels()  # Obtenemos los niveles desde la base de datos
        for row, level in enumerate(levels):
            self.table.insertRow(row)  # Insertamos una nueva fila
            self.table.setItem(row, 0, QTableWidgetItem(level[1]))  # Mostramos el nombre del nivel

    def add_level(self):
        """Añade un nuevo nivel a la base de datos"""
        level_name = self.level_input.text().strip()  # Obtenemos y limpiamos el texto ingresado

        # Validación: el campo no puede estar vacío
        if not level_name:
            QMessageBox.warning(self, "Error", "El campo de nivel no puede estar vacío.")  # Mostramos error
            return  # Salimos del metodo si no hay texto

        # Validación: evitar duplicados (comparando con todos los valores actuales de la tabla)
        existing_levels = [self.table.item(row, 0).text().lower() for row in range(self.table.rowCount())]
        if level_name.lower() in existing_levels:
            QMessageBox.warning(self, "Error", f"El nivel '{level_name}' ya existe.")  # Mostramos error si ya existe
            return  # Cancelamos la acción

        insert_level(level_name)  # Insertamos el nuevo nivel en la base de datos
        self.level_input.clear()  # Limpiamos el campo de texto
        self.load_levels()  # Recargamos la tabla para mostrar el nuevo nivel

    def delete_level(self):
        """Borra el nivel seleccionado de la tabla y base de datos con confirmación y control de errores"""
        selected = self.table.currentRow()  # Obtenemos la fila seleccionada

        if selected != -1:
            level_name = self.table.item(selected, 0).text()  # Nombre del nivel

            # Confirmación del usuario
            confirm = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Estás seguro de que deseas eliminar el nivel '{level_name}'?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                try:
                    delete_level(level_name)  # Intentamos eliminar
                    self.load_levels()  # Recargamos la tabla
                    QMessageBox.information(self, "Nivel eliminado",
                                            f"El nivel '{level_name}' ha sido eliminado correctamente.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el nivel:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Selecciona un nivel para eliminar.")

    def edit_level(self):
        """Edita el nombre del nivel seleccionado con validación"""
        selected = self.table.currentRow()  # Obtenemos la fila actualmente seleccionada de la tabla
        new_name = self.level_input.text().strip()  # Obtenemos el nuevo nombre que el usuario ingresó

        # Validación: debe haber una fila seleccionada
        if selected == -1:
            QMessageBox.warning(self, "Error", "Selecciona un nivel para editar.")  # Si no hay selección, avisamos
            return

        # Validación: el nuevo nombre no puede estar vacío
        if not new_name:
            QMessageBox.warning(self, "Error", "El campo de nivel no puede estar vacío.")  # Mostramos error
            return

        old_name = self.table.item(selected, 0).text()  # Obtenemos el nombre actual del nivel seleccionado

        # Validación: si el nombre cambió, asegurarnos de que no haya duplicados
        if new_name.lower() != old_name.lower():
            existing_levels = [self.table.item(row, 0).text().lower() for row in range(self.table.rowCount())]
            if new_name.lower() in existing_levels:
                QMessageBox.warning(self, "Error", f"El nivel '{new_name}' ya existe.")  # Mostramos error si existe
                return

        update_level(old_name, new_name)  # Actualizamos el nivel en la base de datos
        self.level_input.clear()          # Limpiamos el campo de texto
        self.load_levels()                # Recargamos la tabla con el cambio actualizado