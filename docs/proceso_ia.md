# 📖 Documentación del Proceso de Creación con IA

## Proyecto Piloto — Sistema de Gestión de Biblioteca
**Empresa:** Talento Solutions  
**Fecha:** 2025  
**Asistente IA utilizado:** Claude (Anthropic)

---

## 1. Objetivo del Proyecto

Demostrar cómo la Inteligencia Artificial puede apoyar **todo el flujo de desarrollo de software**, desde la planificación hasta la documentación y reflexión ética, aplicado a un sistema de gestión de biblioteca.

---

## 2. Fases del Desarrollo Asistido por IA

### 📋 Fase 1: Planificación y Análisis de Requisitos

**Prompt utilizado:**  
Se solicitó a la IA diseñar un sistema de gestión de biblioteca con clases para libros, funciones de préstamo/devolución, interfaz gráfica con Tkinter y tests unitarios.

**IA Utilizada:** desde LMArena he utilizado claude-opus-4.6-thimking


**PROMPT:** ROL: eres un experto programador en python 
TAREA: Talento Solutions quiere diseñar un “Proyecto piloto con IA” para un sistema de gestión de biblioteca. El objetivo es demostrar cómo la Inteligencia Artificial puede apoyar todo el flujo de desarrollo de software: desde la planificación y generación de código, hasta el testing, la documentación y la reflexión ética. 

INSTRUCCIONES: 
-crea un pequeño sistema de gestión de biblioteca en python y usa la libreria tkinter.
y documenta el proceso de creacion de la app (lo guardas en el directorio docs).
genera 5 historias de usuario para el sistema de biblioteca.

-la estructura mínima de ficheros que debes usar es esta: 
src/biblioteca.py 
 tests/test_biblioteca.py
 docs/proceso_ia.md
 README.md
 .gitignore
 requirements.txt 
-genera un diagrama de flujo (en texto, en el directorio docs) del proceso de
préstamo
-En src/biblioteca.py, crea las siguientes clases:
▪ una clase Libro
▪ funciones para prestar y devolver libros

**RESULTADO:**  
La IA analizó los requisitos y propuso:
- Una arquitectura basada en clases (`Libro`, `Biblioteca`, `BibliotecaGUI`)
- Funciones independientes para la lógica de negocio (`prestar_libro`, `devolver_libro`)
- Persistencia de datos en JSON
- Estructura de proyecto con separación de código, tests y documentación

**Decisiones de diseño tomadas por la IA:**
- Separar la lógica de préstamo/devolución en funciones puras para facilitar testing
- Usar JSON para persistencia (simplicidad vs. base de datos)
- Incluir datos de ejemplo para facilitar la demostración

---

### 💻 Fase 2: Generación de Código

**Archivos generados:**

| Archivo | Descripción | Líneas aprox. |
|---------|-------------|---------------|
| `src/biblioteca.py` | Clases y GUI principal | ~380 |
| `tests/test_biblioteca.py` | 25+ tests unitarios | ~220 |
| `requirements.txt` | Dependencias del proyecto | ~10 |
| `.gitignore` | Archivos a ignorar en Git | ~40 |

**Patrones aplicados por la IA:**
- **Serialización/Deserialización:** Métodos `to_dict()` y `from_dict()` en la clase `Libro`
- **Separación de responsabilidades:** Lógica de negocio separada de la interfaz gráfica
- **Principio DRY:** Reutilización de funciones `prestar_libro()` y `devolver_libro()` tanto de forma directa como a través de la clase `Biblioteca`
- **Manejo de errores:** Validaciones con `ValueError` y verificaciones de estado

---

### 🧪 Fase 3: Testing

**Framework utilizado:** `unittest` (compatible con `pytest`)

**Cobertura de tests:**

| Módulo | Tests | Aspectos cubiertos |
|--------|-------|--------------------|
| `Libro` | 7 | Creación, representación, serialización |
| `prestar_libro()` | 5 | Éxito, fallo, validaciones, edge cases |
| `devolver_libro()` | 3 | Éxito, fallo, ciclo completo |
| `Biblioteca` | 13 | CRUD, búsquedas, estadísticas, persistencia |

**Casos límite testeados:**
- Préstamo de libro ya prestado
- Devolución de libro disponible
- ISBN duplicado al agregar
- Prestatario con nombre vacío o solo espacios
- Eliminación de libro prestado (no permitida)

---

### 📝 Fase 4: Documentación

**Documentos generados:**
1. `docs/proceso_ia.md` — Este documento (proceso de desarrollo)
2. `docs/diagrama_flujo_prestamo.md` — Diagrama de flujo del préstamo
3. `README.md` — Guía de inicio rápido del proyecto

**Estándares de documentación aplicados:**
- Docstrings en todas las clases y métodos (estilo Google)
- Type hints en parámetros y retornos
- Comentarios explicativos en secciones clave

---

## 3. Historias de Usuario

### 📗 HU-01: Registrar un nuevo libro
> **Como** bibliotecario,  
> **quiero** poder registrar un nuevo libro con su título, autor, ISBN y género,  
> **para que** quede catalogado en el sistema y disponible para préstamo.

**Criterios de aceptación:**
- El sistema permite ingresar título, autor, ISBN y género
- No se permiten libros con ISBN duplicado
- El libro se guarda de forma persistente
- El libro aparece como "Disponible" tras ser registrado

---

### 📘 HU-02: Prestar un libro a un usuario
> **Como** bibliotecario,  
> **quiero** poder registrar el préstamo de un libro indicando el nombre del prestatario,  
> **para que** quede constancia de quién tiene el libro y cuándo debe devolverlo.

**Criterios de aceptación:**
- Solo se pueden prestar libros en estado "Disponible"
- Se registra automáticamente la fecha de préstamo y la fecha límite de devolución (14 días)
- El estado del libro cambia a "Prestado"
- El nombre del prestatario queda registrado

---

### 📙 HU-03: Devolver un libro prestado
> **Como** bibliotecario,  
> **quiero** poder registrar la devolución de un libro,  
> **para que** vuelva a estar disponible para otros usuarios.

**Criterios de aceptación:**
- Solo se pueden devolver libros en estado "Prestado"
- Al devolver, el libro vuelve al estado "Disponible"
- Se eliminan los datos de préstamo (prestatario, fechas)
- Los cambios se guardan de forma persistente

---

### 📕 HU-04: Buscar libros en el catálogo
> **Como** usuario de la biblioteca,  
> **quiero** poder buscar libros por título, autor o ISBN,  
> **para que** pueda encontrar rápidamente el libro que necesito.

**Criterios de aceptación:**
- La búsqueda es parcial (no requiere el texto completo)
- La búsqueda no distingue mayúsculas de minúsculas
- Se muestran todos los resultados que coincidan
- Se puede ver el estado de disponibilidad de cada resultado

---

### 📓 HU-05: Consultar estadísticas de la biblioteca
> **Como** administrador de la biblioteca,  
> **quiero** ver estadísticas generales (total de libros, disponibles, prestados, por género),  
> **para que** pueda tomar decisiones informadas sobre la gestión del acervo.

**Criterios de aceptación:**
- Se muestra el número total de libros
- Se muestra cuántos están disponibles y cuántos prestados
- Se muestra un desglose por género literario
- Las estadísticas se actualizan en tiempo real

---

## 4. Reflexión Ética sobre el Uso de IA en Desarrollo

### ✅ Beneficios observados
- **Velocidad:** El prototipo completo se generó en minutos vs. horas de desarrollo manual
- **Consistencia:** Código con estilo uniforme, documentación completa y tests exhaustivos
- **Buenas prácticas:** La IA aplicó patrones de diseño y estándares automáticamente
- **Cobertura de testing:** Generó casos límite que un desarrollador podría olvidar

### ⚠️ Riesgos y consideraciones
- **Dependencia tecnológica:** Los desarrolladores no deben delegar 100% el pensamiento crítico a la IA
- **Revisión obligatoria:** Todo código generado por IA DEBE ser revisado por un humano
- **Propiedad intelectual:** Considerar las implicaciones legales del código generado
- **Sesgo en decisiones:** La IA toma decisiones de diseño basadas en patrones comunes, que pueden no ser óptimos para cada caso
- **Seguridad:** El código generado puede contener vulnerabilidades que requieren auditoría

### 🎯 Recomendaciones
1. Usar la IA como **herramienta de apoyo**, no como reemplazo del desarrollador
2. Siempre **revisar, entender y validar** el código generado
3. Mantener el **juicio humano** en decisiones arquitectónicas críticas
4. Documentar cuándo y cómo se usó IA en el desarrollo
5. Establecer **políticas claras** sobre el uso de IA en el equipo

---

## 5. Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje principal |
| Tkinter | (incluido) | Interfaz gráfica |
| unittest | (incluido) | Framework de testing |
| pytest | 7.0+ | Runner de tests |
| JSON | (incluido) | Persistencia de datos |
| Git | — | Control de versiones |

---

## 6. Conclusiones

Este proyecto piloto demuestra que la IA puede ser un **acelerador significativo** en todas las fases del desarrollo de software. Sin embargo, el valor real se obtiene cuando se combina la capacidad generativa de la IA con el **criterio, experiencia y supervisión** de desarrolladores humanos.

La IA no reemplaza al programador; lo **potencia**.

---

*Documento generado como parte del Proyecto Piloto con IA de Talento Solutions.*
