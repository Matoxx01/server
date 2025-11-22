import os
import re
import time
import requests
from datetime import datetime
from pathlib import Path

# Configuración
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
LOG_FILE = '/data/logs/latest.log'
CHECK_INTERVAL = 2  # segundos

# Patrón para detectar jugadores uniéndose
# Formato: [HH:MM:SS] [Server thread/INFO]: PlayerName joined the game
JOIN_PATTERN = re.compile(r'\[(\d{2}:\d{2}:\d{2})\] \[Server thread/INFO\]: (.+?) joined the game')

def send_discord_message(player_name, join_time):
    """Envía un mensaje a Discord cuando un jugador se une"""
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ DISCORD_WEBHOOK_URL no está configurado")
        return
    
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
            print(f"✅ Notificación enviada a Discord: {player_name}")
        else:
            print(f"❌ Error al enviar a Discord: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión con Discord: {e}")

def monitor_logs():
    """Monitorea el archivo de logs en tiempo real"""
    print("🔍 Iniciando monitor de Discord...")
    
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ ADVERTENCIA: DISCORD_WEBHOOK_URL no está configurado.")
        print("   Configura la variable de entorno para recibir notificaciones.")
    
    # Esperar a que el archivo de log exista
    log_path = Path(LOG_FILE)
    while not log_path.exists():
        print(f"⏳ Esperando que se cree {LOG_FILE}...")
        time.sleep(5)
    
    print(f"✅ Monitoreando: {LOG_FILE}")
    
    # Abrir el archivo y posicionarse al final
    with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        # Ir al final del archivo
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            
            if line:
                # Buscar el patrón de jugador uniéndose
                match = JOIN_PATTERN.search(line)
                if match:
                    join_time = match.group(1)
                    player_name = match.group(2)
                    print(f"🎮 Jugador detectado: {player_name} a las {join_time}")
                    send_discord_message(player_name, join_time)
            else:
                # No hay nuevas líneas, esperar un momento
                time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        monitor_logs()
    except KeyboardInterrupt:
        print("\n👋 Monitor de Discord detenido")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        raise
