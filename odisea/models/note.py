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

        note_id = fields.Char(
                string=_('Number Com'),
                compute='_comp_note_id'
        )

	release_date = fields.Date(
		string="Release date", 
		required=True
	)

	parent_exp_id = fields.Many2one(
		'odisea.expedient',
		string='Expedient'
	)

	position_ids = fields.Many2many(
		'odisea.position',
		'note_position_rel',
		'note_id_',
		'position_id',
		string='Position'
	)

        @api.one
        @api.depends('id_note','release_year')
        def _comp_note_id(self):
                self.note_id = (str(self.id_note) or '')+'/'+\
			       (str(self.release_year) or '')


	@api.multi 
	def onchange_filename(self, filename):
		return {'value':{'name':filename,}}

	@api.multi
	def get_exp_file(self):
   		return {
         	  'type' : 'ir.actions.act_url',
		  'url': '/web/binary/saveas?model=odisea.note&field=datas&filename_field=datas_fname&id=%s'%(self.id),
                  'target': 'self',
 }
	@api.multi 
	def set_exp_file(self):
   		return 1

