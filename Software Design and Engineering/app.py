from flask import Flask, request, jsonify
from flask_cors import CORS
from main import AnimalShelter
import logging
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the animal shelter
shelter = AnimalShelter()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Animal Shelter Management System',
        'version': '1.0.0'
    })

@app.route('/api/animals', methods=['POST'])
def create_animal():
    """Create a new animal record"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'age', 'animal_type', 'breed', 'outcome']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create the animal
        success = shelter.create(data)
        
        if success:
            logger.info(f"Created animal: {data['name']}")
            return jsonify({
                'message': 'Animal created successfully',
                'animal': data
            }), 201
        else:
            return jsonify({'error': 'Failed to create animal'}), 500
            
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating animal: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals', methods=['GET'])
def get_animals():
    """Get all animals or search by criteria"""
    try:
        # Get query parameters for filtering
        name = request.args.get('name')
        animal_type = request.args.get('animal_type')
        breed = request.args.get('breed')
        outcome = request.args.get('outcome')
        
        # Build query
        query = {}
        if name:
            query['name'] = {'$regex': name, '$options': 'i'}  # Case-insensitive search
        if animal_type:
            query['animal_type'] = animal_type
        if breed:
            query['breed'] = breed
        if outcome:
            query['outcome'] = outcome
        
        # If no query parameters, get all animals
        if not query:
            query = {}
        
        animals = shelter.read(query)
        
        return jsonify({
            'animals': animals,
            'count': len(animals)
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving animals: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals/<animal_id>', methods=['GET'])
def get_animal(animal_id):
    """Get a specific animal by ID"""
    try:
        animals = shelter.read({'_id': animal_id})
        
        if not animals:
            return jsonify({'error': 'Animal not found'}), 404
        
        return jsonify({
            'animal': animals[0]
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving animal {animal_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals/<animal_id>', methods=['PUT'])
def update_animal(animal_id):
    """Update an animal record"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update the animal
        updated_count = shelter.update({'_id': animal_id}, data)
        
        if updated_count > 0:
            logger.info(f"Updated animal: {animal_id}")
            return jsonify({
                'message': 'Animal updated successfully',
                'updated_count': updated_count
            }), 200
        else:
            return jsonify({'error': 'Animal not found or no changes made'}), 404
            
    except Exception as e:
        logger.error(f"Error updating animal {animal_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals/<animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    """Delete an animal record"""
    try:
        deleted_count = shelter.delete({'_id': animal_id})
        
        if deleted_count > 0:
            logger.info(f"Deleted animal: {animal_id}")
            return jsonify({
                'message': 'Animal deleted successfully',
                'deleted_count': deleted_count
            }), 200
        else:
            return jsonify({'error': 'Animal not found'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting animal {animal_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals/bulk', methods=['POST'])
def bulk_create_animals():
    """Create multiple animals at once"""
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Data must be a list of animals'}), 400
        
        created_count = 0
        errors = []
        
        for i, animal_data in enumerate(data):
            try:
                # Validate required fields
                required_fields = ['name', 'age', 'animal_type', 'breed', 'outcome']
                for field in required_fields:
                    if field not in animal_data:
                        errors.append(f'Animal {i}: Missing required field: {field}')
                        continue
                
                success = shelter.create(animal_data)
                if success:
                    created_count += 1
                else:
                    errors.append(f'Animal {i}: Failed to create')
                    
            except Exception as e:
                errors.append(f'Animal {i}: {str(e)}')
        
        return jsonify({
            'message': f'Bulk operation completed',
            'created_count': created_count,
            'total_count': len(data),
            'errors': errors
        }), 200 if created_count > 0 else 400
        
    except Exception as e:
        logger.error(f"Error in bulk create: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals/statistics', methods=['GET'])
def get_statistics():
    """Get statistics about animals"""
    try:
        # Get all animals
        all_animals = shelter.read({})
        
        if not all_animals:
            return jsonify({
                'total_animals': 0,
                'by_type': {},
                'by_outcome': {},
                'by_breed': {}
            }), 200
        
        # Calculate statistics
        total_animals = len(all_animals)
        by_type = {}
        by_outcome = {}
        by_breed = {}
        
        for animal in all_animals:
            # Count by animal type
            animal_type = animal.get('animal_type', 'Unknown')
            by_type[animal_type] = by_type.get(animal_type, 0) + 1
            
            # Count by outcome
            outcome = animal.get('outcome', 'Unknown')
            by_outcome[outcome] = by_outcome.get(outcome, 0) + 1
            
            # Count by breed
            breed = animal.get('breed', 'Unknown')
            by_breed[breed] = by_breed.get(breed, 0) + 1
        
        return jsonify({
            'total_animals': total_animals,
            'by_type': by_type,
            'by_outcome': by_outcome,
            'by_breed': by_breed
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals/search', methods=['GET'])
def search_animals():
    """Advanced search with multiple criteria"""
    try:
        # Get search parameters
        query = request.args.get('q', '')  # General search term
        min_age = request.args.get('min_age')
        max_age = request.args.get('max_age')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Build MongoDB query
        mongo_query = {}
        
        if query:
            # Search in name, breed, and animal_type
            mongo_query['$or'] = [
                {'name': {'$regex': query, '$options': 'i'}},
                {'breed': {'$regex': query, '$options': 'i'}},
                {'animal_type': {'$regex': query, '$options': 'i'}}
            ]
        
        if min_age or max_age:
            age_query = {}
            if min_age:
                age_query['$gte'] = int(min_age)
            if max_age:
                age_query['$lte'] = int(max_age)
            mongo_query['age'] = age_query
        
        # Get animals with pagination
        animals = shelter.read(mongo_query)
        
        # Apply pagination
        total_count = len(animals)
        animals = animals[offset:offset + limit]
        
        return jsonify({
            'animals': animals,
            'count': len(animals),
            'total_count': total_count,
            'offset': offset,
            'limit': limit
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching animals: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=True)


