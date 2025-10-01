from flask import Blueprint, render_template, current_app, send_from_directory
import os

from ..services.image_service import get_all_images, get_image_by_id

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    images = get_all_images()
    return render_template('index.html', images=images)

@main_bp.route('/image/<int:image_id>')
def image_detail(image_id):
    image = get_image_by_id(image_id)
    if image:
        return render_template('image_detail.html', image=image)
    return "Image not found", 404

@main_bp.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    # This route is for serving uploaded files directly
    # The filename includes the date subfolder, e.g., YYYY-MM-DD/image.jpg
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename)
