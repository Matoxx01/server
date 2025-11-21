FROM eclipse-temurin:21-jre-alpine

# Instalamos bash por si acaso, aunque usamos sh
RUN apk add --no-cache bash

# 1. Usamos /app para guardar los archivos originales de la imagen
WORKDIR /app
COPY . .

# 2. Damos permisos de ejecución al script
RUN chmod +x start.sh

# 3. Definimos el volumen (Railway lo montará aquí)
VOLUME /data
WORKDIR /data

# 4. El comando de inicio ejecuta nuestro script
CMD ["/app/start.sh"]