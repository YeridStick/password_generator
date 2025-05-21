import random
import string

class CharacterSet:
    """Clase base para conjuntos de caracteres"""
    def __init__(self):
        self._characters = ""
    
    def get_characters(self):
        return self._characters
    
    def get_random_char(self):
        """Retorna un carácter aleatorio del conjunto"""
        if not self._characters:
            return ""
        return random.choice(self._characters)


class UppercaseSet(CharacterSet):
    """Clase para caracteres en mayúscula"""
    def __init__(self):
        super().__init__()
        self._characters = string.ascii_uppercase


class LowercaseSet(CharacterSet):
    """Clase para caracteres en minúscula"""
    def __init__(self):
        super().__init__()
        self._characters = string.ascii_lowercase


class DigitSet(CharacterSet):
    """Clase para dígitos numéricos"""
    def __init__(self):
        super().__init__()
        self._characters = string.digits


class SpecialCharSet(CharacterSet):
    """Clase para caracteres especiales"""
    def __init__(self, special_chars="¿¡?=)(/¨*+-%&$#!"):
        super().__init__()
        self._characters = special_chars


class PasswordGenerator:
    """Generador de contraseñas aleatorias con opciones personalizables"""
    def __init__(self):
        # Configurar los conjuntos de caracteres disponibles
        self.char_sets = {
            'uppercase': UppercaseSet(),
            'lowercase': LowercaseSet(),
            'digit': DigitSet(),
            'special': SpecialCharSet()
        }
    
    def generate_password(self, **kwargs):
        """
        Genera una contraseña aleatoria según los requisitos personalizados
        
        Args:
            length (int): Longitud total de la contraseña
            min_length (int): Longitud mínima permitida
            require_uppercase (bool): Si se requiere al menos una mayúscula
            require_lowercase (bool): Si se requiere al menos una minúscula
            require_digit (bool): Si se requiere al menos un número
            require_special (bool): Si se requiere al menos un carácter especial
            special_chars (str): Caracteres especiales a usar
            no_repeats (bool): Si se prohíben caracteres repetidos
            
        Returns:
            str: Contraseña generada
        """
        # Obtener parámetros con valores predeterminados
        length = kwargs.get('length', 12)
        min_length = kwargs.get('min_length', 8)
        require_uppercase = kwargs.get('require_uppercase', True)
        require_lowercase = kwargs.get('require_lowercase', True)
        require_digit = kwargs.get('require_digit', True)
        require_special = kwargs.get('require_special', True)
        special_chars = kwargs.get('special_chars', "¿¡?=)(/¨*+-%&$#!")
        no_repeats = kwargs.get('no_repeats', True)
        
        # Validar longitud mínima
        if length < min_length:
            length = min_length
        
        # Actualizar caracteres especiales si se proporcionan
        if special_chars != self.char_sets['special'].get_characters():
            self.char_sets['special'] = SpecialCharSet(special_chars)
        
        # Seleccionar los conjuntos de caracteres activos según los requisitos
        active_sets = []
        required_chars = []
        
        if require_uppercase:
            active_sets.append(self.char_sets['uppercase'])
            required_chars.append(self.char_sets['uppercase'].get_random_char())
        
        if require_lowercase:
            active_sets.append(self.char_sets['lowercase'])
            required_chars.append(self.char_sets['lowercase'].get_random_char())
        
        if require_digit:
            active_sets.append(self.char_sets['digit'])
            required_chars.append(self.char_sets['digit'].get_random_char())
        
        if require_special:
            active_sets.append(self.char_sets['special'])
            required_chars.append(self.char_sets['special'].get_random_char())
        
        # Si no hay conjuntos activos, usar letras minúsculas por defecto
        if not active_sets:
            active_sets.append(self.char_sets['lowercase'])
            required_chars = [self.char_sets['lowercase'].get_random_char()]
        
        # Verificar si la longitud es suficiente para los caracteres requeridos
        if len(required_chars) > length:
            # Si no hay suficiente espacio, reducir los requisitos al azar
            random.shuffle(required_chars)
            required_chars = required_chars[:length]
        
        # Crear el conjunto completo de caracteres disponibles
        all_chars = "".join(char_set.get_characters() for char_set in active_sets)
        
        # Iniciar con los caracteres requeridos
        password_chars = required_chars.copy()
        
        # Completar la contraseña hasta la longitud deseada
        attempts = 0
        max_attempts = 1000  # Prevenir bucles infinitos
        
        while len(password_chars) < length and attempts < max_attempts:
            char = random.choice(all_chars)
            
            # Si no se permiten repeticiones, verificar que el carácter no esté ya en la contraseña
            if no_repeats and char in password_chars:
                attempts += 1
                continue
            
            password_chars.append(char)
            attempts = 0
        
        # Mezclar los caracteres para que el orden sea aleatorio
        random.shuffle(password_chars)
        
        return "".join(password_chars)


class PasswordValidator:
    """Clase para validar contraseñas con requisitos personalizables"""
    def __init__(self, password, **kwargs):
        self.password = password
        
        # Configurar requisitos personalizados
        self.min_length = kwargs.get('min_length', 8)
        self.require_uppercase = kwargs.get('require_uppercase', True)
        self.require_lowercase = kwargs.get('require_lowercase', True)
        self.require_digit = kwargs.get('require_digit', True)
        self.require_special = kwargs.get('require_special', True)
        self.special_chars = kwargs.get('special_chars', "¿¡?=)(/¨*+-%&$#!")
        self.no_repeats = kwargs.get('no_repeats', True)
    
    def has_minimum_length(self):
        """Verifica si la contraseña tiene la longitud mínima requerida"""
        return len(self.password) >= self.min_length
    
    def has_uppercase(self):
        """Verifica si la contraseña contiene al menos una letra mayúscula"""
        # Si no se requiere, devolver True automáticamente
        if not self.require_uppercase:
            return True
        return any(char.isupper() for char in self.password)
    
    def has_lowercase(self):
        """Verifica si la contraseña contiene al menos una letra minúscula"""
        if not self.require_lowercase:
            return True
        return any(char.islower() for char in self.password)
    
    def has_digit(self):
        """Verifica si la contraseña contiene al menos un dígito"""
        if not self.require_digit:
            return True
        return any(char.isdigit() for char in self.password)
    
    def has_special_char(self):
        """Verifica si la contraseña contiene al menos un carácter especial"""
        if not self.require_special:
            return True
        return any(char in self.special_chars for char in self.password)
    
    def has_no_repeats(self):
        """Verifica si la contraseña no tiene caracteres repetidos"""
        if not self.no_repeats:
            return True
        return len(self.password) == len(set(self.password))
    
    def is_valid(self):
        """Verifica si la contraseña cumple con todos los requisitos activos"""
        return (
            self.has_minimum_length() and
            self.has_uppercase() and
            self.has_lowercase() and
            self.has_digit() and
            self.has_special_char() and
            self.has_no_repeats()
        )