from flask import Flask, render_template, request, jsonify
from models.password import PasswordGenerator, PasswordValidator
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Ruta principal que renderiza la página de inicio"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """API para generar contraseña con requisitos personalizados"""
    try:
        # Obtener los requisitos personalizados del JSON enviado
        data = request.get_json()
        
        # Establecer valores predeterminados si no se proporcionan
        length = int(data.get('length', 12))
        min_length = int(data.get('min_length', 8))
        require_uppercase = data.get('require_uppercase', True)
        require_lowercase = data.get('require_lowercase', True)
        require_digit = data.get('require_digit', True)
        require_special = data.get('require_special', True)
        special_chars = data.get('special_chars', "¿¡?=)(/¨*+-%&$#!")
        no_repeats = data.get('no_repeats', True)
        
        # Validar valores
        if length < min_length:
            return jsonify({'error': f'La longitud ({length}) debe ser al menos la mínima ({min_length})'}), 400
        
        # Crear generador con los requisitos personalizados
        generator = PasswordGenerator()
        
        # Configurar los parámetros
        params = {
            'length': length,
            'min_length': min_length,
            'require_uppercase': require_uppercase,
            'require_lowercase': require_lowercase,
            'require_digit': require_digit,
            'require_special': require_special,
            'special_chars': special_chars,
            'no_repeats': no_repeats
        }
        
        # Generar contraseña
        password = generator.generate_password(**params)
        
        # Validar la contraseña generada
        validator = PasswordValidator(password, **params)
        
        # Comprobar si la contraseña cumple con los requisitos
        is_valid = validator.is_valid()
        
        # En caso de fallo (extremadamente raro), intentar nuevamente
        attempts = 0
        while not is_valid and attempts < 5:
            password = generator.generate_password(**params)
            validator = PasswordValidator(password, **params)
            is_valid = validator.is_valid()
            attempts += 1
        
        if not is_valid:
            return jsonify({'error': 'No se pudo generar una contraseña válida. Revisa los requisitos.'}), 500
        
        # Devolver la contraseña generada y su validación
        return jsonify({
            'password': password,
            'validation': {
                'has_minimum_length': validator.has_minimum_length(),
                'has_uppercase': validator.has_uppercase(),
                'has_lowercase': validator.has_lowercase(),
                'has_digit': validator.has_digit(),
                'has_special_char': validator.has_special_char(),
                'has_no_repeats': validator.has_no_repeats()
            },
            'params': params
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Verificar que los directorios estáticos existan antes de iniciar
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    css_dir = os.path.join(static_dir, 'css')
    js_dir = os.path.join(static_dir, 'js')
    
    # Crear directorios si no existen
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)
    
    # Iniciar la aplicación
    app.run(debug=True, port=5000)