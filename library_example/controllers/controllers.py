# -*- coding: utf-8 -*-
# from odoo import http


# class LibraryExample(http.Controller):
#     @http.route('/library_example/library_example/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/library_example/library_example/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('library_example.listing', {
#             'root': '/library_example/library_example',
#             'objects': http.request.env['library_example.library_example'].search([]),
#         })

#     @http.route('/library_example/library_example/objects/<model("library_example.library_example"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('library_example.object', {
#             'object': obj
#         })
