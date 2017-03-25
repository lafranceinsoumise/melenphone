from rest_framework.exceptions import APIException

class CallerCreationError(APIException):
    status_code = 400
    default_detail = "Erreur lors de la création de l'agent"
    default_code = "callhub_creation_error"


class NetworkError(APIException):
    status_code = 500
    default_detail = "Erreur lors de la connexion à l'API Callhub"
    default_code = "network_error"

class CallerValidationError(APIException):
    status_code = 400
    default_detail = "Erreur lors de la validation de l'agent Callhub"
    default_code = "callhub_validation_error"