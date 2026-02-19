"""
Tests unitarios para el Sistema de Gestión de Biblioteca.
Se prueban las clases Libro, Biblioteca y las funciones de préstamo/devolución.

Ejecutar con:  python -m pytest tests/test_biblioteca.py -v
"""

import sys
import os
import unittest

# Agregar el directorio raíz al path para importar src.biblioteca
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.biblioteca import Libro, Biblioteca, prestar_libro, devolver_libro


class TestLibro(unittest.TestCase):
    """Tests para la clase Libro."""

    def setUp(self):
        """Prepara un libro de prueba antes de cada test."""
        self.libro = Libro("Test Title", "Test Author", "978-0-00-000000-0", "Ficción")

    def test_creacion_libro(self):
        """Verifica que un libro se crea con los atributos correctos."""
        self.assertEqual(self.libro.titulo, "Test Title")
        self.assertEqual(self.libro.autor, "Test Author")
        self.assertEqual(self.libro.isbn, "978-0-00-000000-0")
        self.assertEqual(self.libro.genero, "Ficción")
        self.assertTrue(self.libro.disponible)
        self.assertIsNone(self.libro.prestatario)

    def test_genero_por_defecto(self):
        """Verifica que el género por defecto es 'General'."""
        libro = Libro("Libro Sin Género", "Autor", "111")
        self.assertEqual(libro.genero, "General")

    def test_str_disponible(self):
        """Verifica la representación en string cuando está disponible."""
        texto = str(self.libro)
        self.assertIn("Disponible", texto)
        self.assertIn("Test Title", texto)

    def test_str_prestado(self):
        """Verifica la representación en string cuando está prestado."""
        self.libro.disponible = False
        self.libro.prestatario = "Juan Pérez"
        texto = str(self.libro)
        self.assertIn("Prestado a Juan Pérez", texto)

    def test_to_dict(self):
        """Verifica la serialización a diccionario."""
        d = self.libro.to_dict()
        self.assertEqual(d["titulo"], "Test Title")
        self.assertEqual(d["isbn"], "978-0-00-000000-0")
        self.assertTrue(d["disponible"])

    def test_from_dict(self):
        """Verifica la deserialización desde diccionario."""
        d = self.libro.to_dict()
        libro2 = Libro.from_dict(d)
        self.assertEqual(libro2.titulo, self.libro.titulo)
        self.assertEqual(libro2.isbn, self.libro.isbn)
        self.assertEqual(libro2.disponible, self.libro.disponible)

    def test_round_trip_dict(self):
        """Verifica que serializar y deserializar produce un libro equivalente."""
        prestar_libro(self.libro, "Ana López")
        d = self.libro.to_dict()
        libro2 = Libro.from_dict(d)
        self.assertEqual(libro2.prestatario, "Ana López")
        self.assertFalse(libro2.disponible)


class TestPrestarLibro(unittest.TestCase):
    """Tests para la función prestar_libro."""

    def setUp(self):
        self.libro = Libro("Libro de Prueba", "Autor", "001")

    def test_prestamo_exitoso(self):
        """Verifica que un préstamo exitoso retorna True."""
        resultado = prestar_libro(self.libro, "Carlos García")
        self.assertTrue(resultado)
        self.assertFalse(self.libro.disponible)
        self.assertEqual(self.libro.prestatario, "Carlos García")
        self.assertIsNotNone(self.libro.fecha_prestamo)
        self.assertIsNotNone(self.libro.fecha_devolucion)

    def test_prestamo_libro_no_disponible(self):
        """Verifica que no se puede prestar un libro ya prestado."""
        prestar_libro(self.libro, "Persona 1")
        resultado = prestar_libro(self.libro, "Persona 2")
        self.assertFalse(resultado)
        self.assertEqual(self.libro.prestatario, "Persona 1")

    def test_prestamo_prestatario_vacio(self):
        """Verifica que lanza ValueError si el prestatario está vacío."""
        with self.assertRaises(ValueError):
            prestar_libro(self.libro, "")

    def test_prestamo_prestatario_solo_espacios(self):
        """Verifica que lanza ValueError si el prestatario son solo espacios."""
        with self.assertRaises(ValueError):
            prestar_libro(self.libro, "   ")

    def test_prestamo_strip_nombre(self):
        """Verifica que se eliminan espacios extra del nombre."""
        prestar_libro(self.libro, "  María López  ")
        self.assertEqual(self.libro.prestatario, "María López")


class TestDevolverLibro(unittest.TestCase):
    """Tests para la función devolver_libro."""

    def setUp(self):
        self.libro = Libro("Libro de Prueba", "Autor", "002")

    def test_devolucion_exitosa(self):
        """Verifica que una devolución exitosa retorna True."""
        prestar_libro(self.libro, "Juan")
        resultado = devolver_libro(self.libro)
        self.assertTrue(resultado)
        self.assertTrue(self.libro.disponible)
        self.assertIsNone(self.libro.prestatario)
        self.assertIsNone(self.libro.fecha_prestamo)

    def test_devolucion_libro_disponible(self):
        """Verifica que no se puede devolver un libro que ya está disponible."""
        resultado = devolver_libro(self.libro)
        self.assertFalse(resultado)

    def test_ciclo_prestamo_devolucion(self):
        """Verifica un ciclo completo de préstamo y devolución."""
        self.assertTrue(self.libro.disponible)
        prestar_libro(self.libro, "Ana")
        self.assertFalse(self.libro.disponible)
        devolver_libro(self.libro)
        self.assertTrue(self.libro.disponible)
        prestar_libro(self.libro, "Pedro")
        self.assertFalse(self.libro.disponible)
        self.assertEqual(self.libro.prestatario, "Pedro")


class TestBiblioteca(unittest.TestCase):
    """Tests para la clase Biblioteca."""

    def setUp(self):
        """Crea una biblioteca limpia para cada test."""
        self.bib = Biblioteca()
        self.bib.libros = []  # Vaciar para tests
        self.bib.ARCHIVO_DATOS = "test_datos_temp.json"

    def tearDown(self):
        """Limpia archivos temporales."""
        if os.path.exists("test_datos_temp.json"):
            os.remove("test_datos_temp.json")

    def test_agregar_libro(self):
        """Verifica que se puede agregar un libro."""
        libro = self.bib.agregar_libro("Test", "Autor", "100")
        self.assertEqual(len(self.bib.libros), 1)
        self.assertEqual(libro.titulo, "Test")

    def test_agregar_isbn_duplicado(self):
        """Verifica que no se permite ISBN duplicado."""
        self.bib.agregar_libro("Test 1", "Autor", "100")
        with self.assertRaises(ValueError):
            self.bib.agregar_libro("Test 2", "Otro Autor", "100")

    def test_buscar_por_isbn(self):
        """Verifica la búsqueda por ISBN."""
        self.bib.agregar_libro("Libro A", "Autor A", "AAA")
        resultado = self.bib.buscar_por_isbn("AAA")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.titulo, "Libro A")

    def test_buscar_isbn_inexistente(self):
        """Verifica que retorna None si el ISBN no existe."""
        resultado = self.bib.buscar_por_isbn("NOEXISTE")
        self.assertIsNone(resultado)

    def test_buscar_por_titulo(self):
        """Verifica la búsqueda parcial por título."""
        self.bib.agregar_libro("Cien años de soledad", "García Márquez", "200")
        self.bib.agregar_libro("Cien fuegos", "Otro", "201")
        resultados = self.bib.buscar_por_titulo("cien")
        self.assertEqual(len(resultados), 2)

    def test_buscar_por_autor(self):
        """Verifica la búsqueda parcial por autor."""
        self.bib.agregar_libro("Libro 1", "García Márquez", "300")
        self.bib.agregar_libro("Libro 2", "García Lorca", "301")
        resultados = self.bib.buscar_por_autor("garcía")
        self.assertEqual(len(resultados), 2)

    def test_listar_disponibles(self):
        """Verifica el listado de libros disponibles."""
        self.bib.agregar_libro("Libre", "A", "400")
        self.bib.agregar_libro("Prestado", "B", "401")
        self.bib.prestar("401", "Juan")
        disponibles = self.bib.listar_disponibles()
        self.assertEqual(len(disponibles), 1)
        self.assertEqual(disponibles[0].titulo, "Libre")

    def test_listar_prestados(self):
        """Verifica el listado de libros prestados."""
        self.bib.agregar_libro("Libro X", "Autor", "500")
        self.bib.prestar("500", "María")
        prestados = self.bib.listar_prestados()
        self.assertEqual(len(prestados), 1)

    def test_prestar_y_devolver(self):
        """Verifica el ciclo de préstamo y devolución a nivel Biblioteca."""
        self.bib.agregar_libro("Libro Y", "Autor Y", "600")
        self.assertTrue(self.bib.prestar("600", "Pedro"))
        self.assertFalse(self.bib.prestar("600", "Ana"))  # Ya prestado
        self.assertTrue(self.bib.devolver("600"))
        self.assertFalse(self.bib.devolver("600"))  # Ya devuelto

    def test_prestar_isbn_inexistente(self):
        """Verifica que prestar un ISBN inexistente lanza ValueError."""
        with self.assertRaises(ValueError):
            self.bib.prestar("NOEXISTE", "Juan")

    def test_eliminar_libro(self):
        """Verifica que se puede eliminar un libro disponible."""
        self.bib.agregar_libro("Para Borrar", "Autor", "700")
        self.assertTrue(self.bib.eliminar_libro("700"))
        self.assertEqual(len(self.bib.libros), 0)

    def test_eliminar_libro_prestado(self):
        """Verifica que no se puede eliminar un libro prestado."""
        self.bib.agregar_libro("Prestado", "Autor", "800")
        self.bib.prestar("800", "Juan")
        self.assertFalse(self.bib.eliminar_libro("800"))

    def test_estadisticas(self):
        """Verifica las estadísticas de la biblioteca."""
        self.bib.agregar_libro("L1", "A", "901", "Novela")
        self.bib.agregar_libro("L2", "B", "902", "Novela")
        self.bib.agregar_libro("L3", "C", "903", "Ciencia")
        self.bib.prestar("901", "Juan")
        stats = self.bib.estadisticas()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["disponibles"], 2)
        self.assertEqual(stats["prestados"], 1)
        self.assertEqual(stats["generos"]["Novela"], 2)
        self.assertEqual(stats["generos"]["Ciencia"], 1)

    def test_persistencia(self):
        """Verifica que los datos se guardan y cargan correctamente."""
        self.bib.agregar_libro("Persistente", "Autor P", "999")
        self.bib.prestar("999", "Ana")
        # Crear nueva instancia que cargue desde el mismo archivo
        bib2 = Biblioteca()
        bib2.ARCHIVO_DATOS = "test_datos_temp.json"
        bib2.libros = []
        bib2.cargar_datos()
        self.assertEqual(len(bib2.libros), 1)
        self.assertEqual(bib2.libros[0].prestatario, "Ana")


if __name__ == "__main__":
    unittest.main()
