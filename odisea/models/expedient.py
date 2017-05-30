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
from openerp import models, fields, api, tools, _
from openerp.exceptions import Warning

from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
#_logger = logging.getlogger(__name__)

#from openerp import SUPERUSER_ID
#from openerp import tools
#from openerp.modules.module import get_module_resource

_exp_logger = logging.getLogger(__name__)
class OdiseaExpedient(models.Model):
        """Expedient"""

        _name = 'odisea.expedient'

        _description = 'Expedient'

#        _order = "id desc"
        _sql_constraints = [
                        ('expedient_unique',
                         'Unique(dependency,number,created_year,alc_index)',
                         "El número de expediente debe ser único"),
        ]

        _states_ = [
        # State machine: untitle
                ('open', 'Open'),
        	('in_revision', 'In Revision'),
                ('closed', 'Closed'),
        ]

	_event_ = {
		'open': 'Arrive',
		'in_revision': 'Went to revision',
		'closed': 'Departure',
		'none': 'None'
	}	

	_expedient_type_ = [
		('1', 'Actuación'),
		('2', 'Alcance'),
		('3', 'Expediente')
	]

        _issues_ = [
        # Issue definition
                ('criterio', 'Criterio'),
                ('denuncia', 'Denuncia'),
                ('devolucion', 'Devolución'),
                ('consulta', 'Consulta'),
                ('embarque_escalonado', 'Embarque Escalonado'),
                ('posicion_arancelaria', 'Posición Arancelaria'),
		('oficio', 'Oficio'),
		('res_256_2000', 'Resolución 256/2000'),
		('apertura_sim','Apertura SIM'),
		('prorroga_ee', 'Prórroga Emb. Escalonado'),
		('res_1243_1992', 'Resolución 1243/1992')
        ]

        _branches_ = [
        # Branch definition
                ('electricidad', 'Electricidad'), 
                ('maquinas', 'Máquinas'),
                ('ferreteria', 'Ferretería'), 
                ('drogas', 'Drogas'), 
                ('alimentos', 'Alimentos'), 
                ('merceria', 'Mercería'),                                
        ]


        state = fields.Selection(
                _states_,
                'State',
                default='open'
        )

        dependency = fields.Integer(
                string='Dependency',
                required=True,
                readonly=False,
                size=8
        )

        number = fields.Integer(
                string='Number',
                required=True,
                readonly=False,
                size=20
        )


        created_year = fields.Integer(
                string='Created Year',
                required=True,
                readonly=False,
                size=4
        )

        alc_index = fields.Integer(
                string='Number',
                required=True,
                readonly=False,
                size=4
	)

        exp_id = fields.Char(
                string=_('Number Com'),
                compute='_comp_expedient_id',
		store=True
        )

	_rec_name = 'exp_id'

        expedient_type = fields.Selection(
		_expedient_type_,
                string=_('Expedient Type'),
		store=True,
                compute='_comp_expedient_type'
        )

        front_page = fields.Char(
                string='Front Page',
                required=True,
                readonly=False,
                size=100
        )

        issue = fields.Text(
                string='Issue',
                required=True,
                readonly=False
        )

        issue_type = fields.Selection(
                _issues_,
                'Issue Type',
                default='criterio'
        )

        goods = fields.Char(
                string='Goods',
                required=True,
                readonly=False,
                size=50
        )

        registration_date = fields.Date(
                string='Registration date',
                required=False,
                readonly=False
        )

        child_ids = fields.One2many(
                'odisea.expedient',
                'parent_id',
		readonly= True,
#		context = "{'default_is_child': True}",
                string='Childs'
        )

        parent_id = fields.Many2one(
                'odisea.expedient',
                string='Parent'
        )

        note_ids = fields.One2many(
                'odisea.note',
                'parent_exp_id',    
                string='Nota'
        )

#        image_ids = fields.One2many(
#                'odisea.image',
#                'parent_exp_id',    
#                string='Nota'
#        )

        event_ids = fields.One2many(
                'odisea.event',
                'parent_exp_id',    
		readonly= True,
                string='Event'
        )

#        branch = fields.Selection(
#                _branches_,
#                'Branch'                
#        )

        branch = fields.Many2one(
                'odisea.branch',
                string='Branch'
        )

        customs_broker = fields.Many2one(
                'odisea.representative',
		domain = "[('is_company', '=', False)]",
                string='Custom Broker'
        )

        organization = fields.Many2one(
                'odisea.representative',
		domain = "[('is_company', '=', True)]",
		context = "{'default_is_company': True}",
                string='Organization'
        )

        is_child = fields.Boolean(
                string='Is child',
                required=False,
                default=False,
                readonly=False
        )

        assigned_advisor = fields.Many2one(
            'hr.employee',           
            string='Assigned advisor',
	    store=True,
	    default='_employee_get'

        )
	
	assigned_user = fields.Integer(
#		'res.user',
		compute='_comp_user',
		string='User assigned for employee',
		store=True,
		readonly=True
	)

	summary_date = fields.Date(
		string = 'Summary Date',
		default = datetime.now().date()
	)

	prescription_date = fields.Date(
                string=_('Prescription Date'),
                compute='_comp_prescription_date',
		store=True
	)

#	destination_id = fields.Many2one(
#               'odisea.destination',
#               string='Parent'
#        )

        @api.one
        @api.depends('dependency','number','created_year', 'alc_index')
        def _comp_expedient_id(self):
		if self.expedient_type != '2':
	                self.exp_id = (str(self.dependency) or '')+'-'+\
				      (str(self.number) or '')+'-'+\
				      (str(self.created_year) or '')        
		else:
	                self.exp_id = (str(self.dependency) or '')+'-'+\
				      (str(self.number) or '')+'-'+\
				      (str(self.created_year) or '')+'/'+\
				      (str(self.alc_index) or '')        
				
        @api.one
        @api.depends('dependency','number','created_year', 'alc_index')
	def _comp_expedient_type(self):
		if self.dependency == 1:
			#self.write({'expedient_type': 'expediente'})
			# Es Expediente
			self.expedient_type = '3'
		elif self.alc_index != 0:
			# Es alcance
			#self.write({'expedient_type': 'alcance'})
			self.expedient_type = '2'
		else:
			# Es Actuacion
			#self.write({'expedient_type':'actuacion'})
			self.expedient_type = '1'
	
	@api.one
	@api.depends('summary_date')
	def _comp_prescription_date(self):
		self.prescription_date =(datetime.strptime(self.summary_date,'%Y-%m-%d') + relativedelta(years=+5)).strftime('%Y-%m-%d')

	@api.one
        @api.depends('assigned_advisor')
	def _comp_user(self):
		if self.assigned_advisor:
			self.assigned_user = self.assigned_advisor.resource_id
			resource = self.env['resource.resource'].search([('id','=',self.assigned_user)])
#			res = self.env['res.user'].search([('id','=',resource.user_id)])
			self.assigned_user = resource.user_id
#		employee = self.env['hr.employee'].search([('resource_id','=',resource.id)])
#		resource = self.env['resource.resource'].search([('user_id','=',self.env.user.id)])
#			self.assigned_user = self.env['res.user'].search([('user_id','=',employee)])

	@api.one
        @api.depends('assigned_advisor')
	def _employee_get(self):
		record = self.env['hr.employee'].search([('user_id', '=', self.env.user.login)]) 
		return record[0]

	@api.one
        @api.depends('is_child', 'parent_id')
        def _onchange_ischild(self, is_child):
        #        if not is_child:
	#		if self.parent_id != None:
	#			self.write({'parent_id': 'Null'})
		return

	@api.multi
	def write_with_event(self, vals):
		for expedient in self:
			state = vals['state'] if 'state' in vals else 'none'
			#Creamos el event creat	e		
			id_created = self.env['odisea.event'].create({
					'parent_exp_id': expedient.id,
					'state': state,
					'event_id': expedient._event_[state]
				})	
	        super(OdiseaExpedient, self).write(vals)
		return id_created

	@api.multi
	def open_event_view(self, vals):
		id_created = int(self.write_with_event(vals))
		#Me devuelve una lista por lo tanto accedo al primero valor de la misma
		#el cual es el id
		return {
		    'name': 'Evento ' + self.state,
	            'type': 'ir.actions.act_window',
	            'res_model': 'odisea.event',
		    'view_type': 'form',
		    'view_mode': 'form',
	            'views': [(False, "form")],
		    'res_id': id_created,
	            'target': 'new',
		    'flags': {'action_buttons': True},
	        }

	@api.multi
	def open_note_view(self, vals):
		id_created = int(self.write_with_event(vals))
		#Me devuelve una lista por lo tanto accedo al primero valor de la misma
		#el cual es el id
		expCtx = {
			'default_parent_exp_id': str(self.id)
		}
		return {
	#	    'name': 'Evento ' + self.state,
	            'type': 'ir.actions.act_window',
	            'res_model': 'odisea.note',
		    'view_type': 'form',
		    'view_mode': 'form',
	            'views': [(False, "form")],
#		    'res_id': id_created,
		    #'context': "{'parent_exp_id': " + str(self.id) + "}",		
		    'context': "{'default_parent_exp_id': " + str(self.id) + "}",		
#		    'context': expCtx,
	            'target': 'new',
		    'flags': {'action_buttons': True},
	        }

