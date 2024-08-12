import functions_framework
from check_cert import check_cert_expiration
from renew_cert import renew_certificate
@functions_framework.http
def renew_if_needed(request):
    renewed = []
    for service in ['service1', 'service2']:
        if check_cert_expiration(f'{service}-chain.pem'):
            renew_certificate(service)
            renewed.append(service)
    
    if renewed:
        return f"Renewed certificates for: {', '.join(renewed)}"
    return "No certificates needed renewal"