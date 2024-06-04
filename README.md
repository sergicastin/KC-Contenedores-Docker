# Práctica: Contenedores, más que VMs

## Instrucciones:
1. Clonar el repositorio
2. Abrir una terminal en el directorio
3. Ejecutar `docker-compose up`
4. Acceder a http://127.0.0.1:8080
5. Usar la aplicación

## Descripción de la aplicación
Esta aplicación, construida en Docker y Docker-compose, se compone de dos contenedores: uno para la interfaz web y otro para la base de datos.

La página web está compuesta por un frontend HTML y un backend Python. En ella podemos encontrar un formulario simulando una entrega de prácticas, con inputs para el nombre, correo, link de la práctica y un selector de categoría. Justo debajo del formulario aparece la tabla de la base de datos con el contenido que tenga en ese momento, también un botón de eliminar por cada fila de la tabla.

La base de datos está compuesta por un servidor MySQL, creando una base de datos llamada "**sergicastindb**" y una tabla llamada "**practicas**".

## Funcionamiento de la aplicación
### Backend
El backend está compuesto por una función para conectarse a la base de datos, otra para crear la tabla, y tres funciones más para insertar, seleccionar y eliminar datos, junto a otra para configurar los logs.

### Dockerfile
El Dockerfile usa como base un `python:3.8`. En el primer paso, configura el directorio de trabajo en **/app**, copia el fichero de requisitos y los instala todos los requisitos que necesita nuestra aplicación para funcionar. Después, en el mismo directorio de trabajo, crea una carpeta llamada "**logs**", le otorga permisos totales y configura la salida de logs a formato JSON en **/logs/app.log**. Luego, copia los archivos necesarios, módulos de Python y la aplicación de Python. Por último, define el comando por defecto para ejecutar la aplicación como **python app.py**.

### docker-compose.yaml
Empieza por indicar la versión que usaremos, en nuestro caso la **3.9**. Crea el servicio "web", al cual le indica que se construirá utilizando el Dockerfile, le mapea el puerto 8080 del host al puerto 8080 del contenedor, crea un volumen para los logs e indica el archivo **.env** con las variables que usaremos más adelante. El otro servicio que crea es el de la base de datos "db", el cual usa una imagen "**mysql:8.3.0**" y define dentro del environment el nombre de la base de datos y la contraseña. Mapea también el puerto de la base de datos, todo eso desde variables que están en el archivo **.env** antes mencionado.

## Logs de la aplicación
Los logs de la aplicación están configurados para que tengan un formato JSON. Están almacenados en la carpeta logs. El programa contempla los logs del servidor web y la base de datos en el mismo archivo **app.json**.

## Configurabilidad de la aplicación
Existe la opción de cambiar la configuración de la base de datos. Podemos cambiar el nombre de la base de datos y la contraseña del usuario root desde el archivo **.env**.

IMPORTANTE: Para que el cambio haga efecto, se debe eliminar todo rastro de las imágenes de esta aplicación, no funciona con `docker-compose up --build`.
