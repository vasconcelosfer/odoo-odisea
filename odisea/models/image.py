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

class OdiseaImage(models.Model):
	_name = 'odisea.image'

	_rec_name = 'image_filename'

	image = fields.Binary('Image', required=True)
	image_filename = fields.Char("Image Filename", )

	# Scaled Images
	image_big = fields.Binary(string="Big-sized image",
                                 store=False,
                                 compute="_get_image",
                                 help="Big-sized image of this model. It is automatically " \
                                      "resized as a 128x128px image, with aspect ratio preserved. " \
                                      "Use this field in form views or some kanban views.")

	image_medium = fields.Binary(string="Medium-sized image",
                                 store=False,
                                 compute="_get_image",
                                 help="Medium-sized image of this model. It is automatically " \
                                      "resized as a 128x128px image, with aspect ratio preserved. " \
                                      "Use this field in form views or some kanban views.")

	image_small = fields.Binary(string="Small-sized image",
                                store=False,
                                compute="_get_image",
                                help="Small sized image of this model. It is automatically " \
                                     "resized as a 64x64px image, with aspect ratio preserved. " \
                                     "Use this field in form views or some kanban views.")

#	parent_exp_id = fields.Many2one(
#		'odisea.expedient',
#		string='Expedient'
#	)

	expedient_relation = fields.Many2one(
		'odisea.expedient',
		string='Image relation'
	)

	@api.one
	@api.depends("image")
	def _get_image(self):
		""" calculate the images sizes and set the images to the corresponding
		    fields
		"""

		image = self.image

		# check if the context contains the magic `bin_size` key
		if self.env.context.get("bin_size"):
			 # refetch the image with a clean context
			image = self.env[self._name].with_context({}).browse(self.id).image

		data = tools.image_get_resized_images(image, return_big=True, avoid_resize_big=False)
		self.image_big = data["image"]
		self.image_medium = data["image_medium"]
		self.image_small = data["image_small"]
#		self.image_filename = str(image.name)
		return True


