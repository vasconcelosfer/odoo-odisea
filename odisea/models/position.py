# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class OdiseaPosition(models.Model):
	"""Position"""

#	_inherit = 'ir.attachment'
	_name = 'odisea.position'
#	_sort = 'id_note'


#	position_id = fields.Integer(
#		string="Position",
#		required=True
#	)

	name = fields.Char('Position',
		 size=32
	)

	note_ids = fields.Many2many(
		'odisea.note',
		'note_position_rel',
		'position_id',
		'note_id_',
		'Notes'
	)
