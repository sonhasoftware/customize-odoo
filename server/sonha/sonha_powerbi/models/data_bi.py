from odoo import api, fields, models


class DataBI(models.Model):
    _name = 'data.bi'

    name = fields.Many2one('hr.employee')
    date = fields.Date("Ngày")
    quanty = fields.Integer("Qty")
    department_id = fields.Many2one(related='name.department_id', store=True, string='Department')
    level = fields.Selection(related='name.level', store=True, string='Level')

    @api.model
    def _get_user_level_domain(self):
        user = self.env.user
        if user.employee_id and user.employee_id.level:
            user_level = user.employee_id.level
            if user_level == 'N0':
                return []
            elif user_level == 'N1':
                return [('level', 'in', ['N1', 'N2', 'N3', 'N4', 'N5'])]
            elif user_level == 'N2':
                return [('level', 'in', ['N2', 'N3', 'N4', 'N5'])]
            elif user_level == 'N3':
                return [('level', 'in', ['N3', 'N4', 'N5'])]
            elif user_level == 'N4':
                return [('level', 'in', ['N4', 'N5'])]
            elif user_level == 'N5':
                return [('level', '=', 'N5')]
        return []

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        domain = self._get_user_level_domain()
        args.extend(domain)
        return super(DataBI, self).search(args, offset, limit, order, count)
