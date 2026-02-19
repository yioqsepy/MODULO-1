# 📚 Sistema de Gestión de Biblioteca

### Proyecto Piloto con IA — Talento Solutions

> Demostración de cómo la Inteligencia Artificial puede apoyar todo el flujo de
> desarrollo de software: planificación, generación de código, testing,
> documentación y reflexión ética.

---

## 🎯 Descripción

Sistema de gestión de biblioteca desarrollado en **Python** con interfaz gráfica
**Tkinter** que permite:

- ➕ **Agregar** nuevos libros al catálogo
- 🔍 **Buscar** libros por título, autor o ISBN
- 📤 **Prestar** libros a usuarios registrando fechas
- 📥 **Devolver** libros prestados
- 🗑️ **Eliminar** libros del catálogo
- 📊 **Consultar** estadísticas de la biblioteca
- 💾 **Persistencia** automática de datos en JSON

---

## 📁 Estructura del Proyecto

```
biblioteca-ia/
├── src/
│   └── biblioteca.py          # Código principal (clases + GUI)
├── tests/
│   └── test_biblioteca.py     # Tests unitarios (25+ tests)
├── docs/
│   ├── proceso_ia.md          # Documentación del proceso con IA
│   └── diagrama_flujo_prestamo.md  # Diagrama de flujo del préstamo
├── .gitignore                 # Archivos ignorados por Git
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Este archivo
└── index.html                 # Presentación web del proyecto
```

---

## 🚀 Instalación y Ejecución

### Prerrequisitos
- **Python 3.10** o superior
- **Tkinter** (incluido con Python en Windows/macOS; en Linux: `sudo apt install python3-tk`)

### Pasos

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd biblioteca-ia

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python src/biblioteca.py
```

---

## 🧪 Ejecutar Tests

```bash
# Con pytest (recomendado)
python -m pytest tests/test_biblioteca.py -v

# Con unittest
python -m unittest tests/test_biblioteca.py -v

# Con cobertura
python -m pytest tests/test_biblioteca.py --cov=src --cov-report=html
```

### Resultado esperado

```
tests/test_biblioteca.py::TestLibro::test_creacion_libro PASSED
tests/test_biblioteca.py::TestLibro::test_genero_por_defecto PASSED
tests/test_biblioteca.py::TestLibro::test_str_disponible PASSED
...
========================= 28 passed in 0.15s ==========================
```

---

## 📋 Historias de Usuario

| ID | Historia | Prioridad |
|----|----------|-----------|
| HU-01 | Registrar un nuevo libro con título, autor, ISBN y género | Alta |
| HU-02 | Prestar un libro registrando prestatario y fechas | Alta |
| HU-03 | Devolver un libro prestado | Alta |
| HU-04 | Buscar libros por título, autor o ISBN | Media |
| HU-05 | Consultar estadísticas de la biblioteca | Baja |

> Detalle completo en [`docs/proceso_ia.md`](docs/proceso_ia.md)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────┐
│                BibliotecaGUI                    │
│             (Interfaz Tkinter)                  │
├─────────────────────────────────────────────────┤
│                 Biblioteca                      │
│        (Gestión + Persistencia JSON)            │
├──────────────────────┬──────────────────────────┤
│      Libro           │   prestar_libro()        │
│   (Modelo de datos)  │   devolver_libro()       │
│                      │   (Lógica de negocio)    │
└──────────────────────┴──────────────────────────┘
```

---

## 📸 Capturas de Pantalla

La interfaz incluye:
- **Barra de encabezado** con el nombre del sistema
- **Panel lateral** con botones de acciones
- **Tabla principal** con listado de libros y su estado
- **Barra de estadísticas** con contadores en tiempo real
- **Filtro rápido** para búsqueda instantánea

---

## 🤖 Sobre el Uso de IA

Este proyecto fue desarrollado con asistencia de **Claude (Anthropic)** como parte
de un proyecto piloto para evaluar el impacto de la IA en el ciclo de desarrollo
de software.

> Consulta el documento completo: [`docs/proceso_ia.md`](docs/proceso_ia.md)

### Fases asistidas por IA:
1. ✅ Planificación y análisis de requisitos
2. ✅ Generación de código
3. ✅ Creación de tests unitarios
4. ✅ Documentación técnica
5. ✅ Reflexión ética

---

## 📄 Licencia

Proyecto educativo desarrollado por **Talento Solutions** © 2025.  
Uso interno y demostrativo.

---

## 👥 Créditos

- **Talento Solutions** — Concepto y dirección del proyecto
- **Claude (Anthropic)** — Asistente IA para generación de código y documentación
