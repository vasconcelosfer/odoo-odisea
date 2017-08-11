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

class OdiseaGood(models.Model):
	"""Good"""
	_name = 'odisea.good'
	_description = 'Good'

	name = fields.Char(string='Good name', required=True, size=25)
	description = fields.Text(string='Good description') 
	active_good = fields.Boolean(string='Active', default=True)
	related_positions = fields.Many2many(
		'odisea.position',
		'note_position_rel',
		'note_id_',
		'position_id',
		string='Position'
	)

#	good_image = fields.One2many('odisea.image','good_relation' ,string="Image")

#	good_image =  fields.Binary("Image",
#		help="This field holds the image used as image for our customers, limited to 1024x1024px."
#	)
	
#	good_image_medium = fields.Binary(
#		cumpute='_get_image', 
#		fnct_inv='_set_image',
#		string="Image (auto-resized to 128x128):", 
#		type="Binary", 
#		multi="_get_image",
#		store=False,
#		store={'upload_images.tutorial': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
#		help="Medium-sized image of the category. It is automatically "\
#			"resized as a 128x128px image, with aspect ratio preserved. "\
#			"Use this field in form views or some kanban views."
#	)
	
#	goo_image_small = fields.Function('_get_image', fnct_inv='_set_image',
#		string="Image (auto-resized to 64x64):", type="binary", multi="_get_image",
#		store={'odisea.good': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),},
#		help="Small-sized image of the category. It is automatically "\
#			"resized as a 64x64px image, with aspect ratio preserved. "\
#			"Use this field anywhere a small image is required."
#	)

#	@api.one
#	@api.depends("image")
#	def _get_image(self, cr, uid, ids, name, args, context=None):
#		result = dict.fromkeys(ids, False)
		
#		for obj in self.browse(cr, uid, ids, context=context):
#			result[obj.id] = tools.image_get_resized_images(obj.image)
		
#		return result
	
#	@api.one
#	@api.depends("image")
#	def _set_image(self, cr, uid, id, name, value, args, context=None):
#		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
	

