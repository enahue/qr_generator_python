from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import qrcode
import os

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://127.0.0.1:5000/static/openapi.yaml'  # Our API url (can be an URL)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be served at {SWAGGER_URL}/dist/
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "QR Code API"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
        """
        Generate a QR code based on the provided data and return the image link.

        Parameters:
        - data (str): The data to be encoded in the QR code.

        Returns:
        - JSON response: A JSON response containing the message and image link.
            - message (str): A success message indicating that the QR code was generated successfully.
            - image_link (str): The link to the generated QR code image.
        """
        data = request.json.get('data')
        if not data:
                return jsonify({'error': 'No data provided'}), 400
        
        qr = qrcode.QRCode(version=1, box_size=10, border=1)
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')
        
        qr_img_path = 'qr_code.png'
        qr_img.save(qr_img_path)
        
        qr_img_link = os.path.join(request.host_url, qr_img_path)
        
        return jsonify({'message': 'QR code generated successfully', 'image_link': qr_img_link}), 200

if __name__ == '__main__':
    app.run()