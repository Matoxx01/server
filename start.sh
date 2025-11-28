#!/bin/sh

echo "========================================"
echo "  🚀 Iniciando Servidor Spigot 1.21.10"
echo "========================================"

# 1. Mover archivos nucleares del servidor (Siempre se actualizan)
echo "📦 Actualizando núcleo del servidor Spigot..."
cp -f /app/server.jar /data/server.jar
cp -f /app/server-icon.png /data/server-icon.png 
cp -rf /app/libraries /data/
cp -rf /app/versions /data/

# 2. Actualizar configuraciones principales de servidor
echo "⚙️ Actualizando configuraciones del servidor..."
cp -f /app/server.properties /data/server.properties
cp -f /app/ops.json /data/ops.json
cp -f /app/usercache.json /data/usercache.json

# 3. Actualizar configuraciones de Spigot/Bukkit
echo "🔧 Configurando Spigot y Bukkit..."
cp -f /app/spigot.yml /data/spigot.yml
cp -f /app/bukkit.yml /data/bukkit.yml
cp -f /app/commands.yml /data/commands.yml

# Solo copiar permissions.yml si no existe (para preservar cambios manuales)
if [ ! -f /data/permissions.yml ]; then
    echo "   Creando permissions.yml inicial..."
    cp /app/permissions.yml /data/permissions.yml
fi

# 4. Gestión de PLUGINS
echo "🔌 Sincronizando plugins de Spigot..."
# Crear directorio de plugins si no existe
mkdir -p /data/plugins

# Copiar todos los plugins desde /app/plugins a /data/plugins
# Esto asegura que los plugins actualizados se desplieguen
if [ -d /app/plugins ]; then
    echo "   Copiando plugins desde el repositorio..."
    cp -rf /app/plugins/* /data/plugins/ 2>/dev/null || true
    echo "   ✅ Plugins sincronizados"
fi

# Crear carpetas de configuración para cada plugin si no existen
mkdir -p /data/plugins/DecentHolograms
mkdir -p /data/plugins/Graves
mkdir -p /data/plugins/GriefPrevention
mkdir -p /data/plugins/SkinsRestorer

# 5. Archivos de estado (Estos SI los protegemos)
echo "📋 Verificando whitelist y baneos..."
if [ ! -f /data/whitelist.json ]; then
    cp /app/whitelist.json /data/
fi
if [ ! -f /data/banned-players.json ]; then
    cp /app/banned-players.json /data/
fi
if [ ! -f /data/banned-ips.json ]; then
    cp /app/banned-ips.json /data/
fi

# 6. Aceptar EULA
echo "✅ Aceptando EULA de Minecraft..."
echo "eula=true" > /data/eula.txt

# OPCIONAL: Descomentar estas líneas para regenerar el mundo con nueva seed
# ADVERTENCIA: Esto BORRARÁ el mundo actual permanentemente
# echo "🌍 Regenerando mundo con nueva seed..."
# rm -rf /data/world /data/world_nether /data/world_the_end
# rm -rf /data/DIM-1 /data/DIM1

# 7. Iniciar el monitor de Discord en segundo plano
echo "📡 Iniciando monitor de Discord..."
python3 -u /app/discord_monitor.py 2>&1 &
MONITOR_PID=$!
echo "   ✅ Monitor iniciado (PID: $MONITOR_PID)"

# 8. Iniciar el servidor Spigot con optimizaciones
echo "========================================"
echo "  🎮 Arrancando Servidor Spigot"
echo "========================================"
echo "   RAM: 8GB máx, 1GB mín"
echo "   Plugins: DecentHolograms, Graves, GriefPrevention, SkinsRestorer"
echo "   Monitor Discord: Activo"
echo "========================================"

java -Xmx8G -Xms1G \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:+AlwaysPreTouch \
  -XX:G1NewSizePercent=30 \
  -XX:G1MaxNewSizePercent=40 \
  -XX:G1HeapRegionSize=8M \
  -XX:G1ReservePercent=20 \
  -XX:G1HeapWastePercent=5 \
  -XX:G1MixedGCCountTarget=4 \
  -XX:InitiatingHeapOccupancyPercent=15 \
  -XX:G1MixedGCLiveThresholdPercent=90 \
  -XX:G1RSetUpdatingPauseTimePercent=5 \
  -XX:SurvivorRatio=32 \
  -XX:+PerfDisableSharedMem \
  -XX:MaxTenuringThreshold=1 \
  -Dusing.aikars.flags=https://mcflags.emc.gs \
  -Daikars.new.flags=true \
  -jar /data/server.jar nogui &

SERVER_PID=$!
echo "   ✅ Servidor iniciado (PID: $SERVER_PID)"

# 9. Esperar a que el servidor Spigot esté listo y aplicar permisos OP
echo ""
echo "⏳ Esperando que Spigot cargue plugins y mundo (30s)..."
sleep 30

echo "👑 Aplicando permisos de operador via RCON..."
# Enviar comando OP via RCON (mcrcon ya está compilado en el Dockerfile)
mcrcon -H localhost -P 25575 -p railway_rcon_2024 "op Matoxx01" && \
  echo "   ✅ Permisos OP aplicados a Matoxx01" || \
  echo "   ⚠️ No se pudo conectar via RCON (el servidor puede estar iniciando aún)"

echo ""
echo "========================================"
echo "  ✅ Servidor Spigot completamente listo"
echo "========================================"
echo "  Puertos: 25565 (Minecraft), 25575 (RCON)"
echo "  Monitor Discord: Activo"
echo "  Plugins: Cargados"
echo "========================================"

# Mantener el proceso activo
wait $SERVER_PID