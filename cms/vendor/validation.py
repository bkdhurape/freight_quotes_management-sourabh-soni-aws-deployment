from company.models.company import Company
from exceptions import VendorException, VendorError
from utils.base_models import StatusBase


class VendorValidation:

    def validate_companies_mode(request):
        if 'companies_mode' not in request:
            raise VendorException(VendorError.VENDOR_EXPERTISE_TRANSPORT_MODE_REQUIRED)

        mode_fields = ['AI', 'AE', 'ATC', 'FCLI', 'FCLE', 'FCLTC', 'LCLI', 'LCLE', 'LCLTC']
        for company_data in request['companies_mode']:
            Company.find_by(id=list(company_data.keys())[0], status=StatusBase.ACTIVE)
            if not list(company_data.values())[0]:
                raise VendorException(VendorError.VENDOR_EXPERTISE_TRANSPORT_MODE_REQUIRED)
            else:
                for mode_key in list(company_data.values())[0]:
                    if mode_key not in mode_fields:
                        raise VendorException(VendorError.VENDOR_EXPERTISE_TRANSPORT_MODE_IS_INVALID)
