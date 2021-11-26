from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
   _inherit = "purchase.order"

   name = fields.Char(help="Se debe ingresar el codigo de la orden de compra")
   library_example_id = fields.Many2one("library.example", string="Libreria", required=1)

   def button_cancel(self):
      if self.state == "draft":
         raise UserError(_("En estado borrador no se puede cancelar"))
      super(PurchaseOrder, self).button_cancel()

   def validar_todo(self):
      pass
