from rest_framework.exceptions import APIException

class CallerCreationError(APIException):
    status_code = 400
    default_detail = "Error while creating callhub agent"
    default_code = "callhub_creation_error"


class NetworkError(APIException):
    status_code = 500
    default_detail = "Error while trying to reach external API"
    default_code = "network_error"
