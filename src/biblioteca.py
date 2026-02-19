"""
Sistema de Gestión de Biblioteca - Talento Solutions
Proyecto Piloto con IA

Módulo principal que contiene las clases y funciones para gestionar
una biblioteca: registro de libros, préstamos y devoluciones.

Autor: Asistente IA (Claude) + Talento Solutions
Fecha: 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import json
import os


# =============================================================================
# CLASE LIBRO
# =============================================================================
class Libro:
    """
    Representa un libro dentro del sistema de biblioteca.

    Attributes:
        titulo (str): Título del libro.
        autor (str): Autor del libro.
        isbn (str): Código ISBN único del libro.
        genero (str): Género literario.
        disponible (bool): Indica si el libro está disponible para préstamo.
        fecha_prestamo (str | None): Fecha en que fue prestado (ISO format).
        fecha_devolucion (str | None): Fecha límite de devolución (ISO format).
        prestatario (str | None): Nombre de la persona que tiene el libro.
    """

    def __init__(self, titulo: str, autor: str, isbn: str, genero: str = "General"):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.genero = genero
        self.disponible = True
        self.fecha_prestamo = None
        self.fecha_devolucion = None
        self.prestatario = None

    def __str__(self):
        estado = "Disponible" if self.disponible else f"Prestado a {self.prestatario}"
        return f"[{self.isbn}] '{self.titulo}' de {self.autor} - {estado}"

    def __repr__(self):
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}', isbn='{self.isbn}')"

    def to_dict(self) -> dict:
        """Convierte el libro a un diccionario para serialización JSON."""
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "genero": self.genero,
            "disponible": self.disponible,
            "fecha_prestamo": self.fecha_prestamo,
            "fecha_devolucion": self.fecha_devolucion,
            "prestatario": self.prestatario,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Libro":
        """Crea una instancia de Libro a partir de un diccionario."""
        libro = cls(datos["titulo"], datos["autor"], datos["isbn"], datos.get("genero", "General"))
        libro.disponible = datos.get("disponible", True)
        libro.fecha_prestamo = datos.get("fecha_prestamo")
        libro.fecha_devolucion = datos.get("fecha_devolucion")
        libro.prestatario = datos.get("prestatario")
        return libro


# =============================================================================
# FUNCIONES DE PRÉSTAMO Y DEVOLUCIÓN
# =============================================================================

def prestar_libro(libro: Libro, prestatario: str, dias_prestamo: int = 14) -> bool:
    """
    Realiza el préstamo de un libro a un prestatario.

    Args:
        libro: Instancia de Libro a prestar.
        prestatario: Nombre completo de quien recibe el libro.
        dias_prestamo: Número de días del préstamo (por defecto 14).

    Returns:
        True si el préstamo fue exitoso, False si el libro no está disponible.

    Raises:
        ValueError: Si el nombre del prestatario está vacío.
    """
    if not prestatario or not prestatario.strip():
        raise ValueError("El nombre del prestatario no puede estar vacío.")

    if not libro.disponible:
        return False

    libro.disponible = False
    libro.prestatario = prestatario.strip()
    libro.fecha_prestamo = datetime.now().isoformat()
    libro.fecha_devolucion = (datetime.now() + timedelta(days=dias_prestamo)).isoformat()
    return True


def devolver_libro(libro: Libro) -> bool:
    """
    Registra la devolución de un libro prestado.

    Args:
        libro: Instancia de Libro a devolver.

    Returns:
        True si la devolución fue exitosa, False si el libro ya estaba disponible.
    """
    if libro.disponible:
        return False

    libro.disponible = True
    libro.prestatario = None
    libro.fecha_prestamo = None
    libro.fecha_devolucion = None
    return True


# =============================================================================
# CLASE BIBLIOTECA (Gestión completa)
# =============================================================================
class Biblioteca:
    """
    Gestiona una colección de libros con funcionalidades de búsqueda,
    préstamo, devolución y persistencia en archivo JSON.
    """

    ARCHIVO_DATOS = "datos_biblioteca.json"

    def __init__(self):
        self.libros: list[Libro] = []
        self.cargar_datos()

    # -- CRUD de libros -------------------------------------------------------

    def agregar_libro(self, titulo: str, autor: str, isbn: str, genero: str = "General") -> Libro:
        """Agrega un nuevo libro a la colección."""
        if self.buscar_por_isbn(isbn):
            raise ValueError(f"Ya existe un libro con ISBN '{isbn}'.")
        libro = Libro(titulo, autor, isbn, genero)
        self.libros.append(libro)
        self.guardar_datos()
        return libro

    def eliminar_libro(self, isbn: str) -> bool:
        """Elimina un libro por su ISBN."""
        libro = self.buscar_por_isbn(isbn)
        if libro and libro.disponible:
            self.libros.remove(libro)
            self.guardar_datos()
            return True
        return False

    # -- Búsquedas ------------------------------------------------------------

    def buscar_por_isbn(self, isbn: str) -> Libro | None:
        """Busca un libro por su ISBN."""
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        return None

    def buscar_por_titulo(self, titulo: str) -> list[Libro]:
        """Busca libros cuyo título contenga el texto indicado (case-insensitive)."""
        titulo_lower = titulo.lower()
        return [l for l in self.libros if titulo_lower in l.titulo.lower()]

    def buscar_por_autor(self, autor: str) -> list[Libro]:
        """Busca libros cuyo autor contenga el texto indicado (case-insensitive)."""
        autor_lower = autor.lower()
        return [l for l in self.libros if autor_lower in l.autor.lower()]

    def listar_disponibles(self) -> list[Libro]:
        """Retorna todos los libros disponibles para préstamo."""
        return [l for l in self.libros if l.disponible]

    def listar_prestados(self) -> list[Libro]:
        """Retorna todos los libros actualmente prestados."""
        return [l for l in self.libros if not l.disponible]

    # -- Préstamo / Devolución ------------------------------------------------

    def prestar(self, isbn: str, prestatario: str, dias: int = 14) -> bool:
        """Presta un libro identificado por ISBN."""
        libro = self.buscar_por_isbn(isbn)
        if libro is None:
            raise ValueError(f"No se encontró un libro con ISBN '{isbn}'.")
        resultado = prestar_libro(libro, prestatario, dias)
        if resultado:
            self.guardar_datos()
        return resultado

    def devolver(self, isbn: str) -> bool:
        """Devuelve un libro identificado por ISBN."""
        libro = self.buscar_por_isbn(isbn)
        if libro is None:
            raise ValueError(f"No se encontró un libro con ISBN '{isbn}'.")
        resultado = devolver_libro(libro)
        if resultado:
            self.guardar_datos()
        return resultado

    # -- Persistencia ---------------------------------------------------------

    def guardar_datos(self):
        """Guarda la colección de libros en un archivo JSON."""
        datos = [libro.to_dict() for libro in self.libros]
        with open(self.ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def cargar_datos(self):
        """Carga la colección de libros desde un archivo JSON."""
        if os.path.exists(self.ARCHIVO_DATOS):
            with open(self.ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                datos = json.load(f)
                self.libros = [Libro.from_dict(d) for d in datos]

    # -- Estadísticas ---------------------------------------------------------

    def estadisticas(self) -> dict:
        """Retorna un diccionario con estadísticas de la biblioteca."""
        total = len(self.libros)
        disponibles = len(self.listar_disponibles())
        prestados = len(self.listar_prestados())
        generos = {}
        for libro in self.libros:
            generos[libro.genero] = generos.get(libro.genero, 0) + 1
        return {
            "total": total,
            "disponibles": disponibles,
            "prestados": prestados,
            "generos": generos,
        }


# =============================================================================
# INTERFAZ GRÁFICA CON TKINTER
# =============================================================================
class BibliotecaGUI:
    """Interfaz gráfica para el Sistema de Gestión de Biblioteca."""

    def __init__(self):
        self.biblioteca = Biblioteca()
        self._crear_datos_ejemplo()

        # -- Ventana principal ------------------------------------------------
        self.root = tk.Tk()
        self.root.title("📚 Sistema de Gestión de Biblioteca — Talento Solutions")
        self.root.geometry("1050x680")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(True, True)

        self._crear_estilos()
        self._crear_widgets()
        self._actualizar_tabla()
        self._actualizar_estadisticas()

    # --------------------------------------------------------------------- #
    #  Datos de ejemplo                                                      #
    # --------------------------------------------------------------------- #
    def _crear_datos_ejemplo(self):
        """Carga libros de ejemplo si la biblioteca está vacía."""
        if len(self.biblioteca.libros) > 0:
            return
        ejemplos = [
            ("Cien años de soledad", "Gabriel García Márquez", "978-0-06-088328-7", "Novela"),
            ("Don Quijote de la Mancha", "Miguel de Cervantes", "978-84-376-0494-7", "Clásico"),
            ("El Principito", "Antoine de Saint-Exupéry", "978-0-15-601219-5", "Infantil"),
            ("1984", "George Orwell", "978-0-451-52493-5", "Ciencia Ficción"),
            ("Rayuela", "Julio Cortázar", "978-84-376-0602-6", "Novela"),
            ("La sombra del viento", "Carlos Ruiz Zafón", "978-84-08-04171-3", "Misterio"),
            ("Crónica de una muerte anunciada", "Gabriel García Márquez", "978-84-376-0781-8", "Novela"),
            ("Harry Potter y la piedra filosofal", "J.K. Rowling", "978-84-7888-445-8", "Fantasía"),
        ]
        for titulo, autor, isbn, genero in ejemplos:
            try:
                self.biblioteca.agregar_libro(titulo, autor, isbn, genero)
            except ValueError:
                pass

    # --------------------------------------------------------------------- #
    #  Estilos                                                               #
    # --------------------------------------------------------------------- #
    def _crear_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"),
                             background="#1e3a5f", foreground="white")
        self.style.configure("Stats.TLabel", font=("Segoe UI", 11),
                             background="#e8f0fe", padding=8)
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.style.configure("Action.TButton", font=("Segoe UI", 10), padding=6)

    # --------------------------------------------------------------------- #
    #  Widgets                                                               #
    # --------------------------------------------------------------------- #
    def _crear_widgets(self):
        # -- Header -----------------------------------------------------------
        header = tk.Frame(self.root, bg="#1e3a5f", height=60)
        header.pack(fill="x")
        tk.Label(header, text="  📚  Sistema de Gestión de Biblioteca",
                 font=("Segoe UI", 18, "bold"), bg="#1e3a5f", fg="white").pack(
            side="left", padx=10, pady=12)
        tk.Label(header, text="Talento Solutions — Proyecto Piloto IA  ",
                 font=("Segoe UI", 10), bg="#1e3a5f", fg="#a0c4ff").pack(
            side="right", padx=10, pady=12)

        # -- Contenedor principal ---------------------------------------------
        main = tk.Frame(self.root, bg="#f0f4f8")
        main.pack(fill="both", expand=True, padx=16, pady=10)

        # -- Panel izquierdo (botones) ----------------------------------------
        panel_izq = tk.Frame(main, bg="#f0f4f8", width=200)
        panel_izq.pack(side="left", fill="y", padx=(0, 12))

        tk.Label(panel_izq, text="Acciones", font=("Segoe UI", 13, "bold"),
                 bg="#f0f4f8", fg="#1e3a5f").pack(pady=(0, 8))

        botones = [
            ("➕  Agregar Libro", self._agregar_libro),
            ("🔍  Buscar Libro", self._buscar_libro),
            ("📤  Prestar Libro", self._prestar_libro),
            ("📥  Devolver Libro", self._devolver_libro),
            ("🗑️  Eliminar Libro", self._eliminar_libro),
            ("📊  Ver Estadísticas", self._ver_estadisticas),
            ("🔄  Actualizar Lista", self._actualizar_tabla),
        ]
        for texto, comando in botones:
            btn = tk.Button(panel_izq, text=texto, command=comando,
                            font=("Segoe UI", 10), bg="#ffffff", fg="#1e3a5f",
                            activebackground="#d0e0f0", relief="groove",
                            width=20, anchor="w", padx=8, pady=4, cursor="hand2")
            btn.pack(pady=3, fill="x")

        # -- Panel derecho (tabla + estadísticas) -----------------------------
        panel_der = tk.Frame(main, bg="#f0f4f8")
        panel_der.pack(side="left", fill="both", expand=True)

        # Estadísticas rápidas
        self.stats_frame = tk.Frame(panel_der, bg="#e8f0fe", relief="groove", bd=1)
        self.stats_frame.pack(fill="x", pady=(0, 8))
        self.lbl_stats = tk.Label(self.stats_frame, text="", font=("Segoe UI", 10),
                                  bg="#e8f0fe", fg="#1e3a5f", pady=6, padx=10)
        self.lbl_stats.pack(fill="x")

        # Barra de búsqueda
        search_frame = tk.Frame(panel_der, bg="#f0f4f8")
        search_frame.pack(fill="x", pady=(0, 6))
        tk.Label(search_frame, text="🔎 Filtro rápido:", bg="#f0f4f8",
                 font=("Segoe UI", 10)).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filtrar_tabla())
        tk.Entry(search_frame, textvariable=self.search_var, width=40,
                 font=("Segoe UI", 10)).pack(side="left", padx=6)

        # Treeview
        cols = ("isbn", "titulo", "autor", "genero", "estado", "prestatario")
        self.tree = ttk.Treeview(panel_der, columns=cols, show="headings", height=18)
        encabezados = {"isbn": "ISBN", "titulo": "Título", "autor": "Autor",
                       "genero": "Género", "estado": "Estado", "prestatario": "Prestatario"}
        anchos = {"isbn": 160, "titulo": 220, "autor": 170, "genero": 100,
                  "estado": 90, "prestatario": 120}
        for col in cols:
            self.tree.heading(col, text=encabezados[col])
            self.tree.column(col, width=anchos[col], minwidth=60)

        scrollbar = ttk.Scrollbar(panel_der, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        # -- Footer -----------------------------------------------------------
        footer = tk.Frame(self.root, bg="#1e3a5f", height=30)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="Desarrollado con apoyo de IA • Talento Solutions © 2025",
                 font=("Segoe UI", 9), bg="#1e3a5f", fg="#a0c4ff").pack(pady=4)

    # --------------------------------------------------------------------- #
    #  Acciones                                                              #
    # --------------------------------------------------------------------- #
    def _actualizar_tabla(self, libros=None):
        """Refresca el contenido del Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        lista = libros if libros is not None else self.biblioteca.libros
        for libro in lista:
            estado = "✅ Disp." if libro.disponible else "📕 Prest."
            prestatario = libro.prestatario or "—"
            self.tree.insert("", "end", values=(
                libro.isbn, libro.titulo, libro.autor,
                libro.genero, estado, prestatario))
        self._actualizar_estadisticas()

    def _actualizar_estadisticas(self):
        stats = self.biblioteca.estadisticas()
        self.lbl_stats.config(
            text=f"📚 Total: {stats['total']}   |   "
                 f"✅ Disponibles: {stats['disponibles']}   |   "
                 f"📕 Prestados: {stats['prestados']}"
        )

    def _filtrar_tabla(self):
        texto = self.search_var.get().lower()
        if not texto:
            self._actualizar_tabla()
            return
        filtrados = [l for l in self.biblioteca.libros
                     if texto in l.titulo.lower()
                     or texto in l.autor.lower()
                     or texto in l.isbn.lower()
                     or texto in l.genero.lower()]
        self._actualizar_tabla(filtrados)

    def _agregar_libro(self):
        win = tk.Toplevel(self.root)
        win.title("Agregar Libro")
        win.geometry("400x300")
        win.configure(bg="#f0f4f8")
        win.grab_set()

        campos = {}
        for i, (lbl, key) in enumerate([("Título:", "titulo"), ("Autor:", "autor"),
                                         ("ISBN:", "isbn"), ("Género:", "genero")]):
            tk.Label(win, text=lbl, bg="#f0f4f8", font=("Segoe UI", 10)).grid(
                row=i, column=0, padx=12, pady=8, sticky="e")
            entry = tk.Entry(win, width=30, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, padx=12, pady=8)
            campos[key] = entry

        def guardar():
            titulo = campos["titulo"].get().strip()
            autor = campos["autor"].get().strip()
            isbn = campos["isbn"].get().strip()
            genero = campos["genero"].get().strip() or "General"
            if not titulo or not autor or not isbn:
                messagebox.showwarning("Campos vacíos", "Título, Autor e ISBN son obligatorios.", parent=win)
                return
            try:
                self.biblioteca.agregar_libro(titulo, autor, isbn, genero)
                messagebox.showinfo("Éxito", f"Libro '{titulo}' agregado correctamente.", parent=win)
                win.destroy()
                self._actualizar_tabla()
            except ValueError as e:
                messagebox.showerror("Error", str(e), parent=win)

        tk.Button(win, text="💾 Guardar", command=guardar, font=("Segoe UI", 10, "bold"),
                  bg="#1e3a5f", fg="white", padx=16, pady=4).grid(row=4, column=0,
                                                                    columnspan=2, pady=16)

    def _buscar_libro(self):
        texto = simpledialog.askstring("Buscar Libro",
                                       "Ingrese título, autor o ISBN a buscar:",
                                       parent=self.root)
        if texto:
            self.search_var.set(texto)

    def _prestar_libro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Seleccione", "Seleccione un libro de la tabla primero.")
            return
        valores = self.tree.item(seleccion[0], "values")
        isbn = valores[0]
        libro = self.biblioteca.buscar_por_isbn(isbn)
        if not libro:
            return
        if not libro.disponible:
            messagebox.showwarning("No disponible",
                                   f"El libro ya está prestado a '{libro.prestatario}'.")
            return
        prestatario = simpledialog.askstring("Préstamo",
                                             f"¿A quién se presta '{libro.titulo}'?",
                                             parent=self.root)
        if prestatario:
            try:
                self.biblioteca.prestar(isbn, prestatario)
                messagebox.showinfo("Préstamo exitoso",
                                    f"'{libro.titulo}' prestado a {prestatario}.")
                self._actualizar_tabla()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def _devolver_libro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Seleccione", "Seleccione un libro de la tabla primero.")
            return
        valores = self.tree.item(seleccion[0], "values")
        isbn = valores[0]
        libro = self.biblioteca.buscar_por_isbn(isbn)
        if not libro:
            return
        if libro.disponible:
            messagebox.showinfo("Info", "Este libro ya está disponible, no necesita devolución.")
            return
        if messagebox.askyesno("Confirmar devolución",
                               f"¿Confirmar devolución de '{libro.titulo}'?"):
            self.biblioteca.devolver(isbn)
            messagebox.showinfo("Devolución exitosa", f"'{libro.titulo}' devuelto correctamente.")
            self._actualizar_tabla()

    def _eliminar_libro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Seleccione", "Seleccione un libro de la tabla primero.")
            return
        valores = self.tree.item(seleccion[0], "values")
        isbn = valores[0]
        libro = self.biblioteca.buscar_por_isbn(isbn)
        if not libro:
            return
        if not libro.disponible:
            messagebox.showwarning("No se puede eliminar",
                                   "No se puede eliminar un libro que está prestado.")
            return
        if messagebox.askyesno("Confirmar eliminación",
                               f"¿Eliminar '{libro.titulo}' de la biblioteca?"):
            self.biblioteca.eliminar_libro(isbn)
            messagebox.showinfo("Eliminado", "Libro eliminado correctamente.")
            self._actualizar_tabla()

    def _ver_estadisticas(self):
        stats = self.biblioteca.estadisticas()
        generos_txt = "\n".join(f"    • {g}: {c}" for g, c in stats["generos"].items())
        msg = (f"📊 Estadísticas de la Biblioteca\n"
               f"{'─' * 35}\n"
               f"📚 Total de libros: {stats['total']}\n"
               f"✅ Disponibles: {stats['disponibles']}\n"
               f"📕 Prestados: {stats['prestados']}\n\n"
               f"📂 Libros por género:\n{generos_txt}")
        messagebox.showinfo("Estadísticas", msg)

    # --------------------------------------------------------------------- #
    #  Ejecución                                                             #
    # --------------------------------------------------------------------- #
    def ejecutar(self):
        """Inicia el bucle principal de la interfaz gráfica."""
        self.root.mainloop()


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    app = BibliotecaGUI()
    app.ejecutar()
