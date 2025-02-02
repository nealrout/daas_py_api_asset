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
# from .models import Asset
# from .serializers import AssetSerializer
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination

# When navigating to the /api/ endpoint, we will show what API are available.
@api_view(['GET'])
def api_root(request, format=None):
    """API root view to list available endpoints."""
    return Response({
        'assets': reverse('asset-list', request=request, format=format),
        'asset-detail': reverse('asset-detail', args=[1], request=request, format=format),  # Example with ID 1
    })

# Class for getting all assets.
class AssetListCreate(APIView):
    """
    Custom API view to list and create assets using stored procedures.
    """

    def get(self, request):
        """Retrieve all assets using a stored procedure"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_all_assets();")
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
                "SELECT * FROM create_asset(%s, %s, %s);",
                [data.get("asset_id"), data.get("sys_id"), data.get("fac_code")]
            )
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            result = dict(zip(columns, row))

        return Response(result, status=status.HTTP_201_CREATED)

# Class for get, update, delete on a specific asset.
class AssetRetrieveUpdateDestroy(APIView):
    """
    Custom API view to retrieve, update, or delete an asset using stored procedures.
    """

    def get(self, request, pk):
        """Retrieve an asset using a stored procedure"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_asset_by_id(%s);", [pk])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                result = dict(zip(columns, row))
                return Response(result)
            return Response({"error": "Asset not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        """Update an asset using a stored procedure"""
        data = request.data
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT update_asset(%s, %s, %s, %s);",
                [pk, data.get("asset_id"), data.get("sys_id"), data.get("fac_cd")]
            )
        return Response({"message": "Asset updated successfully"})

    def delete(self, request, pk):
        """Delete an asset using a stored procedure"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT delete_asset(%s);", [pk])
        return Response({"message": "Asset deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

