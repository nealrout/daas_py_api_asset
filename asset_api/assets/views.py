"""
File: views.py
Description: Views for the Asset API, including listing, creating, retrieving, updating, and deleting assets.
            I have specifically not used the Django Rest Framework's ModelViewSet because I am using stored procedures
            to perform all of the CRUD operations.  This gives a better learning experience, and allows more control
            in the database layer.

Author: Neal Routson
Date: 2025-02-02
Version: 0.1
"""
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination
from daas_py_config import config
from daas_py_common.logging_config import logger
import pysolr
import json

configs = config.get_configs()
SOLR_URL = f"{configs.SOLR_URL}/{configs.SOLR_COLLECTION_ASSET}"
logger.info (f'SOLR_URL: {SOLR_URL}')

# When navigating to the /api/ endpoint, we will show what API are available.
@api_view(['GET', 'POST'])
def api_root(request, format=None):
    """API root view to list available endpoints."""
    return Response({
        'asset_detail': reverse('asset-detail', request=request, format=format),
        'asset-detail-multiple': reverse('asset-detail-multiple', request=request, format=format),
        'asset_summary': reverse('asset-summary', request=request, format=format),
        'asset-upsert': reverse('asset-upsert', args=[1], request=request, format=format), 
    })

# Class for getting all assets.
class AssetListDetail(APIView):
    """
    Custom API view to list and create assets using stored procedures.
    """

    def get(self, request):
        
        """Retrieve all assets using a stored procedure"""
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {configs.DB_PROC_GET_ASSETS}();")
            columns = [col[0] for col in cursor.description]  # Get column names
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert to dictionary

        # return Response(results)
        
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_results = paginator.paginate_queryset(results, request)

        # Return the paginated response
        return paginator.get_paginated_response(paginated_results)

    def post(self, request):
        """Create a new asset using a stored procedure"""
        data = request.data
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {configs.DB_PROC_CREATE_ASSETS}(%s, %s, %s);",
                [data.get("asset_id"), data.get("sys_id"), data.get("fac_code")]
            )
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            result = dict(zip(columns, row))

        return Response(result, status=status.HTTP_201_CREATED)

# Class for getting all assets in the provided json.
class AssetListDetailMultiple(APIView):
    """
    Custom API view to retrieve multiple assets using stored procedures.
    """

    def post(self, request):
        """Retrieve multiple assets using a stored procedure with JSON list of IDs"""
        asset_ids = request.data.get("ids", [])

        if not asset_ids:
            return Response({"error": "No asset IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            json_ids = json.dumps([int(i) for i in asset_ids])
            logger.debug(f"json_ids: {json_ids}")

            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {configs.DB_PROC_GET_ASSET_ID}(%s);", [json_ids])
                rows = cursor.fetchall()

                if rows:
                    columns = [col[0] for col in cursor.description]
                    results = [dict(zip(columns, row)) for row in rows]
                    return Response(results)

            return Response({"error": "No assets found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error retrieving assets: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Class for get, update, delete on a specific asset.
class AssetUpsert(APIView):
    """
    Custom API view to retrieve, update, or delete an asset using stored procedures.
    """
    def get(self, request, pk):
        
        asset_ids = request.query_params.getlist('id', [pk])

        if not asset_ids:
            return Response({"error": "No asset IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            json_ids = json.dumps([int(i) for i in asset_ids])
            logger.debug(f"json_ids: {json_ids}")
            """Retrieve an asset using a stored procedure"""
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {configs.DB_PROC_GET_ASSET_ID}(%s);", [json_ids])
                row = cursor.fetchone()
                if row:
                    columns = [col[0] for col in cursor.description]
                    result = dict(zip(columns, row))
                    return Response(result)
                return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        
        """Update an asset using a stored procedure"""
        data = request.data
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT update_{configs.DB_PROC_UPDATE_ASSET}asset(%s, %s, %s, %s);",
                [pk, data.get("asset_id"), data.get("sys_id"), data.get("fac_code")]
            )
        return Response({"message": "Asset updated successfully"})

    def delete(self, request, pk):
        """Delete an asset using a stored procedure"""
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT {configs.DB_PROC_DELETE_ASSET}(%s);", [pk])
        return Response({"message": "Asset deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#  Class for getting all assets from SOLR.
class AssetListSummary(APIView):
    """
    API view to fetch assets from a SOLR instance.
    """

    def get(self, request):
        """Retrieve assets from SOLR."""
        solr = pysolr.Solr(SOLR_URL, always_commit=True, timeout=10)

        # Extract query parameters (if any)
        query = request.GET.get("q", "*:*")  # Default to all assets
        filters = request.GET.getlist("fq")  # Filter queries if provided

        # Construct SOLR search parameters
        solr_params = {
            "q": query,
            "fq": filters,  # Apply filters if provided
            "rows": 100  # Fetch up to 100 records (adjust as needed)
        }

        results = solr.search(**solr_params)
        assets = [doc for doc in results]

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set page size
        paginated_results = paginator.paginate_queryset(assets, request)

        return paginator.get_paginated_response(paginated_results)

    def post(self, request):
        """Add a new asset to SOLR."""
        solr = pysolr.Solr(SOLR_URL, always_commit=True, timeout=10)
        data = request.data

        print (data)

        # Validate input data
        if not all(key in data for key in ["asset_id", "sys_id", "fac_code"]):
            return Response(
                {"error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create asset document
        asset_doc = {
            "asset_id": data["asset_id"],
            "sys_id": data["sys_id"],
            "fac_code": data["fac_code"]
        }

        # Add asset to SOLR
        solr.add([asset_doc])

        return Response(asset_doc, status=status.HTTP_201_CREATED)