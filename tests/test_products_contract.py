# from fastapi.testclient import TestClient

# from app.main import app
# from app.core.config import settings


# client = TestClient(app)


# REQUIRED_KEYS = {
#     "_id",
#     "product_name",
#     "age_range",
#     "ingredients",
#     "nutrition",
#     "manufacturer",
#     "mfg_date",
#     "expiry_date",
#     "net_weight",
#     "allergen",
#     "warning",
#     "origin",
#     "createdAt",
#     "timeZone",
#     "createdAtLocal",
# }


# def assert_product_contract(data: dict):
#     assert REQUIRED_KEYS.issubset(set(data.keys()))

#     assert isinstance(data["_id"], int)
#     assert isinstance(data["product_name"], str)
#     assert isinstance(data["age_range"], str)
#     assert isinstance(data["ingredients"], list)
#     assert isinstance(data["nutrition"], dict)

#     nutrition = data["nutrition"]
#     assert {"energy", "protein", "fat", "sugar"}.issubset(set(nutrition.keys()))


# def test_products_v0_contract():
#     response = client.get("/api/v0/products/123")
#     assert response.status_code == 200
#     assert_product_contract(response.json())


# def test_products_v1_contract():
#     response = client.get("/api/v1/products/123")
#     assert response.status_code == 200
#     assert_product_contract(response.json())


# def test_products_alias_contract_default():
#     response = client.get("/api/products/123")
#     assert response.status_code == 200
#     assert response.headers.get("X-Products-Version") in {"v0", "v1"}
#     assert_product_contract(response.json())


# def test_products_alias_canary_switch():
#     prev_enabled = settings.products_canary_enabled
#     prev_percent = settings.products_canary_percent
#     prev_default = settings.products_default_version
#     prev_target = settings.products_canary_target_version

#     try:
#         settings.products_default_version = "v0"
#         settings.products_canary_enabled = True
#         settings.products_canary_percent = 100
#         settings.products_canary_target_version = "v1"

#         response = client.get("/api/products/123", headers={"X-Canary-Key": "always-canary"})
#         assert response.status_code == 200
#         assert response.headers.get("X-Products-Version") == "v1"
#         assert_product_contract(response.json())
#     finally:
#         settings.products_canary_enabled = prev_enabled
#         settings.products_canary_percent = prev_percent
#         settings.products_default_version = prev_default
#         settings.products_canary_target_version = prev_target
