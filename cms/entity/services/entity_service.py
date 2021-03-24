from company.services.company_service import CompanyService
from entity.models.entity import Entity
from entity.serializers import EntitySerializer
from exceptions import EntityException, EntityError
from product.models.product import Product
from product.services.product_service import ProductService
from utils.base_models import StatusBase
from utils.responses import get_paginated_data


class EntityService:

    def __init__(self, data):
        self.data = data

    #  Get all entities
    def get_all(self, company_id):
        CompanyService.get(self, id=company_id)
        entities = Entity.find_by(multi=True, company=company_id, status=StatusBase.ACTIVE)

        entities_paginated_data = get_paginated_data(EntitySerializer, entities, self.data)

        return entities_paginated_data

    #  Create entity
    def create(self, company_id):
        CompanyService.get(self, id=company_id)
        self.data['company'] = company_id

        if self.data['is_shipper'] == False and self.data['is_consignee'] == False:
            raise EntityException(EntityError.ENTITY_TYPE_REQUIRED)

        entity_serializer = EntitySerializer(data=self.data)
        if entity_serializer.is_valid(raise_exception=True):
            entity_serializer.save()

        return True

    #  Get entity by id
    def get(self, id, company_id):
        CompanyService.get(self, id=company_id)
        entity = Entity.find_by(id=id, company=company_id, status=StatusBase.ACTIVE)
        entity_serializer = EntitySerializer(entity)

        return entity_serializer.data


    #  Update entity by id
    def update(self, id, company_id):
        CompanyService.get(self, id=company_id)
        self.data['company'] = company_id

        if self.data['is_shipper'] == False and self.data['is_consignee'] == False:
            raise EntityException(EntityError.ENTITY_TYPE_REQUIRED)

        entity = Entity.find_by(id=id, company=company_id)
        entity_serializer = EntitySerializer(entity, data=self.data)
        if entity_serializer.is_valid(raise_exception=True):
            entity_serializer.save()

        return True

    #  Delete entity by id
    def delete(self, id, company_id):
        CompanyService.get(self, id=company_id)
        self.delete_all_entity_products(id)
        entity = Entity.find_by(id=id, company=company_id, status=StatusBase.ACTIVE)
        entity.status = StatusBase.INACTIVE
        entity.save()

        return True

    def delete_all_entity_products(self, entity_id):
        product_id_list = list(Product.find_by(multi=True, entity=entity_id).values_list('id', flat=True))

        product_service = ProductService({})
        for product_id in product_id_list:
            product_service.delete(id=product_id, entity_id=entity_id)
