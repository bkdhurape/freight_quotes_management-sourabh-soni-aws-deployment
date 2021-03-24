from django.conf import settings
import datetime


class PackageDetailsRequestParams:

    @staticmethod
    def api_url():
        return settings.API_HOST

    # Get seed data list

    def get_seed_data_list():
        fixture_list = [
            'country/fixtures/country.json',
            'state/fixtures/state.json',
            'city/fixtures/city.json',
            'region/fixtures/region.json',
            'commodity/fixtures/commodity.json',
            'port/fixtures/port.json',
            'transport/fixtures/transport.json'
        ]
        return fixture_list

    def quote_fcl_valid_set():
        request_params = {
            "basic_details": {
                "transport_mode": ["FCL"],
                "pickup_location": [
                    {
                        "shipment_terms": "port_to_door",
                        "transport_mode": ["FCL"],
                        "street": "thane_pickup_1",
                        "country": 1,
                        "airport_ids": [1, 2],
                        "seaport_ids": [1, 2]
                    }
                ],
                "drop_location": [
                    {
                        "shipment_terms": "port_to_door",
                        "transport_mode": ["FCL"],
                        "street": "newyork_drop_1",
                        "country": 1,
                        "airport_ids": [1, 2],
                        "seaport_ids": [1, 2]
                    }
                ],
                "shipment_terms": "port_to_door",
                "expected_delivery_date": "2025-04-30",
                "is_origin_custom": True,
                "is_destination_custom": False,
                "is_personal_courier": False,
                "is_commercial_courier": True
            },
            "cargo_details": [
                {
                    "transport_mode": ["FCL"],
                    "pickup_location": {
                        "transport_mode": ["FCL"],
                        "shipment_terms": "port_to_door",
                        "street": "thane_pickup_1",
                        "country": 1,
                        "airport_ids": [1, 2],
                        "seaport_ids": [1, 2]
                    },
                    "drop_location": {
                        "transport_mode": ["FCL"],
                        "shipment_terms": "port_to_door",
                        "street": "newyork_drop_1",
                        "country": 1,
                        "airport_ids": [1, 2],
                        "seaport_ids": [1, 2]
                    },
                    "is_order_ready": False,
                    "multi_drop": True,
                    "order_ready_date": "2026-05-01",
                    "invoice_value": 11234,
                    "invoice_value_currency": "AED",
                    "handover_date": "2026-05-01",
                    "is_fcl_container": False,
                    "packages": [
                        {
                            "type": "bale",
                            "quantity": 5,
                            "length": 100.56,
                            "width": 100,
                            "height": 100,
                            "dimension_unit": "cm",
                            "weight": 100,
                            "weight_unit": "kg",
                            "is_hazardous": False,
                            "is_stackable": False,
                            "package_detail_type": "package"
                        },
                        {
                            "type": "carton",
                            "quantity": 5,
                            "length": 100,
                            "width": 100,
                            "height": 100,
                            "dimension_unit": "cm",
                            "weight": 100,
                            "weight_unit": "kg",
                            "is_hazardous": False,
                            "is_stackable": False,
                            "package_detail_type": "package"
                        }
                    ],
                    "containers": [
                        {
                            "commodity": [
                                1,
                                2
                            ],
                            "multi_drop": True,
                            "stuffing": "factory",
                            "destuffing": "dock",
                            "is_hazardous": True,
                            "is_stackable": False,
                            "weight": 350,
                            "weight_unit": "kg",
                            "container_type": "20Tank",
                            "container_subtype": "Tank",
                            "no_of_containers": 1,
                            "consignee_details": "Test Consignee",
                            "cargo_type": "container",
                            "packages": [
                                {
                                    "container_stuffing": "factory",
                                    "container_subtype": "Tank",
                                    "type": "bale",
                                    "quantity": 5,
                                    "length": 100,
                                    "width": 100,
                                    "height": 100,
                                    "dimension_unit": "cm",
                                    "weight": 350,
                                    "weight_unit": "kg",
                                    "package_detail_type": "package",
                                    "total_weight": 240,
                                    "total_weight_unit": "kg",
                                    "total_volume": 23.45,
                                    "total_volume_unit": "cbm"
                                }
                            ]
                        }
                    ]
                },
                {
                    "pickup_location": {
                        "transport_mode": ["FCL"],
                        "shipment_terms": "port_to_door",
                        "street": "thane_pickup_1",
                        "country": 1,
                        "airport_ids": [1, 2],
                        "seaport_ids": [1, 2]
                    },
                    "drop_location": {
                        "transport_mode": ["FCL"],
                        "shipment_terms": "port_to_door",
                        "street": "newyork_drop_1",
                        "country": 1,
                        "airport_ids": [1, 2],
                        "seaport_ids": [1, 2]
                    },
                    "transport_mode": ["FCL"],
                    "is_order_ready": False,
                    "order_ready_date": "2026-05-01",
                    "invoice_value": 11234,
                    "invoice_value_currency": "AED",
                    "handover_date": "2026-05-01",
                    "is_fcl_container": True,
                    "packages": [],
                    "containers": [
                        {
                            "is_fcl_container": True,
                            "stuffing": "dock",
                            "destuffing": "dock",
                            "is_hazardous": True,
                            "is_stackable": False,
                            "weight": 350,
                            "weight_unit": "kg",
                            "container_type": "20Reefer",
                            "container_subtype": "RF",
                            "no_of_containers": 1,
                            "shipper_details": "RF Shipper Details",
                            "cargo_type": "container",
                            "packages": [
                                {
                                    "pickup_location": {
                                        "transport_mode": ["FCL"],
                                        "shipment_terms": "port_to_door",
                                        "street": "thane_pickup_1",
                                        "country": 1,
                                        "airport_ids": [1, 2],
                                        "seaport_ids": [1, 2]
                                    },
                                    "container_stuffing": "dock",
                                    "stuffing": "factory",
                                    "container_subtype": "RF",
                                    "commodity": [
                                        1,
                                        2
                                    ],
                                    "type": "bale",
                                    "quantity": 5,
                                    "length": 100,
                                    "width": 100,
                                    "height": 100,
                                    "dimension_unit": "cm",
                                    "weight": 100,
                                    "weight_unit": "kg",
                                    "is_hazardous": False,
                                    "is_stackable": False,
                                    "package_detail_type": "package",
                                    "temperature": 27.45,
                                    "temperature_unit": "C"
                                },
                                {
                                    "pickup_location": {
                                        "transport_mode": ["FCL"],
                                        "shipment_terms": "port_to_door",
                                        "street": "thane_pickup_1",
                                        "country": 1,
                                        "airport_ids": [1, 2],
                                        "seaport_ids": [1, 2]
                                    },
                                    "container_stuffing": "dock",
                                    "container_subtype": "RF",
                                    "stuffing": "factory",
                                    "commodity": [
                                        1,
                                        2
                                    ],
                                    "type": "bale",
                                    "quantity": 5,
                                    "length": 100,
                                    "width": 100,
                                    "height": 100,
                                    "dimension_unit": "cm",
                                    "weight": 100,
                                    "weight_unit": "kg",
                                    "is_hazardous": False,
                                    "is_stackable": False,
                                    "package_detail_type": "package",
                                    "temperature": 27.45,
                                    "temperature_unit": "C"
                                }
                            ]
                        }
                    ]
                }
            ],
            "additional_details": {

                "po_number": "",
                "no_of_suppliers": 2,
                "quote_deadline": "2021-05-31",
                "switch_awb": True,
                "switch_b_l": False,
                "packaging": False,
                "palletization": False,
                "preference": [
                    1,
                    2
                ]
            }
        }
        return request_params

    def quote_fcl_valid_set_wo_transport_mode():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        del request_params['basic_details']['transport_mode']
        return request_params

    def quote_fcl_valid_set_blank_transport_mode():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['basic_details']['transport_mode'] = []
        return request_params

    def quote_fcl_valid_set_invalid_transport_mode():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['basic_details']['transport_mode'] = ["FCL1"]
        return request_params

    def quote_fcl_valid_set_wo_pickup_location():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        del request_params['basic_details']['pickup_location']
        return request_params

    def quote_fcl_valid_set_wo_pickup_location_street():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        del request_params['basic_details']['pickup_location'][0]['street']
        return request_params

    def quote_fcl_valid_set_wo_pickup_location_country():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        del request_params['basic_details']['pickup_location'][0]['country']
        return request_params

    def quote_fcl_valid_set_null_pickup_location_country():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['basic_details']['pickup_location'][0]['country'] = None
        return request_params

    def quote_fcl_valid_set_invalid_pickup_location_country():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['basic_details']['pickup_location'][0]['country'] = 100
        return request_params

    def quote_fcl_valid_set_without_seaports():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        del request_params['basic_details']['pickup_location'][0]['seaport_ids']
        return request_params

    def quote_fcl_valid_set_null_seaports():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['basic_details']['pickup_location'][0]['seaport_ids'] = None
        return request_params

    def quote_fcl_valid_set_invalid_seaports():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['basic_details']['pickup_location'][0]['seaport_ids'] = [999999]
        return request_params

    def quote_fcl_valid_set_wo_shipment_terms():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        del request_params['basic_details']['shipment_terms']
        return request_params

    def quote_fcl_valid_set_blank_shipment_terms():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['basic_details']['shipment_terms'] = ""
        return request_params

    def quote_fcl_valid_set_null_shipment_terms():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['basic_details']['shipment_terms'] = None
        return request_params

    def quote_fcl_valid_set_wo_expected_delivery_date():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        del request_params['basic_details']['expected_delivery_date']
        return request_params

    def quote_fcl_valid_set_blank_expected_delivery_date():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['basic_details']['expected_delivery_date'] = ""
        return request_params

    def quote_fcl_valid_set_dock_stuffing_destuffing():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["stuffing"] = "dock"
        request_params['cargo_details'][0]['containers'][0]["packages"] = []
        return request_params

    def quote_fcl_valid_set_container_stuffing_dock_wo_commodity():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["stuffing"] = "dock"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["container_stuffing"] = "dock"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["is_hazardous"] = True
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["is_stackable"] = True
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["commodity"] = []
        del request_params['cargo_details'][0]['containers'][0]["packages"][0]["commodity"]
        return request_params

    def quote_fcl_valid_set_container_stuffing_dock_wo_hazardous():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["stuffing"] = "dock"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["container_stuffing"] = "dock"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["is_hazardous"] = True
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["is_stackable"] = True
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["commodity"] = [1, 2]
        del request_params['cargo_details'][0]['containers'][0]["packages"][0]["is_hazardous"]
        return request_params

    def quote_fcl_valid_set_container_stuffing_dock_wo_stackable():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["stuffing"] = "dock"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["container_stuffing"] = "dock"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["is_hazardous"] = True
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["is_stackable"] = True
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["commodity"] = [1, 2]
        del request_params['cargo_details'][0]['containers'][0]["packages"][0]["is_stackable"]
        return request_params

    def quote_fcl_valid_set_container_stuffing_factory_wo_commodity():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["stuffing"] = "factory"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["container_stuffing"] = "factory"
        del request_params['cargo_details'][0]['containers'][0]["commodity"]
        return request_params

    def quote_fcl_valid_set_container_stuffing_factory_wo_hazardous():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["stuffing"] = "factory"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["container_stuffing"] = "factory"
        del request_params['cargo_details'][0]['containers'][0]["is_hazardous"]
        return request_params

    def quote_fcl_valid_set_container_stuffing_factory_wo_stackable():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["stuffing"] = "factory"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["container_stuffing"] = "factory"
        del request_params['cargo_details'][0]['containers'][0]["is_stackable"]
        return request_params

    def quote_fcl_valid_set_container_type_fr_wo_dimen():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["container_subtype"] = "FR"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["container_subtype"] = "FR"
        request_params['cargo_details'][0]['containers'][0]["packages"][0]["package_detail_type"] = "total"
        return request_params

    def quote_fcl_valid_set_container_type_rf_wo_shipper_details():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["container_subtype"] = "RF"
        request_params['cargo_details'][0]['containers'][0]["temperature"] = 23.56
        request_params['cargo_details'][0]['containers'][0]["temperature_unit"] = "C"
        return request_params

    def quote_fcl_valid_set_container_type_rf_wo_temp():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["container_subtype"] = "RF"
        request_params['cargo_details'][0]['containers'][0]["temperature_unit"] = "C"
        request_params['cargo_details'][0]['containers'][0]["shipper_details"] = "Test"
        return request_params

    def quote_fcl_valid_set_container_type_rf_wo_temp_unit():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["container_subtype"] = "RF"
        request_params['cargo_details'][0]['containers'][0]["temperature"] = 23.56
        request_params['cargo_details'][0]['containers'][0]["shipper_details"] = "Test"
        return request_params

    def quote_fcl_valid_set_container_type_ot_wo_package():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["container_subtype"] = "OT"
        request_params['cargo_details'][0]['containers'][0]["packages"] = []
        return request_params

    def quote_fcl_valid_set_multi_drop_dock_destuffing():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["multi_drop"] = True
        request_params['cargo_details'][0]['containers'][0]["destuffing"] = "factory"
        return request_params

    def quote_fcl_valid_set_container_type_tank_wo_consignee():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][0]['containers'][0]["container_subtype"] = "Tank"
        del request_params['cargo_details'][0]['containers'][0]["consignee_details"]
        return request_params

    def quote_fcl_valid_set_container_type_factory_diff_loc():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][1]['containers'][0]["container_subtype"] = "GP"
        request_params['cargo_details'][1]['containers'][0]["packages"][0]["container_stuffing"] = "factory"
        request_params['cargo_details'][1]['containers'][0]["packages"][0]["stuffing"] = "factory"

        request_params['cargo_details'][1]['containers'][0]["packages"][1]["container_stuffing"] = "factory"
        request_params['cargo_details'][1]['containers'][0]["packages"][1]["stuffing"] = "factory"
        request_params['cargo_details'][1]['containers'][0]["packages"][1]["pickup_location"]["street"] = \
            "thane_pickup_2"

        return request_params

    def quote_fcl_valid_set_non_rf_with_temp_cont_package():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][1]['containers'][0]["container_subtype"] = "GP"
        request_params['cargo_details'][1]['containers'][0]["packages"][0]["container_stuffing"] = "factory"
        request_params['cargo_details'][1]['containers'][0]["packages"][0]["stuffing"] = "factory"

        request_params['cargo_details'][1]['containers'][0]["packages"][1]["container_stuffing"] = "factory"
        request_params['cargo_details'][1]['containers'][0]["packages"][1]["stuffing"] = "factory"

        return request_params

    def quote_fcl_valid_set_same_loc_diff_temp():
        request_params = PackageDetailsRequestParams.quote_fcl_valid_set()
        request_params['cargo_details'][1]['containers'][0]["container_subtype"] = "RF"
        request_params['cargo_details'][1]['containers'][0]["packages"][0]["container_stuffing"] = "factory"
        request_params['cargo_details'][1]['containers'][0]["packages"][0]["stuffing"] = "factory"
        request_params['cargo_details'][1]['containers'][0]["packages"][0]["temperature"] = 34.45

        request_params['cargo_details'][1]['containers'][0]["packages"][1]["container_stuffing"] = "factory"
        request_params['cargo_details'][1]['containers'][0]["packages"][1]["stuffing"] = "factory"
        request_params['cargo_details'][1]['containers'][0]["packages"][0]["temperature"] = 31.45

        return request_params

    def quote_valid_set():
        request_params = {
            "basic_details": {
                "transport_mode": ["Air", "FCL"],
                "shipment_terms": "door_to_door",
                "pickup_location": [{
                    "street": "Bhandup",
                    "country": 1
                }],
                "pickup_sea_port": [],
                "pickup_air_port": [],
                "drop_location": [{
                    "street": "kurla",
                    "country": 1
                }],
                "drop_sea_port": [],
                "drop_air_port": [],
                "expected_delivery_date": str(datetime.date.today()),
                "is_personal_courier": True,
                "is_commercial_courier": False,
                "is_origin_custom": False,
                "is_destination_custom": False
            }
        }
        return request_params

    def quote_valid_set_with_single_pickup_and_multi_drop():
        request_params = {
            "basic_details": {
                "transport_mode": [
                    "FCL"
                ],
                "shipment_terms": "door_to_door",
                "pickup_location": [
                    {
                        "street": "andheri_pickup_1",
                        "country": 1
                    }
                ],
                "pickup_air_port": [1, 2],
                "pickup_sea_port": [1, 2],
                "drop_location": [
                    {
                        "street": "pune_drop_1",
                        "country": 1
                    },
                    {
                        "street": "pune_drop_2",
                        "country": 1
                    }
                ],
                "drop_air_port": [1],
                "drop_sea_port": [1],
                "expected_delivery_date": "2025-04-30",
                "is_origin_custom": True,
                "is_destination_custom": False,
                "is_personal_courier": False,
                "is_commercial_courier": False
            }
        }

        return request_params

    def quote_valid_set_for_port_to_port():
        request_params = {
            "basic_details": {
                "transport_mode": ["LCL"],
                "shipment_terms": "port_to_port",
                "pickup_location": [],
                "pickup_sea_port": [1, 2],
                "pickup_air_port": [],
                "drop_location": [],
                "drop_sea_port": [1, 2],
                "drop_air_port": [],
                "expected_delivery_date": str(datetime.date.today()),
                "expected_arrival_date": str(datetime.date.today()),
                "is_personal_courier": True,
                "is_commercial_courier": False,
                "is_origin_custom": False,
                "is_destination_custom": False
            }
        }
        return request_params

    def cargo_details_get_request_keys():
        transport_mode_keys = [
            'id',
            'transport_mode',
            'total_weight_unit',
            'total_weight',
            'total_volume_unit',
            'total_volume',
            'total_volumetric_weight_unit',
            'total_volumetric_weight',
            'quote'
        ]

        order_ready_keys = [
            'id',
            'total_weight_unit',
            'total_weight',
            'total_volume_unit',
            'total_volume',
            'total_volumetric_weight_unit',
            'total_volumetric_weight',
            'is_order_ready',
            'order_ready_date',
            'invoice_value',
            'invoice_value_currency',
            'quote',
            'transport_mode',
            'address'
        ]

        return transport_mode_keys, order_ready_keys

    def package_details_valid_set_air():
        request_params = {

            "pickup_location": 2,
            "transport_mode": [
                1
            ],
            "commodity": [
                1,
                2
            ],
            "product": "Textile",
            "drop_location": 3,
            "type": "bale",
            "quantity": 2,
            "length": 100,
            "width": 100,
            "height": 100,
            "dimension_unit": "cm",
            "weight": 100,
            "weight_unit": "lbs",
            "is_hazardous": False,
            "is_stackable": False,
            "container_type": "20GP",
            "container_subtype": "GP",
            "no_of_containers": 2,
            "stuffing": "factory",
            "destuffing": "factory",
            "package_detail_type": "package",
            "cargo_type": "loose_cargo"

        }
        return request_params

    def package_details_valid_set_air_with_total_weight_volume():
        request_params = {
            "pickup_location": 2,
            "transport_mode": [
                1
            ],
            "commodity": [
                1,
                2
            ],
            "drop_location": 3,
            "is_hazardous": False,
            "is_stackable": False,
            "package_detail_type": "total",
            "total_weight": 10000,
            "total_weight_unit": "kg",
            "total_volume": 10,
            "total_volume_unit": "cbm"
        }
        return request_params

    def cargo_details_set():
        request_params = {
            "pickup_location": 2,
            "transport_mode": [
                1
            ],
            "commodity": [
                1,
                2
            ],
            "drop_location": 3,
            "is_hazardous": False,
            "is_stackable": False,
            "package_detail_type": "total",
            "total_weight": 10000,
            "total_weight_unit": "kg",
            "total_volume": 10,
            "total_volume_unit": "cbm",
            "is_order_ready": False,
            "order_ready_date": "2030-05-06",
            "invoice_value": 1771,
            "invoice_value_currency": "HKD",
            "expected_delivery_date": "2030-05-06",
        }
        return request_params

    def cargo_details_set_with_invalid_order_ready_date():
        request_params = PackageDetailsRequestParams.cargo_details_set()
        request_params['order_ready_date'] = "2020-05-01"
        return request_params

    def cargo_details_set_with_invalid_format_order_ready_date():
        request_params = PackageDetailsRequestParams.cargo_details_set()
        request_params['order_ready_date'] = "01/05/2020"
        return request_params

    def cargo_details_set_with_order_ready_date_required():
        request_params = PackageDetailsRequestParams.cargo_details_set()
        request_params['order_ready_date'] = None
        return request_params

    def cargo_details_set_with_invoice_value_required():
        request_params = PackageDetailsRequestParams.cargo_details_set()
        request_params['invoice_value'] = None
        return request_params

    def cargo_details_set_with_invoice_value_currency_required():
        request_params = PackageDetailsRequestParams.cargo_details_set()
        request_params['invoice_value_currency'] = None
        return request_params

    def cargo_details_set_with_total_weight_volume_and_empty_total_weight():
        request_params = PackageDetailsRequestParams.cargo_details_set()
        request_params['total_weight'] = None
        return request_params

    def cargo_details_set_with_total_weight_volume_and_empty_total_weight_unit():
        request_params = PackageDetailsRequestParams.cargo_details_set()
        request_params['total_weight_unit'] = None
        return request_params

    def cargo_details_set_with_total_weight_volume_and_empty_total_volume():
        request_params = PackageDetailsRequestParams.cargo_details_set()
        request_params['total_volume'] = None
        return request_params

    def cargo_details_set_with_total_weight_volume_and_empty_total_volume_unit():
        request_params = PackageDetailsRequestParams.cargo_details_set()
        request_params['total_volume_unit'] = None
        return request_params

    def package_details_invalid_set_port_to_port():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params["pickup_location"] = 2
        request_params['transport_mode'] = [2]
        request_params['pickup_sea_port'] = [3]
        request_params['drop_sea_port'] = [1, 2]
        request_params['is_fcl_container'] = False
        return request_params

    def package_details_valid_set_fcl():
        request_params = {
            "pickup_location": 2,
            "transport_mode": [
                2
            ],
            "commodity": [
                1,
                2
            ],
            "product": "Textile",
            "drop_location": 3,
            "is_hazardous": False,
            "is_stackable": False,
            "container_type": "20GP",
            "container_subtype": "GP",
            "no_of_containers": 2,
            "stuffing": "factory",
            "destuffing": "factory",
            "package_detail_type": "package",
            "is_fcl_container": False,
            "cargo_type": "container"

        }
        return request_params

    def package_details_valid_set_fcl_container_set():
        request_params = {
            "pickup_location": 2,
            "transport_mode": [
                2
            ],
            "commodity": [
                1,
                2
            ],
            "product": "Textile",
            "drop_location": 3,
            "type": "bale",
            "quantity": 2,
            "length": 100,
            "width": 100,
            "height": 100,
            "dimension_unit": "cm",
            "weight": 100,
            "weight_unit": "lbs",
            "is_hazardous": False,
            "is_stackable": False,
            "stuffing": "factory",
            "destuffing": "factory",
            "package_detail_type": "package",
            "container_type": None

        }
        return request_params

    def package_details_valid_set_fcl_container_loose_cargo_set():
        request_params = {
            "pickup_location": 10,
            "transport_mode": [
                5
            ],
            "commodity": [
                1,
                2
            ],
            "product": None,
            "drop_location": None,
            "type": None,
            "quantity": None,
            "length": None,
            "width": None,
            "height": None,
            "dimension_unit": None,
            "weight": None,
            "weight_unit": None,
            "is_hazardous": False,
            "is_stackable": False,
            "stuffing": "factory",
            "destuffing": "factory",
            "package_detail_type": "package",
            "container_type": None,
            "loose_cargo": {
                "packages": [
                    {
                        "drop_location": 11,
                        "commodity": [
                            1,
                            2
                        ],
                        "is_hazardous": True,
                        "is_stackable": False,
                        "package_detail_type": "package",
                        "type": "carton",
                        "quantity": 2,
                        "length": 100,
                        "width": 300,
                        "height": 400,
                        "dimension_unit": "cm",
                        "weight": 610,
                        "weight_unit": "kg",
                        "is_fcl_container": False,
                        "cargo_type": "loose_cargo",
                        "stuffing": "factory"
                    }
                ]
            },
            "is_fcl_container": False,
            "cargo_type": "loose_cargo"

        }
        return request_params

    def package_details_valid_set_fcl_container_loose_cargo_set2():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_loose_cargo_set()
        request_params['transport_mode'] = [4]
        request_params['pickup_location'] = 7
        request_params['loose_cargo']['packages'][0]['drop_location'] = 8

        return request_params

    def package_details_valid_set_fcl_container_loose_cargo_set3():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_loose_cargo_set()
        request_params['transport_mode'] = [4]
        request_params['pickup_location'] = 7
        request_params['loose_cargo']['packages'][0]['drop_location'] = 9

        return request_params

    def package_details_fcl_container_tab_set():
        request_params = {
            "transport_mode": [3],
            "container_type": "20GP",
            "container_subtype": "GP",
            "no_of_containers": 1,
            "destuffing": "dock",
            "is_order_ready": False,
            "order_ready_date": "2026-05-01",
            "invoice_value": 11234,
            "invoice_value_currency": "AED",
            "handover_date": "2026-05-01",
            "packages": [339, 340],
            "is_fcl_container": True,
            "cargo_type": "container"
        }
        return request_params

    def container_single_package():
        request_params = {
            "commodity": [
                1,
                2
            ],
            "is_stackable": False,
            "is_hazardous": False,
            "package_detail_type": "package",
            "type": "carton",
            "quantity": 2,
            "length": 100,
            "width": 300,
            "height": 400,
            "dimension_unit": "cm",
            "weight": 610,
            "weight_unit": "kg",
            "cargo_type": "container",
            "is_fcl_container": False
        }
        return request_params

    def container_packages(package1, package2):
        request_params = [package1, package2]
        return request_params

    def package_details_valid_set_fcl_container_set_with_loose_cargo():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_set()
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'loose_cargo'
        return request_params

    def package_details_fcl_with_dock_stuffing_set():
        request_params = PackageDetailsRequestParams.package_details_fcl_container_tab_set()
        request_params['transport_mode'] = [5]
        request_params['stuffing'] = "factory"
        request_params['is_fcl_container'] = True
        request_params['cargo_type'] = 'container'
        return request_params

    def package_details_fcl_with_factory_destuffing_set():
        request_params = PackageDetailsRequestParams.package_details_fcl_container_tab_set()
        request_params['transport_mode'] = [4]
        request_params['destuffing'] = "factory"
        request_params['is_fcl_container'] = True
        request_params['cargo_type'] = 'container'
        return request_params

    def package_details_fcl_with_dock_stuffing_and_without_packages_set():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_set()
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        request_params['packages'] = []
        return request_params

    def package_details_create_fcl_with_dock_stuffing_package_stackable_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_set()
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'

        package1 = PackageDetailsRequestParams.container_single_package()
        package2 = PackageDetailsRequestParams.container_single_package()
        del package1['is_stackable']

        packages = PackageDetailsRequestParams.container_packages(package1, package2)
        request_params['packages'] = packages
        return request_params

    def package_details_create_fcl_with_dock_stuffing_package_hazardous_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_set()
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'

        package1 = PackageDetailsRequestParams.container_single_package()
        package2 = PackageDetailsRequestParams.container_single_package()
        del package1['is_hazardous']

        packages = PackageDetailsRequestParams.container_packages(package1, package2)
        request_params['packages'] = packages
        return request_params

    def package_details_create_fcl_with_dock_stuffing_package_commodity_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_set()
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'

        package1 = PackageDetailsRequestParams.container_single_package()
        package2 = PackageDetailsRequestParams.container_single_package()
        del package1['commodity']

        packages = PackageDetailsRequestParams.container_packages(package1, package2)
        request_params['packages'] = packages
        return request_params

    def package_details_create_fcl_with_factory_stuffing_container_stackable_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_set()
        request_params['stuffing'] = "factory"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        del request_params['is_stackable']

        return request_params

    def package_details_create_fcl_with_factory_stuffing_container_hazardous_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_set()
        request_params['stuffing'] = "factory"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        del request_params['is_hazardous']

        return request_params

    def package_details_create_fcl_with_factory_stuffing_container_commodity_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl_container_set()
        request_params['stuffing'] = "factory"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        del request_params['commodity']

        return request_params

    def package_details_create_fcl_flactrack_container_with_package_details_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl()
        request_params['container_type'] = "20Flat-Rack"
        request_params['container_subtype'] = "FR"
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        request_params['packages'] = []

        return request_params

    def package_details_create_fcl_flactrack_container_only_package_details_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl()
        request_params['container_type'] = "20Flat-Rack"
        request_params['container_subtype'] = "FR"
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'

        package1 = PackageDetailsRequestParams.container_single_package()
        package2 = PackageDetailsRequestParams.container_single_package()
        package1['package_detail_type'] = 'total'
        package1['total_weight'] = 200
        package1['total_weight_unit'] = "kg"
        package1['total_volume'] = 23.56
        package1['total_volume_unit'] = "cbm"

        packages = PackageDetailsRequestParams.container_packages(package1, package2)
        request_params['packages'] = packages

        return request_params

    def package_details_create_fcl_reefer_container_with_temperature_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl()
        request_params['container_type'] = "20Reefer"
        request_params['container_subtype'] = "RF"
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        request_params['packages'] = []

        return request_params

    def package_details_create_fcl_reefer_container_with_temperature_unit_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl()
        request_params['container_type'] = "20Reefer"
        request_params['container_subtype'] = "RF"
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        request_params['temperature'] = 37.89
        request_params['packages'] = []

        return request_params

    def package_details_create_fcl_reefer_container_with_invalid_temperature_unit():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl()
        request_params['container_type'] = "20Reefer"
        request_params['container_subtype'] = "RF"
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        request_params['temperature'] = 37.89
        request_params['temperature_unit'] = "DD"
        request_params['shipper_details'] = "Shipper 1"
        request_params['packages'] = []

        return request_params

    def package_details_create_fcl_reefer_container_with_shipper_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl()
        request_params['container_type'] = "20Reefer"
        request_params['container_subtype'] = "RF"
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        request_params['temperature'] = 37.89
        request_params['temperature_unit'] = "C"
        request_params['packages'] = []

        return request_params

    def package_details_create_fcl_container_multi_drop_with_package_details_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl()
        request_params['transport_mode'] = [3]
        request_params['pickup_location'] = 4
        request_params['drop_location'] = 5
        request_params['stuffing'] = "factory"
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        request_params['packages'] = []

        return request_params

    def package_details_fcl_with_dock_stuffing_and_invalid_packages_id_set():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl()
        request_params['stuffing'] = "dock"
        request_params['is_fcl_container'] = True
        request_params['packages'] = [999999999]
        return request_params

    def package_details_fcl_type_and_container_type_set():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['transport_mode'] = [2]
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        return request_params

    def package_details_invalid_pickup_location():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['pickup_location'] = 10
        return request_params

    def package_details_invalid_drop_location():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['drop_location'] = 10
        return request_params

    def package_details_invalid_transport_mode():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['transport_mode'] = [200]
        return request_params

    def package_details_fcl_no_of_containers_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['transport_mode'] = [2]
        request_params['is_fcl_container'] = False
        request_params['no_of_containers'] = None
        request_params['cargo_type'] = 'container'
        return request_params

    def package_details_fcl_stuffing_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['transport_mode'] = [2]
        request_params['stuffing'] = None
        request_params['cargo_type'] = 'container'
        request_params['is_fcl_container'] = False
        return request_params

    def package_details_fcl_destuffing_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_fcl()
        request_params['transport_mode'] = [2]
        request_params['destuffing'] = None
        request_params['is_fcl_container'] = False
        return request_params

    def package_details_air_type_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['type'] = None
        return request_params

    def package_details_air_length_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['length'] = None
        return request_params

    def package_details_air_width_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['width'] = None
        return request_params

    def package_details_air_height_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['height'] = None
        return request_params

    def package_details_air_dimension_unit_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['dimension_unit'] = None
        return request_params

    def package_details_air_weight_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['weight'] = None
        return request_params

    def package_details_air_weight_unit_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['weight_unit'] = None
        return request_params

    def package_details_check_for_negative_value():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['quantity'] = -2
        return request_params

    def package_details_check_for_fcl_type_or_container_type_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['transport_mode'] = [2]
        request_params['type'] = None
        request_params['container_type'] = None
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        return request_params

    def package_details_check_fcl_container_subtype_required():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['transport_mode'] = [2]
        request_params['container_subtype'] = ""
        request_params['is_fcl_container'] = False
        request_params['cargo_type'] = 'container'
        return request_params

    def package_details_temperature_validation_for_air():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['temperature'] = None
        return request_params

    def package_details_temperature_unit_validation_for_air():
        request_params = PackageDetailsRequestParams.package_details_valid_set_air()
        request_params['temperature_unit'] = None
        return request_params

    def package_details_get_all_keys():
        package_details_keys = [
            'id',
            'status',
            'product',
            'type',
            'quantity',
            'length',
            'width',
            'height',
            'dimension_unit',
            'weight',
            'weight_unit',
            'is_hazardous',
            'is_stackable',
            'container_type',
            'no_of_containers',
            'stuffing',
            'destuffing',
            'quote',
            'pickup_location',
            'drop_location',
            'pickup_air_port',
            'pickup_sea_port',
            'drop_air_port',
            'drop_sea_port',
            'transport_mode',
            'commodity',
            'temperature',
            'temperature_unit'
        ]

        return package_details_keys
