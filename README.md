<div align="left">
  <img src="docs/source/_static/logo.png" alt="KinielaGPT Logo" width="70" align="left" style="margin-right: 20px;"/>
  
  <div>
    <h1>KinielaGPT - Kiniela Game Prediction Tool</h1>
  </div>
  <br clear="left"/>
</div>

<p align="left">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"/></a>
  <a href="https://modelcontextprotocol.io"><img src="https://img.shields.io/badge/MCP-compatible-green.svg" alt="MCP"/></a>
  <a href="https://www.gnu.org/licenses/agpl-3.0"><img src="https://img.shields.io/badge/License-AGPL%20v3-red.svg" alt="License: AGPL v3"/></a>
  <a href="https://ricardomoya.github.io/KinielaGPT/"><img src="https://img.shields.io/badge/docs-sphinx-orange.svg" alt="Documentation"/></a>
</p>

**KinielaGPT** es un servidor MCP (Model Context Protocol) diseñado para potenciar tus predicciones de la Quiniela mediante un análisis avanzado de datos. Combina las probabilidades oficiales de LAE con un análisis contextual profundo: histórico de enfrentamientos, rachas recientes, clasificación y rendimiento como local o visitante. Ofrece tres estrategias de predicción, detección de sorpresas y un análisis pormenorizado partido a partido.

## 🎯 Características

- 🎲 **Predicción de Resultados**: Genera pronósticos mediante tres estrategias: *conservadora* (máxima probabilidad), *arriesgada* (balancea probabilidad y contexto) o *personalizada* (indicando el número de 'unos', 'equis' y 'doses').
- 📊 **Análisis Integral de Partidos**: Integra probabilidades de LAE, histórico de duelos (últimos 10 años), rachas, clasificación y contexto para ofrecer una predicción razonada.
- 🔍 **Detección de Sorpresas**: Detecta discrepancias entre las probabilidades oficiales y el rendimiento real (rachas, histórico, forma) para anticipar posibles sorpresas.
- 👥 **Estado de Forma de Equipos**: Evalúa el rendimiento detallado: últimos marcadores, rachas vigentes, desempeño local/visitante y tendencias clasificatorias.
- 📈 **Consulta Flexible de Datos**: Accede tanto a análisis interpretados como a los datos en bruto para sacar tus propias conclusiones.
- 🔌 **Servidor MCP Nativo**: Incluye 7 herramientas especializadas, totalmente compatibles con Claude Desktop, VS Code y otros clientes MCP.

## 🚀 Instalación

### Opción 1: Usando uv (recomendado)

#### 1. Instalar uv

<details>
<summary>Windows</summary>

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
</details>

<details>
<summary>macOS/Linux</summary>

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
</details>

#### 2. Usar KinielaGPT

Con [`uv`](https://docs.astral.sh/uv/) instalado, no necesitas instalar `kinielagpt`. Usarás [`uvx`](https://docs.astral.sh/uv/guides/tools/) para ejecutarlo directamente (ver sección de [Configuración](#-configuración)).

---

### Opción 2: Usando pip

#### 1. Instalar Python y pip

<details>
<summary>Windows</summary>

1. Descarga Python 3.10+ desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, marca "Add Python to PATH"
3. pip se instala automáticamente con Python
</details>

<details>
<summary>macOS/Linux</summary>

```bash
# macOS (con Homebrew)
brew install python@3.10

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3.10 python3-pip
```
</details>

#### 2. Instalar KinielaGPT

<details>
<summary>Comando de instalación</summary>

```bash
pip install kinielagpt
```
</details>

---

### Instalación desde código fuente (desarrolladores)

<details>
<summary>Instrucciones</summary>

```bash
git clone https://github.com/RicardoMoya/KinielaGPT.git
cd KinielaGPT
pip install -e .
```
</details>

## 🔧 Configuración

### 🤖 Configurar para Claude.app

Añade la siguiente configuración a tu archivo `claude_desktop_config.json`:

<details>
<summary>Usando uvx</summary>

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "kinielagpt": {
      "command": "uvx",
      "args": ["kinielagpt"]
    }
  }
}
```
</details>

<details>
<summary>Usando pip (Windows)</summary>

Ruta: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "kinielagpt": {
      "command": "python",
      "args": ["-m", "kinielagpt"]
    }
  }
}
```
</details>

<details>
<summary>Usando pip (macOS/Linux)</summary>

Ruta: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "kinielagpt": {
      "command": "python3",
      "args": ["-m", "kinielagpt"]
    }
  }
}
```
</details>

### 💻 Configurar para VS Code

Para una instalación rápida, usa el botón de instalación con un clic:

[![Instalar con Python en VS Code](https://img.shields.io/badge/VS_Code-Python-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=kinielagpt&config=%7B%22command%22%3A%22python%22%2C%22args%22%3A%5B%22-m%22%2C%22kinielagpt%22%5D%7D)

Para instalación manual, puedes configurar el servidor MCP usando uno de estos métodos:

**Método 1: Configuración de Usuario (Recomendado)**  
Añade la configuración a tu archivo de configuración MCP a nivel de usuario. Abre la Paleta de Comandos (`Ctrl + Shift + P`) y ejecuta `MCP: Open User Configuration`. Esto abrirá tu archivo `mcp.json` de usuario donde puedes añadir la configuración del servidor.

**Método 2: Configuración de Workspace**  
Alternativamente, puedes añadir la configuración a un archivo llamado `.vscode/mcp.json` en tu workspace. Esto te permitirá compartir la configuración con otros.

> Para más detalles sobre la configuración de MCP en VS Code, consulta la [documentación oficial de VS Code MCP](https://code.visualstudio.com/docs/copilot/customization/mcp-servers).

<details>
<summary>Usando uvx</summary>

```json
{
  "servers": {
    "kinielagpt": {
      "command": "uvx",
      "args": ["kinielagpt"]
    }
  }
}
```
</details>

<details>
<summary>Usando pip</summary>

```json
{
  "servers": {
    "kinielagpt": {
      "command": "python",
      "args": ["-m", "kinielagpt"]
    }
  }
}
```
</details>

## 📚 Documentación

La documentación completa está disponible en: **https://ricardomoya.github.io/KinielaGPT/**

Incluye:
- TODO

## 📖 Uso

### ¿Cómo interactuar con un LLM?

Una vez configurado el MCP, puedes interactuar con un LLM usando comandos naturales como los siguientes:

**Consultas de información:**
- "¿Cuál es la última quiniela disponible?"
- "Muéstrame los partidos de la jornada 26 de la temporada 2025/2026"
- "¿Qué probabilidades tiene cada partido de la jornada actual?"

**Predicciones de quiniela:**
- "Dame una predicción conservadora para la jornada 26"
- "Quiero una predicción arriesgada para la próxima jornada"
- "Genera una quiniela personalizada con 7 unos, 4 equis y 4 doses"

**Análisis de partidos:**
- "Analiza el partido del Real Madrid de la jornada 26"
- "¿Qué pasará en el partido Villarreal - Getafe?"
- "Muéstrame el histórico de enfrentamientos del partido Alavés - Real Sociedad"

**Detección de sorpresas:**
- "¿Hay algún partido donde pueda haber sorpresa en la jornada 26?"
- "Detecta sorpresas con un umbral más sensible (threshold=20)"

**Análisis de equipos:**
- "¿Cómo está jugando el Rayo Vallecano últimamente?"
- "Analiza el rendimiento del Barcelona en la jornada 26"
- "¿Qué racha tiene el Atletico de Madrid actualmente?"

### Herramientas Disponibles

**Total: 7 herramientas MCP disponibles**

<details>
<summary>1. <code>get_last_quiniela</code></summary>

**Descripción:** Obtiene la información de la última quiniela disponible.  
**Devuelve:** Jornada, temporada y lista de partidos de la quiniela más reciente
</details>

<details>
<summary>2. <code>get_quiniela</code></summary>

**Descripción:** Obtiene la información de una jornada específica de quiniela.  
**Parámetros:**
- `jornada` (int): Número de jornada (mínimo: 1)
- `temporada` (int): Año de la temporada (mínimo: 2026)

**Devuelve:** Información completa con todos los partidos programados de la jornada
</details>

<details>
<summary>3. <code>get_probabilities</code></summary>

**Descripción:** Obtiene las probabilidades basadas en LAE para cada partido de una jornada.  
**Parámetros:**
- `jornada` (int): Número de jornada (mínimo: 1)
- `temporada` (int): Año de la temporada (mínimo: 2026)

**Devuelve:** Probabilidades de 1, X, 2 y pronósticos de goles para todos los partidos
</details>

<details>
<summary>4. <code>predict_quiniela</code></summary>

**Descripción:** Genera una predicción completa de quiniela con diferentes estrategias.  
**Parámetros:**
- `jornada` (int): Número de jornada (mínimo: 1)
- `temporada` (int): Año de la temporada (mínimo: 2000)
- `strategy` (string): Estrategia de predicción
  - `"conservadora"`: Máxima probabilidad
  - `"arriesgada"`: Balancea probabilidad y contexto
  - `"personalizada"`: Distribución personalizada de 1-X-2
- `custom_distribution` (object, opcional): Solo para estrategia personalizada
  - Ejemplo: `{"1": 7, "X": 4, "2": 4}`

**Devuelve:** Predicción completa de los 15 partidos según la estrategia elegida
</details>

<details>
<summary>5. <code>detect_surprises</code></summary>

**Descripción:** Identifica partidos con inconsistencias significativas entre probabilidades basadas en LAE y análisis contextual.  
**Parámetros:**
- `jornada` (int): Número de jornada (mínimo: 1)
- `temporada` (int): Año de la temporada (mínimo: 2026)
- `threshold` (float, opcional): Umbral de divergencia (0-100, default: 30)

**Devuelve:** Lista de partidos con alertas de posibles sorpresas, clasificadas por nivel de gravedad (🚨 ALERTA ROJA, ⚠️ ALERTA MEDIA, ⚠️ ALERTA)
</details>

<details>
<summary>6. <code>analyze_match</code></summary>

**Descripción:** Analiza un partido específico con dos modos de operación.  
**Parámetros:**
- `jornada` (int): Número de jornada (mínimo: 1)
- `temporada` (int): Año de la temporada (mínimo: 2026)
- `match_id` (int): ID del partido (1-15)
- `include_prediction` (bool, opcional, default: true):
  - `true`: Análisis completo con predicción justificada
  - `false`: Solo datos en crudo sin predicción

**Devuelve:**
- **Con predicción:** Predicción, nivel de confianza (ALTA/MEDIA/BAJA), justificación detallada, probabilidades, histórico, rachas, clasificación
- **Sin predicción:** Datos en crudo como histórico de enfrentamientos, evolución reciente, clasificaciones, comparativa de últimos partidos, datos destacados
</details>

<details>
<summary>7. <code>analyze_team</code></summary>

**Descripción:** Analiza el rendimiento completo de un equipo específico.  
**Parámetros:**
- `jornada` (int): Número de jornada (mínimo: 1)
- `temporada` (int): Año de la temporada (mínimo: 2000)
- `team_name` (string): Nombre del equipo (debe coincidir con el nombre en los datos)

**Devuelve:** Análisis completo con últimos resultados, rachas actuales, rendimiento como local/visitante, clasificación y tendencia (Excelente/Buena/Irregular/Mala)
</details>



## 🧪 Testing

TODO

El proyecto incluye una suite completa de tests organizados por módulo:

```bash
# Ejecutar todos los tests
# TODO
```

**Cobertura**: TODO

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📏 Licencia

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Este proyecto está licenciado bajo [GNU Affero General Public License v3.0 (AGPL-3.0)](https://www.gnu.org/licenses/agpl-3.0).

**Esto significa que puedes:**
- ✅ Usar el código libremente (incluso comercialmente)
- ✅ Modificar y adaptar el proyecto
- ✅ Distribuir copias y versiones modificadas

**Bajo las siguientes condiciones:**
- 📝 **Copyleft**: Cualquier modificación debe ser AGPL-3.0 también
- 🌐 **Uso en red**: Si usas este código en un servidor/servicio, **debes compartir el código fuente**
- 📦 **Código abierto**: Toda versión modificada debe distribuirse con código fuente
- ©️ **Atribución**: Debes mantener los avisos de copyright

**Protección especial**: La AGPL-3.0 cierra la "laguna del servidor" – incluso si ejecutas este código como servicio web sin distribuir binarios, debes ofrecer el código fuente a tus usuarios.

Ver el archivo [LICENSE](LICENSE) para el texto legal completo.

## ⚠️ Disclaimer

Este proyecto es únicamente para fines de entretenimiento. Las predicciones no garantizan resultados y no deben usarse como única base para decisiones de apuestas. Juega responsablemente.


## 👨‍💻 Autor

**Ricardo Moya**
- 🐙 GitHub: [@RicardoMoya](https://github.com/RicardoMoya)
- 💼 LinkedIn: [Ricardo Moya, PhD](https://www.linkedin.com/in/phdricardomoya/)

## 📧 Contacto

Para preguntas, sugerencias o reportar issues:
- 📝 [GitHub Issues](https://github.com/RicardoMoya/KinielaGPT/issues)
- 💬 [GitHub Discussions](https://github.com/RicardoMoya/KinielaGPT/discussions)

---

Hecho con ❤️ por Ricardo Moya para los aficionados a la quiniela española
