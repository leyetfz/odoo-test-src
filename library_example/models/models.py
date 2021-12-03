# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
_logger = logging.getLogger(__name__)


class LibraryExample(models.Model):
    _name = 'library.example'
    _description = 'gestion de librerias'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    # @api.onchange("director")
    # def _onchange_director(self):
    #     if self.director: # self tiene la version cambiada del objeto
    #         # self._origin => valores del objeto antes de cambiar
    #         self.user_id = self.director.user_id.id


    name = fields.Char(string="Nombre", help="nombre de la biblioteca", required=True, default="Biblioteca de ejemplo")
    code = fields.Char('Code', default='/')
    date = fields.Date(string="Fecha de fundación", default=fields.Date.today)
    director = fields.Many2one("hr.employee", string="Nombre del director", copy=False)
    user_id = fields.Many2one("res.users", string="Usuario relacionado al director", related='director.user_id')
    library_book_ids = fields.One2many("library.book", "library_example_id", string="Libros")
    state = fields.Selection([('open', 'Abierto'), ('closed', 'Cerrado')], string="Estado", default='open')

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('library.seq')
        return super(LibraryExample, self).create(vals)

    def write(self, vals):
        return super(LibraryExample, self).write(vals)

    def unlink(self):
        if len(self.library_book_ids) == 0:
            return super(LibraryExample, self).unlink()
        else:
            raise UserError(_("Para poder eliminar una libreria 1ro reasigne sus libros a otra."))

    def lista_autores_libros_archivados(self):
        books = self.env["library.book"].search([('state', '=', 'archivado')])
        autores = set([bo.name for bo in books])
        return list(autores)

    def set_closed(self):
        self.write({'state':'closed'})

    def set_open(self):
        self.write({'state': 'open'})


    def _send_mail_library(self):
        ''' Function colled from cron job'''
        try:
            libraries = self.env['library.example'].search([('state','=','open')])
            for record in libraries:
                mail_template = self.env.ref("library_example.email_template_library_send")

                if record.create_uid.partner_id and record.create_uid.partner_id.email:
                    vals = {'name': self.env.user.partner_id.name,
                            'library': '{} / {}'.format(record.code, record.name),
                            'date': fields.Date.today().strftime("%d/%m/%Y")}

                    rendered_body = mail_template._render(vals, engine="ir.qweb")
                    body = self.env["mail.render.mixin"]._replace_local_links(rendered_body)
                    self.env["mail.mail"].sudo().create(
                        {
                            "email_from": self.env.user.email_formatted,
                            "author_id": self.env.user.partner_id.id,
                            "body_html": body,
                            "subject": _("Email notification for Open Library"),
                            "email_to": record.create_uid.partner_id.email,
                            "auto_delete": True,
                        }
                    ).send()

                    #Poner mensaje en el chatter cada vez que esto ocurra
                    message = "<ul class=\"o_mail_thread_message_tracking\">\n<li>Status:<span> " + record.state + " </span><b>-></b> Send to User. Attachment included </span></li></ul>"
                    record.message_post(body=message, subject="Library record send to Creation User")
                else:
                    _logger.debug(_("User must have partners email to notify."))
        except:
            _logger.critical(_("Something went wrong while sending library report through email."))





class Book(models.Model):
    _name = 'library.book'
    _description = 'gestion de libros'

    @api.depends("cost_book")
    def _compute_price_sale(self):
        for record in self:
            record.price_sale = record.cost_book + record.cost_book * 0.30

    name = fields.Char(string="Nombre", required=True)
    isbn = fields.Char(string="ISBN", required=True)
    price_sale = fields.Float(string="Precio de venta", compute="_compute_price_sale", digits='Payment Terms') #Ejemplo para visualizar la forma de controlar la precis. decimal, este ejemplo muestra 6
    cost_book = fields.Float(string="Costo")
    autor = fields.Many2one("res.users", string="Autor")
    abstract = fields.Text(string="Resumen")
    library_example_id = fields.Many2one("library.example", string="Libreria")
    state = fields.Selection(
        [('disponible', 'Disponible'), ('prestado', 'Prestado'), ('vendido', 'Vendido'), ('archivado', 'Archivado')],
        string="Estado", default="disponible")
