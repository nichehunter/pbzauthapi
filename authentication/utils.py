from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status

import time
import uuid

#============================================================== exception handler util ====================================================================================

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        # An exception occurred during request processing
        error_code = 500  # Internal Server Error
        error_message = str(exc)  # Get the exception message
        print(f"Error {error_code}: {error_message}")
        
        # Return a JSON response with error details
        return Response(
            data={'error': error_message},
            status=error_code,
            content_type='application/json'
        )

    elif response.status_code >= 400:
        # Client or server error response
        response.data['status_code'] = response.status_code
        response.data['error'] = response.data.get('detail', 'Error')

        # Return the modified response as JSON
        return Response(
            data=response.data,
            status=response.status_code,
            content_type='application/json'
        )

    return response



def generate_unique_number():
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    unique_id = uuid.uuid4().hex[:6]  # Unique identifier
    return f"{timestamp}{unique_id}"