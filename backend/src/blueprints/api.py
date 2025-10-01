from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from PIL import Image as PILImage

from ..models.image import db, Image
from ..services.image_service import save_image_to_db, get_all_images, get_image_by_id, delete_image_by_id

api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 415

    if file and allowed_file(file.filename):
        try:
            # Check file size before saving
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0) # Reset file pointer to the beginning

            if file_size > current_app.config['MAX_CONTENT_LENGTH']:
                return jsonify({'error': f'File size exceeds limit of {current_app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024):.0f}MB'}), 413

            original_filename = secure_filename(file.filename)
            upload_date = datetime.utcnow().strftime('%Y-%m-%d')
            upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], upload_date)
            os.makedirs(upload_folder, exist_ok=True)

            unique_filename = f'{os.urandom(16).hex()}_{int(datetime.utcnow().timestamp())}_{original_filename}'
            filepath = os.path.join(upload_folder, unique_filename)
            file.save(filepath)

            # Get image dimensions and MIME type using Pillow
            with PILImage.open(filepath) as img:
                width, height = img.size
                mime_type = img.format.lower()

            # Generate URL (assuming Flask serves static files from /uploads)
            url = f'/uploads/{upload_date}/{unique_filename}'

            image_data = {
                'filename': original_filename,
                'filepath': filepath,
                'url': url,
                'file_size': file_size,
                'mime_type': mime_type,
                'width': width,
                'height': height
            }
            new_image = save_image_to_db(image_data)

            return jsonify({
                'message': 'Image uploaded successfully',
                'image': {
                    'id': new_image.id,
                    'filename': new_image.filename,
                    'url': new_image.url,
                    'upload_timestamp': new_image.upload_timestamp.isoformat(),
                    'file_size': new_image.file_size,
                    'mime_type': new_image.mime_type,
                    'width': new_image.width,
                    'height': new_image.height
                }
            }), 201
        except Exception as e:
            current_app.logger.error(f"Error uploading image: {e}")
            return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/images', methods=['GET'])
def list_images():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    images = get_all_images(page, limit)
    return jsonify([
        {
            'id': img.id,
            'filename': img.filename,
            'url': img.url,
            'upload_timestamp': img.upload_timestamp.isoformat(),
            'file_size': img.file_size,
            'mime_type': img.mime_type,
            'width': img.width,
            'height': img.height
        } for img in images
    ]), 200

@api_bp.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = get_image_by_id(image_id)
    if image:
        return jsonify({
            'id': image.id,
            'filename': image.filename,
            'url': image.url,
            'upload_timestamp': image.upload_timestamp.isoformat(),
            'file_size': image.file_size,
            'mime_type': image.mime_type,
            'width': image.width,
            'height': image.height
        }), 200
    return jsonify({'error': 'Image not found'}), 404

@api_bp.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    if delete_image_by_id(image_id):
        return '', 204
    return jsonify({'error': 'Image not found'}), 404

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200
