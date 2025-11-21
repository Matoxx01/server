FROM eclipse-temurin:21-jre-alpine

# Instalamos bash para el script
RUN apk add --no-cache bash

# 1. Usamos /app para guardar los archivos originales
WORKDIR /app
COPY . .

# 2. Damos permisos de ejecución al script
RUN chmod +x start.sh

# 3. IMPORTANTE: No ponemos "VOLUME" aquí.
# Railway montará el volumen automáticamente en /data porque lo configuraste en la web.
# Solo cambiamos el directorio de trabajo para que Java se ejecute allí.
WORKDIR /data

# 4. El comando de inicio ejecuta nuestro script que mueve los archivos
CMD ["/app/start.sh"]