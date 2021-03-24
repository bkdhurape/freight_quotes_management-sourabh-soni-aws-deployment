from branch.models.branch_transport_mode import BranchTransportMode
from branch.models.branch import Branch
from branch.serializers import BranchTransportModeSerializer
from exceptions import BranchTransportModeException, BranchTransportModeError
from utils.base_models import StatusBase
from utils.responses import get_paginated_data

class BranchTransportModeService:

    def __init__(self, data):
        self.data = data

    def create(self, branch_id):

        Branch.find_by(multi=False, status=StatusBase.ACTIVE, id=branch_id)
        self.data['branch'] = branch_id
        branch_transport_serializer = BranchTransportModeSerializer(
            data=self.data)

        # Calling transport mode required fields function
        self.transport_mode_required_fields()

        if branch_transport_serializer.is_valid(raise_exception=True):
            branch_transport_serializer.save()
        return True

    def get(self, branch_id, id=None, action = 'get'):

        Branch.find_by(multi=False, status=StatusBase.ACTIVE, id=branch_id)
        filter_params = {'branch_id': branch_id}
        if id is not None:
            filter_params.update({'id': id})

        branch_transport_mode_data = BranchTransportMode.find_by(
            multi=True, status=StatusBase.ACTIVE, **filter_params)
        if not branch_transport_mode_data:
            if action == 'delete':
                return False
            raise BranchTransportModeException(
                BranchTransportModeError.BRANCH_TRANSPORT_MODE_NOT_FOUND)

        branch_paginated_data = get_paginated_data(
            BranchTransportModeSerializer, branch_transport_mode_data, self.data, id)


        return branch_paginated_data

    def update(self, branch_id, id):

        Branch.find_by(multi=False, status=StatusBase.ACTIVE, id=branch_id)
        self.data['branch'] = branch_id
        branch_transport_mode = BranchTransportMode.find_by(
            multi=False, branch_id=branch_id, id=id)

        branch_transport_serialiazer = BranchTransportModeSerializer(
            branch_transport_mode, data=self.data)

        # Calling transport mode required fields function
        self.transport_mode_required_fields()

        if branch_transport_serialiazer.is_valid(raise_exception=True):
            branch_transport_serialiazer.save()

        return True

    # Delete transport details based on branch id and transport detail id
    def delete(self, branch_id, id):
        Branch.find_by(multi=False, status=StatusBase.ACTIVE, id=branch_id)
        branch_transport_mode_data = BranchTransportMode.find_by(
            multi=False, join=False, branch_id=branch_id, id=id)

        branch_transport_mode_data.delete()

    def transport_mode_required_fields(self):

        # For FCL container type should not be blank
        if self.data['transport_mode'] in ['FCLI', 'FCLE', 'FCLTC'] and ('container_type' not in self.data or not self.data['container_type']):
            raise BranchTransportModeException(
                BranchTransportModeError.BRANCH_FCL_CONTAINER_TYPE_REQUIRED)

        # For Air and LCL container type should be blank
        if self.data['transport_mode'] in ['AI', 'AE', 'ATC', 'LCLI', 'LCLE', 'LCLTC'] and (self.data['container_type']):
            raise BranchTransportModeException(
                BranchTransportModeError.BRANCH_CONTAINER_NOT_REQUIRED)

        # For Third country from_trade_lanes and to_trade_lanes are required
        if self.data['transport_mode'] in ['ATC', 'FCLTC', 'LCLTC']:
            if (('from_trade_lanes' not in self.data or 'to_trade_lanes' not in self.data) or not self.data['from_trade_lanes'] or not self.data['to_trade_lanes']):
                raise BranchTransportModeException(
                    BranchTransportModeError.BRANCH_THIRD_COUNTRY)
            else:
                self.data['trade_lanes'] = []

        # For Air, FCL and LCL trade_lanes is required
        if self.data['transport_mode'] in ['AI', 'AE', 'FCLI', 'FCLE', 'LCLI', 'LCLE']:
            if ('trade_lanes' not in self.data or not self.data['trade_lanes']):
                raise BranchTransportModeException(
                    BranchTransportModeError.BRANCH_TRADE_LANES_REQUIRED)
            else:
                self.data['from_trade_lanes'] = []
                self.data['to_trade_lanes'] = []
