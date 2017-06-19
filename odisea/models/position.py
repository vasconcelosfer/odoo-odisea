# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from openerp import models, fields, api, _


class OdiseaPosition(models.Model):
	"""Position"""

#	_inherit = 'ir.attachment'
	_name = 'odisea.position'
	_description = 'Position'
#	_sort = 'id_note'

        _sql_constraints = [
		('expedient_unique',
		 'Unique(name)',
		 "El número de Posición debe ser único"),
	]


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
