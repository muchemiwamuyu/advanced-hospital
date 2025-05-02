from flask import Blueprint, request, jsonify
from config.database import get_db
from models.patients import PatientSchema
from bson import ObjectId  # Correct import for ObjectId

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/api/add_patient', methods=['POST'])
def add_patient():
    db = get_db()

    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        patient_data = request.get_json()
        patient = PatientSchema(**patient_data)
    except Exception as e:
        return jsonify({"error": f"Invalid data: {e}"}), 400

    # Check if a patient with the same unique data already exists
    # Assuming 'name' and 'contact' are unique identifiers (update with relevant fields)
    existing_patient = db.patients.find_one({
        "$or": [
            {"number": patient.number},
            {"contact_history": patient.contact_history}
        ]
    })

    if existing_patient:
        return jsonify({"error": "A patient with the same number or contact-history already exists."}), 409

    try:
        result = db.patients.insert_one(patient.dict())
        return jsonify({
            "message": "Patient added",
            "patient_id": str(result.inserted_id)
        }), 201
    except Exception as db_error:
        return jsonify({"error": f"Database insertion failed: {db_error}"}), 500


# getting registered patients by id
@patient_bp.route('/api/get_patient/<string:patient_id>', methods=['GET'])
def get_patient(patient_id):
    db = get_db()

    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    if not ObjectId.is_valid(patient_id):
        return jsonify({"error": "Invalid patient ID format"}), 400

    try:
        patient_data = db.patients.find_one({"_id": ObjectId(patient_id)})

        if patient_data:
            # Convert ObjectId to string
            patient_data['_id'] = str(patient_data['_id'])

            # Parse the data using Pydantic schema
            patient = PatientSchema(**patient_data)
            return jsonify(patient.model_dump()), 200
        else:
            return jsonify({"error": "Patient not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Error retrieving patient: {e}"}), 500
    
# getting all patients 
@patient_bp.route('/api/get_all_patients', methods=['GET'])
def get_all_patients():
    db = get_db()

    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        patients_cursor = db.patients.find()
        patients_list = []

        for patient_doc in patients_cursor:
            patient_doc['_id'] = str(patient_doc['_id'])  # Convert ObjectId to string
            try:
                patient = PatientSchema(**patient_doc)
                patients_list.append(patient.model_dump())
            except Exception as validation_error:
                # Skip invalid records and optionally log them
                continue

        return jsonify(patients_list), 200

    except Exception as e:
        return jsonify({"error": f"Error retrieving patients: {e}"}), 500