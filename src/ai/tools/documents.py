from documents.models import Document
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from django.db.models import Q
from asgiref.sync import async_to_sync
from mypermit import permit_client as permit

@tool
def search_query_documents(query:str, limit:int=5, config:RunnableConfig= {}):
    """ search the most recent LIMIT documents for the current user  with maximum of 25
    arguments:
    query:stirng or lookup search across title or content of document
    limit: number of results
    """
    if limit > 25:
            limit = 25
    configurable = config.get('configurable') or {}
    user_id = configurable.get('user_id')
    qs=Document.objects.filter(owner_id = user_id, active=True).order_by("-created_at")
    default_lookups={
        
        "active":True,
        "title__icontains":query
    }
    has_perms = async_to_sync(permit.check)(f"{user_id}","read","document")
    if not has_perms:
        raise Exception("You do not have permission to do search the document.")
    qs = Document.objects.filter(**default_lookups).filter(
        Q(title__icontains = query) |
        Q(content__icontains=query)
        ).order_by("-created_at")
    response_data=[]
    for obj in qs[:limit]:
        response_data.append(
            {
                "id":obj.id,
                "title":obj.title
            }
        )
    return response_data


@tool
def list_documents(limit:int=5, config:RunnableConfig = {} ):
    """ Get the most recent Limit documents for the current user with maximum of 25 
    arguments
    limit: number of result
    """
    if limit > 25:
        limit = 25
    configurable = config.get('configurable') or {}
    user_id = configurable.get('user_id')
    has_perms = async_to_sync(permit.check)(f"{user_id}","read","document")
    if not has_perms:
            raise Exception("You do not have permission to do list the document.")
     
    qs=Document.objects.filter( active=True).order_by("-created_at")
    response_data=[]
    for obj in qs[:limit]:
        response_data.append(
            {
                "id":obj.id,
                "title":obj.title
            }
        )
    return response_data

@tool
def get_document(document_id:int, config:RunnableConfig):
    """ get the details of a document for the current user"""
    configurable = config.get('configurable') or {}
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    has_perms = async_to_sync(permit.check)(f"{user_id}","read","document")
    if not has_perms:
            raise Exception("You do not have permission to do Get the individual document.")
     
    try:
        obj= Document.objects.get(id=document_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
            raise Exception("Invalid request for a document detail, try again")
        
    response_data={
        "id":obj.id,
        "title":obj.title,
        "content":obj.content,
        "created_at":obj.created_at
    }
    return response_data

@tool
def create_document(title:str, content:str, config:RunnableConfig):
    """ Create a new document to store for the user 
    Argument are:
     title: string max character of 10
     content: lang form text in many paragraphs or pages
     """
    configurable = config.get('configurable') or {}
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    has_perms = async_to_sync(permit.check)(f"{user_id}","read","document")
    if not has_perms:
            raise Exception("You do not have permission to do Create the document.")
     
    obj= Document.objects.create(title = title, content = content,owner_id=user_id, active=True)
    
    response_data={
        "id":obj.id,
        "title":obj.title,
        "content":obj.content,
        "created_at":obj.created_at
    }
    return response_data

@tool
def update_document(document_id:int, title:str = None, content:str = None , config:RunnableConfig= None):
    """ Update the document for the user by the document id and related field 
    Argument are:
    document_id: id of the document (required)
     title: string max character of 10 (optional)
     content: lang form text in many paragraphs or pages (optional)
     """
    configurable = config.get('configurable') or {}
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    has_perms = async_to_sync(permit.check)(f"{user_id}","update","document")
    if not has_perms:
            raise Exception("You do not have permission to do update the document.")
     
    try:
        obj= Document.objects.get(id=document_id,owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
            raise Exception("Invalid request for a document detail, try again")
    if title is not None:
        obj.title = title
    if content is not None:
        obj.content = content
    if title or content:
        obj.save()
    # obj= Document.objects.create(title = title, content = content,owner_id=user_id, active=True)
    
    response_data={
        "id":obj.id,
        "title":obj.title,
        "content":obj.content,
        "created_at":obj.created_at
    }
    return response_data


@tool
def delete_document(document_id:int, config:RunnableConfig):
    """ delete the document for the current user by document_id"""
    configurable = config.get('configurable') or {}
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    has_perms = async_to_sync(permit.check)(f"{user_id}","delete","document")
    if not has_perms:
            raise Exception("You do not have permission to do delete the document.")
     
    try:
        obj= Document.objects.get(id=document_id,owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
            raise Exception("Invalid request for a document detail, try again")
    obj.delete()
        
    response_data={
        "message":"success"
       
    }
    return response_data

document_tools =[
    search_query_documents,
    create_document,
    list_documents,
    get_document,
    update_document,
    delete_document
]