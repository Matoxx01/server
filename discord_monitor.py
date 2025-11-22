import os
import re
import sys
import time
import requests
from datetime import datetime
from pathlib import Path

# Forzar salida sin buffer para que aparezca en Railway
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

# Configuración
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
LOG_FILE = '/data/logs/latest.log'
CHECK_INTERVAL = 2  # segundos

# Patrón para detectar jugadores uniéndose
# Formato: [HH:MM:SS] [Server thread/INFO]: PlayerName joined the game
JOIN_PATTERN = re.compile(r'\[(\d{2}:\d{2}:\d{2})\]\s+\[Server thread/INFO\]:\s+(.+?)\s+joined the game')

def send_discord_message(player_name, join_time):
    """Envía un mensaje a Discord cuando un jugador se une"""
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ DISCORD_WEBHOOK_URL no está configurado", flush=True)
        return
    
    print(f"📤 Enviando notificación a Discord para: {player_name}...", flush=True)
    
    # Crear el mensaje embebido
    embed = {
        "title": "🎮 Jugador conectado",
        "description": f"**{player_name}** se ha unido al servidor",
        "color": 5763719,  # Color verde
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {
            "text": "iClub Minecraft Server"
        },
        "fields": [
            {
                "name": "⏰ Hora",
                "value": join_time,
                "inline": True
            }
        ]
    }
    
    payload = {
        "embeds": [embed]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 204:
            print(f"✅ NOTIFICACIÓN ENVIADA A DISCORD: {player_name} conectado!", flush=True)
        else:
            print(f"❌ Error al enviar a Discord: HTTP {response.status_code}", flush=True)
            print(f"   Respuesta: {response.text}", flush=True)
    except Exception as e:
        print(f"❌ Error de conexión con Discord: {e}", flush=True)

def monitor_logs():
    """Monitorea el archivo de logs en tiempo real"""
    print("=" * 50, flush=True)
    print("🔍 MONITOR DE DISCORD INICIADO", flush=True)
    print("=" * 50, flush=True)
    
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ ADVERTENCIA: DISCORD_WEBHOOK_URL no está configurado.", flush=True)
        print("   Configura la variable de entorno para recibir notificaciones.", flush=True)
    else:
        print(f"✅ Webhook configurado: {DISCORD_WEBHOOK_URL[:50]}...", flush=True)
    
    # Esperar a que el archivo de log exista
    log_path = Path(LOG_FILE)
    wait_count = 0
    while not log_path.exists():
        print(f"⏳ Esperando que se cree {LOG_FILE}... ({wait_count + 1})", flush=True)
        time.sleep(5)
        wait_count += 1
        if wait_count > 12:  # 1 minuto
            print(f"❌ Timeout esperando el archivo de log", flush=True)
            return
    
    print(f"✅ MONITOREANDO: {LOG_FILE}", flush=True)
    print("   Esperando que jugadores se conecten...", flush=True)
    print("   Buscando el patrón: 'joined the game'", flush=True)
    
    # Conjunto para rastrear jugadores ya notificados (evitar duplicados)
    notified_players = set()
    
    # Abrir el archivo y leer desde el principio para no perder eventos
    with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        # Leer líneas existentes primero (para procesar conexiones que ya ocurrieron)
        print("📖 Leyendo eventos existentes...", flush=True)
        for line in f:
            if 'joined the game' in line:
                match = JOIN_PATTERN.search(line)
                if match:
                    join_time = match.group(1)
                    player_name = match.group(2)
                    notified_players.add(player_name)  # Marcar como ya procesado
                    print(f"📋 Evento anterior encontrado: {player_name} a las {join_time}", flush=True)
        
        print("✅ Listo! Ahora monitoreando eventos nuevos en tiempo real...", flush=True)
        
        # Contador para debug
        heartbeat_counter = 0
        
        # Ahora monitorear nuevas líneas en tiempo real
        while True:
            # Verificar si el archivo fue truncado/rotado
            current_pos = f.tell()
            f.seek(0, 2)  # Ir al final
            file_size = f.tell()
            
            if current_pos > file_size:
                print("🔄 Archivo rotado, reiniciando lectura...", flush=True)
                f.seek(0)
            else:
                f.seek(current_pos)
            
            line = f.readline()
            
            if line:
                # Reset heartbeat cuando hay actividad
                heartbeat_counter = 0
                
                # Debug: mostrar TODAS las líneas del servidor para verificar que está leyendo
                if '[Server thread/INFO]' in line:
                    print(f"📝 LOG: {line.strip()}", flush=True)
                
                # Debug: mostrar líneas que contienen "joined"
                if 'joined' in line.lower():
                    print(f"🔍 Línea con 'joined' detectada: {line.strip()}", flush=True)
                
                # Buscar el patrón de jugador uniéndose
                match = JOIN_PATTERN.search(line)
                if match:
                    join_time = match.group(1)
                    player_name = match.group(2)
                    
                    # Solo notificar si es un evento nuevo (no procesado antes)
                    if player_name not in notified_players:
                        print(f"\n🎮 JUGADOR DETECTADO: {player_name} a las {join_time}", flush=True)
                        send_discord_message(player_name, join_time)
                        notified_players.add(player_name)
                    else:
                        print(f"⏭️ Evento duplicado ignorado: {player_name}", flush=True)
                elif 'joined the game' in line:
                    print(f"⚠️ Línea no coincidió con el patrón: {line.strip()}", flush=True)
            else:
                # No hay nuevas líneas, esperar un momento
                heartbeat_counter += 1
                
                # Mostrar señal de vida cada 30 segundos
                if heartbeat_counter % 15 == 0:
                    print(f"💓 Monitor activo... ({heartbeat_counter * CHECK_INTERVAL}s esperando)", flush=True)
                
                time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        monitor_logs()
    except KeyboardInterrupt:
        print("\n👋 Monitor de Discord detenido", flush=True)
    except Exception as e:
        print(f"❌ Error fatal en monitor: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise
