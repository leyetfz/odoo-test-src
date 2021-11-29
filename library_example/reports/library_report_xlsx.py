from odoo import models
from datetime import date


class LibraryXlsx(models.AbstractModel):
    _name = 'report.library_example.library_xlsx'   # el mismo name del action report --- name="library_example.library_xlsx" ---
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, libraries):

        print(data)  # Observar en el log el contenido de este parametro
        print(libraries) #Observar en el log el contenido de este parametro
        for obj in libraries:
            report_name = obj.name
            # One sheet by library
            sheet = workbook.add_worksheet(report_name[:31])
            bold = workbook.add_format({'bold': True})
            nrml = workbook.add_format({'bold': False})
            merge_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': 'gray'})
            sheet.merge_range('A1:E1', obj.name, merge_format)
            sheet.write(1, 1, 'Fecha', bold)
            sheet.write(1, 2, date.strftime(date.today(), '%Y-%m-%d'), nrml)
            sheet.write(2, 1, 'Director', bold)
            sheet.write(2, 2, obj.director.name, nrml)
            books = obj.library_book_ids
            row = 4
            col = 0
            # Encabezados
            sheet.write(row, col, 'LIBRO', merge_format)
            sheet.write(row, col + 1, 'DESCRIP', merge_format)
            sheet.write(row, col + 2, 'AUTOR', merge_format)
            sheet.write(row, col + 3, 'PRECIO', merge_format)
            sheet.write(row, col + 4, 'ESTADO', merge_format)
            row = 5
            for bk in books:
                sheet.write(row, col, bk.name, nrml)
                sheet.write(row, col + 1, bk.abstract, nrml)
                sheet.write(row, col + 2, bk.autor.name, nrml)
                sheet.write(row, col + 3, bk.price_sale, nrml)
                sheet.write(row, col + 4, bk.state, nrml)
                row += 1

            # Ver mas ejemplos y opciones en https://xlsxwriter.readthedocs.io/examples.html