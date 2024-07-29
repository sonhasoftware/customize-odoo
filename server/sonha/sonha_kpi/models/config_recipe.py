from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ConfigRecipe(models.Model):
    _name = 'config.recipe'

    result_field_id = fields.Many2one('ir.model.fields', string='Result Field', domain=[('model_id', '=', 'sonha.kpi.rel')], ondelete='cascade')
    recipe = fields.Char('Công thức')
