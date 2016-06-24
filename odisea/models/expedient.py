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

class OdiseaExpedient(models.Model):
        """Expedient"""

        _name = 'odisea.expedient'

        _description = 'Expedient'

#        _order = "id desc"

        _states_ = [
        # State definition
                ('open', 'Open'),
                ('in_revision', 'In Revision'),
                ('closed', 'Closed'),
                ('annulled', 'Annulled'),
                ('cancel', 'Cancel'),
        ]

        _issues_ = [
        # Issue definition
                ('criterio', 'Criterio'),
                ('denuncia', 'Denuncia'),
                ('devolución', 'Devolución'),
                ('consulta', 'Consulta'),
                ('embarque_escalonado', 'Embarque Escalonado'),
                ('posicion_arancelaria', 'Posición Arancelaria'),
        ]

        _branches_ = [
        # Branch definition
                ('electricidad', 'Electricidad'), 
                ('maquinas', 'Maquinas'),
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

        exp_id = fields.Char(
                string=_('Number Com'),
                compute='_comp_expedient_id'
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
                string='Childs'
        )

        parent_id = fields.Many2one(
                'odisea.expedient',
                string='Parent'
        )

#        note_ids = fields.One2many(
#                'odisea.note',
#                'parent_id',    
#                string='Nota'
#        )

        branch = fields.Selection(
                _branches_,
                'Branch'                
        )

        is_child = fields.Boolean(
                string='Is child',
                required=False,
                default=False,
                readonly=False
        )

        _sql_constraints = [
                        ('expedient_unique',
                         'Unique(dependency,number,created_year)',
                         "El número de expediente debe ser único"),
        ]

        @api.one
        @api.depends('dependency','number','created_year' )
        def _comp_expedient_id(self):
                self.exp_id = (str(self.dependency) or '')+'-'+(str(self.number) or '')+'-'+(str(self.created_year) or '')        


#       files = fields.One2many(
#               "ir.attachment",
#       'odisea.salida_exp',
#               'num_exp',
#               string="Attachments"
#       )

        #Utiilzamos el campo que genera odoo create_date
#       issue_date = fields.Datetime(
#               string='Issue Date',
#           readonly=True,
#           required=False,
#           default=fields.Datetime.now
#       )
