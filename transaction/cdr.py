from elasticsearch import Elasticsearch
import os

client = Elasticsearch(
    "http://ov2xmp-elasticsearch...",  # Elasticsearch endpoint
    basic_auth=('elastic', os.environ["ELASTIC_PASSWORD"])
)

CDR = {
    "country_code": "BE",
    "party_id": "BEC",
    "id": "12345",
    "start_date_time": "2015-06-29T21:39:09Z",
    "end_date_time": "2015-06-29T23:37:32Z",
    "cdr_token": {
        "uid": "012345678",
        "type": "RFID",
        "contract_id": "DE8ACC12E46L89"
    },
    "auth_method": "WHITELIST",
    "cdr_location": {
        "id": "LOC1",
        "name": "Gent Zuid",
        "address": "F.Rooseveltlaan 3A",
        "city": "Gent",
        "postal_code": "9000",
        "country": "BEL",
        "coordinates": {
            "latitude": "3.729944",
            "longitude": "51.047599"
        },
        "evses_uid": "3256",
        "evse_id": "BE*BEC*E041503003",
        "connectors_id": "1",
        "connectors_standard": "IEC_62196_T2",
        "connectors_format": "SOCKET",
        "connectors_power_type": "AC_1_PHASE"
    },
    "currency": "EUR",
    "tariffs": [{
        "country_code": "BE",
        "party_id": "BEC",
        "id": "12",
        "currency": "EUR",
        "elements": [{
            "price_components": [{
                "type": "TIME",
                "price": 2.00,
                "vat": 10.0,
                "step_size": 300
            }]
        }],
        "last_updated": "2015-02-02T14:15:01Z"
    }],
    "charging_periods": [{
        "start_date_time": "2015-06-29T21:39:09Z",
        "dimensions": [{
            "type": "TIME",
            "volume": 1.973
        }],
        "tariff_id": "12"
    }],
    "total_cost": {
        "excl_vat": 4.00,
        "incl_vat": 4.40
    },
    "total_energy": 15.342,
    "total_time": 1.973,
    "total_time_cost": {
        "excl_vat": 4.00,
        "incl_vat": 4.40
    },
    "last_updated": "2015-06-29T22:01:13Z"
}


def create_cdr()
    

def save_cdr()