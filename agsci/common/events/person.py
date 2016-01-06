# Update person when person edited

def onPersonEdit(context, event):

    username = getattr(context, 'username', '')
    
    if username:
    
        username = username.encode('utf-8')
    
        if username != context.getId():
        
            parent = context.aq_parent
            
            if username not in parent.objectIds():
                parent.manage_renameObjects(ids=[context.getId()], new_ids=[username])
