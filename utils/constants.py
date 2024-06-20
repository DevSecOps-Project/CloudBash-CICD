class AWS:
    AWS_ACCOUNT_ID = "080994616921"
    AWS_REGION = "eu-north-1"
    ECR_REPO = "cloudbash"

class DOCKER:
    LOCAL_IMAGE_NAME = "cloudbash"

class EMAIL:
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    MAIN_RECEIVER = 'raismandavid@gmail.com'
    SENDER_EMAIL = 'devsecopsproj@gmail.com'

class K8S:
    DEPLOYMENT_FILE = '/cloudbash-deployment.yml'
    SERVICE_FILE = '/cloudbash-service.yml'
    IGRESS_FILE = '/cloudbash-indress.yml'

class JENKINS:
    PORT = '8888'
