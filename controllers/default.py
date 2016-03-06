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
    return dict(message=T('Welcome to web2py!'),form=auth())


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
def handle_user():
   return dict(form=auth())

def login_modal():
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
                    items = db((db.item.ownedBy == auth.user.id)).select(),form=auth())
    else:
        return dict(collections= db((db.collection.id > 0) & (db.collection.name != "Have List")& (db.collection.name != "Want List")).select(),
                    items = db((db.item.id > 0)).select(),form=auth())

def collection():
    return dict(items =db(db.item.inCollection.contains(request.args(0))).select(), collection = db.collection(request.args(0)))

def new_collection():
    addform = FORM(DIV(LABEL('Name*', _for='product_name',_class="checkbox col-xs-12")),
               DIV(INPUT(_name='name', _placeholder = "Name of collection...",requires=IS_NOT_EMPTY(),_class="form-control"),_class = "form-group col-xs-6"),
               DIV(LABEL(INPUT(_name='private',_type="checkbox", _checked="checked"),'Private'),_class="checkbox col-xs-12"),
               DIV(INPUT(_type='submit', _value='Submit',_class="btn btn-primary"),_class="col-xs-12"),_class="small_margins")
    if addform.accepts(request,session):
        db.collection.insert(name=request.vars.name,private=request.vars.private)
        db.commit
        redirect(URL('default','collections'))
    elif addform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(addform=addform)
@auth.requires_login()
def edit_collection():
    record = db.collection(request.args(0))
    updateform = FORM(DIV(LABEL('Name*', _for='product_name',_class="checkbox col-xs-12")),
               DIV(INPUT(_name='name', value = record.name,_placeholder = "Name of collection...",requires=IS_NOT_EMPTY(),_class="form-control"),_class = "form-group col-xs-6"),
               DIV(LABEL(INPUT(_name='private',_type="checkbox", _checked=record.private),'Private'),_class="checkbox col-xs-12"),
               DIV(INPUT(_type='submit', _value="Submit" ,_class="btn btn-primary"),_class="col-xs-12"),_class="small_margins")
    if updateform.accepts(request,session):
        record.update_record(name=request.vars.name,private=request.vars.private)
        redirect(URL('default','collections'))
    elif updateform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(updateform=updateform, collection=record)
def add_to_collection():
    record = db.collection(request.args(0))
    inCollectionList=[record.id]
    addform = FORM(DIV(
               DIV(LABEL('Name*', _for='product_name')),
               DIV(INPUT(_name='name',_placeholder = "Name of item...",requires=IS_NOT_EMPTY(),_class="form-control")),
               BR(),
               DIV(LABEL('Value*', _for='product_value')),
               DIV(INPUT(_name='value',_placeholder = "Value of item...",requires=IS_NOT_EMPTY() and IS_INT_IN_RANGE(0,9999),_class="form-control")),
               BR(),
               DIV(LABEL('Type*', _for='product_type')),
               DIV(SELECT('Advertising and Brand','Architectural','Art','Books,Magazines and Paper','Clothing,Fabric and Textiles','Coins,Currency,Stamps',
                          'Film and Television','Glass and Pottery','Household Items','Memorabilia','Music','Nature and Animals','Sports','Technology',
                          'Themed','Toys and Games','Miscellaneous', value='Miscellaneous',_name='type',_class="form-control")),
               BR(),
               DIV(LABEL(INPUT(_name='have_list',_type="checkbox"),'Add to have list'),_class="small_margins checkbox"),
              _class='form-group col-xs-6'),
               DIV(
               DIV(LABEL('Image*', _for='product_name')),
               DIV(INPUT(_name='image',_type='file')),
               BR(),
               DIV(LABEL('Description', _for='product_name')),
               DIV(TEXTAREA(_name='description',_class='form-control',_rows='8',_placeholder='Please enter item description')),
               BR(),
               DIV(INPUT(_type='submit', _value='Submit', _class="form-control btn btn-primary")),
                   _class='form-group col-xs-6'),_class="small_margins")
    if addform.accepts(request,session):
        if request.vars.have_list:
            myHaveList = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Have List")).select()
            inCollectionList.append(myHaveList[0].id)
        try:
            len(request.vars.image) #This means image not uploaded
            image = None
        except TypeError:
            #Image has been uploaded (as the exception occured); update image in db
            image = db.item.image.store(request.vars.image.file,request.vars.image.filename)
        db.item.insert(name=request.vars.name,price=request.vars.value,type=request.vars.type,description=request.vars.description,
                       inCollection=inCollectionList,ownedBy=auth.user.id,image=image)
        db.commit
        redirect(URL('default','collections'))
    elif addform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(addform=addform, collection=record)

@auth.requires_login()
def wishlist():
    myWishList = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Want List")).select()
    return dict(items = db((db.item.inCollection.contains(myWishList[0].id))).select())

@auth.requires_login()
def have_list():
    myHaveList = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Have List")).select()
    return dict(items = db((db.item.inCollection.contains(myHaveList[0].id))).select())

def edit_item():
    record = db.item(request.args(0))
    if record.image == None:
        src = URL('static','images/question.jpg')
        alt = "?"
    else:
        src = URL('default','download', args=record.image)
        alt = "img for" + record.name
    editform = FORM(DIV(
               DIV(LABEL('Name*', _for='product_name')),
               DIV(INPUT(_name='name',_value=record.name,_placeholder = "Name of item...",requires=IS_NOT_EMPTY(),_class="form-control")),
               BR(),
               DIV(LABEL('Value*', _for='product_value')),
               DIV(INPUT(_name='value',_value=record.price,_placeholder = "Value of item...",requires=IS_NOT_EMPTY() and IS_INT_IN_RANGE(0,9999),_class="form-control")),
               BR(),
               DIV(LABEL('Type*', _for='product_type')),
               DIV(SELECT('Advertising and Brand','Architectural','Art','Books,Magazines and Paper','Clothing,Fabric and Textiles','Coins,Currency,Stamps',
                          'Film and Television','Glass and Pottery','Household Items','Memorabilia','Music','Nature and Animals','Sports','Technology',
                          'Themed','Toys and Games','Miscellaneous',_name='type',value=record.type,_class="form-control")),
              _class='form-group col-xs-6'),
               DIV(
               DIV(LABEL('Current Image', _for='product_image')),
               DIV(IMG(_src=src,_alt=alt,_class="item_view")),
               BR(),
               DIV(LABEL('Change image: ', _for='product_name')),
               DIV(INPUT(_name='image',_type='file')),
               BR(),
               DIV(LABEL('Description', _for='product_name')),
               DIV(TEXTAREA(_name='description',value=record.description,_class='form-control',_rows='8',_placeholder='Please enter item description')),
               BR(),
               DIV(INPUT(_type='submit', _value='Submit', _class="form-control btn btn-primary")),
                   _class='form-group col-xs-6'),_class="small_margins")
    if editform.accepts(request,session):
        try:
            len(request.vars.image) #This means image not uploaded
            image = record.image
        except TypeError:
            image = db.item.image.store(request.vars.image.file,request.vars.image.filename)
        record.update_record(name=request.vars.name,price=request.vars.value,type=request.vars.type,description=request.vars.description,
                       image=image)
        redirect(URL('default','collections'))
    elif editform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(editform=editform)
def add_to_wishlist():
    record = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Want List")).select()[0]
    inCollectionList=[record.id]
    addform = FORM(DIV(
               DIV(LABEL('Name*', _for='product_name')),
               DIV(INPUT(_name='name',_placeholder = "Name of item...",requires=IS_NOT_EMPTY(),_class="form-control")),
               BR(),
               DIV(LABEL('Value*', _for='product_value')),
               DIV(INPUT(_name='value',_placeholder = "Value of item...",requires=IS_NOT_EMPTY() and IS_INT_IN_RANGE(0,9999),_class="form-control")),
               BR(),
               DIV(LABEL('Type*', _for='product_type')),
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
               DIV(INPUT(_type='submit', _value='Submit', _class="form-control btn btn-primary")),
                   _class='form-group col-xs-6'),_class="small_margins")
    if addform.accepts(request,session):
        try:
            len(request.vars.image) #This means image not uploaded
            image = None
        except TypeError:

            image = db.item.image.store(request.vars.image.file,request.vars.image.filename)
        db.item.insert(name=request.vars.name,price=request.vars.value,type=request.vars.type,description=request.vars.description,
                       inCollection=inCollectionList,ownedBy=auth.user.id,image=image)
        db.commit
        redirect(URL('default','wishlist'))
    elif addform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(addform=addform, collection=record)

def add_to_havelist():
    record = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Have List")).select()[0]
    inCollectionList=[record.id]
    addform = FORM(DIV(
               DIV(LABEL('Name*', _for='product_name')),
               DIV(INPUT(_name='name',_placeholder = "Name of item...",requires=IS_NOT_EMPTY(),_class="form-control")),
               BR(),
               DIV(LABEL('Value*', _for='product_value')),
               DIV(INPUT(_name='value',_placeholder = "Value of item...",requires=IS_NOT_EMPTY() and IS_INT_IN_RANGE(0,9999),_class="form-control")),
               BR(),
               DIV(LABEL('Type*', _for='product_type')),
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
               DIV(INPUT(_type='submit', _value='Submit', _class="form-control btn btn-primary")),
                   _class='form-group col-xs-6'),_class="small_margins")
    if addform.accepts(request,session):
        try:
            len(request.vars.image) #This means image not uploaded
            image = None
        except TypeError:

            image = db.item.image.store(request.vars.image.file,request.vars.image.filename)
        db.item.insert(name=request.vars.name,price=request.vars.value,type=request.vars.type,description=request.vars.description,
                       inCollection=inCollectionList,ownedBy=auth.user.id,image=image)
        db.commit
        redirect(URL('default','wishlist'))
    elif addform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(addform=addform, collection=record)
def advanced_search():
    return dict(form=auth())

def trade():
    return dict()

def trade_history():
    return dict()

def logged_in():
    return dict(logged_in = auth.user)

def item_info_by_id():
    info = db(db.item.id == request.get_vars.id).select()
    owner_id = db(db.item.id == request.get_vars.id).select(db.item.ownedBy)[0].ownedBy
    owner = db(db.auth_user.id == owner_id).select(db.auth_user.username)

    theirHaveList = db((db.collection.ownedBy == owner_id) & (db.collection.name == "Have List")).select()
    if (owner_id != auth.user.id) and (theirHaveList[0].id in info[0].inCollection):
        is_tradable = True
    else:
        is_tradable = False
    ## NEED is_tradable = True/False


    myHaveList = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Have List")).select()
    if (info[0].ownedBy == auth.user.id) and (myHaveList[0].id not in info[0].inCollection):
        have_list_ok = True
    else:
        have_list_ok = False

    myWishList = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Want List")).select()
    if (info[0].ownedBy != auth.user.id) and (myWishList[0].id not in info[0].inCollection):
        wishlist_ok = True
    else:
        wishlist_ok = False
    return dict(info = info, owner= owner, is_tradable = is_tradable, have_list_ok = have_list_ok, wishlist_ok = wishlist_ok)
