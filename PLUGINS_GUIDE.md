# 🔌 Guía de Configuración de Plugins

Esta guía te ayudará a configurar cada uno de los plugins instalados en el servidor Spigot.

## 📋 Índice

1. [DecentHolograms](#decentholograms---hologramas-3d)
2. [Graves](#graves---sistema-de-tumbas)
3. [GriefPrevention](#griefprevention---protección-de-terrenos)
4. [SkinsRestorer](#skinsrestorer---skins-personalizadas)

---

## DecentHolograms - Hologramas 3D

### 🎯 Propósito
Crear hologramas flotantes con texto, items y animaciones para decorar el servidor.

### 📝 Comandos Básicos

```bash
# Crear hologramas
/holo create <nombre> <línea1> [línea2] [línea3]...
/holo create spawn &6¡Bienvenido!

# Gestión
/holo delete <nombre>           # Eliminar
/holo edit <nombre>             # Editar modo interactivo
/holo list                      # Listar todos
/holo info <nombre>             # Ver información
/holo teleport <nombre>         # Teletransportarse

# Editar líneas
/holo addline <nombre> <texto>       # Añadir línea
/holo setline <nombre> <num> <texto> # Editar línea
/holo removeline <nombre> <num>      # Eliminar línea

# Extras
/holo move <nombre>             # Mover holograma
/holo movehere <nombre>         # Mover a tu posición
```

### 🎨 Códigos de Color

```
&0 - Negro          &8 - Gris oscuro
&1 - Azul oscuro    &9 - Azul
&2 - Verde oscuro   &a - Verde
&3 - Cyan oscuro    &b - Cyan
&4 - Rojo oscuro    &c - Rojo
&5 - Púrpura        &d - Rosa
&6 - Dorado         &e - Amarillo
&7 - Gris           &f - Blanco

&l - Negrita        &o - Cursiva
&n - Subrayado      &m - Tachado
&k - Ofuscado       &r - Reset
```

### 💡 Ejemplos de Uso

```bash
# Spawn principal
/holo create spawn_title &6&l═════════════════
/holo addline spawn_title &e&lSERVIDOR SMILING FRIENDS
/holo addline spawn_title &6&l═════════════════
/holo addline spawn_title &7Versión 1.21.10

# Tienda
/holo create shop &a&l⚡ TIENDA ⚡
/holo addline shop &7Click para comprar

# Zona de PvP
/holo create pvp &c&l⚔ ZONA PVP ⚔
/holo addline pvp &7¡Cuidado! Combate habilitado

# Ranking
/holo create top_player &6&l👑 MEJOR JUGADOR
/holo addline top_player &e%player_name%
/holo addline top_player &7%player_kills% kills
```

### 📁 Archivos de Configuración

**Ubicación:** `/data/plugins/DecentHolograms/config.yml`

```yaml
# Configuración principal
update-interval: 20  # Ticks entre actualizaciones
default-height: 1.0  # Altura por defecto
```

---

## Graves - Sistema de Tumbas

### 🎯 Propósito
Proteger los items de los jugadores al morir, guardándolos en una tumba temporal.

### 📝 Comandos Básicos

```bash
# Jugadores
/graves                    # Ver tus tumbas activas
/graves list               # Lista detallada
/graves teleport <id>      # TP a una tumba
/graves info <id>          # Info de una tumba

# Administradores
/graves admin list         # Ver todas las tumbas
/graves admin teleport <player> <id>
/graves admin delete <id>  # Eliminar tumba
/graves reload            # Recargar config
```

### ⚙️ Configuración Principal

**Ubicación:** `/data/plugins/Graves/config.yml`

```yaml
# Tiempo de protección de tumbas
grave-time: 600  # 10 minutos (en segundos)

# Hologramas sobre tumbas
hologram:
  enabled: true
  height: 1.5
  line1: "&c⚰ Tumba de %player%"
  line2: "&7%time% restante"

# XP guardada
save-xp: true
xp-percentage: 100  # 100% del XP se guarda

# Protección
protected: true
break-protection: true

# Partículas
particles:
  enabled: true
  type: SOUL  # SOUL, FLAME, SMOKE, etc.
```

### 💡 Características

- ⏱️ **Tiempo limitado**: Las tumbas desaparecen después de X minutos
- 🔒 **Protección**: Solo el dueño puede abrir su tumba
- 💎 **XP incluido**: Se guarda la experiencia también
- 🌟 **Holograma**: Muestra dueño y tiempo restante
- 🎨 **Partículas**: Efectos visuales personalizables

---

## GriefPrevention - Protección de Terrenos

### 🎯 Propósito
Proteger construcciones de griefing (robos, destrucción) con sistema de claims.

### 🛠️ Cómo Proteger tu Terreno

1. **Obtén una pala de oro** (Golden Shovel)
2. **Click derecho** en una esquina del área a proteger
3. **Click derecho** en la esquina opuesta (diagonal)
4. ✅ ¡Área protegida!

### 📝 Comandos de Claims

```bash
# Gestión básica
/abandonclaim               # Abandonar claim actual
/abandonallclaims          # Abandonar todos
/claimslist                # Ver tus claims
/trust <jugador>           # Dar acceso total
/untrust <jugador>         # Remover acceso

# Tipos de trust
/trust <jugador>           # Full access (construir/destruir)
/containertrust <jugador>  # Cofres, puertas, animales
/accesstrust <jugador>     # Botones, palancas
/permissiontrust <jugador> # Puede dar permisos a otros

# Subdivisiones
/subdivideclaims           # Activar modo subdivisión
/restrictsubclaim          # Restringir subdivisión

# Admin
/adminclaims               # Crear claim de admin
/deleteclaim               # Eliminar claim (admin)
/deleteallclaims <jugador> # Borrar todos de un jugador
```

### 🎁 Bloques de Claim Gratis

Los jugadores obtienen bloques automáticamente:
- **Inicial**: 100 bloques al unirse
- **Por hora**: +100 bloques por cada hora jugada
- **Máximo**: 80,000 bloques por jugador

```bash
# Ver bloques disponibles
/claimbook  # O mira en el chat al usar la pala
```

### ⚙️ Configuración

**Ubicación:** `/data/plugins/GriefPrevention/config.yml`

```yaml
Claims:
  InitialBlocks: 100          # Bloques iniciales
  BlocksAccruedPerHour: 100   # Bloques por hora
  MaxAccruedBlocks: 80000     # Límite máximo
  MinimumArea: 100            # Área mínima del claim
  MaximumDepth: 0             # Profundidad (0 = bedrock to sky)

Protection:
  ProtectCreatures: true      # Proteger animales
  ProtectHorses: true         # Proteger caballos
  PreventTheft: true          # Prevenir robo de cofres
  ProtectFires: true          # Proteger de fuego
```

### 💡 Tips

- 🏠 **Protege tu casa primero**: Los claims protegen desde bedrock hasta el cielo
- 👥 **Trust solo a conocidos**: Los permisos son permanentes
- 📦 **Cofres automáticos**: Al colocar un cofre, se auto-protege
- 🐴 **Mascotas**: Usa `/givepet <jugador>` para transferir animales domados

---

## SkinsRestorer - Skins Personalizadas

### 🎯 Propósito
Permitir que jugadores en modo offline usen skins premium de Minecraft.

### 📝 Comandos

```bash
# Para jugadores
/skin set <nombre>         # Cambiar a skin de otro jugador
/skin url <url>            # Usar skin desde URL
/skin update               # Actualizar skin actual
/skin clear                # Limpiar/remover skin

# Para administradores
/skin set <jugador> <skin>     # Cambiar skin de otro
/skin clear <jugador>          # Limpiar skin de otro
/sr reload                     # Recargar plugin
```

### 💡 Ejemplos

```bash
# Usar skin de un jugador premium
/skin set Notch
/skin set Dream

# Usar skin desde URL (requiere permisos)
/skin url https://mineskin.org/...

# Resetear al skin original
/skin clear
```

### ⚙️ Configuración

**Ubicación:** `/data/plugins/SkinsRestorer/config.yml`

```yaml
# API de skins
MojangAPI:
  enabled: true
  
# Actualización automática
auto-update:
  enabled: true
  interval: 60  # minutos

# Comandos
disable-commands: []
```

### 🔒 Permisos

```yaml
# permissions.yml
skinsrestorer.command: true           # Comando básico
skinsrestorer.command.set: true       # Cambiar skin
skinsrestorer.command.clear: true     # Limpiar skin
skinsrestorer.command.set.url: false  # Solo admins
```

---

## 🔐 Sistema de Permisos

El servidor usa `permissions.yml` para permisos básicos. Para algo más avanzado, instala **LuckPerms**.

### Grupos Predefinidos

```yaml
groups:
  default:      # Jugadores normales
    - Todos los comandos de plugins básicos
    
  moderator:    # Moderadores
    - Comandos de moderación
    - Admin de Graves
    - Ver todas las tumbas
    
  admin:        # Administradores
    - Acceso total a todos los plugins
    - Bypass de protecciones
```

### Añadir Usuario a Grupo

Edita `/data/permissions.yml`:

```yaml
users:
  TuNombreDeUsuario:
    group:
      - admin
```

---

## 🚀 Recomendaciones Finales

### Plugins Adicionales Sugeridos

1. **EssentialsX** - Comandos esenciales (/home, /warp, /tpa)
2. **LuckPerms** - Sistema de permisos avanzado
3. **Vault** - API de economía (requerido por muchos plugins)
4. **WorldEdit** - Edición de terreno masiva
5. **CoreProtect** - Logging y rollback
6. **Dynmap** - Mapa web en tiempo real

### Optimización

- Limita el número de hologramas (DecentHolograms)
- Configura tiempo de expiración de tumbas (Graves)
- Ajusta los bloques de claim según jugadores (GriefPrevention)
- Usa SkinsRestorer con moderación (consulta APIs de Mojang)

### Seguridad

- ✅ Habilita whitelist si es servidor privado
- ✅ Configura backups automáticos del mundo
- ✅ Usa RCON con contraseña segura
- ✅ Revisa logs regularmente

---

**¿Necesitas ayuda?** Consulta los logs en `/data/logs/latest.log` o la documentación oficial de cada plugin.
