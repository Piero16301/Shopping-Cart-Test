import unittest

from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from . import crud, models, schemas


class TestCrud(unittest.TestCase):
    def test_create_cart_product(self):
        mock_db = MagicMock()
        mock_product = schemas.ProductCreate(title="Test Product", price=10.0, description="Test Description", category="Test Category", image="Test Image", rating="Test Rating")
        mock_db_product = models.Product(id=1, title="Test Product", price=10.0, description="Test Description", category="Test Category", image="Test Image", rating="Test Rating")
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        mock_db.add.return_value = mock_db_product
        product = crud.create_cart_product(mock_db, mock_product, 1)
        assert product.category == mock_db_product.category
        assert product.description == mock_db_product.description
        assert product.image == mock_db_product.image
        assert product.price == mock_db_product.price
        assert product.rating == mock_db_product.rating
        assert product.title == mock_db_product.title

    def test_update_product(self):
        mock_db = MagicMock()
        mock_product = models.Product(id=1, title="Test Product", price=10.0, description="Test Description", category="Test Category", image="Test Image", rating="Test Rating")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_product
        mock_db.commit.return_value = None
        updated_product = schemas.UpdateProduct(id=1, title="Updated Product", price=10.0, description="Test Description", category="Test Category", image="Test Image", rating="Test Rating")
        product = crud.update_product(1, updated_product, mock_db)
        assert product == mock_product

    def test_create_cart(self):
        mock_db = MagicMock()
        mock_cart_create = schemas.CartCreate(id=1, created_at="2021-01-01 00:00:00", updated_at="2021-01-01 00:00:00")
        mock_cart = models.Cart(id=1, created_at="2021-01-01 00:00:00", updated_at="2021-01-01 00:00:00")
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        mock_db.query.return_value.filter.return_value.first.return_value = mock_cart
        cart = crud.create_cart(mock_db, mock_cart_create)
        assert cart.id == mock_cart.id

    def test_get_products(self):
        mock_db = MagicMock()
        mock_products = [models.Product(id=1, title="Test Product 1"), models.Product(id=2, title="Test Product 2")]
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_products
        products = crud.get_products(mock_db, skip=0, limit=2)
        assert products == mock_products

    def test_get_product(self):
        mock_db = MagicMock()
        mock_product = models.Product(id=1, title="Test Product")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_product
        product = crud.get_product(mock_db, 1)
        assert product == mock_product

    def test_delete_product(self):
        mock_db = MagicMock()
        mock_product = models.Product(id=1, title="Test Product")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_product
        mock_db.commit.return_value = None
        response = crud.delete_product(1, mock_db)
        assert response.status_code == 204

    def test_get_cart(self):
        mock_db = MagicMock()
        mock_cart = models.Cart(id=1, created_at="2021-01-01 00:00:00", updated_at="2021-01-01 00:00:00")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_cart
        cart = crud.get_cart(mock_db, 1)
        assert cart == mock_cart

    def test_get_carts(self):
        mock_db = MagicMock()
        mock_carts = [models.Cart(id=1, created_at="2021-01-01 00:00:00", updated_at="2021-01-01 00:00:00"), models.Cart(id=2, created_at="2021-01-01 00:00:00", updated_at="2021-01-01 00:00:00")]
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_carts
        carts = crud.get_carts(mock_db, 0, 2)
        assert carts == mock_carts


if __name__ == "__main__":
    unittest.main()
