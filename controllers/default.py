# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def addItem():
    addform = SQLFORM(db.item, formstyle = 'bootstrap3_stacked')
    if addform.process().accepted:
       response.flash = 'form accepted'
       redirect(URL('default','index'))
    elif addform.errors:
       response.flash = 'form has errors'
    return dict (form=addform)
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def collections():
    return dict()

def collection():
    return dict()

def new_collection():
    addform = FORM(DIV(LABEL('Name*', _for='product_name',_class="checkbox col-xs-12")),
               DIV(INPUT(_name='name', _placeholder = "Name of collection...",requires=IS_NOT_EMPTY(),_class="form-control"),_class = "form-group col-xs-6"),
               DIV(LABEL(INPUT(_name='private',_type="checkbox", _checked="checked"),'Private?'),_class="checkbox col-xs-12"),
               DIV(INPUT(_type='submit',_class="btn btn-default"),_class="col-xs-12"),_class="small_margins")
    if addform.accepts(request,session):
        db.collection.insert(name=request.vars.name,private=request.vars.private)
        db.commit
        response.flash = 'New product added to store.'
    elif addform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(addform=addform)

def edit_collection():
    return dict()

def add_to_collection():
    return dict()

def wishlist():
    return dict()

def have_list():
    return dict()

def edit_wishlist_item():
    return dict()

def add_to_wishlist():
    return dict()
