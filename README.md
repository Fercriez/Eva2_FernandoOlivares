# Eva2_FernandoOlivares

Proyecto de práctica para TI3041: registra equipos y sus arriendos y los
administra desde Django Admin.

## Requisitos

- Python 3.12 o superior.

## Instalación en Windows

Desde la carpeta del proyecto, crea y activa un entorno virtual e instala las
dependencias:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Prepara la base de datos, carga los datos de demostración e inicia el servidor:

```powershell
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Abre <http://127.0.0.1:8000/admin/> para ingresar al panel. `seed_data` se puede
volver a ejecutar: actualiza los registros de ejemplo sin duplicarlos.

## Cuentas de demostración

Las tres cuentas usan la contraseña `Inacap.2026`.

| Usuario | Grupo | Acceso |
| --- | --- | --- |
| `gerente` | Ninguno | Superusuario |
| `vendedor` | Vendedor | Ver, agregar y modificar; no puede eliminar |
| `supervisor` | Supervisor | Solo puede ver |

Estas credenciales y la clave de desarrollo de Django son únicamente para esta
actividad local. No reutilizarlas en un despliegue público.

## Modelos y administración

- **Equipo** guarda nombre, categoría, marca, modelo, valor diario y
  disponibilidad.
- **Arriendo** guarda código, equipo asociado, arrendatario, fechas, valor total
  y estado. Eliminar un equipo elimina también sus arriendos.
- Los listados del panel incluyen columnas, filtros, búsqueda y montos en pesos
  chilenos, por ejemplo `$12.990`.
- La base `db.sqlite3` incluida contiene los usuarios y registros de muestra.

## Pruebas

```powershell
python manage.py test arriendos
```
