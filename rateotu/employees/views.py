from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rateotu.accounts.permissions import IsEmployee
from rateotu.employees.services import generate_employee_dashboard_chart_data


# Returned data can be split into several separate endpoints
# in the case if called in several different pages on the client,
# but this is not the case right now.
class EmployeeDashboardDataView(APIView):
    """
    Get data needed to populate tables and charts on the main employee dashboard page.
    """

    permission_classes = [IsAuthenticated & IsEmployee]

    def get(self, request, *args, **kwargs):
        return Response(
            data=generate_employee_dashboard_chart_data(), status=status.HTTP_200_OK
        )
