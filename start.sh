#!/bin/sh

echo "Iniciando despliegue..."

# 1. Mover archivos vitales (Sobrescribir para permitir actualizaciones)
# Copiamos el JAR y las librerías desde la imagen (/app) al volumen (/data)
echo "Actualizando núcleo del servidor..."
cp -f /app/server.jar /data/server.jar
cp -rf /app/libraries /data/
cp -rf /app/versions /data/

# 2. Mover archivos de configuración (SIN sobrescribir)
# Solo copiamos server.properties y jsons si NO existen en el volumen
# Esto evita borrar tu configuración si reinicias el servidor.
echo "Verificando configuraciones..."
if [ ! -f /data/server.properties ]; then
    cp /app/server.properties /data/
fi

if [ ! -f /data/whitelist.json ]; then
    cp /app/whitelist.json /data/
fi

if [ ! -f /data/ops.json ]; then
    cp /app/ops.json /data/
fi

# 3. Aceptar EULA siempre
echo "eula=true" > /data/eula.txt

# 4. Iniciar el servidor
echo "Arrancando Minecraft..."
exec java -Xmx2G -Xms1G -jar /data/server.jar nogui