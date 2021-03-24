from enum import Enum
from exceptions.base_exceptions import BaseException


class PackageDetailsException(BaseException):

    def getHTTPCode(self):
        return 400


class PackageDetailsError(Enum):
    PACKAGE_DETAILS_NOT_FOUND = {'code': 'F4001', 'msg': 'Package details not found'}
    PICKUP_LOCATION_NOT_FOUND_FOR_QUOTE = {'code':'F4002', 'msg':'For the selected quote this pickup location is not found'}
    DROP_LOCATION_NOT_FOUND_FOR_QUOTE = {'code':'F4003', 'msg':'For the selected quote this drop location is not found'}
    TRANSPORT_MODE_NOT_FOUND_FOR_QUOTE = {'code':'F4004', 'msg':'For the selected quote this transport mode is not found'}
    CONTAINERT_TYPE_REQUIRED_FOR_FCL = {'code': 'F4005', 'msg':'For FCL, container_type is required'}
    NO_OF_CONTAINERS_REQUIRED_FOR_FCL = {'code': 'F4006', 'msg':'For FCL, no_of_containers is required'}
    STUFFING_REQUIRED_FOR_FCL = {'code':'F4007', 'msg':'For FCL, stuffing is required'}
    DESTUFFING_REQUIRED_FOR_FCL = {'code':'F4008', 'msg':'For FCL, destuffing is required'}
    TYPE_REQUIRED = {'code':'F4009', 'msg':'type is required'}
    QUANTITY_REQUIRED = {'code':'F4010', 'msg':'quantity is required'}
    LENGTH_REQUIRED = {'code':'F4011', 'msg':'length is required'}
    WIDTH_REQUIRED = {'code':'F4012', 'msg':'width is required'}
    HEIGHT_REQUIRED = {'code':'F4013', 'msg':'height is required'}
    DIMENSION_UNIT_REQUIRED = {'code':'F4014', 'msg':'dimension_unit is required'}
    WEIGHT_REQUIRED = {'code':'F4015', 'msg':'weight is required'}
    WEIGHT_UNIT_REQUIRED = {'code':'F4016', 'msg':'weight_unit is required'}
    FOR_FCL_TYPE_OR_CONTAINER_TYPE_REQUIRED = {'code':'F4017', 'msg':'For FCL, either type or container_type is required'}
    PICKUP_AIR_PORT_INVALID = {'code':'F4018', 'msg':'Entered pickup_air_port does not belong to selected quote'}
    PICKUP_SEA_PORT_INVALID = {'code':'F4019', 'msg':'Entered pickup_sea_port does not belong to selected quote'}
    DROP_AIR_PORT_INVALID = {'code':'F4020', 'msg':'Entered drop_air_port does not belong to selected quote'}
    DROP_SEA_PORT_INVALID = {'code':'F4021', 'msg':'Entered drop_sea_port does not belong to selected quote'}
    PICKUP_AIR_PORT_REQUIRED = {'code': 'F4022', 'msg': 'pickup_air_port is required'}
    PICKUP_SEA_PORT_REQUIRED = {'code': 'F4023', 'msg': 'pickup_sea_port is required'}
    DROP_AIR_PORT_REQUIRED = {'code': 'F4024', 'msg': 'drop_air_port is required'}
    DROP_SEA_PORT_REQUIRED = {'code': 'F4025', 'msg': 'drop_sea_port is required'}
    PICKUP_LOCATION_REQUIRED = {'code': 'F4026', 'msg': 'pickup_location is required'}
    DROP_LOCATION_REQUIRED = {'code': 'F4027', 'msg': 'drop_location is required'}
    PACKAGE_REQUIRED = {'code': 'F4028', 'msg': 'Please add package to this container'}
    INVALID_PACKAGE = {'code': 'F4029', 'msg': 'Selected package(s) does not belong to this quote or transport mode'}
    CONTAINER_SUBTYPE_REQUIRED = {'code':'F4030', 'msg':'Container subtype is required'}
    FACTORY_SAME_PICUKUP_PACKAGE_REQUIRED = {'code':'F4031', 'msg':'For factory stuffing, package needs to be from same location.'}
    ONLY_DOCK_DESTUFFING_REQUIRED = {'code':'F4032', 'msg':'For multiple drop location, only dock destuffing is required.'}
    DIFFERENT_CONTAINER_REQUIRED = {'code':'F4033', 'msg':'For multiple packages with factory and dock stuffing, same container cannot be used for different stuffing.'}
    INVALID_CONTAINER = {'code':'F4034', 'msg':'You cannot add this package to invalid container.'}
    STACKABLE_REQUIRED = {'code':'F4035', 'msg':'Please select if package is stackable or not.'}
    HAZARDOUS_REQUIRED = {'code':'F4036', 'msg':'Please select if package is hazardous or not.'}
    COMMODITY_REQUIRED = {'code':'F4037', 'msg':'Commodity is required.'}
    TEMPERATURE_REQUIRED = {'code':'F4038', 'msg':'Temperature is required.'}
    TEMPERATURE_UNIT_REQUIRED = {'code':'F4039', 'msg':'Temperature unit is required.'}
    SHIPPER_DETAILS_REQUIRED = {'code':'F4040', 'msg':'Shipper details is required.'}
    CONSIGNEE_DETAILS_REQUIRED = {'code':'F4041', 'msg':'Consignee details is required.'}
    INVALID_CONTAINER_TYPE = {'code':'F4042', 'msg':'Cannot add temperature controlled packages in this type of container'}
    FOR_TEMPERATURE_DIFFERENT_CONTAINER_REQUIRED = {'code':'F4043', 'msg':'Same container cannot be used for different temperature packages.'}
    INVALID_PACKAGE_TYPE = {'code':'F4042', 'msg':'Cannot add non temperature controlled packages in this type of container'}
