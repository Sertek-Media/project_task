# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class sale_order(osv.osv):
    _inherit='sale.order'
    
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        invoice_vals=super(sale_order,self)._prepare_invoice(cr,uid,order,lines,context)
        additional_notes=""
        i=1
        total_tasks=order.associated_tasks
        
        for task_obj in total_tasks:
            additional_notes+= "\n"+str(i)+"."+ (task_obj.name)+"("+str(task_obj.sequence1)+")"
            i+=1
        invoice_vals['comment']=additional_notes
        return invoice_vals
    
    def _associated_tasks_with_saleorder(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for id in ids:
            project_task_ids = self.pool.get('project.task').search(cr,uid,[('sale_order_id','=',id)], offset=0, limit=200, order=None, context=None, count=False)
            result.update({id:[(6,0,project_task_ids)]})
        return result
        
        
    _columns={
               'associated_tasks':fields.function(_associated_tasks_with_saleorder,type='many2many',relation='project.task',string="Associated Tasks"),
#               'task_id':fields.many2many('project.task',string='Associated Task'),
#               'task_no':fields.char(string="Task No"),
              }
     
