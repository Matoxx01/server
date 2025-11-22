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
    print("=" * 50, flush=True)
    print(f"📤 INICIANDO ENVÍO DE WEBHOOK", flush=True)
    print(f"   Jugador: {player_name}", flush=True)
    print(f"   Hora: {join_time}", flush=True)
    
    if not DISCORD_WEBHOOK_URL:
        print("❌ ERROR: DISCORD_WEBHOOK_URL no está configurado", flush=True)
        return
    
    # Mostrar webhook ofuscado
    webhook_preview = DISCORD_WEBHOOK_URL[:50] + "..." if len(DISCORD_WEBHOOK_URL) > 50 else DISCORD_WEBHOOK_URL
    print(f"   Webhook: {webhook_preview}", flush=True)
    print("   Preparando payload...", flush=True)
    
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
    
    print("   Realizando petición POST...", flush=True)
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        print(f"   Código de respuesta: {response.status_code}", flush=True)
        
        if response.status_code == 204:
            print("✅ ¡NOTIFICACIÓN ENVIADA EXITOSAMENTE A DISCORD!", flush=True)
            print(f"   Jugador: {player_name}", flush=True)
        elif response.status_code == 429:
            print("⚠️ Rate limit alcanzado (demasiadas solicitudes)", flush=True)
            print(f"   Respuesta: {response.text}", flush=True)
        else:
            print(f"❌ Error al enviar webhook", flush=True)
            print(f"   HTTP Status: {response.status_code}", flush=True)
            print(f"   Respuesta: {response.text[:200]}", flush=True)
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT: La petición tardó más de 10 segundos", flush=True)
        print("   ¿Hay problemas de conectividad?", flush=True)
    except requests.exceptions.ConnectionError as e:
        print(f"❌ ERROR DE CONEXIÓN: No se pudo conectar a Discord", flush=True)
        print(f"   Detalles: {str(e)[:200]}", flush=True)
        print("   ¿Railway tiene acceso a internet?", flush=True)
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {type(e).__name__}", flush=True)
        print(f"   Mensaje: {str(e)[:200]}", flush=True)
        import traceback
        print("   Traceback:", flush=True)
        traceback.print_exc()
    
    print("=" * 50, flush=True)

def test_connectivity():
    """Prueba la conectividad a Discord"""
    print("🔌 Probando conectividad a Discord...", flush=True)
    try:
        test_response = requests.get("https://discord.com", timeout=5)
        print(f"   ✅ Discord alcanzable (Status: {test_response.status_code})", flush=True)
        return True
    except Exception as e:
        print(f"   ❌ No se puede alcanzar Discord: {e}", flush=True)
        return False

def monitor_logs():
    """Monitorea el archivo de logs en tiempo real"""
    print("=" * 50, flush=True)
    print("🔍 MONITOR DE DISCORD INICIADO", flush=True)
    print("=" * 50, flush=True)
    
    # Debug de variables de entorno
    print("🔧 Verificando configuración:", flush=True)
    webhook_var = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_var:
        print("   ❌ DISCORD_WEBHOOK_URL: NO CONFIGURADA", flush=True)
        print("   Variables disponibles:", flush=True)
        for key in sorted(os.environ.keys()):
            if 'DISCORD' in key.upper() or 'WEBHOOK' in key.upper():
                print(f"      - {key}", flush=True)
    else:
        webhook_preview = webhook_var[:50] + "..." if len(webhook_var) > 50 else webhook_var
        print(f"   ✅ DISCORD_WEBHOOK_URL: {webhook_preview}", flush=True)
        print(f"   Longitud: {len(webhook_var)} caracteres", flush=True)
    
    # Test de conectividad
    test_connectivity()
    print("=" * 50, flush=True)
    
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
        print("   DEBUG: Mostrando todas las líneas que lee...", flush=True)
        
        # Contador para debug
        heartbeat_counter = 0
        lines_read = 0
        
        # Ahora monitorear nuevas líneas en tiempo real
        while True:
            where = f.tell()
            line = f.readline()
            
            if line:
                # Reset heartbeat cuando hay actividad
                heartbeat_counter = 0
                lines_read += 1
                
                # Debug: mostrar TODAS las líneas para verificar que está leyendo
                print(f"📖 [{lines_read}] {line.strip()}", flush=True)
                
                # Buscar el patrón de jugador uniéndose
                if 'joined the game' in line:
                    print(f"🔍 ¡DETECTADA LÍNEA CON 'JOINED'!", flush=True)
                    
                    match = JOIN_PATTERN.search(line)
                    if match:
                        join_time = match.group(1)
                        player_name = match.group(2)
                        print(f"✅ REGEX MATCH: {player_name} a las {join_time}", flush=True)
                        
                        # Solo notificar si es un evento nuevo (no procesado antes)
                        if player_name not in notified_players:
                            print(f"\n🎮 ¡NUEVO JUGADOR! {player_name}", flush=True)
                            send_discord_message(player_name, join_time)
                            notified_players.add(player_name)
                        else:
                            print(f"⏭️ Jugador ya notificado: {player_name}", flush=True)
                    else:
                        print(f"❌ REGEX NO COINCIDE: {line.strip()}", flush=True)
            else:
                # No hay nuevas líneas, volver a la posición anterior
                f.seek(where)
                
                # Incrementar heartbeat
                heartbeat_counter += 1
                
                # Mostrar señal de vida cada 30 segundos
                if heartbeat_counter % 15 == 0:
                    print(f"💓 Monitor activo ({heartbeat_counter * CHECK_INTERVAL}s esperando, {lines_read} líneas leídas)", flush=True)
                
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
