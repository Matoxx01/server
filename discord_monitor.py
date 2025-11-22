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
# Soporta múltiples webhooks separados por coma
DISCORD_WEBHOOKS_STR = os.getenv('DISCORD_WEBHOOK_URL', '')
DISCORD_WEBHOOKS = [w.strip() for w in DISCORD_WEBHOOKS_STR.split(',') if w.strip()]

LOG_FILE = '/data/logs/latest.log'
CHECK_INTERVAL = 2  # segundos

# Patrones para detectar eventos
# Formato: [HH:MM:SS] [Server thread/INFO]: PlayerName joined the game
JOIN_PATTERN = re.compile(r'\[(\d{2}:\d{2}:\d{2})\]\s+\[Server thread/INFO\]:\s+(.+?)\s+joined the game')
# Formato: [HH:MM:SS] [Server thread/INFO]: PlayerName left the game
LEAVE_PATTERN = re.compile(r'\[(\d{2}:\d{2}:\d{2})\]\s+\[Server thread/INFO\]:\s+(.+?)\s+left the game')

def send_discord_notification(player_name, event_time, event_type="join"):
    """Envía una notificación a Discord cuando ocurre un evento"""
    print("=" * 50, flush=True)
    print(f"📤 INICIANDO ENVÍO DE WEBHOOK", flush=True)
    print(f"   Jugador: {player_name}", flush=True)
    print(f"   Evento: {event_type}", flush=True)
    print(f"   Hora: {event_time}", flush=True)
    
    if not DISCORD_WEBHOOKS:
        print("❌ ERROR: DISCORD_WEBHOOK_URL no está configurado", flush=True)
        return
    
    print(f"   Webhooks configurados: {len(DISCORD_WEBHOOKS)}", flush=True)
    
    # Configurar el mensaje según el tipo de evento
    if event_type == "join":
        title = "🎮 Jugador conectado"
        description = f"**{player_name}** se ha unido al servidor"
        color = 5763719  # Verde
    else:  # leave
        title = "👋 Jugador desconectado"
        description = f"**{player_name}** se ha retirado del servidor"
        color = 15158332  # Rojo
    
    # Crear el mensaje embebido
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {
            "text": "Smiling Friends server"
        },
        "fields": [
            {
                "name": "⏰ Hora",
                "value": event_time,
                "inline": True
            }
        ]
    }
    
    payload = {
        "embeds": [embed]
    }
    
    # Enviar a todos los webhooks configurados
    success_count = 0
    for i, webhook_url in enumerate(DISCORD_WEBHOOKS, 1):
        webhook_preview = webhook_url[:50] + "..." if len(webhook_url) > 50 else webhook_url
        print(f"   [{i}/{len(DISCORD_WEBHOOKS)}] Enviando a: {webhook_preview}", flush=True)
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code == 204:
                print(f"   [{i}] ✅ Enviado exitosamente", flush=True)
                success_count += 1
            elif response.status_code == 429:
                print(f"   [{i}] ⚠️ Rate limit alcanzado", flush=True)
            else:
                print(f"   [{i}] ❌ Error HTTP {response.status_code}", flush=True)
        except requests.exceptions.Timeout:
            print(f"   [{i}] ❌ Timeout", flush=True)
        except requests.exceptions.ConnectionError:
            print(f"   [{i}] ❌ Error de conexión", flush=True)
        except Exception as e:
            print(f"   [{i}] ❌ Error: {type(e).__name__}", flush=True)
    
    if success_count == len(DISCORD_WEBHOOKS):
        print(f"✅ ¡NOTIFICACIÓN ENVIADA A TODOS LOS WEBHOOKS! ({success_count}/{len(DISCORD_WEBHOOKS)})", flush=True)
    elif success_count > 0:
        print(f"⚠️ Notificación enviada parcialmente ({success_count}/{len(DISCORD_WEBHOOKS)})", flush=True)
    else:
        print(f"❌ No se pudo enviar a ningún webhook", flush=True)
    
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
    if not DISCORD_WEBHOOKS:
        print("   ❌ DISCORD_WEBHOOK_URL: NO CONFIGURADA", flush=True)
        print("   Variables disponibles:", flush=True)
        for key in sorted(os.environ.keys()):
            if 'DISCORD' in key.upper() or 'WEBHOOK' in key.upper():
                print(f"      - {key}", flush=True)
    else:
        print(f"   ✅ Webhooks configurados: {len(DISCORD_WEBHOOKS)}", flush=True)
        for i, webhook in enumerate(DISCORD_WEBHOOKS, 1):
            preview = webhook[:50] + "..." if len(webhook) > 50 else webhook
            print(f"      [{i}] {preview}", flush=True)
    
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
    
    # Leer eventos existentes primero (solo para posicionarnos al final)
    print("📖 Leyendo eventos existentes...", flush=True)
    try:
        with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            join_count = 0
            leave_count = 0
            for line in f:
                if 'joined the game' in line:
                    join_count += 1
                elif 'left the game' in line:
                    leave_count += 1
            last_position = f.tell()
            if join_count > 0 or leave_count > 0:
                print(f"📋 Eventos anteriores: {join_count} conexiones, {leave_count} desconexiones (no se notificarán)", flush=True)
    except:
        last_position = 0
    
    print("✅ Listo! Monitoreando eventos nuevos...", flush=True)
    print(f"   Posición inicial: {last_position} bytes", flush=True)
    print("   Detectando: conexiones y desconexiones", flush=True)
    
    # Contador para debug
    heartbeat_counter = 0
    lines_read = 0
    last_size = log_path.stat().st_size
    
    # Diccionario para rastrear última notificación por jugador (evitar spam)
    last_notification_time = {}
    NOTIFICATION_COOLDOWN = 60  # segundos entre notificaciones del mismo jugador
    
    # Monitorear archivo usando stat() para detectar cambios
    while True:
        try:
            # Obtener tamaño actual del archivo
            current_size = log_path.stat().st_size
            
            # Si el archivo creció, leer las nuevas líneas
            if current_size > last_size:
                print(f"📊 Archivo creció de {last_size} a {current_size} bytes", flush=True)
                
                with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                    # Ir a la última posición conocida
                    f.seek(last_position)
                    
                    # Leer todas las líneas nuevas
                    new_lines = f.readlines()
                    last_position = f.tell()
                    
                    print(f"📥 Leídas {len(new_lines)} líneas nuevas", flush=True)
                    
                    for line in new_lines:
                        lines_read += 1
                        heartbeat_counter = 0
                        
                        # Mostrar la línea
                        print(f"📖 [{lines_read}] {line.strip()}", flush=True)
                        
                        # Buscar conexiones de jugadores
                        if 'joined the game' in line:
                            print(f"🔍 ¡DETECTADA CONEXIÓN!", flush=True)
                            
                            match = JOIN_PATTERN.search(line)
                            if match:
                                event_time = match.group(1)
                                player_name = match.group(2)
                                print(f"✅ MATCH: {player_name} a las {event_time}", flush=True)
                                
                                # Verificar cooldown para evitar spam
                                current_time = time.time()
                                last_notif = last_notification_time.get(f"join_{player_name}", 0)
                                time_since_last = current_time - last_notif
                                
                                if time_since_last >= NOTIFICATION_COOLDOWN:
                                    print(f"🎮 ¡CONEXIÓN DETECTADA! {player_name}", flush=True)
                                    send_discord_notification(player_name, event_time, "join")
                                    last_notification_time[f"join_{player_name}"] = current_time
                                else:
                                    remaining = int(NOTIFICATION_COOLDOWN - time_since_last)
                                    print(f"⏭️ Cooldown activo: {player_name} (esperar {remaining}s)", flush=True)
                            else:
                                print(f"❌ REGEX NO COINCIDE: {line.strip()}", flush=True)
                        
                        # Buscar desconexiones de jugadores
                        elif 'left the game' in line:
                            print(f"🔍 ¡DETECTADA DESCONEXIÓN!", flush=True)
                            
                            match = LEAVE_PATTERN.search(line)
                            if match:
                                event_time = match.group(1)
                                player_name = match.group(2)
                                print(f"✅ MATCH: {player_name} a las {event_time}", flush=True)
                                
                                # Verificar cooldown para evitar spam
                                current_time = time.time()
                                last_notif = last_notification_time.get(f"leave_{player_name}", 0)
                                time_since_last = current_time - last_notif
                                
                                if time_since_last >= NOTIFICATION_COOLDOWN:
                                    print(f"👋 ¡DESCONEXIÓN DETECTADA! {player_name}", flush=True)
                                    send_discord_notification(player_name, event_time, "leave")
                                    last_notification_time[f"leave_{player_name}"] = current_time
                                else:
                                    remaining = int(NOTIFICATION_COOLDOWN - time_since_last)
                                    print(f"⏭️ Cooldown activo: {player_name} (esperar {remaining}s)", flush=True)
                            else:
                                print(f"❌ REGEX NO COINCIDE: {line.strip()}", flush=True)
                
                last_size = current_size
            
            elif current_size < last_size:
                # El archivo fue truncado/rotado
                print("🔄 Archivo truncado, reiniciando...", flush=True)
                last_position = 0
                last_size = current_size
            
            # Incrementar heartbeat
            heartbeat_counter += 1
            
            # Mostrar señal de vida cada 30 segundos
            if heartbeat_counter % 15 == 0:
                print(f"💓 Monitor activo ({heartbeat_counter * CHECK_INTERVAL}s, {lines_read} líneas, {last_size} bytes)", flush=True)
            
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            print(f"❌ Error en loop: {e}", flush=True)
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
