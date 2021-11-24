# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime


class LibraryExample(models.Model):
    _name = 'library.example'
    _description = 'gestion de librerias'

    name = fields.Char(string="Nombre", help="nombre de la biblioteca", required=True, default="Biblioteca de ejemplo")
    date = fields.Date(string="Fecha de fundación", required=True, default=lambda self: self.Date.today)
    director = fields.Many2one("hr.employee", string="Nombre del director")
    library_book_ids = fields.One2many("library.book", "library_example_id", string="Libros")
    state = fields.Selection([('open', 'Abierto'), ('closed', 'Cerrado')], string="Estado", default='open')

    @api.model
    def create(self, vals):
        if 'director' in vals:
            record = super(LibraryExample, self).create(vals)
            return record
        else:
            raise UserError(_("Debe ingresar el valor al campo director"))

    def write(self, vals):
        return super(LibraryExample, self).write(vals)

    def unlink(self):
        if len(self.library_book_ids) == 0:
            return super(LibraryExample, self).unlink()
        else:
            raise UserError(_("Para poder eliminar una libreria 1ro reasigne sus libros a otra."))

    def lista_autores_libros_archivados(self):
        books = self.env["library.book"].search([('state', '=', 'archivado')])
        autores = []
        for b in books:
            autores.append(b.autor)
        aut_conjunto = set(autores)
        return list(aut_conjunto)


class Book(models.Model):
    _name = 'library.book'
    _description = 'gestion de libros'

    name = fields.Char(string="Nombre", required=True)
    isbn = fields.Char(string="ISBN", required=True)
    price_sale = fields.Float(string="Precion de venta")
    autor = fields.Many2one("res.users", string="Autor")
    abstract = fields.Text(string="Resumen")
    library_example_id = fields.Many2one("library.book", string="Libreria")
    state = fields.Selection(
        [('disponible', 'Disponible'), ('prestado', 'Prestado'), ('vendido', 'Vendido'), ('archivado', 'Archivado')],
        string="Estado", default="disponible")


