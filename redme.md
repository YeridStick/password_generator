# Generador de Contraseñas - Guía Rápida

## Descripción
Esta es una aplicación web para generar contraseñas seguras con opciones personalizables. Permite ajustar la longitud y los tipos de caracteres incluidos en las contraseñas generadas.

## Requisitos
- Python 3.7 o superior
- Flask

## Instalación

1. **Instalar Flask**:
   ```
   pip install flask
   ```

2. **Estructura de carpetas**:
   Asegúrate de tener esta estructura de archivos:
   ```
   password_generator/
   ├── app.py
   ├── models/
   │   ├── __init__.py
   │   └── password.py
   ├── static/
   │   ├── css/
   │   │   └── styles.css
   │   └── js/
   │       └── scripts.js
   └── templates/
       └── index.html
   ```

## Ejecución

1. Abre una terminal en la carpeta principal del proyecto
2. Ejecuta:
   ```
   python app.py
   ```
3. Abre tu navegador web y visita:
   ```
   http://127.0.0.1:5000
   ```

## Cómo usar la aplicación

### Generación básica
1. Ajusta la longitud de la contraseña usando los botones + y -
2. Haz clic en "Generar Contraseña"
3. La contraseña aparecerá en el campo superior
4. Haz clic en el icono de copia para copiarla al portapapeles

### Personalización de requisitos
1. Haz clic en "Personalizar requisitos" para ver opciones avanzadas
2. Activa/desactiva requisitos según tus necesidades:
   - Longitud mínima
   - Letras mayúsculas
   - Letras minúsculas
   - Números
   - Caracteres especiales
   - Repetición de caracteres
3. Haz clic en "Generar Contraseña" para aplicar los cambios

## Solución de problemas comunes

- **Error 404 en archivos CSS/JS**: Verifica que los archivos están en las carpetas correctas (static/css y static/js)
- **Error al generar contraseña**: Asegúrate de no deshabilitar todos los tipos de caracteres
- **Aplicación no inicia**: Comprueba que Flask está instalado correctamente

## Estructura del código (breve)

- **app.py**: Servidor web y rutas principales
- **models/password.py**: Clases para generar y validar contraseñas
- **templates/index.html**: Plantilla HTML de la interfaz
- **static/css/styles.css**: Estilos visuales
- **static/js/scripts.js**: Interactividad de la página

---

Desarrollado por: Yerid Stick Ramirez Guzman  
Universidad Nacional Abierta y a Distancia (UNAD)  
2025