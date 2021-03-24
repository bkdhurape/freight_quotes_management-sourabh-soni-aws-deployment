import pint
ureg = pint.UnitRegistry()

def get_total_weight_volume(package_details, transport_mode = None):

    result = {}
    total_weight = 0 
    total_volume = 0

    total_package_weight = 0
    total_package_volume = 0
    total_package_volumetric_weight = 0

    for data in package_details:

        if data['package_detail_type'] == 'package':
            length = ureg(data['length']+data['dimension_unit']);
            width = ureg(data['width']+data['dimension_unit'])
            height = ureg(data['height']+data['dimension_unit'])

            weight = ureg(data['weight']+data['weight_unit'])

            length_cm = length.to('cm')
            width_cm = width.to('cm')
            height_cm = height.to('cm')
            weight_kg = weight.to('kg')

            total_volume +=  (length_cm.magnitude * width_cm.magnitude * height_cm.magnitude * data['quantity']) / 6000
            total_weight +=  weight_kg.magnitude * data['quantity']

        else:
            total_package_volume += float(data['total_volume'])
            total_package_weight += float(data['total_weight'])
            total_package_volumetric_weight += float(data['total_volumetric_weight'])


    if transport_mode == 'Air' or transport_mode == 'Air_courier' or transport_mode is None:

        result['total_weight'] = round((total_weight+total_package_weight),4)
        result['total_weight_unit'] = 'kg'

        result['total_volumetric_weight'] = round((total_volume+total_package_volumetric_weight),4)
        result['total_volumetric_weight_unit'] = 'kg'


    if transport_mode == 'LCL':
        result['total_weight'] = round(((total_weight+total_package_weight)/1000),4)
        result['total_weight_unit'] = 'tonnes'

        result['total_volumetric_weight'] = None
        result['total_volumetric_weight_unit'] = None


    result['total_volume'] = round(((total_volume * 0.006) + total_package_volume),4)
    result['total_volume_unit'] = 'cbm'

    return result



def get_package_total_weight_volume(data):

    total_weight = ureg(str(data['total_weight'])+data['total_weight_unit'])
    total_volume = data['total_volume']

    total_weight_kg = total_weight.to('kg')

    data['total_weight'] = round(total_weight_kg.magnitude,4)
    data['total_weight_unit'] = 'kg'

    data['total_volume'] = round((data['total_volume']),4)
    data['total_volume_unit'] = 'cbm'

    data['total_volumetric_weight'] = round((data['total_volume']/ 0.006),4)
    data['total_volumetric_weight_unit'] = 'kg'

    return data
 