# 🎮 Smiling Friends Minecraft Server

![Server Icon](server-icon.png)

Servidor oficial de Minecraft para Smiling Friends, ejecutándose en **Spigot 1.21.10** con Java 21.

## 📋 Descripción

Este es un servidor de Minecraft basado en **Spigot** con soporte completo para plugins, configurado para ejecutarse en contenedores Docker. Ideal para despliegue en plataformas como Railway, Render o cualquier servicio que soporte Docker.

## 🚀 Características

- **Versión**: Minecraft 1.21.10 (Spigot)
- **Java**: Eclipse Temurin 21 JRE
- **Modo de juego**: Survival
- **Dificultad**: Hard
- **Máximo de jugadores**: 50
- **Puerto**: 25565
- **MOTD**: Smiling Friends server
- **🔔 Notificaciones Discord**: Alertas automáticas cuando jugadores se conectan/desconectan

### 🔌 Plugins Instalados

1. **DecentHolograms 2.9.8** - Sistema de hologramas 3D personalizables
   - Crea hologramas flotantes con texto, items y animaciones
   - Ideal para spawn, tiendas, letreros informativos
   
2. **Graves 4.9** - Sistema de tumbas al morir
   - Protege tus items al morir en una tumba
   - Evita pérdida de items por despawn
   - Teletransporte a tu última muerte
   
3. **GriefPrevention** - Protección de terrenos anti-griefing
   - Protege construcciones de otros jugadores
   - Sistema de claims con pala de oro
   - Previene robos y destrucción de builds
   
4. **SkinsRestorer** - Restaurador de skins personalizadas
   - Usa skins premium en modo offline
   - Sincronización con Mojang API

## 🐳 Despliegue con Docker

### Requisitos previos
- Docker instalado en tu sistema
- Al menos 3GB de RAM disponible (configurable)

### Construcción de la imagen

```bash
docker build -t smiling-friends-spigot .
```

### Ejecución del contenedor

```bash
docker run -d -p 25565:25565 --name minecraft-server smiling-friends-spigot
```

### Con volúmenes persistentes

Para guardar el progreso del mundo, plugins y configuraciones:

```bash
docker run -d -p 25565:25565 \
  -v $(pwd)/world:/data/world \
  -v $(pwd)/plugins:/data/plugins \
  -v $(pwd)/logs:/data/logs \
  --name minecraft-server \
  smiling-friends-spigot
```

### Con Docker Compose (Recomendado)

```bash
docker-compose up -d
```

Esto iniciará el servidor con todas las configuraciones predeterminadas.

## ⚙️ Configuración

### 🔔 Configurar notificaciones de Discord

El servidor envía notificaciones a Discord cuando jugadores se conectan/desconectan:

1. **Crea un webhook en Discord:**
   - Ve a tu servidor de Discord
   - Selecciona el canal donde quieres recibir las notificaciones
   - Click derecho → Editar canal → Integraciones → Webhooks
   - Crear webhook
   - Copia la URL del webhook

2. **Configura la variable de entorno:**

   **En Railway:**
   - Ve a tu proyecto → Variables
   - Añade: `DISCORD_WEBHOOK_URL` = `tu-webhook-url`

   **En Docker local:**
   ```bash
   docker run -d -p 25565:25565 \
     -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/TU_WEBHOOK" \
     --name minecraft-server \
     smiling-friends-spigot
   ```

3. **Reinicia el servidor** y recibirás notificaciones de eventos de jugadores

### Memoria RAM y optimizaciones

El servidor está configurado con:
- **RAM**: 8GB máxima, 1GB mínima (configurable en `start.sh`)
- **Aikar's Flags**: Optimizaciones G1GC avanzadas para Spigot/Paper
- **Performance tuning**: `spigot.yml` optimizado para mejor rendimiento

**Para ajustar la RAM**, edita las líneas en `start.sh`:
```bash
java -Xmx8G -Xms1G ...  # Cambia 8G y 1G según necesites
```

### Optimizaciones incluidas

El servidor incluye optimizaciones de rendimiento avanzadas:
- **Aikar's Flags**: Configuración óptima de JVM para Minecraft
- **G1GC**: Recolector de basura con bajo pause time
- **Spigot tuning**: Entity tracking, mob spawn y tick optimizados
- **Parallel processing**: Mejoras de multi-threading
- **RCON**: Control remoto del servidor habilitado

### Modificar propiedades del servidor

Edita el archivo `server.properties` para cambiar:
- Modo de juego
- Dificultad
- Número máximo de jugadores
- Whitelist
- Y más...

## 📁 Estructura del proyecto

```
.
├── Dockerfile                # Configuración de Docker
├── docker-compose.yml        # Orquestación con Docker Compose
├── start.sh                  # Script de inicio optimizado para Spigot
├── discord_monitor.py        # Monitor de eventos para Discord
├── requirements.txt          # Dependencias Python
├── server.jar                # Ejecutable de Spigot 1.21.10
├── server.properties         # Configuración principal del servidor
├── spigot.yml               # Configuración específica de Spigot
├── bukkit.yml               # Configuración de Bukkit API
├── commands.yml             # Comandos personalizados
├── permissions.yml          # Sistema de permisos básico
├── server-icon.png          # Icono del servidor (64x64)
├── eula.txt                 # Aceptación de EULA
├── ops.json                 # Operadores del servidor
├── whitelist.json           # Lista blanca de jugadores
├── banned-players.json      # Jugadores baneados
├── banned-ips.json          # IPs baneadas
├── plugins/                 # Plugins de Spigot
│   ├── DecentHolograms-2.9.8.jar
│   ├── Graves-4.9.jar
│   ├── GriefPrevention.jar
│   └── SkinsRestorer.jar
├── world/                   # Datos del mundo principal
├── logs/                    # Registros del servidor
├── libraries/               # Librerías de Minecraft
└── versions/                # Versiones instaladas
```

## 🔧 Comandos útiles

### Ver logs del servidor
```bash
docker logs -f minecraft-server
```

### Detener el servidor
```bash
docker stop minecraft-server
```

### Reiniciar el servidor
```bash
docker restart minecraft-server
```

### Eliminar el contenedor
```bash
docker rm -f minecraft-server
```

## 👥 Administración

### Añadir operadores

Edita el archivo `ops.json` o ejecuta en la consola del servidor:
```
op <nombre_de_usuario>
```

### Activar whitelist

1. Edita `server.properties` y cambia `white-list=true`
2. Añade jugadores en `whitelist.json` o con el comando:
```
whitelist add <nombre_de_usuario>
```

### Control RCON

El servidor tiene RCON habilitado en el puerto 25575:

```bash
# Instalar mcrcon (Linux/Mac)
brew install mcrcon  # o compílalo desde GitHub

# Conectar
mcrcon -H localhost -P 25575 -p railway_rcon_2024

# Enviar comando
mcrcon -H localhost -P 25575 -p railway_rcon_2024 "say Hola desde RCON"
```

## 🔌 Guía de Plugins

### DecentHolograms - Hologramas 3D

**Comandos principales:**
```
/holo create <nombre> <texto>    - Crear holograma
/holo delete <nombre>            - Eliminar holograma
/holo edit <nombre>              - Editar holograma
/holo list                       - Listar todos los hologramas
/holo teleport <nombre>          - Teletransportarse a un holograma
```

**Ejemplo:**
```
/holo create spawn &6¡Bienvenido al servidor!
/holo addline spawn &aDisfruta tu estadía
```

### Graves - Sistema de Tumbas

**Comandos principales:**
```
/graves                   - Ver tus tumbas
/graves list              - Listar todas tus tumbas
/graves teleport <id>     - Teletransportarse a una tumba
/graves admin             - Comandos de administrador
```

**Características:**
- Al morir, tus items se guardan en una tumba
- Tiempo de protección: configurable
- Hologramas muestran contenido y tiempo restante

### GriefPrevention - Protección de Terrenos

**Comandos principales:**
```
/abandonclaim                    - Abandonar el claim actual
/abandonallclaims               - Abandonar todos tus claims
/trust <jugador>                - Dar acceso total
/containertrust <jugador>       - Acceso a cofres/puertas
/accesstrust <jugador>          - Acceso a botones/palancas
/untrust <jugador>              - Remover permisos
/claimslist                     - Ver todos tus claims
/givepet <jugador>              - Transferir mascota
```

**Cómo proteger:**
1. Usa una **pala de oro** (golden shovel)
2. Click derecho en una esquina del área
3. Click derecho en la esquina opuesta
4. ¡Protegido! Otros no pueden construir/destruir

### SkinsRestorer - Skins Personalizadas

**Comandos principales:**
```
/skin set <nombre>       - Cambiar tu skin
/skin clear              - Limpiar tu skin
/skin update             - Actualizar skin
```

## 🔧 Añadir Nuevos Plugins

1. **Descarga** el plugin desde SpigotMC, Bukkit o el sitio oficial
2. **Coloca** el archivo `.jar` en la carpeta `plugins/`
3. **Rebuild** la imagen Docker:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```
4. **Verifica** que se cargó correctamente en los logs:
   ```bash
   docker logs -f minecraft-server
   ```

### Plugins Recomendados Adicionales

- **EssentialsX** - Comandos útiles (/home, /warp, /tpa)
- **Vault** - API de economía y permisos
- **LuckPerms** - Sistema de permisos avanzado
- **WorldEdit** - Edición de terreno masiva
- **CoreProtect** - Logs y rollback de cambios
- **Dynmap** - Mapa web en tiempo real

## 🌐 Conexión al servidor

1. Abre Minecraft (versión 1.21.10)
2. Ve a Multijugador
3. Añadir servidor
4. Dirección: `tu-dominio.com:25565` o `tu-ip:25565`

## 🔍 Troubleshooting

### El servidor no inicia
- Verifica que el puerto 25565 no esté en uso
- Revisa los logs: `docker logs -f minecraft-server`
- Asegúrate de tener al menos 2GB RAM libre

### Plugins no cargan
- Verifica compatibilidad con Spigot 1.21.10
- Revisa `/data/logs/latest.log` para errores
- Algunos plugins requieren dependencias (Vault, ProtocolLib)

### Lag o bajo rendimiento
- Ajusta la RAM en `start.sh` (aumenta `-Xmx`)
- Reduce `view-distance` en `server.properties`
- Optimiza `spigot.yml` (reduce `mob-spawn-range`)
- Considera usar Paper en lugar de Spigot (más optimizado)

### Discord webhook no funciona
- Verifica que la URL del webhook sea correcta
- Comprueba la variable `DISCORD_WEBHOOK_URL` en Railway
- Revisa los logs del monitor: busca "Monitor de Discord"

## 🆚 Spigot vs Vanilla vs Paper

| Característica | Vanilla | Spigot | Paper |
|---------------|---------|--------|-------|
| Plugins | ❌ | ✅ | ✅ |
| Rendimiento | Base | +30% | +50% |
| Configuración | Básica | Avanzada | Muy avanzada |
| Compatibilidad | 100% | 99% | 98% |
| Anti-lag | ❌ | ✅ | ✅✅ |

**Spigot** es perfecto para servidores con plugins sin comprometer demasiado la compatibilidad vanilla.

## 📝 Notas

- El EULA se acepta automáticamente en `start.sh`
- Los datos se persisten en volúmenes Docker
- Configuraciones de plugins se guardan en `/data/plugins/<NombrePlugin>/`
- El servidor usa **Aikar's Flags** para máximo rendimiento
- RCON habilitado para control remoto (puerto 25575)
- Monitor de Discord detecta conexiones/desconexiones en tiempo real

## 📚 Recursos Útiles

- [SpigotMC](https://www.spigotmc.org/) - Descargar plugins
- [Bukkit Wiki](https://bukkit.fandom.com/wiki/Main_Page) - Documentación
- [Aikar's Flags](https://docs.papermc.io/paper/aikars-flags) - Optimización JVM
- [MCVersions](https://mcversions.net/) - Descargar versiones de Minecraft

## 📄 Licencia

Este servidor utiliza:
- **Spigot** - GPL v3 License
- **Minecraft** - [Términos de servicio de Minecraft](https://www.minecraft.net/es-es/terms)
- Plugins individuales tienen sus propias licencias

---

**Desarrollado para Smiling Friends** 🎮😊
