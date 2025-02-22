from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

swagger = Swagger(app, config=swagger_config)
db = SQLAlchemy(app)

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

@app.route('/query', methods=['POST'])
@swag_from({
    'tags': ['Queries'],
    'summary': 'Create a new query',
    'description': 'Creates a new query and forwards it to Service 2',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'content': {
                        'type': 'string',
                        'description': 'The query content'
                    }
                },
                'required': ['content']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Query created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Created in both services'
                    }
                }
            }
        },
        500: {
            'description': 'Service 2 forwarding failed',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Created in Service1 but failed to forward to Service2'
                    }
                }
            }
        }
    }
})
def create_query():
    data = request.json
    new_query = Query(content=data['content'])
    db.session.add(new_query)
    db.session.commit()
    
    # Forward to Microservice 2
    try:
        requests.post('http://localhost:5001/query', json={'content': data['content']})
    except:
        return jsonify({'message': 'Created in Service1 but failed to forward to Service2'}), 500
    
    return jsonify({'message': 'Created in both services'}), 201

@app.route('/queries', methods=['GET'])
@swag_from({
    'tags': ['Queries'],
    'summary': 'Get all queries',
    'description': 'Retrieves all queries stored in the SQLite database',
    'responses': {
        200: {
            'description': 'List of all queries',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer',
                            'description': 'Query ID'
                        },
                        'content': {
                            'type': 'string',
                            'description': 'Query content'
                        }
                    }
                }
            }
        }
    }
})
def get_queries():
    queries = Query.query.all()
    return jsonify([
        {'id': query.id, 'content': query.content}
        for query in queries
    ]), 200

@app.route('/query/<int:query_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Queries'],
    'summary': 'Delete a query',
    'description': 'Deletes a query from the SQLite database and forwards deletion to Service 2',
    'parameters': [
        {
            'name': 'query_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the query to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Query deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Deleted from both services'
                    }
                }
            }
        },
        404: {
            'description': 'Query not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Query not found'
                    }
                }
            }
        },
        500: {
            'description': 'Service 2 forwarding failed',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Deleted from Service1 but failed to forward to Service2'
                    }
                }
            }
        }
    }
})
def delete_query(query_id):
    query = Query.query.get(query_id)
    if not query:
        return jsonify({'message': 'Query not found'}), 404
    
    db.session.delete(query)
    db.session.commit()
    
    # Forward deletion to Microservice 2
    try:
        requests.delete(f'http://localhost:5001/query/{query_id}')
    except:
        return jsonify({'message': 'Deleted from Service1 but failed to forward to Service2'}), 500
    
    return jsonify({'message': 'Deleted from both services'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000)