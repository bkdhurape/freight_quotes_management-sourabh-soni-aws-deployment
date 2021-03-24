from address.models.address import Address
from address.services.address_service import AddressService
from address.serializers import AddressSerializer
from exceptions import ProductException, ProductError, PortException, PortError, AddressException, AddressError
from entity.models.entity import Entity
from port.models.port import Port
from product.models.product import Product
from product.serializers import ProductSerializer
from utils.base_models import StatusBase
from utils.responses import get_paginated_data


class ProductService:

    def __init__(self, data):
        self.data = data

    #  Get all products
    def get_all(self, entity_id):
        Entity.find_by(id=entity_id, status=StatusBase.ACTIVE)
        products = Product.find_by(multi=True, entity=entity_id, status=StatusBase.ACTIVE)

        products_paginated_data = get_paginated_data(ProductSerializer, products, self.data)

        if products_paginated_data:
            for product in products_paginated_data:
                product['addresses'] = self.get_all_product_address(entity_type = 'product', entity_id = product['id'])

            return products_paginated_data

        return False


    #  Create product
    def create(self, entity_id):
        Entity.find_by(id=entity_id, status=StatusBase.ACTIVE)
        self.data['entity'] = entity_id

        self.validate_address_transport_mode_and_ports();

        product_serializer = ProductSerializer(data=self.data)
        if product_serializer.is_valid(raise_exception=True):
            product_id = product_serializer.save().id
            self.create_or_update_product_address(product_id)


        return True

    #  Get product by id
    def get(self, id, entity_id):
        Entity.find_by(id=entity_id, status=StatusBase.ACTIVE)
        product = Product.find_by(id=id, entity=entity_id, status=StatusBase.ACTIVE)
        product_serializer = ProductSerializer(product)

        product_data = product_serializer.data

        product_data['addresses'] = self.get_all_product_address(entity_type = 'product', entity_id = id)

        return product_data


    #  Update product by id
    def update(self, id, entity_id):
        Entity.find_by(id=entity_id, status=StatusBase.ACTIVE)
        self.validate_address_transport_mode_and_ports();

        self.data['entity'] = entity_id

        product = Product.find_by(id=id, entity=entity_id)
        product_serializer = ProductSerializer(product, data=self.data)
        if product_serializer.is_valid(raise_exception=True):
            product_id = product_serializer.save().id
            self.create_or_update_product_address(product_id)

        return True

    #  Delete product by id
    def delete(self, id, entity_id):
        Entity.find_by(id=entity_id, status=StatusBase.ACTIVE)
        product = Product.find_by(id=id, entity=entity_id, status=StatusBase.ACTIVE)
        product.status = StatusBase.INACTIVE
        product.save()

        return True

    def create_or_update_product_address(self, product_id):
        if 'addresses' in self.data and self.data['addresses']:
            for address in self.data['addresses']:
                self.check_product_street(address)
                address['address1'] = address['street']
                address['entity_id'] = product_id
                address['entity_type'] = 'product'
                address_service = AddressService(data=address)
                if 'id' in address and address['id']:
                    address_service.update(product_id,'product',address['id'])
                else:
                    address_service.create()

    def get_all_product_address(self, entity_type, entity_id):
        address = Address.find_by(status=StatusBase.ACTIVE,
                                  entity_type=entity_type,
                                  entity_id=entity_id,
                                  multi=True)
        address_serializer = AddressSerializer(address,
                                               many=True,fields=['id','address1','pincode','city','country','state'])
        return address_serializer.data if len(
            address_serializer.data) > 0 else []

    def check_product_street(self, address):
        if ('street' not in address) or address['street'] == '' or address['street'] is None:
            raise AddressException(AddressError.STREET_IS_REQUIRED)


    def validate_address_transport_mode_and_ports(self):

        if 'addresses' not in self.data or not self.data['addresses']:
            raise ProductException(ProductError.PRODUCT_ADDRESS_REQUIRED)

        if 'Air' in self.data['transport_modes'] and not self.data['airports']:
            raise ProductException(ProductError.PRODUCT_AIRPORT_REQUIRED)

        if ('LCL' in self.data['transport_modes'] or 'FCL' in self.data['transport_modes']) and not self.data['seaports']:
            raise ProductException(ProductError.PRODUCT_SEAPORT_REQUIRED)

        if 'Air' in self.data['transport_modes'] and ('LCL' not in self.data['transport_modes'] or 'FCL' not in self.data['transport_modes']):
            self.data['seaports'] = []
            self.validate_port_by_type('airport',self.data['airports']);


        if 'Air' not in self.data['transport_modes'] and ('LCL' in self.data['transport_modes'] or 'FCL' in self.data['transport_modes']):
            self.data['airports'] = []
            self.validate_port_by_type('seaport',self.data['seaports']);

        if 'Air' in self.data['transport_modes'] and 'LCL' in self.data['transport_modes'] and 'FCL' in self.data['transport_modes']:
            self.validate_port_by_type('airport',self.data['airports']);
            self.validate_port_by_type('seaport',self.data['seaports']);


    def validate_port_by_type(self, type, port_ids):
        #id__in=id
        ports = Port.find_by(multi=True, id__in=port_ids, type=type, status=StatusBase.ACTIVE)
        if not ports:
            if type == 'seaport':
                raise PortException(PortError.INVALID_SEAPORT_ID)

            raise PortException(PortError.INVALID_AIRPORT_ID)
