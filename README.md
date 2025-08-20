# SecureCloudDocs

SecureCloudDocs is a modular, security-first backend service built with FastAPI for securely uploading documents to AWS S3 using presigned URLs. Designed for practicing production-like system, it features context-aware logging, JWT-based authentication, and modular design.

## Architecture Overview

- FastAPI for high-performance async routing  
- Modular routers for upload logic and future extensibility
- Presigned S3 uploads using boto3  
- JWT authentication with user context propagation  
- Structured logging with injection of request_id and username  
- Middleware for traceability and observability  
- Security first design: input validation, IAM least privilege, audit logging  

![Architecture Diagram](https://github.com/user-attachments/assets/edd21c6b-2756-4f05-acd4-0267ffbce9e5)

## Features

| Feature            | Description                                                  |
|--------------------|--------------------------------------------------------------|
| JWT Auth           | Add auth to endpoints and inject information via claims      |
| Presigned Uploads  | Securely upload documents to S3 using presigned URLs         |
| Structured Logging | Inject request_id and username for traceability              |
| Modular Design | Modular splitting up of functionality              |
| IAM Scoped Access | Enforce least‑privilege policy for upload prefix in S3              |

![Logging Screenshot](https://github.com/user-attachments/assets/f5599bc1-455c-4360-9cbd-ed0584d5c11f)

## Setup
```
# 1. Clone the repo
git clone https://github.com/<your‑username>/SecureCloudDocs.git
cd SecureCloudDocs

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_BUCKET_NAME=...
export JWT_SECRET=...

# 4. Run the app
uvicorn main:app --reload
```

## Sample Flow
### 1. User requests and receives a JWT token
Call the POST ```/auth/token``` with stored username and password

![Auth Token Screenshot](https://github.com/user-attachments/assets/b298dd19-240d-4a21-b728-a216aba4f373)
### 2. User requests pre-signed URL
Call the POST ```/presign-upload``` with all the necessary data

![Presigned URL Request Screenshot](https://github.com/user-attachments/assets/7b52e1d9-a2e5-489a-aa09-a5ef7d7a120c)
### 3. Server returns pre-signed URL
Returns a JSON response including ```URL```, ```key```, and ```expiry_timestamp```

![Presigned URL Return Screenshot](https://github.com/user-attachments/assets/da955917-0149-4900-b8a3-9ed509d2b088)
### 4. User uploads file to S3 bucket via API caller/CURL
Using ```PUT``` API method to the signed URL with correct headers/file type in the time-window

![Calling Presigned URL Screenshot](https://github.com/user-attachments/assets/8de118a7-b8e3-4143-9045-c90b86c57029)
## Validation
User can check the file has been uploaded via:
- The AWS site's S3 bucket

![AWS Site Screenshot](https://github.com/user-attachments/assets/ad08c956-1a79-4752-96be-bcdc051e0374)

- AWS CLI verification:
```
aws s3api head-object \
  --bucket <your-bucket> \
  --key uploads/
```

![AWS CLI Screenshot](https://github.com/user-attachments/assets/22ec92c8-9989-43f7-a478-79271376378b)
## Design decisions
- Presigned URL: Offload uploads directly to S3 to reduce load on this system
- ContextVAR Logging: Globally accessable variables to wire into logging
- Modular Routers: Isolate functionality to aid maintainability and reflect production-grade systems
- Security First Decision Making: Strict IAM policy for uploading/viewing files

## Future scope
- File type / size validation before presigning
- Presigned download support
- Actual DB creation via DynamoDB
