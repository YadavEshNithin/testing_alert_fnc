# import OpenSSL
# import datetime

# def check_cert_expiration(cert_path, days_threshold=7):
#     with open(cert_path, 'r') as f:
#         cert_data = f.read()
#     cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)
#     expiration_date = datetime.datetime.strptime(cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
#     days_until_expiration = (expiration_date - datetime.datetime.now()).days
#     return days_until_expiration <= days_threshold

# if __name__ == '__main__':
#     if check_cert_expiration('service1-chain.pem'):
#         print("Service1 certificate needs renewal")
#     if check_cert_expiration('service2-chain.pem'):
#         print("Service2 certificate needs renewal")


import OpenSSL
import datetime
def check_cert_expiration(cert_path, days_threshold=7):
    with open(cert_path, 'r') as f:
        cert_data = f.read()
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)
    expiration_date = datetime.datetime.strptime(cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
    days_until_expiration = (expiration_date - datetime.datetime.now()).days
    needs_renewal = days_until_expiration <= days_threshold
    return needs_renewal, days_until_expiration
if __name__ == '__main__':
    for service in ['service1', 'service2']:
        cert_path = f'{service}-chain.pem'
        needs_renewal, days_left = check_cert_expiration(cert_path)
        print(f"{service} certificate:")
        print(f"  Days until expiration: {days_left}")
        print(f"  Needs renewal: {'Yes' if needs_renewal else 'No'}")
        print()