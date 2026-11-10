# Lab Grupo 08 — Sistema de Gestión de Notas y Rendimiento Académico

Aplicación de escritorio (Tkinter) para registrar alumnos, sus 4 notas por curso, y consultar
promedios, estados (APROBADO / DESAPROBADO) y estadísticas del salón. Los datos se guardan en `alumnos.csv`.

## Cómo ejecutarla

```
python main.py            # interfaz gráfica
python demostraciones.py  # valor vs referencia + getters/setters, herencia y polimorfismo en consola
```

## Estructura

| Archivo | Contenido |
|---|---|
| `main.py` | Interfaz: `AppNotas` (hereda de `tk.Tk`) y `DialogoEdicion` (hereda de `tk.Toplevel`) |
| `gestor.py` | `GestorNotas`: registrar, editar, eliminar y buscar, con todas las reglas de negocio |
| `modelos.py` | `Persona` → `Alumno` (herencia) y `Registro`, con getters y setters (`@property`) |
| `almacenamiento.py` | `RepositorioNotas` (clase base abstracta) → `RepositorioCSV`, `RepositorioMemoria` |
| `reportes.py` | `Reporte` (clase base abstracta) → `ReporteAlumno`, `ReporteEstadisticas` |
| `consultas.py` | `calcular_estadisticas()` y la clase de datos `Estadisticas` |
| `logica.py` | Funciones puras: `calcular_promedio`, `determinar_estado` y constantes de las reglas |
| `validaciones.py` | Funciones de validación y normalización; excepciones `ErrorValidacion` y `ErrorCursoDuplicado` |
| `demostraciones.py` | Paso por valor/referencia y demostración de POO |

## Temas de programación que se aplican

- **Funciones**: `logica.py` y `validaciones.py` (puras, con docstring, una sola responsabilidad).
- **Clases**: modelos, gestor, repositorios, reportes y ventanas.
- **Getters y setters**: `Persona.nombre`, `Registro.curso` y `Registro.notas` validan al asignar; `dni`, `promedio` y `estado` son solo lectura.
- **Herencia**: `Persona` → `Alumno`; `RepositorioNotas` → `RepositorioCSV`/`RepositorioMemoria`; `Reporte` → `ReporteAlumno`/`ReporteEstadisticas`; `ErrorValidacion` → `ErrorCursoDuplicado`; `Tk`/`Toplevel` → las ventanas.
- **Polimorfismo**: `descripcion()` (Persona/Alumno), `generar()` (cualquier Reporte), `guardar()`/`cargar()` (cualquier repositorio).
