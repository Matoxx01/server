# 🎮 iClub Minecraft Server

![Server Icon](server-icon.png)

Servidor oficial de Minecraft para iClub, ejecutándose en Minecraft 1.21.10 con Java 21.

## 📋 Descripción

Este es un servidor de Minecraft vanilla configurado para ejecutarse en contenedores Docker, ideal para despliegue en plataformas como Railway, Render o cualquier servicio que soporte Docker.

## 🚀 Características

- **Versión**: Minecraft 1.21.10
- **Java**: Eclipse Temurin 21 JRE
- **Modo de juego**: Survival
- **Dificultad**: Easy
- **Máximo de jugadores**: 20
- **Puerto**: 25565
- **MOTD**: iClub official server
- **🔔 Notificaciones Discord**: Alertas automáticas cuando jugadores se unen al servidor

## 🐳 Despliegue con Docker

### Requisitos previos
- Docker instalado en tu sistema
- Al menos 3GB de RAM disponible (configurable)

### Construcción de la imagen

```bash
docker build -t iclub-minecraft-server .
```

### Ejecución del contenedor

```bash
docker run -d -p 25565:25565 --name minecraft-server iclub-minecraft-server
```

### Con volúmenes persistentes

Para guardar el progreso del mundo y las configuraciones:

```bash
docker run -d -p 25565:25565 \
  -v $(pwd)/world:/data/world \
  -v $(pwd)/logs:/data/logs \
  --name minecraft-server \
  iclub-minecraft-server
```

### Con RAM personalizada

Puedes ajustar la RAM usando la variable de entorno `SERVER_RAM`:

```bash
docker run -d -p 25565:25565 \
  -e SERVER_RAM=4G \
  --name minecraft-server \
  iclub-minecraft-server
```

## ⚙️ Configuración

### 🔔 Configurar notificaciones de Discord

El servidor puede enviar notificaciones a Discord cuando un jugador se une:

1. **Crea un webhook en Discord:**
   - Ve a tu servidor de Discord
   - Selecciona el canal donde quieres recibir las notificaciones
   - Click derecho -> Editar canal -> Integraciones -> Webhooks
   - Crear webhook
   - Copia la URL del webhook

2. **Configura la variable de entorno:**

   **En Railway:**
   - Ve a tu proyecto -> Variables
   - Añade: `DISCORD_WEBHOOK_URL` = `tu-webhook-url`

   **En Docker local:**
   ```bash
   docker run -d -p 25565:25565 \
     -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/TU_WEBHOOK" \
     --name minecraft-server \
     iclub-minecraft-server
   ```

3. **Reinicia el servidor** y recibirás notificaciones cuando los jugadores se conecten

### Ajustar memoria RAM

La RAM está configurada mediante la variable de entorno `SERVER_RAM` (por defecto: 3G).

**Opción 1: Al ejecutar el contenedor**
```bash
docker run -d -p 25565:25565 -e SERVER_RAM=4G --name minecraft-server iclub-minecraft-server
```

**Opción 2: En Railway/Render**
Añade una variable de entorno:
- Variable: `SERVER_RAM`
- Valor: `4G` (o `2G`, `8G`, etc.)

**Opción 3: Modificar el DockerFile**
Cambia la línea `ENV SERVER_RAM=3G` por el valor deseado.

### Optimizaciones incluidas

El servidor incluye optimizaciones para mejor rendimiento:
- **G1GC**: Recolector de basura optimizado para Minecraft 1.18+
- **Xms = Xmx**: Evita lag por redimensionamiento de memoria
- **UnlockExperimentalVMOptions**: Activa optimizaciones avanzadas de JVM

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
├── DockerFile              # Configuración de Docker
├── server.jar              # Ejecutable del servidor (versión 1.21.10)
├── server.properties       # Configuración del servidor
├── server-icon.png         # Icono del servidor (64x64)
├── eula.txt               # Aceptación de EULA
├── world/                 # Datos del mundo
├── logs/                  # Registros del servidor
├── libraries/             # Librerías de Minecraft
├── versions/              # Versiones instaladas
├── whitelist.json         # Lista blanca de jugadores
├── ops.json              # Operadores del servidor
├── banned-players.json    # Jugadores baneados
└── banned-ips.json       # IPs baneadas
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

1. Edita `server.properties` y cambia `enforce-whitelist=true`
2. Añade jugadores en `whitelist.json` o con el comando:
```
whitelist add <nombre_de_usuario>
```

## 🌐 Conexión al servidor

1. Abre Minecraft (versión 1.21.10)
2. Ve a Multijugador
3. Añadir servidor
4. Dirección: `tu-dominio.com:25565` o `tu-ip:25565`

## 📝 Notas

- El EULA se acepta automáticamente durante la construcción de la imagen
- Los datos del mundo se guardan en `/data/world` dentro del contenedor
- Se recomienda usar volúmenes para persistencia de datos
- El servidor se ejecuta en modo `nogui` (sin interfaz gráfica)

## 📄 Licencia

Este servidor utiliza el software oficial de Minecraft, sujeto a los [términos de servicio de Minecraft](https://www.minecraft.net/es-es/terms).

---

**Desarrollado para iClub** 🎮✨
