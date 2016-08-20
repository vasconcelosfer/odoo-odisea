# -*- coding: utf-8 -*-
{
    'name': "Odisea",
    'summary': """Odoo sIstema de Seguimiento de Expedientes y Actuaciones
       """,
    'description': """
      
    """,
    'author': "Your Company",
    'website': "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        "views/event_view.xml",
        "views/note_view.xml",
        "views/expedient_view.xml",
	"views/odisea_menuitems.xml",
	"workflow/expedient_workflow.xml"
        # 'security/ir.model.access.csv',
    ],
    'update_xml': [
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
