# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

typeList = ['Advertising and Brand','Architectural','Art','Books,Magazines and Paper','Clothing,Fabric and Textiles','Coins,Currency,Stamps',
                          'Film and Television','Glass and Pottery','Household Items','Memorabilia','Music','Nature and Animals','Sports','Technology',
                          'Themed','Toys and Games','Miscellaneous']
import re
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
    form = auth()
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

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
        return dict(collections= db((db.collection.id > 0)& (db.collection.name != "Have List")& (db.collection.name != "Want List")).select(),
                    items = db((db.item.id > 0)).select(),form=auth())


def collections_of_user():
    return dict(collections= db((db.collection.ownedBy == request.args(0)) & (db.collection.private == False)).select(),
                items = db((db.item.id > 0)).select())

@auth.requires_login()
def collection():
    return dict(items =db(db.item.inCollection.contains(request.args(0))).select(), collection = db.collection(request.args(0)))

@auth.requires_login()
def collection_of_user():
    return dict(items =db(db.item.inCollection.contains(request.args(0))).select(), collection = db.collection(request.args(0)))

def new_collection():
    addform = FORM(DIV(LABEL('Name*', _for='product_name',_class="checkbox col-xs-12")),
               DIV(INPUT(_name='name', _placeholder = "Name of collection...",requires=IS_NOT_EMPTY(),_class="form-control"),_class = "form-group col-xs-6"),
               DIV(LABEL(INPUT(_name='private',_type="checkbox", _checked="checked"),'Private'),_class="checkbox col-xs-12"),
               DIV(INPUT(_type='submit', _value='Submit',_class="btn btn-primary"),_class="col-xs-12"),_class="small_margins")
    if addform.accepts(request,session):
        db.collection.insert(name=request.vars.name,private=request.vars.private)
        db.commit
        session.notification = "New collection added"
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
               DIV(INPUT(_name='name',_id='product_name', value = record.name,_placeholder = "Name of collection...",requires=IS_NOT_EMPTY(),_class="form-control"),_class = "form-group col-xs-6"),
               DIV(LABEL(INPUT(_name='private',_type="checkbox", _checked=record.private),'Private'),_class="checkbox col-xs-12"),
               DIV(INPUT(_type='submit', _value="Submit" ,_class="btn btn-primary"),_class="col-xs-12"),_class="small_margins")
    if updateform.accepts(request,session):
        if request.vars.private:
            x = True
        else:
            x = False
        record.update_record(name=request.vars.name,private=x)
        session.notification = "Collection edited"
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
               DIV(INPUT(_name='name',_id='product_name',_placeholder = "Name of item...",requires=IS_NOT_EMPTY(),_class="form-control")),
               BR(),
               DIV(LABEL('Value in £(British Pounds)*', _for='product_value')),
               DIV(INPUT(_name='value',_id='product_value',_placeholder = "Value of item...",requires=[IS_NOT_EMPTY(), IS_MATCH('[0-9]+',error_message='Please input value without any symbols. Numbers only') ,IS_INT_IN_RANGE(0,1000000001,error_message='Please input a value between 0 and 1 billion')] ,_class="form-control")),
               BR(),
               DIV(LABEL('Type*', _for='product_type')),
               DIV(SELECT('Advertising and Brand','Architectural','Art','Books,Magazines and Paper','Clothing,Fabric and Textiles','Coins,Currency,Stamps',
                          'Film and Television','Glass and Pottery','Household Items','Memorabilia','Music','Nature and Animals','Sports','Technology',
                          'Themed','Toys and Games','Miscellaneous', value='Miscellaneous',_name='type',_id='product_type',_class="form-control")),
               BR(),
               DIV(H2(LABEL(INPUT(_name='have_list',_type="checkbox"),'  Add to tradable items',_class="label label-default"))),
              _class='form-group col-xs-6'),
               DIV(
               DIV(LABEL('Image', _for='product_image')),
               DIV(INPUT(_name='image',_type='file',_id='product_image')),
               BR(),
               DIV(IMG(_id="upld_image", _alt="Preview of upload",_src=URL('static','images/question.jpg'),_width = 170, _height = 105)),
               BR(),
               DIV(LABEL('Description', _for='product_description')),
               DIV(TEXTAREA(_name='description',_id='product_description',_class='form-control',_rows='8',_placeholder='Please enter item description')),
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
        session.notification = "New item added to collection"
        redirect(URL('default','collections'))
    elif addform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(addform=addform, collection=record)

def delete_collection():
    db(db.collection.id ==  request.args(0)).delete()
    return dict()

@auth.requires_login()
def wishlist():
    myWishList = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Want List")).select()
    return dict(items = db((db.item.inCollection.contains(myWishList[0].id))).select())

@auth.requires_login()
def have_list():
    myHaveList = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Have List")).select()
    return dict(items = db((db.item.inCollection.contains(myHaveList[0].id))).select())


@auth.requires_login()
def trade():
    recordUser1 = db((db.collection.ownedBy == request.args(0)) & (db.collection.name == "Have List")).select()[0]
    recordUser2 = db((db.collection.ownedBy == request.args(1)) & (db.collection.name == "Have List")).select()[0]
    return dict(user1Tradables = db((db.item.inCollection.contains(recordUser1.id))).select(),
                user2Tradables = db((db.item.inCollection.contains(recordUser2.id))).select())

def trade_info():
    record = db.trades(request.args(0))
    user_1_trading_items = ""
    user_2_trading_items = ""
    for x in record.user_1_trading_items:
        user_1_trading_items += str(x.id) + ","
    for x in record.user_2_trading_items:
        user_2_trading_items += str(x.id) + ","

    return dict(user_1_trading_items = user_1_trading_items,user_2_trading_items=user_2_trading_items
                ,user_1 = record.user_1, user_2 = record.user_2, user_to_respond = record.user_to_respond)

@auth.requires_login()
def trade_history():
    myTrades = db((db.trades.user_1 == auth.user.id ) | (db.trades.user_2 == auth.user.id)).select()
    tradedItems = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Traded Items")).select()

    completed = []
    offer_received= []
    offer_sent = []
    for x in myTrades:
        ITEMSREC = ""
        for y in x.user_1_trading_items:
            ITEMSREC += y.name + ","

        ITEMSSENT = ""
        for y in x.user_2_trading_items:
            ITEMSSENT += y.name + ","

        if x.user_1 == auth.user.id:
            tradePartner = x.user_2
            itemsReceived = ITEMSSENT[:-1]
            itemsSent = ITEMSREC[:-1]

            IR = x.user_2_trading_items
            IS = x.user_1_trading_items
        else:
            tradePartner = x.user_1
            itemsReceived = ITEMSREC[:-1]
            itemsSent = ITEMSSENT[:-1]

            IR = x.user_1_trading_items
            IS = x.user_2_trading_items

        other_traded_items = db((db.collection.ownedBy == tradePartner) & (db.collection.name == "Traded Items")).select()
        temp = dict(trade_partner = tradePartner,items_received = itemsReceived, items_sent= itemsSent, trade_id = x.id)
        if x.user_to_respond is None:
            completed.append(temp)
            if not x.items_traded:
                for l in IR:
                    db.item.insert(name=l.name,price=l.price,type=l.type,description=l.description,inCollection=[tradedItems[0].id],ownedBy=auth.user.id,image=l.image)
                for l in IS:
                    db.item.insert(name=l.name,price=l.price,type=l.type,description=l.description,inCollection=[other_traded_items[0].id],ownedBy=tradePartner,image=l.image)
                x.update_record(items_traded = True)
        elif x.user_to_respond != auth.user.id:
            offer_sent.append(temp)
        elif x.user_to_respond == auth.user.id:
            offer_received.append(temp)


    return dict(form=auth(),completed = completed,offer_sent=offer_sent,offer_received = offer_received)

def edit_trade():
    record = db.trades(request.args(0))
    user_1_trading_items = request.vars.user_1_trading_items.split(',')
    user_2_trading_items = request.vars.user_2_trading_items.split(',')
    record.update_record(user_1_trading_items=user_1_trading_items,user_2_trading_items=user_2_trading_items,
                   user_1 = request.vars.user_1,user_2 = request.vars.user_2, user_to_respond = request.vars.user_to_respond)
    return dict()

def accept_trade():
    record = db.trades(request.args(0))
    record.update_record(user_to_respond = None)
    session.notification = "Trade Accepted"
    return dict()

def delete_trade():
    db(db.trades.id ==  request.args(0)).delete()
    return dict()

def all_users():
    allusers = []
    users = db(db.auth_user.id > 0).select(db.auth_user.username)
    for x in users:
        allusers.append(x.username)
    return response.json(allusers)


def create_new_trade():
    user_1_trading_items = request.vars.user_1_trading_items.split(',')
    user_2_trading_items = request.vars.user_2_trading_items.split(',')
    db.trades.insert(user_1_trading_items=user_1_trading_items,user_2_trading_items=user_2_trading_items,
                   user_1 = request.vars.user_1,user_2 = request.vars.user_2, user_to_respond = request.vars.user_to_respond)
    db.commit
    return dict()
    ## the request.vars.... is where you can add what is coming from your form and this will create a new trade.

def TEST_PAGE():
    return dict(s = session.tests)

def delete_item():
    if (request.args(0) == '0'):
        db(db.item.id ==  request.args(1)).delete()
    elif request.args(0) == '1':
        record = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Have List")).select()[0]
        item = db.item(request.args(1))
        collectionList = item.inCollection
        collectionList.remove(record.id)
        item.update_record(inCollection=collectionList)
    elif request.args(0) == '2':
        record = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Want List")).select()[0]
        item = db.item(request.args(1))
        collectionList = item.inCollection
        collectionList.remove(record.id)
        item.update_record(inCollection=collectionList)
    session.notification = "Item deleted"
    return dict()
def edit_item():
    record = db.item(request.args(0))
    if record.image == None:
        src = URL('static','images/question.jpg')
        alt = "?"
    else:
        src = URL('default','download', args=record.image)
        alt = "image for " + record.name
    editform = FORM(DIV(
               DIV(LABEL('Name*', _for='product_name')),
               DIV(INPUT(_name='name',_id='product_name',_value=record.name,_placeholder = "Name of item...",requires=IS_NOT_EMPTY(),_class="form-control")),
               BR(),
               DIV(LABEL('Value in £(British Pounds)*', _for='product_value')),
               DIV(INPUT(_name='value',_id='product_value',_value=record.price,_placeholder = "Value of item...",requires=[IS_NOT_EMPTY(), IS_MATCH('[0-9]+',error_message='Please input value without any symbols. Numbers only') ,IS_INT_IN_RANGE(0,1000000001,error_message='Please input a value between 0 and 1 billion')],_class="form-control")),
               BR(),
               DIV(LABEL('Type*', _for='product_type')),
               DIV(SELECT('Advertising and Brand','Architectural','Art','Books,Magazines and Paper','Clothing,Fabric and Textiles','Coins,Currency,Stamps',
                          'Film and Television','Glass and Pottery','Household Items','Memorabilia','Music','Nature and Animals','Sports','Technology',
                          'Themed','Toys and Games','Miscellaneous',_name='type',_id='product_type',value=record.type[0],_class="form-control")),
              _class='form-group col-xs-6'),
               DIV(
               DIV(IMG(_id='upld_image',_src=src,_alt=alt,_class="item_view")),
               BR(),
               DIV(LABEL('Change image: ', _for='product_image')),
               DIV(INPUT(_name='image',_type='file',_id='product_image')),
               BR(),
               DIV(LABEL('Description', _for='product_description')),
               DIV(TEXTAREA(_name='description',_id='product_description',value=record.description,_class='form-control',_rows='8',_placeholder='Please enter item description')),
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
        if request.vars['list_id'] == '0':
            session.notification = "Item edited"
            redirect(URL('default','collections'))
        if request.vars['list_id'] == '1':
            session.notification = "Item edited"
            redirect(URL('default','have_list'))
        if request.vars['list_id'] == '2':
            session.notification = "Item edited"
            redirect(URL('default','wishlist'))
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
               DIV(INPUT(_name='name',_id='product_name',_placeholder = "Name of item...",requires=IS_NOT_EMPTY(),_class="form-control")),
               BR(),
               DIV(LABEL('Value in £(British Pounds)*', _for='product_value')),
               DIV(INPUT(_name='value',_id='product_value',_placeholder = "Value of item...",requires=[IS_NOT_EMPTY(), IS_MATCH('[0-9]+',error_message='Please input value without any symbols. Numbers only') ,IS_INT_IN_RANGE(0,1000000001,error_message='Please input a value between 0 and 1 billion')],_class="form-control")),
               BR(),
               DIV(LABEL('Type*', _for='product_type')),
               DIV(SELECT('Advertising and Brand','Architectural','Art','Books,Magazines and Paper','Clothing,Fabric and Textiles','Coins,Currency,Stamps',
                          'Film and Television','Glass and Pottery','Household Items','Memorabilia','Music','Nature and Animals','Sports','Technology',
                          'Themed','Toys and Games','Miscellaneous', value='Miscellaneous',_name='type',_id='product_type',_class="form-control")),
              _class='form-group col-xs-6'),
               DIV(
               DIV(LABEL('Image', _for='product_image')),
               DIV(INPUT(_name='image',_id='product_image',_type='file')),
               BR(),
               DIV(LABEL('Description', _for='product_description')),
               DIV(TEXTAREA(_name='description',_id='product_description',_class='form-control',_rows='8',_placeholder='Please enter item description')),
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
        session.notification = "Item added to wishlist"
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
               DIV(INPUT(_name='name',_id='product_name',_placeholder = "Name of item...",requires=IS_NOT_EMPTY(),_class="form-control")),
               BR(),
               DIV(LABEL('Value in £(British Pounds)*', _for='product_value')),
               DIV(INPUT(_name='value',_id='product_value',_placeholder = "Value of item...",requires=[IS_NOT_EMPTY(), IS_MATCH('[0-9]+',error_message='Please input value without any symbols. Numbers only') ,IS_INT_IN_RANGE(0,1000000001,error_message='Please input a value between 0 and 1 billion')],_class="form-control")),
               BR(),
               DIV(LABEL('Type*', _for='product_type')),
               DIV(SELECT('Advertising and Brand','Architectural','Art','Books,Magazines and Paper','Clothing,Fabric and Textiles','Coins,Currency,Stamps',
                          'Film and Television','Glass and Pottery','Household Items','Memorabilia','Music','Nature and Animals','Sports','Technology',
                          'Themed','Toys and Games','Miscellaneous', value='Miscellaneous',_name='type',_id='product_type',_class="form-control")),
              _class='form-group col-xs-6'),
               DIV(
               DIV(LABEL('Image', _for='product_image')),
               DIV(INPUT(_name='image',_id='product_image',_type='file')),
               BR(),
               DIV(LABEL('Description', _for='product_description')),
               DIV(TEXTAREA(_name='description',_id='product_description',_class='form-control',_rows='8',_placeholder='Please enter item description')),
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
        session.notification = "Item added to tradable list"
        redirect(URL('default','have_list'))
    elif addform.errors:
        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'
    return dict(addform=addform, collection=record)

@auth.requires_login()
def advanced_search():
    searchform = FORM(DIV(
               DIV(LABEL('Keyword* (for both item name and description)', _for='keyword')),
               DIV(INPUT(_name='keyword',_id='keyword',_placeholder = "Search for...",requires=IS_NOT_EMPTY(),_class="form-control")),
               BR(),
               DIV(LABEL('Minimum price (in £)*', _for='price_range_min'),
               INPUT(_name='price_range_min',_value = 0,requires=[IS_NOT_EMPTY(), IS_MATCH('[0-9]+',error_message='Please input value without any symbols. Numbers only') ,IS_INT_IN_RANGE(0,1000000001,error_message='Please input a value between 0 and 1 billion')],_class="form-control col-xs-8",_id='price_range_min'),_class='form-group col-xs-6'),
               DIV(LABEL('Maximum price (in £)*', _for='price_range_max'),
               INPUT(_name='price_range_max',_value = 1000000000,requires=[IS_NOT_EMPTY(), IS_MATCH('[0-9]+',error_message='Please input value without any symbols. Numbers only') ,IS_INT_IN_RANGE(0,1000000001,error_message='Please input a value between 0 and 1 billion')] ,_class="form-control col-xs-8",_id='price_range_max'),_class='form-group col-xs-6'),
               BR(),
               BR(),
               DIV(LABEL(INPUT(_name='my_collection',_type="checkbox",_id='my_collection' ),'Search my collection'),_class="checkbox-inline",_for='my_collection'),
               BR(),
               DIV(LABEL(INPUT(_name='all_collections',_type="checkbox",_id='all_collections',_checked=True ),'Search all public collections'),_class="checkbox-inline",_for='all_collections'),
               BR(),BR(),
               DIV(LABEL(INPUT(_name='only_one_user',_type="checkbox",_id='only_one_user' ),'Only search collection of: (Name of collection owner) '),_class="checkbox-inline",_for='only_one_user'),
               LABEL('**Selecting this option deselects the two options above**', _for='single_collection_owner'),
               BR(),
               DIV(INPUT(_name='single_collection_owner',_id='single_collection_owner',_placeholder = "Search for...",_disabled = True,_class="form-control")),
               BR(),BR(),
               DIV(LABEL(INPUT(_type="checkbox",_name='only_tradables',id='only_tradables' ),'Only show tradable items'),_class="checkbox-inline",),

              _class='form-group col-xs-6'),
               DIV(
               P(B('Search in categories:')),
               DIV(INPUT(_type='button',_id = 'untickall', _value='Unselect All', _class="form-group col-xs-5 btn btn-info"),
               INPUT(_type='button',_id = 'tickall', _value='Select All', _class="form-group col-xs-5 btn btn-info pull-right")),
               BR(),BR(),
               DIV(LABEL(INPUT(_name ='art',_id ='art',_type="checkbox",_checked=True ),'Art', _class="categ1"),_class="checkbox-inline"),
               DIV(LABEL(INPUT(_name ='music',_id ='music',_type="checkbox",_checked=True ),'Music', _class="categ"),_class="checkbox-inline"),
               BR(),
               DIV(LABEL(INPUT(_name ='sports',_id ='sports',_type="checkbox",_checked=True ),'Sports', _class="categ"),_class="checkbox-inline"),
               DIV(LABEL(INPUT(_name ='tech',_id ='tech',_type="checkbox",_checked=True  ),'Technology', _class="categ"),_class="checkbox-inline"),
               BR(),
               DIV(LABEL(INPUT(_name ='themed',_id ='themed',_type="checkbox",_checked=True  ),'Themed', _class="categ2"),_class="checkbox-inline"),
               DIV(LABEL(INPUT(_name ='memorabilia',_id ='memorabilia',_type="checkbox",_checked=True  ),'Memorabilia', _class="categ"),_class="checkbox-inline"),
               BR(),
               DIV(LABEL(INPUT(_name ='ads',_id ='ads',_type="checkbox",_checked=True  ),'Advertising and Brand', _class="categ"),),
               DIV(LABEL(INPUT(_name ='architect',_id ='architect',_type="checkbox",_checked=True ),'Architectural', _class="categ"),),
               DIV(LABEL(INPUT(_name ='books',_id ='books',_type="checkbox",_checked=True ),'Books,Magazines and Paper', _class="categ"),),
               DIV(LABEL(INPUT(_name ='clothing',_id ='clothing',_type="checkbox",_checked=True ),'Clothing,Fabric and Textiles', _class="categ"),),
               DIV(LABEL(INPUT(_name ='coins',_id ='coins',_type="checkbox",_checked=True  ),'Coins,Currency,Stamps', _class="categ"),),
               DIV(LABEL(INPUT(_name ='glass',_id ='glass',_type="checkbox",_checked=True  ),'Glass and Pottery', _class="categ"),),
               DIV(LABEL(INPUT(_name ='house',_id ='house',_type="checkbox",_checked=True  ),'Household Items', _class="categ"),),
               DIV(LABEL(INPUT(_name ='nature',_id ='nature',_type="checkbox",_checked=True ),'Nature and Animals', _class="categ"),),
               DIV(LABEL(INPUT(_name ='toys',_id ='toys',_type="checkbox",_checked=True ),'Toys and Games', _class="categ"),),
               DIV(LABEL(INPUT(_name ='misc',_id ='misc',_type="checkbox",_checked=True  ),'Miscellaneous', _class="categ"),),
                    BR(),
               DIV(INPUT(_type='submit', _value='Submit', _class="form-control btn btn-primary")),
                   _class='form-group col-xs-6'),_class="small_margins")
    results = []
    thingthing = []
    if request.vars.art:thingthing.append('Art')
    if request.vars.music:thingthing.append('Music')
    if request.vars.sports:thingthing.append('Sports')
    if request.vars.tech:thingthing.append('Technology')
    if request.vars.themed:thingthing.append('Themed')
    if request.vars.memorabilia:thingthing.append('Memorabilia')
    if request.vars.ads:thingthing.append('Advertising and Brand')
    if request.vars.architect:thingthing.append('Architectural')
    if request.vars.books:thingthing.append('Books,Magazines and Paper')
    if request.vars.clothing:thingthing.append('Clothing,Fabric and Textiles')
    if request.vars.coins:thingthing.append('Coins,Currency,Stamps')
    if request.vars.glass:thingthing.append('Glass and Pottery')
    if request.vars.house:thingthing.append('Household Items')
    if request.vars.nature:thingthing.append('Nature and Animals')
    if request.vars.toys:thingthing.append('Toys and Games')
    if request.vars.misc:thingthing.append('Miscellaneous')


    if request.vars.only_tradables:
        temprows = db(db.collection.name == 'Have List').select()
    else:
        temprows = db((db.collection.private == False) & (db.collection.name != "Want List")).select()
    public_collection = []
    for x in temprows:
        public_collection.append(x.id)
    if searchform.accepts(request,session):

        s = request.vars.keyword
        s = re.sub(r'[^\w\s]','',s)
        if (request.vars.my_collection and request.vars.all_collections):
            tempresults = db(
                 ((db.item.name.like('%' + s + '%'))| (db.item.description.like('%' + s + '%')))
             & (db.item.price <= request.vars.price_range_max) & (db.item.price >= request.vars.price_range_min)
             ).select()
            for x in tempresults:
                if ([i for i in x.inCollection if i in public_collection] != []):
                        if x.type in thingthing:
                            results.append(x)


        elif request.vars.my_collection:

             if request.vars.only_tradables:
                 record = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Have List")).select()[0]
                 tempresults = db(
                 ((db.item.name.like('%' + s + '%'))| (db.item.description.like('%' + s + '%')))
            & (db.item.ownedBy == auth.user.id) & (db.item.inCollection.contains(record.id))& (db.item.price <= request.vars.price_range_max) & (db.item.price >= request.vars.price_range_min)
             ).select()
                 for x in tempresults:
                    if x.type in thingthing:
                        results.append(x)
             else:
                tempresults = db(
                 ((db.item.name.like('%' + s + '%'))| (db.item.description.like('%' + s + '%')))
            & (db.item.ownedBy == auth.user.id) & (db.item.price <= request.vars.price_range_max) & (db.item.price >= request.vars.price_range_min)
             ).select()
                for x in tempresults:
                    if x.type in thingthing:
                        results.append(x)

        elif request.vars.all_collections:

            tempresults = db(
                 ((db.item.name.like('%' + s + '%'))| (db.item.description.like('%' + s + '%')))
            & (db.item.ownedBy != auth.user.id) & (db.item.price <= request.vars.price_range_max) & (db.item.price >= request.vars.price_range_min)
             ).select()
            for x in tempresults:
                if ([i for i in x.inCollection if i in public_collection] != []):
                        if x.type in thingthing:
                            results.append(x)

        elif request.vars.only_one_user:

            record = db((db.auth_user.username == request.vars.single_collection_owner)).select()[0]

            tempresults = db(
                 ((db.item.name.like('%' + s + '%'))| (db.item.description.like('%' + s + '%')))
            & (db.item.ownedBy == record.id) & (db.item.price <= request.vars.price_range_max) & (db.item.price >= request.vars.price_range_min)
             ).select()
            for x in tempresults:
                if ([i for i in x.inCollection if i in public_collection] != []):
                        if x.type in thingthing:
                            results.append(x)

        session.results = results
        redirect(URL('default','search_results'))
    elif searchform.errors:

        response.flash = 'One or more of your form fields has an error. Please see below for more information'
    else:
        response.flash = 'Please complete the form below to add a new product.'

    return dict(searchform=searchform, form=auth())

def quick_search():
    results = []
    temprows = db((db.collection.private == False) & (db.collection.name != "Want List")).select()
    public_collection = []
    for x in temprows:
        public_collection.append(x.id)
    tempresults = db(
                 ((db.item.name.like('%' + request.vars.top_search + '%'))| (db.item.description.like('%' + request.vars.top_search + '%')))
             ).select()
    for x in tempresults:
        if ([i for i in x.inCollection if i in public_collection] != []):#
                results.append(x)
    return dict(items = results, form = auth())

@auth.requires_login()
def search_results():
    results = session.results
    return dict(items=results)




def logged_in():
    return dict(logged_in = auth.user)

def add_item_to_havelist():
    myHaveList = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Have List")).select()
    item = db.item(request.args(0))
    collectionList = item.inCollection
    collectionList.append(myHaveList[0].id)
    item.update_record(inCollection=collectionList)
    session.notification = "Item added to tradable list"

def add_item_to_wishlist():
    myWantList = db((db.collection.ownedBy == auth.user.id) & (db.collection.name == "Want List")).select()
    item = db.item(request.args(0))
    collectionList = [myWantList[0].id]

    db.item.insert(name=item.name,price=item.price,type=item.type,description=item.description,
                       inCollection=collectionList,ownedBy=item.ownedBy,image=item.image)
    db.commit
    session.notification = "Item added to wishlist"

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
    return dict(info = info, owner= owner, is_tradable = is_tradable, have_list_ok = have_list_ok, wishlist_ok = wishlist_ok, logged_in = auth.user.id)

def clearNotifications():
    session.notification = "None"

    return dict(x = session.notification)