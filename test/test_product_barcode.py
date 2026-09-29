from pygrocy2.data_models.product import ProductBarcode
from pygrocy2.grocy_api_client import ProductBarcodeData


def test_legacy_product_barcode_payload_still_validates():
    data = ProductBarcodeData(barcode="0000000000000", amount=None)

    assert data.barcode == "0000000000000"
    assert data.amount is None
    assert data.id is None
    assert data.userfields is None


def test_full_product_barcode_payload_validates():
    data = ProductBarcodeData(
        id=508,
        product_id=305,
        barcode="4311501333778",
        qu_id=80,
        amount=1,
        shopping_location_id=2,
        last_price=0.85,
        row_created_timestamp="2024-06-13 19:06:30",
        note="Synthetic generic-object fixture",
    )
    barcode = ProductBarcode(data)

    assert data.id == 508
    assert data.product_id == 305
    assert data.qu_id == 80
    assert data.amount == 1.0
    assert data.shopping_location_id == 2
    assert data.last_price == 0.85
    assert str(data.row_created_timestamp) == "2024-06-13 19:06:30"
    assert data.note == "Synthetic generic-object fixture"
    assert barcode.id == 508
    assert barcode.product_id == 305
    assert barcode.barcode == "4311501333778"
    assert barcode.qu_id == 80
    assert barcode.amount == 1.0
    assert barcode.shopping_location_id == 2
    assert barcode.last_price == 0.85
    assert str(barcode.row_created_timestamp) == "2024-06-13 19:06:30"
    assert barcode.note == "Synthetic generic-object fixture"


def test_product_barcode_optional_fields_accept_null():
    data = ProductBarcodeData(
        id=None,
        product_id=None,
        barcode="0000000000000",
        qu_id=None,
        amount=None,
        shopping_location_id=None,
        last_price=None,
        row_created_timestamp=None,
        note=None,
        userfields=None,
    )

    assert data.model_dump(exclude={"barcode"}) == {
        "id": None,
        "product_id": None,
        "qu_id": None,
        "amount": None,
        "shopping_location_id": None,
        "last_price": None,
        "row_created_timestamp": None,
        "note": None,
        "userfields": None,
    }


def test_product_barcode_preserves_zero_numeric_values():
    barcode = ProductBarcode(
        ProductBarcodeData(
            id=0,
            product_id=0,
            barcode="0000000000000",
            qu_id=0,
            amount=0,
            shopping_location_id=0,
            last_price=0,
        )
    )

    assert barcode.id == 0
    assert barcode.product_id == 0
    assert barcode.qu_id == 0
    assert barcode.amount == 0.0
    assert barcode.shopping_location_id == 0
    assert barcode.last_price == 0.0


def test_product_barcode_preserves_opaque_userfields():
    userfields = {
        "brand": None,
        "ingredients": "opaque source value",
        "custom_future_field": {"preserve": True},
    }

    barcode = ProductBarcode(
        ProductBarcodeData(barcode="4311501333778", userfields=userfields)
    )

    assert barcode.userfields == userfields
