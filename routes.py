from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from PIL import Image
import io
import tempfile
from tryon import start_tryon

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Invalid data'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Invalid data'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(username=user.username), 200



@auth.route('/vton', methods=['POST'])
@jwt_required()
def vton():
    print(request.files)
    if 'image' not in request.files:
        return jsonify({'message': f'No image file provided: {request.files}'}), 400
    
    if 'dress' not in request.files:
        return jsonify({'message': f'No image file provided: {request.files}'}), 400
    
    img = request.files['image']
    garm_img = request.files['dress']
    data = request.form
    category = data.get('category', '')
    garment_des = data.get('description', '')

    try:
        img = Image.open(io.BytesIO(img.read()))
        garm_img = Image.open(io.BytesIO(garm_img.read()))
    except Exception as e:
        return jsonify({'message': f'Error processing images: {str(e)}'}), 400

    img = {
        'background':img
    }

    # check category in ["upper_body", "lower_body", "dresses"]
    if category not in ["upper_body", "lower_body", "dresses"]:
        return jsonify({'message': 'Invalid category'}), 400

    is_checked_crop = True
    is_checked = True
    denoise_steps = 30
    is_randomize_seed = True
    seed = 1
    number_of_images = 1
    img, masked_img = start_tryon(img, garm_img, garment_des, category, is_checked, is_checked_crop, denoise_steps, is_randomize_seed, seed, number_of_images)


    img = img[0]

    return send_file(img, mimetype='image/jpeg')


