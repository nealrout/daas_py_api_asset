from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class AssetListCreateTest(TestCase):
    def setUp(self):
        """Set up API client for testing."""
        self.client = APIClient()
        self.asset_list_url = reverse("asset-list")

    @patch("django.db.connection.cursor")  
    def test_get_assets(self, mock_cursor):
        """Test retrieving all assets using the stored procedure."""
        mock_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.description = [("id",), ("asset_id",), ("sys_id",), ("fac_code",)]
        mock_cursor.fetchall.return_value = [(1, "A123", "SYS1", "FAC1"), (2, "A124", "SYS2", "FAC2")]

        response = self.client.get(self.asset_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Check pagination results
        self.assertEqual(response.data["results"][0]["asset_id"], "A123")

    @patch("django.db.connection.cursor")
    def test_post_asset(self, mock_cursor):
        """Test creating an asset using the stored procedure."""
        mock_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.description = [("id",), ("asset_id",), ("sys_id",), ("fac_code",)]
        mock_cursor.fetchone.return_value = (3, "A125", "SYS3", "FAC3")

        response = self.client.post(self.asset_list_url, {
            "asset_id": "A125",
            "sys_id": "SYS3",
            "fac_code": "FAC3"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["asset_id"], "A125")

class AssetRetrieveUpdateDestroyTest(TestCase):
    def setUp(self):
        """Set up API client and test URL."""
        self.client = APIClient()
        self.asset_detail_url = reverse("asset-detail", args=[1])  # Assume asset ID = 1

    @patch("django.db.connection.cursor")
    def test_get_asset(self, mock_cursor):
        """Test retrieving a single asset."""
        mock_cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.description = [("id",), ("asset_id",), ("sys_id",), ("fac_code",)]
        mock_cursor.fetchone.return_value = (1, "A123", "SYS1", "FAC1")

        response = self.client.get(self.asset_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["asset_id"], "A123")

    @patch("django.db.connection.cursor")
    def test_update_asset(self, mock_cursor):
        """Test updating an asset using a stored procedure."""
        mock_cursor.return_value.__enter__.return_value = mock_cursor

        response = self.client.put(self.asset_detail_url, {
            "asset_id": "A126",
            "sys_id": "SYS4",
            "fac_cd": "FAC4"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Asset updated successfully")

    @patch("django.db.connection.cursor")
    def test_delete_asset(self, mock_cursor):
        """Test deleting an asset using a stored procedure."""
        mock_cursor.return_value.__enter__.return_value = mock_cursor

        response = self.client.delete(self.asset_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
