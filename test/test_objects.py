from pygrocy2.data_models.generic import EntityType


def test_api_client_get_objects_preserves_entity_and_filters(grocy_api_client, mocker):
    rows = [{"id": 508}]
    query_filters = ["product_id=305"]
    request = mocker.patch.object(
        grocy_api_client, "_do_get_request", return_value=rows
    )

    result = grocy_api_client.get_objects(
        EntityType.PRODUCT_BARCODES, query_filters=query_filters
    )

    assert result is rows
    request.assert_called_once_with("objects/product_barcodes", query_filters)


def test_api_client_get_object_uses_entity_url(grocy_api_client, mocker):
    row = {"id": 508}
    request = mocker.patch.object(grocy_api_client, "_do_get_request", return_value=row)

    result = grocy_api_client.get_object(EntityType.PRODUCT_BARCODES, 508)

    assert result is row
    request.assert_called_once_with("objects/product_barcodes/508")


def test_grocy_object_read_proxies_delegate(grocy, mocker):
    rows = [{"id": 508}]
    row = rows[0]
    get_objects = mocker.patch.object(
        grocy._api_client, "get_objects", return_value=rows
    )
    get_object = mocker.patch.object(grocy._api_client, "get_object", return_value=row)
    query_filters = ["product_id=305"]

    assert (
        grocy.get_objects(EntityType.PRODUCT_BARCODES, query_filters=query_filters)
        is rows
    )
    assert grocy.get_object(EntityType.PRODUCT_BARCODES, 508) is row
    get_objects.assert_called_once_with(EntityType.PRODUCT_BARCODES, query_filters)
    get_object.assert_called_once_with(EntityType.PRODUCT_BARCODES, 508)
