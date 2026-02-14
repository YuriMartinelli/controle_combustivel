# from odoo import models, fields, api


# class custom_addons/controle_combustivel(models.Model):
#     _name = 'custom_addons/controle_combustivel.custom_addons/controle_combustivel'
#     _description = 'custom_addons/controle_combustivel.custom_addons/controle_combustivel'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

