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
    if auth.user:
        return dict(collections= db((db.collection.ownedBy == auth.user.id) & (db.collection.name != "Have List")& (db.collection.name != "Want List")).select(),
                    items = db((db.item.ownedBy == auth.user.id)).select())
    else:
        return dict(collections= db((db.collection.id > 0) & (db.collection.name != "Have List")& (db.collection.name != "Want List")).select())

def collection():
    return dict(items =db(db.item.inCollection.contains(request.args(0))).select(), collection = db.collection(request.args(0)))

def new_collection():
    addform = FORM(DIV(LABEL('Name*', _for='product_name',_class="checkbox col-xs-12")),
               DIV(INPUT(_name='name', _placeholder = "Name of collection...",requires=IS_NOT_EMPTY(),_class="form-control"),_class = "form-group col-xs-6"),
               DIV(LABEL(INPUT(_name='private',_type="checkbox", _checked="checked"),'Private?'),_class="checkbox col-xs-12"),
               DIV(INPUT(_type='submit',_class="btn btn-default"),_class="col-xs-12"),_class="small_margins")
    if addform.accepts(request,session):
        db.collection.insert(name=request.vars.name,private=request.vars.private)
        db.commit
        redirect(URL('default','collections'))
    elif addform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(addform=addform)

def edit_collection():
    record = db.collection(request.args(0))
    updateform = FORM(DIV(LABEL('Name*', _for='product_name',_class="checkbox col-xs-12")),
               DIV(INPUT(_name='name', value = record.name,_placeholder = "Name of collection...",requires=IS_NOT_EMPTY(),_class="form-control"),_class = "form-group col-xs-6"),
               DIV(LABEL(INPUT(_name='private',_type="checkbox", _checked=record.private),'Private?'),_class="checkbox col-xs-12"),
               DIV(INPUT(_type='submit',_class="btn btn-default"),_class="col-xs-12"),_class="small_margins")
    if updateform.accepts(request,session):
        record.update_record(name=request.vars.name,private=request.vars.private)
        redirect(URL('default','collections'))
    elif updateform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(updateform=updateform)
def add_to_collection():
    record = db.collection(request.args(0))
    inCollectionList=[record.id]
    addform = FORM(DIV(
               DIV(LABEL('Name*', _for='product_name')),
               DIV(INPUT(_name='name',_placeholder = "Name of item...",requires=IS_NOT_EMPTY(),_class="form-control")),
               BR(),
               DIV(LABEL('Value*', _for='product_name')),
               DIV(INPUT(_name='value',_placeholder = "Value of item...",requires=IS_NOT_EMPTY() and IS_INT_IN_RANGE(0,9999),_class="form-control")),
               BR(),
               DIV(LABEL('Type*', _for='product_name')),
               DIV(SELECT('Advertising and Brand','Architectural','Art','Books,Magazines and Paper','Clothing,Fabric and Textiles','Coins,Currency,Stamps',
                          'Film and Television','Glass and Pottery','Household Items','Memorabilia','Music','Nature and Animals','Sports','Technology',
                          'Themed','Toys and Games','Miscellaneous', value='Miscellaneous',_name='type',_class="form-control")),
              _class='form-group col-xs-6'),
               DIV(
               DIV(LABEL('Image*', _for='product_name')),
               DIV(INPUT(_name='image',_type='file')),
               BR(),
               DIV(LABEL('Description', _for='product_name')),
               DIV(TEXTAREA(_name='description',_class='form-control',_rows='8',_placeholder='Please enter item description')),
               BR(),
               DIV(INPUT(_type='submit',_class="form-control btn btn-default")),
                   _class='form-group col-xs-6'),_class="small_margins")
    if addform.accepts(request,session):
        image = db.item.image.store(request.vars.image.file,request.vars.image.filename)
        db.item.insert(name=request.vars.name,price=request.vars.value,type=request.vars.type,description=request.vars.description,
                       inCollection=inCollectionList,ownedBy=auth.user.id,image=image)
        db.commit
        redirect(URL('default','collections'))
    elif addform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(addform=addform)

def wishlist():
    return dict()

def have_list():
    return dict()

def edit_wishlist_item():
    return dict()

def add_to_wishlist():
    return dict()

def advanced_search():
    return dict()

def trade():
    return dict()

def trade_history():
    return dict()
