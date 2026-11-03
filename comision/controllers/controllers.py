# from odoo import http


# class Comision(http.Controller):
#     @http.route('/comision/comision', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/comision/comision/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('comision.listing', {
#             'root': '/comision/comision',
#             'objects': http.request.env['comision.comision'].search([]),
#         })

#     @http.route('/comision/comision/objects/<model("comision.comision"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('comision.object', {
#             'object': obj
#         })

