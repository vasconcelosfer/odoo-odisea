# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class OdiseaExpedient(models.Model):
	"""Expedient"""

	_name = 'odisea.expedient'
	_description = 'Expedient'

	_order = "id desc"

	_states_ = [
	# State machine: untitle
        ('open', 'Open'),
        ('in_revision', 'In Revision'),
        ('closed', 'Closed'),
        ('annulled', 'Annulled'),
        ('cancel', 'Cancel'),
	]

	_issues_ = [
	# State machine: untitle
        ('criterio', 'Criterio'),
        ('denuncia', 'Denuncia'),
        ('devolución', 'Devolución'),
        ('consulta', 'Consulta'),
        ('embarque_escalonado', 'Embarque Escalonado'),
	('posicion_arancelaria', 'Posición Arancelaria'),
	]


	state = fields.Selection(
	        _states_,
      		'State',
	        default='open',
	)

	dependency = fields.Integer(
		string='Dependency',
		required=True, 
		readonly=False
	)

	number = fields.Integer(
		string='Number',
		required=True, 
		readonly=False
	)

	created_year = fields.Integer(
		string='Created Year',
		required=True, 
		readonly=False
	)
		
	exp_id = fields.Char(
		string=_('Number Com'),
		compute='_comp_expedient_id'
	)
	
	front_page = fields.Char(
		string='Front Page',
		required=True,
		readonly=False
	)

	issue = fields.Char(
		string='Issue',
		required=True,
		readonly=False
	)

	issue_type = fields.Selection(
	        _issues_,
      		'Issue Type',
	        default='criterio',
	)

	goods = fields.Char(
		string='Goods',
		required=True,
		readonly=False
	)

	#Utiilzamos el campo que genera odoo create_date
#	issue_date = fields.Datetime(
#		string='Issue Date',
#	        readonly=True,
#	        required=False,
#	        default=fields.Datetime.now
#	)
	child_ids = fields.One2many(
	        'odisea.expedient',
	        'parent_id',
	        string='Childs'
	)

	parent_id = fields.Many2one(
		'odisea.expedient',
       		string='Parent'
	)

	note_ids = fields.One2many(
		'odisea.note',
		'parent_id',	
		string='Nota'
	)

#	files = fields.One2many(
#		"ir.attachment",
 #               'odisea.salida_exp',
#		'num_exp',
#		string="Attachments"
#	)
	
	@api.one
	@api.depends('dependency','number','created_year' )
	def _comp_expedient_id(self):
    		self.exp_id = (str(self.dependency) or '')+'-'+(str(self.number) or '')+'-'+(str(self.created_year) or '')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
