#!/bin/sh

echo "Iniciando despliegue..."

# 1. Mover archivos vitales (Sobrescribir para permitir actualizaciones)
echo "Actualizando núcleo del servidor e icono..."
cp -f /app/server.jar /data/server.jar
cp -f /app/server-icon.png /data/server-icon.png  <-- ¡Esta es la línea nueva!
cp -rf /app/libraries /data/
cp -rf /app/versions /data/

# 2. Mover archivos de configuración (SIN sobrescribir)
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

# 3. Aceptar EULA
echo "eula=true" > /data/eula.txt

# 4. Iniciar el servidor
echo "Arrancando Minecraft..."
exec java -Xmx2G -Xms1G -jar /data/server.jar nogui