# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class project_task(osv.osv):
    _inherit="project.task"
    
    def create(self,cr,uid,vals,context=None):
        if vals.get('sequence1','/')=='/':
            vals['sequence1']=self.pool.get('ir.sequence').get(cr,uid,'project.task.seq',context=None) or '/'
        return super(project_task,self).create(cr,uid,vals,context=None)

    def seq2existing(self,cr,uid,id1,context):
        ids=self.search(cr, uid, args=[], offset=0, limit=None, order=None, context=None, count=False)
        for id in ids:
            seq=self.browse(cr,uid,id,context)
            if seq.sequence1=='/' or seq.sequence1=='':
                vals={'sequence1':self.pool.get('ir.sequence').get(cr,uid,'project.task.seq',context=None) or '/'}
                self.write(cr,uid,id,vals,context)
        return True
    
    def name_get(self, cr, uid, ids, context=None):
        l = super(project_task,self).name_get(cr, uid, ids, context=None)
        p_task =self.pool.get("project.task")
        final_dict = []
        for i in l:
            result = p_task.read(cr,uid,i[0],['sequence1'],context)
            if result.get('sequence1',False):
                final_dict.append((i[0],i[1]+'['+result.get('sequence1',"-")+']'))
        return final_dict  
    
    _defaults={
               'sequence1':'/',
               }
    
    _columns={
              'sequence1':fields.char(),
              }
    
