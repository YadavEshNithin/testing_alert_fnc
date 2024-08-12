import grpc
import service_pb2
import service_pb2_grpc
def run():
    with open('service1-chain.pem', 'rb') as f:
        root_certificates = f.read()
    creds = grpc.ssl_channel_credentials(root_certificates=root_certificates)
    with grpc.secure_channel('service1:50051', creds) as channel:
        stub = service_pb2_grpc.CertificateServiceStub(channel)
        response = stub.ExchangeCertificates(service_pb2.CertRequest(
            service_name="Service2",
            certificate="SERVICE2_CERTIFICATE_PLACEHOLDER"
        ))
    print("Received response:", response.message)
    print("Received certificate:", response.certificate)
if __name__ == '__main__':
    run()