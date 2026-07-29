from rest_framework import viewsets

class StandardModelViewSet(viewsets.ModelViewSet):
	"""
	A base ViewSet that automatically wraps successful responses 
	in the standard format without needing to rewrite list/create/etc.
	"""
	def finalize_response(self, request, response, *args, **kwargs):
		# let DRF process the response normally
		response = super().finalize_response(request, response, *args, **kwargs)
		
		# only wrap successful responses (status < 400)
		if response.status_code < 400:
			
			# prevent double-wrapping if a custom action already used SuccessResponse
			if isinstance(response.data, dict) and 'success' in response.data:
				return response
				
			# handle empty responses (like 204 No Content on DELETE)
			if response.data is None or response.data == '':
				response.data = {
					"success": True,
					"status_code": response.status_code,
					"message": "Action completed successfully.",
					"data": None
				}
				return response

			# handle DRF Pagination automatically
			if isinstance(response.data, dict) and 'results' in response.data:
				response.data = {
					"success": True,
					"status_code": response.status_code,
					"message": "Data retrieved successfully.",
					"data": response.data['results'],
					"pagination": {
						"count": response.data.get('count'),
						"next": response.data.get('next'),
						"previous": response.data.get('previous')
					}
				}
			# standard single object or list
			else:
				# generate a nice message based on the HTTP method
				method_messages = {
					'GET': 'Data retrieved successfully.',
					'POST': 'Resource created successfully.',
					'PUT': 'Resource updated successfully.',
					'PATCH': 'Resource updated successfully.',
					'DELETE': 'Resource deleted successfully.'
				}
				message = method_messages.get(request.method, 'Success')
				
				response.data = {
					"success": True,
					"status_code": response.status_code,
					"message": message,
					"data": response.data
				}
					
		return response