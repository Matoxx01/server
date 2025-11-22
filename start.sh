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
echo "Actualizando server.properties, ops.json y usercache.json..."
cp -f /app/server.properties /data/server.properties
cp -f /app/ops.json /data/ops.json
cp -f /app/usercache.json /data/usercache.json

# 3. Archivos de estado (Estos SI los protegemos)
# La whitelist se suele cambiar desde dentro del juego
# así que es mejor no sobrescribirla si ya existe.
if [ ! -f /data/whitelist.json ]; then
    cp /app/whitelist.json /data/
fi

# 4. Aceptar EULA
echo "eula=true" > /data/eula.txt

# OPCIONAL: Descomentar estas líneas para regenerar el mundo con nueva seed
# ADVERTENCIA: Esto BORRARÁ el mundo actual permanentemente
# echo "Regenerando mundo con nueva seed..."
# rm -rf /data/world /data/world_nether /data/world_the_end
# rm -rf /data/DIM-1 /data/DIM1

# 5. Iniciar el monitor de Discord en segundo plano (sin buffer)
echo "Iniciando monitor de Discord..."
python3 -u /app/discord_monitor.py 2>&1 &
MONITOR_PID=$!
echo "Monitor de Discord iniciado con PID: $MONITOR_PID"

# 6. Iniciar el servidor
echo "Arrancando Minecraft..."
java -Xmx8G -Xms1G -jar /data/server.jar nogui &
SERVER_PID=$!
echo "Servidor iniciado con PID: $SERVER_PID"

# 7. Esperar a que el servidor esté listo y forzar OP
echo "Esperando a que el servidor inicie completamente..."
sleep 10
echo "Forzando permisos de operador para Matoxx01..."
echo "op Matoxx01" > /proc/$SERVER_PID/fd/0 2>/dev/null || echo "op Matoxx01" | nc localhost 25575 2>/dev/null || echo "OP se debe aplicar manualmente"

# Mantener el proceso activo
wait $SERVER_PID