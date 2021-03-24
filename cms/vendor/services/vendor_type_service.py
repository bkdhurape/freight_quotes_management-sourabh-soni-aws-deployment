from exceptions import VendorTypeException, VendorTypeError
from utils.responses import get_paginated_data
from utils.base_models import StatusBase
from vendor.models.vendor_type import VendorType
from vendor.serializers import VendorTypeSerializer

class VendorTypeService:

    def __init__(self, data):
        self.data = data

    #  Get all vendor types
    def get_all(self):
        vendor_types = VendorType.find_by(multi=True, status=StatusBase.ACTIVE)
        get_vendor_type_paginated_data = get_paginated_data(VendorTypeSerializer, vendor_types, self.data)
        return get_vendor_type_paginated_data

    #  Create vendor types
    def create(self):
        vendor_type_serializer = VendorTypeSerializer(data=self.data)
        if vendor_type_serializer.is_valid(raise_exception=True):
            vendor_type_serializer.save()

        return True

    #  Get vendor type by id
    def get(id):
        vendor_type = VendorType.find_by(multi=False, id=id, status=StatusBase.ACTIVE)
        vendor_type_serializer = VendorTypeSerializer(vendor_type)

        return vendor_type_serializer.data

    def get_vendor_type_id_by_slug(self, slug):
        vendor_type=VendorType.find_by(multi=True, slug=slug)

        if not vendor_type:
            raise  VendorTypeException(VendorTypeError.INVALID_VENDOR_TYPE)

        vendor_type_id = list(vendor_type.values_list('id', flat=True))[0]
        return vendor_type_id

    #  Update vendor type by id
    def update(self, id):
        vendor_type = VendorType.find_by_ids(id=id)
        vendor_type_serializer = VendorTypeSerializer(vendor_type, data=self.data)
        if vendor_type_serializer.is_valid(raise_exception=True):
            vendor_type_serializer.save()

        return True

    #  Delete vendor type by id
    def delete(id):
        vendor_type = VendorType.find_by(id=id, status=StatusBase.ACTIVE)
        vendor_type.status = StatusBase.INACTIVE
        vendor_type.save()

        return True
