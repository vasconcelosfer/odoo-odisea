# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

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
	_sort = 'note_id' # 'id_note':


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

	content_index = fields.Text(
		string = "Content Index",
		compute="_comp_content",
		store=True
		#index=True
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



