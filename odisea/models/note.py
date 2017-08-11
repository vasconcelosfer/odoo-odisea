# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any laer version.
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

import time
import logging
import subprocess
from PIL import Image
from StringIO import StringIO


_MARKER_PHRASE = '[[waiting for OCR]]'
_logger = logging.getLogger(__name__)
class OdiseaNote(models.Model):
	"""Note"""

	_inherit = 'ir.attachment'
	_name = 'odisea.note'
	_description = 'Note'
	_order = 'release_year desc,id_note desc'


	_sql_constraints = [
		('note_unique',
		 'Unique(note_type,id_note,release_year)',
		 "El número de Nota debe ser único"),
	]
	
	_defaults = {
		'release_date': fields.Date.today(),
	}

	note_type = fields.Selection([
		('1', 'CRITERIO'),
		('2', 'DICTAMEN TÉCNICO'),
                ('3', 'DV CLAR'),
                ('5', 'DE TNCA'),
 		('6', 'RESOLUCIÓN')
                ],
		 string='Type',
		 required=True
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
                compute='_comp_note_id',
		store=True
        )

	release_date = fields.Date(
		string="Release date", 
		required=False
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

	content_index = fields.Text(
		string = "Content Index",
		compute="_comp_content",
		store=True
		#index=True
	)

	assigned_advisor = fields.Many2one(
		'hr.employee',		
		string='Assigned advisor',			
		store=True,							                
								        
	)

	is_reserved = fields.Boolean(
		string = 'Reserved',
		compute ='_comp_change_reserved',
		store=True,
		default=True,
		
	)

	exp_type = fields.Char(
		string=_('Expedient type'),
		compute='_comp_exp_type',
		store=True
	)

	exp_type_id = fields.Many2one(
		'issue_type',
		string='Issue type',
		store=True
	)
	
        @api.one
        @api.depends('id_note','release_year')
        def _comp_note_id(self):
                self.note_id = (str(self.id_note) or '')+'/'+\
			       (str(self.release_year) or '')



	@api.one
	@api.depends('datas')
	def _comp_content(self):
		self.content_index = _MARKER_PHRASE	

	@api.multi 
	def onchange_filename(self, filename):
		return {'value':{'name':filename,}}

	@api.multi
	def get_exp_file(self):
   		return {
         	  'type' : 'ir.actions.act_url',
		  'url': '/web/binary/saveas?model=odisea.note&field=datas&filename_field=datas_fname&id=%s'%(self.id),
                  'target': 'self',
		  'string':'Download',
 }
	@api.multi 
	def set_exp_file(self):
   		return 1

	@api.model
	def _get_pdf_content(self, datas):
	        dpi = 300
		depth = 8
	        top_type = "application"
		sub_type = "pdf"
		if datas == False:
			return True
		process = subprocess.Popen(
		['convert', '-density', str(dpi), '-', '-append', '-depth', str(depth), 'tiff:-'],
		stdin=subprocess.PIPE, stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		)
		stdout, stderr = process.communicate(datas)
		if stderr:
			_logger.error('Error converting to PDF: %s', stderr)

		imagePDF = StringIO(stdout)

		process = subprocess.Popen(
		['tesseract', 'stdin', 'stdout', '-l spa'],
		stdin=subprocess.PIPE, stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		)
		stdout, stderr = process.communicate(imagePDF.getvalue())
		if stderr:
			_logger.error('Error during OCR: %s', stderr)
			return _MARKER_PHRASE
		return stdout


	@api.model
	def _index_content_cron(self):
		_logger.error('Disparando cron ')
		for this in self.search([('content_index', '=', _MARKER_PHRASE),]):
			if not this.datas:
				continue
			index_content = this._get_pdf_content(this.datas.decode('base64'))
			this.write({
	                'content_index': index_content,
			})


	@api.model
	def create(self, vals, context=None):	
#	 ... your coe..."""
#		for expedient in self:
#			if expedient.parent_exp_id
		if vals.get('parent_exp_id'):
			# Se obtiene el año
			year = str(vals.get('release_year'))
			reserve_note = vals.get('id_note')
			
			if  vals.get('is_reserved'):
				year = ""
				year = time.strftime('%Y')
				year = year.replace("20","")

			#Se obtiene el número de nota que se va a utilizar. 
				self.env.cr.execute(
					""" 
						SELECT id_note 
						FROM odisea_note 
						WHERE note_type = '3'
						AND release_year = %r
						ORDER BY id_note DESC 
						LIMIT 1 
					""" % (year) )
				reserve_note = self.env.cr.fetchone()[0] + 1
			
			# Nesesario para reservar nota.
			value =  {
      				'note_type':'3',
   				'id_note':reserve_note,
                       		'release_year': int(year),
                       		'note_id':(str(self.id_note))+'/'+(str(self.release_year)),
		       		'name':'',
		       		'parent_exp_id': vals.get('parent_exp_id'),
		       		'assigned_advisor': vals.get('assigned_advisor'),
		       		'is_reserved':'True',
			}

			res_id = super(OdiseaNote, self).create(value, context=context)
		else:
			#Creación cuando se carga la nota digitalizada.
			vals['is_reserved'] = False
			res_id = super(OdiseaNote, self).create(vals,  context=context)


		return res_id

	@api.one
	@api.depends('parent_exp_id')
	def _comp_exp_type(self):
		self.exp_type = self.env['odisea.expedient'].search(
				[('id','=',self.parent_exp_id.id)]).issue_type

	@api.one
	@api.depends('name')
	def _comp_change_reserved(self):
		if self.name != "":
			self.is_reserved = False
		else:
			self.is_reserved = True

		return True

	@api.multi
	def charge_digital_pdf(self):
		#reserved_note = self.env['odisea.note'].
		#model_data = self.pool.get('ir.model.data')
		#form_view = model_data.get_object_reference(cr, uid, 'odisea', 'view_odisea_note_form_edit')
		#form_view = ['view_odisea_note_form_edit']
		return {
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'odisea.note',
			#'view_id': False,
			'type': 'ir.actions.act_window',	
			'res_id': self.id,
			'create':True,
			#'views': [(form_view and form_view[1] or False, 'form')],
		}

