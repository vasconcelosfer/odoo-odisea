# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class OdiseaNote(models.Model):
	"""Note"""

	_inherit = 'ir.attachment'
	_name = 'odisea.note'
	_sort = 'id_note'

        note_type = fields.Selection([
		('1', 'CRITERIO'),
		('2', 'DICTAMEN TÉCNICO'),
                ('3', 'DV CLAR'),
                ('5', 'DI TECN'),
 		('6', 'RESOLUCIÓN')
                ],
		 string='Tipo' 
	)

	id_note = fields.Integer(
		string="Number",
		required=True
	)

	release_year = fields.Integer(
		string="Release year",
		required=True
	)

	release_date = fields.Date(
		string="Release date", 
		required=True
	)

	parent_exp_id = fields.Many2one(
		'odisea.expedient',
		string='Expedient'
	)


