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

class odisea_representative(models.Model):

	_name = 'odisea.representative'

	@api.multi
	def _has_image(self):
		return dict((p.id, bool(p.image)) for p in self)

        name = fields.Char(string='Name', required=True)
	cuit = fields.Char(string='CUIT', size=13)
	title = fields.Many2one('res.partner.title', 'Title')
        company = fields.Char(string='Company')
        ref = fields.Char('Contact Reference', select=1)
        website = fields.Char('Website', help="Website of Partner or Company")
        comment = fields.Text('Notes')
        category_id = fields.Many2many('res.partner.category', id1='partner_id', id2='category_id', string='Tags')
        active = fields.Boolean('Active', default=True)
        street = fields.Char('Street')
        street2 = fields.Char('Street2')
 	zip = fields.Char('Zip', size=24, change_default=True)
        city = fields.Char('City')
        state_id = fields.Many2one("res.country.state", 'State', ondelete='restrict')
        country_id = fields.Many2one('res.country', 'Country', ondelete='restrict')
        email = fields.Char('Email')
        phone = fields.Char('Phone')
        fax = fields.Char('Fax')
        mobile = fields.Char('Mobile')
        birthdate = fields.Char('Birthdate')
        function = fields.Char('Job Position')
        is_company = fields.Boolean('Is a Company', help="Check if the contact is a company, otherwise it is a person")
        use_parent_address = fields.Boolean('Use Company Address', help="Select this if you want to set company's address information  for this contact")
        # image: all image fields are base64 encoded and PIL-supported
        image = fields.Binary("Image",
            help="This field holds the image used as avatar for this contact, limited to 1024x1024px")
        image_medium = fields.Binary(compute="_get_image",
            string="Medium-sized image",
            store= False,
            help="Medium-sized image of this contact. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views.")
        image_small = fields.Binary(compute="_get_image",
            string="Small-sized image",
            store= False,
            help="Small-sized image of this contact. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required.")
        has_image = fields.Boolean(compute=_has_image)
        color = fields.Integer('Color Index')

	@api.multi
	def onchange_state(self, state_id):
		if state_id:
			state = self.env['res.country.state'].browse(state_id)
			return {'value': {'country_id': state.country_id.id}}
		return {}

	@api.multi
	def onchange_type(self, is_company):
		value = {'title': False}
		if is_company:
			value['use_parent_address'] = False
			domain = {'title': [('domain', '=', 'partner')]}
		else:
			domain = {'title': [('domain', '=', 'contact')]}
		return {'value': value, 'domain': domain}


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
		return True

