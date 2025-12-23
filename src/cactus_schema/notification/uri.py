#
# GET - Returns a text/plain response with server status
# POST Not Supported
# PUT - Not Supported
# DELETE - Not Supported
#
URI_MANAGE_SERVER = "/manage"

#
# GET - Not Supported
# POST CreateEndpointRequest -> CreateEndpointResponse
# PUT - Not Supported
# DELETE - Not Supported
#
URI_MANAGE_ENDPOINT_LIST = "/manage/endpoint"

#
# GET -> CollectEndpointResponse
# POST Not Supported
# PUT ConfigureEndpointRequest -> No Body
# DELETE -> No body
#
URI_MANAGE_ENDPOINT = "/manage/endpoint/{endpoint_id}"


#
# Listens and logs any method
#
URI_ENDPOINT = "/webhook/{endpoint_id}"
