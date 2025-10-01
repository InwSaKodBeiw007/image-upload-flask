import os
from datetime import datetime
from flask import current_app

from ..models.image import db, Image

def save_image_to_db(image_data):
    new_image = Image(
        filename=image_data['filename'],
        filepath=image_data['filepath'],
        url=image_data['url'],
        file_size=image_data['file_size'],
        mime_type=image_data['mime_type'],
        width=image_data['width'],
        height=image_data['height']
    )
    db.session.add(new_image)
    db.session.commit()
    return new_image

def get_all_images(page=1, limit=20):
    return Image.query.order_by(Image.upload_timestamp.desc()).paginate(page=page, per_page=limit, error_out=False).items

def get_image_by_id(image_id):
    return Image.query.get(image_id)

def delete_image_by_id(image_id):
    image = Image.query.get(image_id)
    if image:
        try:
            os.remove(image.filepath)
            db.session.delete(image)
            db.session.commit()
            return True
        except OSError as e:
            current_app.logger.error(f"Error deleting file {image.filepath}: {e}")
            db.session.rollback()
            return False
    return False
