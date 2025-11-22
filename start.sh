#!/bin/sh

echo "Iniciando despliegue..."

# 1. Mover archivos nucleares (Siempre se actualizan)
echo "Actualizando núcleo del servidor e icono..."
cp -f /app/server.jar /data/server.jar
# Aseguramos que el icono se fuerce también
cp -f /app/server-icon.png /data/server-icon.png 
cp -rf /app/libraries /data/
cp -rf /app/versions /data/

# 2. CONFIGURACIÓN: AQUI ESTABA EL PROBLEMA
# Antes preguntábamos si existía. Ahora lo forzamos para que tus cambios en GitHub
# se apliquen en el servidor real.
echo "Actualizando server.properties..."
cp -f /app/server.properties /data/server.properties

# 3. Archivos de estado (Estos SI los protegemos)
# La whitelist y ops (administradores) se suelen cambiar desde dentro del juego
# así que es mejor no sobrescribirlos si ya existen.
if [ ! -f /data/whitelist.json ]; then
    cp /app/whitelist.json /data/
fi

if [ ! -f /data/ops.json ]; then
    cp /app/ops.json /data/
fi

# 4. Aceptar EULA
echo "eula=true" > /data/eula.txt

# 5. Iniciar el monitor de Discord en segundo plano (sin buffer)
echo "Iniciando monitor de Discord..."
python3 -u /app/discord_monitor.py 2>&1 &
MONITOR_PID=$!
echo "Monitor de Discord iniciado con PID: $MONITOR_PID"

# 6. Iniciar el servidor
echo "Arrancando Minecraft..."
exec java -Xmx8G -Xms1G -jar /data/server.jar nogui