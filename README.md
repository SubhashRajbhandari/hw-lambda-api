# Restaurant API for AWS Lambda

This project is a Python Flask application designed to run on AWS Lambda, providing RESTful APIs for restaurant management.

## Features

- Flask application configured for AWS Lambda deployment
- RESTful API endpoints for restaurant functions
- SQLAlchemy ORM for Aurora DB connectivity
- Environment variables for secure database credentials

## API Endpoints

- `GET /api/users`: Retrieve all registered users
- `POST /api/waiter/call`: Notify waitstaff for assistance
- `GET /api/menu`: Display restaurant menu items

## Setup

### Prerequisites

- Python 3.8 or later
- AWS CLI configured (for deployment)
- Virtual environment (recommended)

### Installation

1. Clone this repository
2. Create and activate a virtual environment (optional but recommended)
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

### Environment Variables

Set the following environment variables for database connection:

- `DB_USERNAME`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database hostname or IP
- `DB_PORT`: Database port (default: 3306)
- `DB_NAME`: Database name

### Local Development

Run the application locally with:

```
python app.py
```

### Deployment to AWS Lambda

1. Package the application
   ```
   pip install -t package -r requirements.txt
   cp -r app package/
   cp lambda_handler.py package/
   cd package
   zip -r ../deployment-package.zip .
   ```

2. Deploy to AWS Lambda using AWS CLI
   ```
   aws lambda create-function --function-name restaurant-api \
     --runtime python3.8 --handler lambda_handler.lambda_handler \
     --memory-size 256 --timeout 30 \
     --role arn:aws:iam::ACCOUNT_ID:role/lambda-role \
     --zip-file fileb://deployment-package.zip
   ```

3. Set environment variables in AWS Lambda console

## Project Structure

```
hw-api/
├── app/
│   ├── __init__.py           # Flask application initialization
│   ├── config/               # Configuration settings
│   ├── models/               # Database models
│   └── routes/               # API routes and controllers
├── lambda_handler.py         # AWS Lambda handler
├── app.py                    # Local development entry point
└── requirements.txt          # Python dependencies
```
