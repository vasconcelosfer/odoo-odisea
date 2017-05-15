# -*- coding: utf-8 -*-
{
    'name': "Odisea",
    'summary': """Odoo sistema de Seguimiento de Expedientes y Actuaciones
       """,
    'description': """
      
    """,
    'author': "Leandro Fredes, Fernando Vasconcelos",
    'website': "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','hr'],
    # always loaded
    'data': [
        "views/event_view.xml",
        "views/note_view.xml",

	#"views/note_view_criterio.xml",
	#"views/image_view.xml",

#	"views/image_view.xml",

        "views/expedient_view.xml",
	"views/odisea_menuitems.xml",
        "views/hr_employee_view_inh.xml",
	"views/representative_view.xml",
	"views/odisea_statics_view.xml",
	"workflow/expedient_workflow.xml",
	"views/branch_view.xml",
	"data/ir_cron.xml",
        #"views/res_partner_view_inh.xml",
        #'security/ir.model.access.csv',
    ],
    'update_xml': [
    ],

    # only loaded in demonstration mode
    'demo': [
#        'demo.xml',
    ],
}
