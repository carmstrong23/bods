import datetime

import pytest
from dateutil.parser import parse as parse_datetime_str
from dateutil.tz import tzutc

from transit_odp.fares.extract import NeTExDocumentsExtractor
from transit_odp.fares.netex import get_documents_from_file
from transit_odp.fares.tests.conftest import FIXTURES

SAMPLE_FILES = [
    (
        "sample1.xml",
        {
            "schema_version": "1.1",
            "num_of_lines": 1,
            "num_of_fare_zones": 8,
            "num_of_fare_products": 1,
            "num_of_sales_offer_packages": 1,
            "num_of_user_profiles": 1,
            "num_of_pass_products": 0,
            "num_of_trip_products": 0,
            "valid_from": parse_datetime_str("2020-06-22T13:51:43.044Z"),
            "valid_to": parse_datetime_str("2119-06-22T13:51:43.044Z"),
            "stop_point_refs": [
                "atco:3290YYA00077",
                "atco:3290YYA00928",
                "atco:3290YYA00359",
                "atco:3290YYA03623",
                "atco:3290YYA01607",
                "atco:3290YYA01666",
                "atco:3290YYA01609",
                "atco:3290YYA01611",
                "atco:3290YYA00193",
                "atco:3290YYA00192",
                "atco:3290YYA00149",
                "atco:3290YYA00136",
                "atco:3290YYA00103",
                "atco:3290YYA00100",
                "atco:3290YYA00922",
            ],
            "fares_data_catalogue": [
                {
                    "xml_file_name": "/app/transit_odp/fares/tests/fixtures/sample1.xml",
                    "valid_from": "2020-01-01",
                    "valid_to": "2022-12-31",
                    "national_operator_code": ["HCTY"],
                    "line_id": ["16"],
                    "line_name": ["16"],
                    "atco_area": ["329"],
                    "tariff_basis": ["zoneToZone"],
                    "product_type": [],
                    "product_name": ["single Ticket - adult"],
                    "user_type": ["adult"],
                }
            ],
        },
    ),
    (
        "sample2.xml",
        {
            "schema_version": "1.1",
            "num_of_lines": 1,
            "num_of_fare_zones": 7,
            "num_of_fare_products": 1,
            "num_of_sales_offer_packages": 1,
            "num_of_user_profiles": 0,
            "num_of_pass_products": 0,
            "num_of_trip_products": 0,
            "valid_from": parse_datetime_str("2020-04-15T18:23:45.412Z"),
            "valid_to": parse_datetime_str("2119-04-15T18:23:45.412Z"),
            "stop_point_refs": [
                "naptan:2500B0271",
                "naptan:2500IMG88",
                "naptan:2500B0287",
                "naptan:2500B0295",
                "naptan:2590BTA01301",
                "naptan:2590B0311",
                "naptan:2590B0764",
                "naptan:2500B0272",
                "naptan:2500B0280",
                "naptan:2500B0288",
                "naptan:2500B0296",
                "naptan:2590B0304",
                "naptan:2590B0312",
                "naptan:250012414",
                "naptan:2500B0281",
                "naptan:2500B0289",
                "naptan:2500385",
                "naptan:2590B0305",
                "naptan:2590B0313",
                "naptan:2500B0274",
                "naptan:2500B0282",
                "naptan:2500B0290",
                "naptan:2590B0298",
                "naptan:2590B0306",
                "naptan:2590B0228",
                "naptan:2500B0275",
                "naptan:2500IMG99",
                "naptan:2500B0291",
                "naptan:2590B0300",
                "naptan:2590B0307",
                "naptan:2590B1018",
                "naptan:250010067",
                "naptan:2500B0284",
                "naptan:2500B0292",
                "naptan:2590B0301",
                "naptan:2590B0308",
                "naptan:2590B0177",
                "naptan:2500LAA16551",
                "naptan:2500B0285",
                "naptan:2500B0293",
                "naptan:2590B0302",
                "naptan:2590B0309",
                "naptan:2590B2027",
            ],
            "fares_data_catalogue": [
                {
                    "xml_file_name": "/app/transit_odp/fares/tests/fixtures/sample2.xml",
                    "valid_from": "2020-01-01",
                    "valid_to": "2022-12-31",
                    "national_operator_code": ["BLAC"],
                    "line_id": ["11"],
                    "line_name": ["11"],
                    "atco_area": ["250", "259"],
                    "tariff_basis": ["zoneToZone"],
                    "product_type": [],
                    "product_name": ["Single Ticket"],
                    "user_type": [],
                }
            ],
        },
    ),
]


EXPECTED_METADATA_ZIP = {
    "schema_version": "1.1",
    "num_of_lines": 2,
    "num_of_fare_zones": 15,
    "num_of_sales_offer_packages": 2,
    "num_of_fare_products": 2,
    "num_of_user_profiles": 1,
    "num_of_pass_products": 0,
    "num_of_trip_products": 0,
    "valid_from": datetime.datetime(2020, 4, 15, 18, 23, 45, 412000, tzinfo=tzutc()),
    "valid_to": datetime.datetime(2119, 6, 22, 13, 51, 43, 44000, tzinfo=tzutc()),
    "stop_point_refs": [
        "atco:3290YYA00077",
        "atco:3290YYA00928",
        "atco:3290YYA00359",
        "atco:3290YYA03623",
        "atco:3290YYA01607",
        "atco:3290YYA01666",
        "atco:3290YYA01609",
        "atco:3290YYA01611",
        "atco:3290YYA00193",
        "atco:3290YYA00192",
        "atco:3290YYA00149",
        "atco:3290YYA00136",
        "atco:3290YYA00103",
        "atco:3290YYA00100",
        "atco:3290YYA00922",
        "naptan:2500B0271",
        "naptan:2500IMG88",
        "naptan:2500B0287",
        "naptan:2500B0295",
        "naptan:2590BTA01301",
        "naptan:2590B0311",
        "naptan:2590B0764",
        "naptan:2500B0272",
        "naptan:2500B0280",
        "naptan:2500B0288",
        "naptan:2500B0296",
        "naptan:2590B0304",
        "naptan:2590B0312",
        "naptan:250012414",
        "naptan:2500B0281",
        "naptan:2500B0289",
        "naptan:2500385",
        "naptan:2590B0305",
        "naptan:2590B0313",
        "naptan:2500B0274",
        "naptan:2500B0282",
        "naptan:2500B0290",
        "naptan:2590B0298",
        "naptan:2590B0306",
        "naptan:2590B0228",
        "naptan:2500B0275",
        "naptan:2500IMG99",
        "naptan:2500B0291",
        "naptan:2590B0300",
        "naptan:2590B0307",
        "naptan:2590B1018",
        "naptan:250010067",
        "naptan:2500B0284",
        "naptan:2500B0292",
        "naptan:2590B0301",
        "naptan:2590B0308",
        "naptan:2590B0177",
        "naptan:2500LAA16551",
        "naptan:2500B0285",
        "naptan:2500B0293",
        "naptan:2590B0302",
        "naptan:2590B0309",
        "naptan:2590B2027",
    ],
    "fares_data_catalogue": [
        {
            "xml_file_name": "sample1.xml",
            "valid_from": "2020-01-01",
            "valid_to": "2022-12-31",
            "national_operator_code": ["HCTY"],
            "line_id": ["16"],
            "line_name": ["16"],
            "atco_area": ["329"],
            "tariff_basis": ["zoneToZone"],
            "product_type": [],
            "product_name": ["single Ticket - adult"],
            "user_type": ["adult"],
        },
        {
            "xml_file_name": "sample2.xml",
            "valid_from": "2020-01-01",
            "valid_to": "2022-12-31",
            "national_operator_code": ["BLAC"],
            "line_id": ["11"],
            "line_name": ["11"],
            "atco_area": ["250", "259"],
            "tariff_basis": ["zoneToZone"],
            "product_type": [],
            "product_name": ["Single Ticket"],
            "user_type": [],
        },
    ],
}


@pytest.mark.parametrize("filename,expected", SAMPLE_FILES)
def test_get_metadata_from_documents(filename, expected):
    source = str(FIXTURES.joinpath(filename))
    docs = get_documents_from_file(source)
    extractor = NeTExDocumentsExtractor(docs)
    actual = extractor.to_dict()
    assert expected == actual


def test_netex_extractor(netexdocuments):
    extractor = NeTExDocumentsExtractor(netexdocuments)
    assert EXPECTED_METADATA_ZIP == extractor.to_dict()
