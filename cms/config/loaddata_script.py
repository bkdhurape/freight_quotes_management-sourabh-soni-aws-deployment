from django.core.management import call_command


call_command('loaddata', 'country/fixtures/country.json')
call_command('loaddata', 'state/fixtures/state.json')
call_command('loaddata', 'city/fixtures/city.json')
call_command('loaddata', 'commodity/fixtures/commodity.json')
call_command('loaddata', 'region/fixtures/region.json')
call_command('loaddata', 'transport/fixtures/transport.json')
call_command('loaddata', 'vendor/fixtures/vendor_type.json')
call_command('loaddata', 'port/fixtures/port.json')