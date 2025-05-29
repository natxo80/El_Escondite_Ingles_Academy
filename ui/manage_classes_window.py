from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
                               QLineEdit, QMessageBox, QHeaderView, QAbstractScrollArea, QAbstractItemView, QLabel)
from db.database import insert_class, fetch_classes, update_class, delete_class

class ManageClassesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionar Clases")  # Establece el título de la ventana
        self.setWindowIcon(QIcon("resources/el_escondite_ingles.bmp"))
        self.setGeometry(100, 100, 900, 800)     # Define tamaño y posición de la ventana
        self.init_ui()  # Inicializa la interfaz gráfica

    def init_ui(self):
        """Configura los elementos visuales de la ventana de gestión de clases"""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 30, 30, 30)  # Márgenes exteriores
        self.layout.setSpacing(15)  # Espaciado entre secciones

        # ---------- CABECERA VISUAL (Logo + Título) ----------
        header_layout = QHBoxLayout()

        self.logo = QLabel()
        self.logo.setPixmap("resources/el_escondite_ingles.jpg")  # Ruta al logo
        self.logo.setFixedSize(60, 60)
        self.logo.setScaledContents(True)
        header_layout.addWidget(self.logo)

        title = QLabel("Gestión de Clases - El Escondite Inglés")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4B0082;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.layout.addLayout(header_layout)
        # ------------------------------------------------------

        # ---------- TABLA DE CLASES ----------
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nombre", "Fecha", "Profesor"])

        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setStretchLastSection(True)

        self.layout.addWidget(self.table)
        # -------------------------------------

        # ---------- FORMULARIO DE ENTRADA ----------
        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre de la clase")
        form_layout.addWidget(self.name_input)

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Fecha (YYYY-MM-DD)")
        form_layout.addWidget(self.date_input)

        self.professor_input = QLineEdit()
        self.professor_input.setPlaceholderText("Profesor")
        form_layout.addWidget(self.professor_input)

        self.layout.addLayout(form_layout)
        # ------------------------------------------

        # ---------- BOTONES DE ACCIÓN ----------
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Añadir Clase")
        self.add_button.clicked.connect(self.add_class)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Editar Clase")
        self.edit_button.clicked.connect(self.edit_class)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Borrar Clase")
        self.delete_button.clicked.connect(self.delete_class)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)
        # -------------------------------------

        # Aplicamos el layout principal y cargamos datos
        self.setLayout(self.layout)
        self.load_classes()

    def load_classes(self):
        """Carga las clases desde la base de datos y actualiza la tabla."""
        self.table.setRowCount(0)  # Limpia la tabla
        classes = fetch_classes()  # Obtiene la lista de clases
        for row, c in enumerate(classes):
            self.table.insertRow(row)  # Añade una nueva fila
            self.table.setItem(row, 0, QTableWidgetItem(c[1]))  # Nombre
            self.table.setItem(row, 1, QTableWidgetItem(c[2]))  # Fecha
            self.table.setItem(row, 2, QTableWidgetItem(c[3]))  # Profesor

    def add_class(self):
        """Añade una nueva clase a la base de datos con los datos introducidos."""
        name = self.name_input.text().strip()  # Obtenemos el nombre de la clase ingresado
        date = self.date_input.text().strip()  # Obtenemos la fecha ingresada
        professor = self.professor_input.text().strip()  # Obtenemos el nombre del profesor

        # Validación: todos los campos deben estar llenos
        if not name or not date or not professor:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")  # Mostramos error
            return  # Cancelamos si falta algún campo

        # Validación: evitar clases duplicadas por nombre (ignorando mayúsculas/minúsculas)
        existing_names = [self.table.item(row, 0).text().lower() for row in range(self.table.rowCount())]
        if name.lower() in existing_names:
            QMessageBox.warning(self, "Error", f"La clase '{name}' ya existe.")  # Error si el nombre ya está en uso
            return

        insert_class(name, date, professor)  # Insertamos la clase en la base de datos
        self.clear_fields()  # Limpiamos los campos de entrada
        self.load_classes()  # Recargamos la tabla para mostrar la nueva clase

    def edit_class(self):
        """Edita una clase seleccionada con los nuevos datos introducidos."""
        row = self.table.currentRow()  # Obtenemos la fila seleccionada en la tabla
        if row == -1:
            QMessageBox.warning(self, "Error","Selecciona una clase para editar.")  # Mostramos error si no hay selección
            return

        new_name = self.name_input.text().strip()  # Nuevo nombre ingresado
        new_date = self.date_input.text().strip()  # Nueva fecha ingresada
        new_professor = self.professor_input.text().strip()  # Nuevo nombre del profesor

        # Validación: todos los campos deben estar llenos
        if not new_name or not new_date or not new_professor:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")  # Mostramos error
            return

        old_name = self.table.item(row, 0).text()  # Nombre anterior de la clase (de la tabla)

        # Validación: si cambió el nombre, asegurarnos de que no esté duplicado
        if new_name.lower() != old_name.lower():
            existing_names = [self.table.item(r, 0).text().lower() for r in range(self.table.rowCount())]
            if new_name.lower() in existing_names:
                QMessageBox.warning(self, "Error", f"La clase '{new_name}' ya existe.")  # Mostramos error si ya existe
                return

        update_class(old_name, new_name, new_date, new_professor)  # Actualizamos los datos en la base de datos
        self.clear_fields()  # Limpiamos los campos
        self.load_classes()  # Recargamos la tabla con los cambios

    def delete_class(self):
        """Elimina la clase seleccionada de la base de datos con confirmación y manejo de errores."""
        selected = self.table.currentRow()  # Fila seleccionada

        if selected != -1:
            name = self.table.item(selected, 0).text()  # Nombre de la clase a eliminar

            # Confirmación del usuario
            confirm = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Estás seguro de que deseas eliminar la clase '{name}'?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                try:
                    delete_class(name)  # Intentamos eliminar de la base de datos
                    self.load_classes()  # Recargamos la tabla
                    QMessageBox.information(self, "Clase eliminada",
                                            f"La clase '{name}' ha sido eliminada correctamente.")
                except Exception as e:
                    QMessageBox.critical(self, "Error al eliminar", f"No se pudo eliminar la clase:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Selecciona una clase para eliminar.")

    def clear_fields(self):
        """Limpia los campos de entrada."""
        self.name_input.clear()
        self.date_input.clear()
        self.professor_input.clear()