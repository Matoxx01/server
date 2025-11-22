FROM eclipse-temurin:21-jre-alpine

# Instalamos bash, python3 y pip para el script y el monitor de Discord
RUN apk add --no-cache bash python3 py3-pip

# 1. Usamos /app para guardar los archivos originales
WORKDIR /app
COPY . .

# Instalar dependencias de Python para el monitor de Discord
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# 2. Convertir finales de línea y dar permisos de ejecución
RUN apk add --no-cache dos2unix && \
    dos2unix start.sh && \
    chmod +x start.sh && \
    apk del dos2unix

# 3. IMPORTANTE: No ponemos "VOLUME" aquí.
# Railway montará el volumen automáticamente en /data porque lo configuraste en la web.
# Solo cambiamos el directorio de trabajo para que Java se ejecute allí.
WORKDIR /data

# 4. El comando de inicio ejecuta nuestro script que mueve los archivos
CMD ["/app/start.sh"]