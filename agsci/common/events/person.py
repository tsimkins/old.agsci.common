# Update person when person edited

def onPersonEdit(context, event):

    user_id = getattr(context, 'user_id', '')
    
    if user_id:
    
        user_id = user_id.encode('utf-8')
    
        if user_id != context.getId():
        
            parent = context.aq_parent
            
            if user_id not in parent.objectIds():
                parent.manage_renameObjects(ids=[context.getId()], new_ids=[user_id])
