


## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)
from gluon.tools import Auth
import datetime

#if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
#    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
#else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')


db = DAL('sqlite://whatever.db')


auth = Auth(db)
db.define_table(
    auth.settings.table_user_name,
    Field('username', length=128, default='',unique=True), # required
    Field('password', 'password', length=512,            # required
          readable=False, label='Password'),
    Field('registration_key', length=512,                # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,              # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,                 # required
          writable=False, readable=False, default=''))

## do not forget validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.username.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [ CRYPT()]
custom_auth_table.password.requires = [IS_NOT_EMPTY(error_message="Please type a password")]
custom_auth_table.username.requires = [IS_NOT_IN_DB(db, custom_auth_table.username)]




auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table
auth.define_tables(username=True)


db.define_table('collection',
Field('dateCreated','date',readable = False, writable = False, default = datetime.date.today()),
Field('name','string', label='Name*', length = 128),
Field('private','boolean',label='Private?', default = True),
Field('ownedBy','reference auth_user', readable = False, writable = False, default = auth.user))

#validators
db.collection.dateCreated.requires = IS_DATE(format=T('%d-%m-%Y'),error_message='Date must be in format DD-MM-YYYY')
db.collection.name.requires = IS_NOT_EMPTY(error_message="Please enter a name for the collection")
db.collection.name.widget = lambda f,v: SQLFORM.widgets.string.widget(f, v,
    _placeholder='Name of collection...', _class = "form-control")

db.define_table('trades',
Field('user_1_trading_items', 'list:reference item'),
Field('user_2_trading_items', 'list:reference item'),
Field('user_1','reference auth_user'),
Field('user_2','reference auth_user'),
Field('user_to_respond','reference auth_user'))

#validators


db.define_table('item',
Field('image','upload'),
Field('name','string'),
Field('price','integer'),
Field('type', 'list:string'),
Field('description','string'),
Field('inCollection', 'list:reference collection'),
Field('ownedBy','reference auth_user', readable = False, writable = False, default = auth.user))

#validators
db.item.name.requires = IS_NOT_EMPTY(error_message="Please add a name for the item")
db.item.description.requires = IS_LENGTH(maxsize=300, error_message = "Description is too long. Maximum 300 characters")

if auth.user:
    db.item.inCollection.requires = IS_IN_DB(db((db.collection.ownedBy==auth.user.id) &(db.collection.name != "Want List") & (db.collection.name != "Have List")), 'collection.id', '%(name)s', multiple = True)
else: db.item.inCollection.requires = IS_IN_DB(db(db.collection.id > 0), 'collection.id', '%(name)s')

db.item.type.requires = IS_IN_SET(['Advertising and Brand',
                                   'Architectural',
                                   'Art',
                                   'Books,Magazines and Paper',
                                   'Clothing,Fabric and Textiles',
                                   'Coins,Currency,Stamps',
                                   'Film and Television',
                                   'Glass and Pottery',
                                   'Household Items',
                                   'Memorabilia',
                                   'Music',
                                   'Nature and Animals',
                                   'Sports',
                                   'Technology',
                                   'Themed',
                                   'Toys and Games'],
                                  zero=T('Select one from below'),
         error_message='Must be one from list')


    ## session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## login after registration and redirect to home page

auth.settings.login_after_registration = True
auth.settings.login_url = URL('default','index')



auth.settings.register_onaccept.append(lambda form: db.collection.insert(dateCreated = datetime.date.today(), private = True, name = "Default Collection", ownedBy = form.vars.id ))
auth.settings.register_onaccept.append(lambda form: db.collection.insert(dateCreated = datetime.date.today(), private = False, name = "Have List", ownedBy = form.vars.id ))
auth.settings.register_onaccept.append(lambda form: db.collection.insert(dateCreated = datetime.date.today(), private = False, name = "Want List", ownedBy = form.vars.id ))

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
