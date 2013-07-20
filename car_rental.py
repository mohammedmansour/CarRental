import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
import netsvc
from osv import fields, osv
import tools
from tools.translate import _
import decimal_precision as dp


###################################
##This Object to specify the veihcle make

class car_make(osv.osv):
    _name='car.make'
    _description='this module to add a new veihcle make'
    _columns={
              'name':fields.char('Car Make',size=100,required=True,translate=True),
              'car_rental_id': fields.one2many('car.rental', 'car_make_id' , 'Veihcle Make'),
                             
             }
car_make()  

###################################
##This Object to specify the veihcle brand

class car_brand(osv.osv):
    _name='car.brand'
    _description='this module to add a new veihcle brand'
    _columns={
              'name':fields.char('Car Brand',size=100,required=True,translate=True),
              'car_rental_id': fields.one2many('car.rental', 'car_brand_id' , 'Veihcle Brand'),
               
             }
car_brand()  

    
###################################
#This Object to specify the veihcle class

class car_class(osv.osv):
    _name='car.class'
    _description='this module to add a new veihcle class'
    _columns={
              'name':fields.char('Car Class',size=100,required=True,translate=True),
              'car_rental_id': fields.one2many('car.rental', 'car_class_id' , 'Veihcle Class'),
               
             }
car_class()  

###################################
#This Object to specify the veihcle color

class car_color(osv.osv):
    _name='car.color'
    _description='this module to add a new veihcle color'
    _columns={
              'name':fields.char('Car Class',size=100,required=True,translate=True),
              'car_rental_id': fields.one2many('car.rental', 'car_color_id' , 'Veihcle Color'),
               
             }
car_color()  

###################################
# this Object to determine the veihcle information

class car_rental(osv.osv):

    _name='car.rental'
    _inherits = {'product.product': 'product_id'}
    #_inherit='product.product'
    _description='Module for Veihcle Information'
    _columns={              
              'car_make_id': fields.many2one('car.make', 'Vehicle Make'),
              'car_brand_id': fields.many2one('car.brand', 'Vehicle Brand'),
              'car_class_id': fields.many2one('car.class', 'Vehicle Class'),
              'car_color_id': fields.many2one('car.color', 'Vehicle Color'),
              'product_image': fields.binary('Image' , 'Vehicle Image'),  #inherited from product.product             
              'notes':fields.text('Details'),
              
              'name':fields.char('Vehicle Name',size=20,required=True),
              'regnno':fields.char('Vehicle Registration #',size=11,required=True),
              'company':fields.many2one('res.company','Company',required=True),              
              'year':fields.char('Year',size=4),              
              'serial':fields.char('productSerial #',size=50),
              'type': fields.selection([
                         ('truck','Truck'),
                         ('bus','Bus'),
                         ('car','Car')], 'Class', required=True,),        
              'status': fields.selection([
                        ('active','Active'),
                        ('inactive','InActive'),
                        ('outofservice','Out of Service'),                        
                        ], 'status', required=True,),
              'ownership': fields.selection([
                        ('owned','Owned'),
                        ('leased','Leased'),
                        ('rented','Rented'),                       
                        ], 'Ownership', required=True),                               
              'cmil':fields.float('Current Mileage',digits = (16,3)),
              'bmil':fields.float('Base Mileage',digits=(16,3),help="The last recorded mileage"),
              'bdate':fields.date('Recorded Date',help="Date on which the mileage is recorded"),
              'pdate':fields.date('Purchase Date',help="Date of Purchase of vehicle"),
              'pcost':fields.float('Purchase Value',digits=(16,2)),
              
              'ppartner':fields.many2one('res.partner','Purchased From'),              
			  
              'pinvoice':fields.char('Purchase Invoice',size=15),
              'podometer':fields.integer('Odometer at Purchase'),
              'startodometer':fields.integer('Start Odometer',required=True),                            
              'deprecperc':fields.float('Depreciation in %',digits=(10,2),required=True),
              'deprecperd':fields.selection([
                                               ('monthly','Monthly'),
                                               ('quarterly','Quarterly'),
                                               ('halfyearly','Half Yearly'),
                                               ('annual','Yearly')
                                               ],'Depr. period',required=True),                
              'primarymeter':fields.selection([
                                                 ('odometer','Odometer'),
                                                 ('hourmeter','Hour Meter'),
                                                 ],'Primary Meter',required=True),
              'fueltype':fields.selection([
                                             ('hyrbrid','Hybrid'),
                                             ('diesel','Diesel'),
                                             ('gasoline','Gasoline'),
                                             ('cng','C.N.G'),
                                             ('lpg','L.P.G'),
                                             ('electric','Electric')
                                             ],'Fuel Used',required=True),             
              'fueltankcap':fields.float('Fuel Tank Capacity'),
              'warrexp':fields.date('Date',help="Expiry date for warranty of product"),
              'warrexpmil':fields.integer('(or) Mileage',help="Expiry mileage for warranty of product"),         
		      'veihcle_id': fields.one2many('car.rental.contract', 'veihcle_id' , 'Veihcle To Rent'),                              
              
    }
    _defaults = {
        'type':lambda *a:'vehicle',
        'status':lambda *a:'active',
        'ownership':lambda *a:'owned',
        'fueltype':lambda *a:'diesel',
        'primarymeter':lambda *a:'odometer',
        'deprecperd':lambda *a:'annual'
        
    }
car_rental()
       

###################################
#this Object for making a rental contract between the company and the customer

class car_rental_contract(osv.osv):
    _name='car.rental.contract'
    _description='Module for Car Rental Management'
	
	#this method to autocomlete the vehicle information by vehicle_id
    def onchange_veihcle_id(self, cr, uid, ids, vehicle_id):
		val={}
		if vehicle_id:
			vehicle=self.pool.get('car.rental').browse(cr,uid,vehicle_id)
			val['car_make']=vehicle.car_make_id.name			
			val['car_brand']=vehicle.car_brand_id.name
			val['car_class']=vehicle.car_class_id.name
			val['car_color']=vehicle.car_color_id.name
		return {'value':val}
		
    _columns={
              'customer_id': fields.many2one('res.partner', 'Renter Name', required=True),
			  'veihcle_id':  fields.many2one('car.rental', 'Veihcle To Rent', required=True),
			  ############ AutoComplete this fields ################
			  #type='many2one',relation='car.make',
			  'car_make':fields.char('Car Make', size=50, readonly=True),
			  'car_brand':fields.char('Car Brand', size=50, readonly=True),
			  'car_class':fields.char('Car Class', size=50, readonly=True),
			  'car_color':fields.char('Car Color', size=50, readonly=True),
			  #'car_make': fields.related('veihcle_id', 'car_make_id', readonly=True , type='char', string='Vehicle Make'),			  			  
			  ############
              'cost':fields.float('Rent Cost',help='This fiels to determine the cost of rent per hour', required=True),
              'rent_start_date': fields.date('Rent Start Date', required=True),
              'rent_end_date':fields.date('Rent End Date', required=True),
              'rent_state':fields.selection([('cancelled','Cancelled'),('running','Running'),('finished','Finished')],'Rent State'),              
              'notes':fields.text('Details'),                                                
    }
    _defaults = {
        'rent_state' : lambda *a : 'running',        
        'rent_start_date': lambda *a: time.strftime('%Y-%m-01'),
        'rent_end_date': lambda *a: str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10],        
    }
car_rental_contract()
