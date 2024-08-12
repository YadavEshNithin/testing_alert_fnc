import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc
class CertificateService(service_pb2_grpc.CertificateServiceServicer):
    def ExchangeCertificates(self, request, context):
        print(f"Received certificate from {request.service_name}")
        # In a real scenario, you would validate and store the received certificate
        return service_pb2.CertResponse(
            message=f"Received certificate from {request.service_name}",
            certificate="SERVICE1_CERTIFICATE_PLACEHOLDER"
        )
def serve():
    with open('service1.key', 'rb') as f:
        private_key = f.read()
    with open('service1-chain.pem', 'rb') as f:
        certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials(
        ((private_key, certificate_chain,),))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_CertificateServiceServicer_to_server(CertificateService(), server)
    server.add_secure_port('[::]:50051', server_credentials)
    server.start()
    print("Service1 started on port 50051 (SSL/TLS enabled)")
    server.wait_for_termination()
if __name__ == '__main__':
    serve()