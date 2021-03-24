from exceptions import PortException, PortError
from port.models.port import Port
from port.serializers import PortSerializer
from utils.base_models import StatusBase
from utils.responses import get_paginated_data


class PortService:

    def __init__(self, data):
        self.data = data

    #  Get all ports
    def get_all(self):
        ports = Port.find_by(multi=True, status=StatusBase.ACTIVE)

        ports_paginated_data = get_paginated_data(PortSerializer, ports, self.data)

        return ports_paginated_data

    #  Create port
    def create(self):

        self.validate_port_code()

        port_serializer = PortSerializer(data=self.data)
        if port_serializer.is_valid(raise_exception=True):
            port_serializer.save()

        return True

    #  Get port by id
    def get(self, id):
        port = Port.find_by(multi=False, id=id, status=StatusBase.ACTIVE)
        port_serializer = PortSerializer(port)

        return port_serializer.data


    #  Update port by id
    def update(self, id):

        self.validate_port_code()

        port = Port.find_by(id=id)
        port_serializer = PortSerializer(port, data=self.data)
        if port_serializer.is_valid(raise_exception=True):
            port_serializer.save()

        return True

    #  Delete port by id
    def delete(self, id):
        port = Port.find_by(id=id, status=StatusBase.ACTIVE)
        port.status = StatusBase.INACTIVE
        port.save()

        return True


    def validate_port_code(self):
        if (self.data['type'] == 'airport') and ('iata' not in self.data or not self.data['iata']):
            raise PortException(PortError.PORT_IATA_REQUIRED)

        if (self.data['type'] == 'seaport') and ('code' not in self.data or not self.data['code']):
            raise PortException(PortError.PORT_CODE_REQUIRED)
