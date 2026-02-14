# from odoo import http


# class CustomAddons/controleCombustivel(http.Controller):
#     @http.route('/custom_addons/controle_combustivel/custom_addons/controle_combustivel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_addons/controle_combustivel/custom_addons/controle_combustivel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_addons/controle_combustivel.listing', {
#             'root': '/custom_addons/controle_combustivel/custom_addons/controle_combustivel',
#             'objects': http.request.env['custom_addons/controle_combustivel.custom_addons/controle_combustivel'].search([]),
#         })

#     @http.route('/custom_addons/controle_combustivel/custom_addons/controle_combustivel/objects/<model("custom_addons/controle_combustivel.custom_addons/controle_combustivel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_addons/controle_combustivel.object', {
#             'object': obj
#         })

