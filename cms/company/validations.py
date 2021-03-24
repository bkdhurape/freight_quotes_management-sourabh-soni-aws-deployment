from exceptions import CompanyException, CompanyError

class CompanyValidation:

    # Validate industry if other is selected & other field is empty
    def validate_industry(industry, industry_other):
        if (type(industry) is list) and ('other' in industry) and (not industry_other):
            raise CompanyException(CompanyError.COMPANY_INDUSTRY_IS_REQUIRED)

        if (type(industry) is list) and (not 'other' in industry) and (industry_other):
            raise CompanyException(CompanyError.COMPANY_INDUSTRY_OTHER_MUST_BE_EMPTY)

    # Validate business activity if other is selected & other field is empty
    def validate_business_activity(business_activity, business_activity_other):
        if (type(business_activity) is list) and ('other' in business_activity) and (not business_activity_other):
            raise CompanyException(CompanyError.COMPANY_BUSINNESS_ACTIVITY_IS_REQUIRED)

        if (type(business_activity) is list) and (not 'other' in business_activity) and (business_activity_other):
            raise CompanyException(CompanyError.COMPANY_BUSINNESS_ACTIVITY_OTHER_MUST_BE_EMPTY)