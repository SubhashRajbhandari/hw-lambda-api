import json
import os
import logging
# from dotenv import load_dotenv
from app import create_app

# Configure logging for AWS Lambda/CloudWatch
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load environment variables from .env file if running locally
# load_dotenv()

# Initialize Flask app
app = create_app()

def lambda_handler(event, context):
    """AWS Lambda handler function"""
    logger.info("Lambda handler invoked with event: %s", json.dumps(event))
    
    # Get HTTP method and path from API Gateway event
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    
    logger.info("Processing request: %s %s", http_method, path)
    
    # Convert API Gateway format to WSGI format
    environ = {
        'REQUEST_METHOD': http_method,
        'PATH_INFO': path,
        'QUERY_STRING': (
            '&'.join(f"{k}={v}" for k, v in (event.get('queryStringParameters') or {}).items())
            if event.get('queryStringParameters') else ''
        ),
        'CONTENT_LENGTH': len(event.get('body') or ''),
        'CONTENT_TYPE': event.get('headers', {}).get('Content-Type', ''),
        'SERVER_NAME': 'lambda',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': event.get('body', ''),
        'wsgi.errors': None,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add headers
    for header, value in event.get('headers', {}).items():
        environ[f'HTTP_{header.replace("-", "_").upper()}'] = value
    
    # Response data
    response_data = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        },
        'body': '',
        'isBase64Encoded': False
    }
    
    # Process request with Flask app
    def start_response(status, response_headers, exc_info=None):
        """WSGI start_response function"""
        status_code = int(status.split(' ')[0])
        response_data['statusCode'] = status_code
        
        for key, value in response_headers:
            response_data['headers'][key] = value
    
    # Call Flask application
    try:
        logger.info("Calling Flask application")
        output = app(environ, start_response)
        
        # Get response body
        response_body = b''.join(output)
        
        if response_body:
            response_data['body'] = response_body.decode('utf-8')
        
        logger.info("Response generated with status code: %s", response_data['statusCode'])
        return response_data
    except Exception as e:
        logger.error("Error processing request: %s", str(e), exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"error": str(e)}),
            'isBase64Encoded': False
        }
