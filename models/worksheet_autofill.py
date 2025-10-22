# -*- coding: utf-8 -*-
from odoo import api, fields, models

# Modelo Studio esperado:
#   _name = "x_project_task_worksheet_template_4"
# Campo enlace a tarea (m2o a project.task):
#   suele llamarse x_studio_task_id (puede variar según Studio)
#
# Este mixin añade:
#   - Método action_fill_from_task(): copia valores desde la tarea
#   - Hook en create() para autocompletar al crear

class WorksheetStudio(models.Model):
    _inherit = "x_project_task_worksheet_template_4"

    def _find_task_field_name(self):
        '''Devuelve el nombre del campo m2o hacia project.task en el modelo Studio.'''
        # 1) nombre común en Studio
        if "x_project_task_id" in self._fields and self._fields["x_project_task_id"].comodel_name == "project.task":
            return "x_project_task_id"
        # 2) detectar cualquier m2o → project.task
        for fname, f in self._fields.items():
            if getattr(f, "type", None) == "many2one" and getattr(f, "comodel_name", "") == "project.task":
                return fname
        return None

    def action_fill_from_task(self):
        '''Copia campos desde la tarea origen hacia la hoja de trabajo.'''
        for rec in self:
            task_field = rec._find_task_field_name()
            task = getattr(rec, task_field, False) if task_field else False
            if not task:
                # permitir pasar task_id vía contexto si se abre desde tarea
                ctx_task_id = rec.env.context.get("task_id")
                if ctx_task_id:
                    task = rec.env["project.task"].browse(ctx_task_id)
            if not task:
                continue

            # --- MAPEO: ajusta según tus campos Studio ---
            mvals = {}
            # Ejemplo: comitente (m2o res.partner) desde partner de la tarea
            if "x_studio_comitente" in rec._fields:
                mvals["x_studio_comitente"] = task.partner_id.id or False

            # Otros ejemplos (descomentar y adaptar si existen en tu Studio):
            # if "x_studio_responsable" in rec._fields:
            #     mvals["x_studio_responsable"] = task.user_id.id or False
            # if "x_studio_proyecto" in rec._fields:
            #     mvals["x_studio_proyecto"] = task.project_id.id or False
            # if "x_studio_nombre_tarea" in rec._fields:
            #     mvals["x_studio_nombre_tarea"] = task.name

            # Escribe solo campos presentes
            if mvals:
                rec.write(mvals)

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        recs.action_fill_from_task()
        return recs
