import subprocess
import os

def renew_certificate(service_name):
    # Generate new CSR
    subprocess.run(['openssl', 'req', '-new', '-key', f'{service_name}.key', '-out', f'{service_name}.csr', '-subj', f'/CN={service_name}/O=CertDemo Inc/C=US'])

    # Sign the new CSR
    subprocess.run(['gcloud', 'privateca', 'certificates', 'create', f'{service_name}-cert-new',
                    '--issuer-pool=grpc-ca-pool',
                    '--csr', f'{service_name}.csr',
                    '--validity=P30D',
                    '--location=us-central1'])

    # Download the new certificate chain
    subprocess.run(['gcloud', 'privateca', 'certificates', 'describe', f'{service_name}-cert-new',
                    '--issuer-pool=grpc-ca-pool',
                    '--location=us-central1',
                    '--format=get(pemCertificateChain)',
                    '--output-file', f'{service_name}-chain-new.pem'])

    # Replace the old certificate with the new one
    os.rename(f'{service_name}-chain-new.pem', f'{service_name}-chain.pem')

    # Restart the deployment to use the new certificates
    subprocess.run(['kubectl', 'rollout', 'restart', f'deployment/{service_name}'])

if __name__ == '__main__':
    renew_certificate('service1')
    renew_certificate('service2')