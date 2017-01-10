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
from openerp.exceptions import Warning

class OdiseaEvent(models.Model):
        """Event"""

        _name = 'odisea.event'

        _description = 'Event'

	_sort = "create_date"

#	_event_type_ = [
        # Issue definition
##               ('arrive', 'Arrive'),
#                ('departure', 'Departure'),
#                ('revision', 'Revision'),
#                ('add_child', 'Add Child'),
#        ]

	

# Tomamos las que no da odoo
#	registration_date = fields.Date(
#                string='Registration date',
#                required=False,
#                readonly=False
#        )

	parent_exp_id = fields.Many2one(
		'odisea.expedient',
		string='Expedient',
	#	readonly=True
	)

	event_id = fields.Char(
		string="Event Id",
		readonly=True
	)
	
	description = fields.Text(
		"Description",
		readonly=False,
	)

	# Aca se guardara el estado del expediente al momento de 
	# generar el evento TODO: Hay que sacar el campo estado
	# de expediente.
	state = fields.Char(
		string="State",
		readonly=True
	)



#	@api.multi
#	def write(self, vals):


#
