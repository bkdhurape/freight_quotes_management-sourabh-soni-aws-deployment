from tag.serializers import TagSerializer
from tag.models.tag import Tag
from company.models.company import Company
from exceptions.tag_exceptions import TagException, TagError
from utils.base_models import StatusBase
from customer.models.customer import Customer
from company.services.company_service import CompanyService

class TagService:
    def __init__(self, data):
        self.data = data

    def check_tag_company(self, tags):
        for company in tags:
            if self.data['company'] == company['company_id']:
                if company['status'] == 1:
                    raise TagException(TagError.TAG_EXISTS)
                return True
        return False

    def check_tag_exist(self):
        tag_object = Tag.find_by(
            multi=True, join=False, name=self.data['name'])
        if tag_object:
            tag_details = tag_object.values()
            company_id_exists = self.check_tag_company(tags=tag_details)
            if company_id_exists:
                return True
            else:
                return False
        else:
            return False

    '''Create new tag '''

    def create(self, company_id=None):
        tags_exists = self.check_tag_exist()
        if tags_exists:
            raise TagException(TagError.TAG_EXISTS)
        
        CompanyService.get(id=self.data['company'])
        tags_serializer = TagSerializer(data=self.data)

        if tags_serializer.is_valid(raise_exception=True):
            tags_id = (tags_serializer.save()).id
        return tags_id

    '''Update tags detail based on company id and tags id '''

    def update(self, company_id, tag_id):
        tags = Tag.find_by(multi=False, join=False,
                           id=tag_id, company_id=company_id)
        tags_serializer = TagSerializer(tags, data=self.data)

        if tags_serializer.is_valid(raise_exception=True):
            tags_serializer.save()
        else:
            return tags_serializer.errors

    '''Delete tag based on company id and tag id '''

    def delete(self, company_id, tag_id):

        tag = Tag.find_by(
            multi=True, join=False, status=StatusBase.ACTIVE, id=tag_id, company_id=company_id)
        
        if not tag:
            raise TagException(TagError.TAG_NOT_FOUND)
    
        customers = Customer.find_by(multi=True, tag=tag_id, status=StatusBase.ACTIVE)

        if customers.count():
            tag_obj = Tag.find_by(id=tag_id)
            for customer in customers:
                customer.tag.remove(tag_obj)  # clear() does not take any parameter and remove take arguement and parameter
            self.delete_tag(tag, tag_id, company_id)
        else:
            self.delete_tag(tag, tag_id, company_id)


    ''' get all the child of the tag '''

    def delete_tag(self, tag, tag_id, company_id):
        tag_serializer = TagSerializer(tag, many=True)
        parent_id = tag_serializer.data[0]['parent']

        if self.get_tag_childrens(tag_id, company_id, parent_id):
            tag.delete()
        else:
            tag.delete()


    def get_tag_childrens(self, id, company_id, parent_id):
        tag = Tag.find_by(multi=True, join=False,
                          parent_id=id, company_id=company_id)
        if tag.count():
            tag_serializer = TagSerializer(tag, many=True)
            for tag in tag_serializer.data:
                self.update_tag_parent(
                    tag['id'], company_id, parent_id, tag['name'])
            return True
        return False

    '''update tag with respective parent id '''

    def update_tag_parent(self, id, company_id, parent_id, name):
        tag_update_obj = {}
        tag_update_obj.update(
            {'name': name, 'company': company_id, 'parent': parent_id})
        self.data = tag_update_obj
        self.update(company_id, id)
