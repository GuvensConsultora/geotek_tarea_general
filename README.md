# Task Worksheet Autofill (Odoo 18)

**Objetivo**: Autocompletar campos de la hoja de trabajo Studio (`x_project_task_worksheet_template_4`) con datos de la tarea (`project.task`). Incluye botón en el header y automatización al crear.

## Instalación
1. Copia la carpeta `task_ws_autofill` a tu ruta de addons.
2. Actualiza la lista de Apps e instala **Task Worksheet Autofill**.

## Configuración mínima
- El modelo de Studio debe existir: `x_project_task_worksheet_template_4`.
- Debe haber un campo m2o hacia `project.task` (Studio suele crearlo como `x_studio_task_id`). El módulo lo detecta automáticamente; si no existe, el botón no hará nada.
- Campo de destino de ejemplo: `x_studio_comitente` (m2o a `res.partner`). Ajusta el mapeo en `models/worksheet_autofill.py` si necesitas más campos.

## Vista (botón)
- El XML asume que la vista formulario principal de Studio tiene el external id `x_x_project_task_worksheet_template_4_view_form`.
- Si en tu base es otro, edita `views/worksheet_button.xml` y reemplaza el `inherit_id` por el correcto (modo desarrollador → Vista → External ID).

**Alternativa si aún no sabes el external id**: comenta `views/worksheet_button.xml` en el `__manifest__.py`, instala el módulo para validar la automatización, y luego reactívalo con el id correcto.

## Cómo probar
1. Abre/crea una hoja desde una Tarea que tenga `partner_id`.
2. Verifica que al crear la hoja se complete **Comitente** (`x_studio_comitente`).
3. Pulsa el botón **Autocompletar desde Tarea** para rellenar/actualizar manualmente.

## Deshacer
- Desinstala el módulo desde Apps.
- O comenta el bloque `@api.model_create_multi` si solo quieres desactivar la autocompletación automática y dejar el botón manual.

## Manifest
- Odoo 18, depends: `base`, `project`, `web`.

## Nota
- Si tu modelo o nombres de campo difieren, busca y reemplaza en los archivos:
  - `x_project_task_worksheet_template_4`
  - `x_x_project_task_worksheet_template_4_view_form`
  - `x_studio_comitente`