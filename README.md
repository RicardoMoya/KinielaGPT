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

### 🎲 Predicción de Resultados
Genera pronósticos mediante tres estrategias: *conservadora* (máxima probabilidad), *arriesgada* (balancea probabilidad y contexto) o *personalizada* (indicando el número de 'unos', 'equis' y 'doses').

### 📊 Análisis Integral de Partidos
Integra probabilidades de LAE, histórico de duelos (últimos 10 años), rachas, clasificación y contexto para ofrecer una predicción razonada.

### 🔍 Detección de Sorpresas
Detecta discrepancias entre las probabilidades oficiales y el rendimiento real (rachas, histórico, forma) para anticipar posibles sorpresas.

### 👥 Estado de Forma de Equipos
Evalúa el rendimiento detallado: últimos marcadores, rachas vigentes, desempeño local/visitante y tendencias clasificatorias.

### 📈 Consulta Flexible de Datos
Accede tanto a análisis interpretados como a los datos en bruto para sacar tus propias conclusiones.

### 🔌 Servidor MCP Nativo
Incluye 7 herramientas especializadas, totalmente compatibles con Claude Desktop, VS Code y otros clientes MCP.


---


## 🏁 Pasos para empezar a usar KinielaGPT

Sigue estos pasos para tener KinielaGPT listo y funcionando en tu equipo:

1. [Instala UV o Python 3.10+](#antes_de_empezar) en tu PC.
2. [Instala](#instalacion) KinielaGPT.
3. [Configura](#configuracion) el servidor MCP, eligiendo Claude o VS Code como cliente.

Una vez completados estos pasos, ¡ya puedes empezar a hacer predicciones y análisis con KinielaGPT!


---

<a name="antes_de_empezar"></a>

## ✅ Instalar UV o Python 3.10+

Antes de usar `KinielaGPT` necesitaras tener instalado **UV** (recomendado) o **Python 3.10+**.

A continuación se muestran como instalar las dos opciones, aunque *debes elegir una de las dos*:

### Opción 1: UV (Recomendado) ⚡

[UV](https://docs.astral.sh/uv/) es un gestor de paquetes y proyectos Python ultrarrápido que simplifica la instalación y ejecución de herramientas Python. **No requiere tener Python pre-instalado**.

<details>
<summary><b>🪟 UV en Windows</b></summary>

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verificar:
```powershell
uv --version
```
</details>

<details>
<summary><b>🍎🐧 UV en macOS/Linux</b></summary>

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verificar:
```bash
uv --version
```

> [!IMPORTANT]
> Reinicia tu terminal después de la instalación.
</details>


### Opción 2: Python 3.10+ y pip

Si ya tienes Python instalado y prefieres el método tradicional, puedes usar pip (el gestor de paquetes de Python). Requiere tener Python 3.10 o superior ya instalado en tu sistema.

<details>
<summary><b>🪟 Python en Windows</b></summary>

1. Descarga Python 3.10+ desde [python.org/downloads](https://www.python.org/downloads/)
2. **Marca "Add Python to PATH"** durante la instalación
3. Verifica:
```powershell
python --version
pip --version
```
</details>

<details>
<summary><b>🍎 Python en macOS</b></summary>

**macOS:**
1. Ve a [python.org/downloads](https://www.python.org/downloads/)
2. Descarga Python 3.10+ para macOS
3. Ejecuta el instalador . pkg

Verifica:
```bash
python3 --version
pip3 --version
```
</details>

<details>
<summary><b>🐧 Python en Linux (Ubuntu/Debian)</b></summary>

```bash
sudo apt update
sudo apt install python3.10 python3-pip python3.10-venv
```

Verifica:
```bash
python3 --version
pip3 --version
```
</details>


<a name="instalacion"></a>

## 🚀 Instalación

### Opción 1: Usando UV (recomendado)

Con UV instalado, **no necesitas instalar** KinielaGPT. Usarás `uvx` para ejecutarlo directamente - ver [Configuración](#configuracion).


### Opción 2: Usando pip

Instala KinielaGPT desde PyPI:

```bash
pip install kinielagpt
```


<a name="configuracion"></a>

## 🔧 Configuración

### 🤖 Configurar para Claude.app

Edita el archivo de configuración `claude_desktop_config.json` que según tu sistema operativo se encuentra en:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Añade una de las siguientes configuraciones según tu método de instalación:

<details>
<summary><b>Usando uvx</b></summary>

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
<summary><b>Usando pip</b></summary>

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

> [!NOTE]
> En macOS/Linux, si `python` no funciona, usa `python3` en su lugar.
</details>


### 💻 Configurar para VS Code

**Instalación rápida (un clic):**

Haz clic en el siguiente botón para instalar automáticamente el servidor MCP en VS Code:

[![Instalar con Python en VS Code](https://img.shields.io/badge/VS_Code-Python-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=kinielagpt&config=%7B%22command%22%3A%22python%22%2C%22args%22%3A%5B%22-m%22%2C%22kinielagpt%22%5D%7D)

**Instalación manual:**

Abre la Paleta de Comandos (`Ctrl + Shift + P`), ejecuta `MCP: Open User Configuration` y añade una de las siguientes configuraciones:

<details>
<summary><b>Usando uvx</b></summary>

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
<summary><b>Usando pip</b></summary>

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

> [!NOTE]
> En macOS/Linux, si `python` no funciona, usa `python3` en su lugar.
</details>

<br>

> [!TIP]
> Como alternativa puedes crear el archivo `.vscode/mcp.json` en tu workspace para compartir la configuración con otros. Más detalles en la [documentación oficial de VS Code MCP](https://code.visualstudio.com/docs/copilot/customization/mcp-servers).

---

## 📖 ¿Cómo usar KinielaGPT?

Una vez configurado el MCP, puedes interactuar con tu LLM (Claude, GPT, Gemini, etc.) en lenguaje natural. Simplemente hazle preguntas como las siguientes:

| Categoría | Ejemplos de Preguntas |
|-----------|----------------------|
| **Consultas de información** | 🔹 "¿Cuál es la última quiniela disponible?"<br>🔹 "Muéstrame los partidos de la jornada 26 de la temporada 2025/2026"<br>🔹 "¿Qué probabilidades tiene cada partido de la jornada actual?" |
| **Predicciones de quiniela** | 🔹 "Dame una predicción conservadora para la jornada 26"<br>🔹 "Quiero una predicción arriesgada para la próxima jornada"<br>🔹 "Genera una quiniela personalizada con 7 unos, 4 equis y 4 doses" |
| **Análisis de partidos** | 🔹 "Analiza el partido del Real Madrid de la jornada 26"<br>🔹 "¿Qué pasará en el partido Villarreal - Getafe?"<br>🔹 "Muéstrame el histórico de enfrentamientos del partido Alavés - Real Sociedad" |
| **Detección de sorpresas** | 🔹 "¿Hay algún partido donde pueda haber sorpresa en la jornada 26?"<br>🔹 "Detecta sorpresas con un umbral más sensible (threshold=20)" |
| **Análisis de equipos** | 🔹 "¿Cómo está jugando el Rayo Vallecano últimamente?"<br>🔹 "Analiza el rendimiento del Barcelona en la jornada 26"<br>🔹 "¿Qué racha tiene el Atletico de Madrid actualmente?" |

---

### Herramientas Disponibles

| Herramienta | Descripción | Parámetros Principales | Devuelve |
|-------------|-------------|----------------------|----------|
| `get_last_quiniela` | Obtiene la última quiniela disponible | - | Jornada, temporada y partidos |
| `get_quiniela` | Información de jornada específica | `jornada`, `temporada` | Partidos programados |
| `get_probabilities` | Probabilidades basadas en LAE de una jornada | `jornada`, `temporada` | Probabilidades 1/X/2 y goles |
| `predict_quiniela` | Predicción completa con estrategias: conservadora, arriesgada, personalizada | `jornada`, `temporada`, `strategy` | Quiniela de 15 partidos |
| `detect_surprises` | Detecta inconsistencias en partidos | `jornada`, `temporada`, `threshold` | Lista de partidos con alertas de sorpresas potenciales |
| `analyze_match` | Análisis detallado de un partido | `jornada`, `temporada`, `partido` | Predicción y datos contextuales |
| `analyze_team` | Rendimiento completo de un equipo | `jornada`, `temporada`, `equipo` | Análisis con rachas y tendencias |

**Total: 7 herramientas MCP disponibles**

Para detalles completos de parámetros y ejemplos, consulta la [documentación completa](https://ricardomoya.github.io/KinielaGPT/).


---

## 📚 Documentación

La documentación completa está disponible en: **https://ricardomoya.github.io/KinielaGPT/**

Incluye:
- **Guía de inicio rápido:** Instalación, configuración y primeros pasos para usar KinielaGPT en tu entorno.
- **Manual de instalación:** Instrucciones detalladas para instalar con UV o pip, y requisitos previos.
- **Configuración avanzada:** Cómo conectar KinielaGPT con Claude Desktop, VS Code y otros clientes MCP.
- **Uso y ejemplos:** Preguntas frecuentes, ejemplos de comandos y flujos de trabajo recomendados.
- **Referencia de API:** Explicación de todas las herramientas MCP disponibles, parámetros y ejemplos de uso.
- **Contribución:** Guía para contribuir al proyecto, abrir issues y enviar pull requests.
- **Licencia y créditos:** Información legal y reconocimiento a los autores y colaboradores.

---

## 🧪 Testing

El proyecto incluye una suite completa de tests automatizados que cubren todas las funcionalidades principales. Los tests están organizados por módulo y utilizan pytest para la ejecución.

### Tests Disponibles

| Archivo de Test | Número de Tests | Descripción |
|-----------------|-----------------|-------------|
| `test_data_source.py` | 4 | Tests para la obtención y procesamiento de datos de quiniela desde APIs externas |
| `test_predictor.py` | 9 | Tests para las estrategias de predicción (conservadora, arriesgada, personalizada) |
| `test_detector.py` | 30 | Tests para la detección de sorpresas e inconsistencias en partidos |
| `test_analyzer.py` | 12 | Tests para el análisis de partidos y rendimiento de equipos |

### Ejecutar Tests Localmente

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ -v --cov=kinielagpt --cov-report=term-missing

# Ejecutar un módulo específico
pytest tests/test_predictor.py -v

# Ejecutar tests en paralelo (si tienes pytest-xdist)
pytest tests/ -v -n auto
```

### Cobertura de Código

Los tests proporcionan cobertura completa del código principal. La cobertura actual por módulo es:

| Módulo | Cobertura | Descripción |
|--------|-----------|-------------|
| `data_source` | 67% | Funciones de obtención y parsing de datos de quiniela |
| `predictor` | 84% | Algoritmos de predicción y estrategias (conservadora, arriesgada, personalizada) |
| `detector` | 88% | Lógica de detección de sorpresas e inconsistencias |
| `analyzer` | 48% | Análisis de partidos y rendimiento de equipos |

### CI/CD

Los tests se ejecutan automáticamente en GitHub Actions:

- **En cada push/PR** a las ramas `main` y `develop`
- **Programados**: Todos los jueves a las 9:00 AM (hora UTC)
- **Matrices de testing**: Python 3.10, 3.11, 3.12, 3.13 en Ubuntu
- **Notificaciones**: Email automático con resultados cuando se ejecuta programadamente

Para ver los resultados de CI, visita la pestaña [Actions](https://github.com/RicardoMoya/KinielaGPT/actions) del repositorio.

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

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


>[!IMPORTANT]
>Este proyecto es únicamente para fines de entretenimiento. Las predicciones no garantizan resultados y no deben usarse como única base para decisiones de apuestas. Juega responsablemente.


## 👨‍💻 Autor - Ricardo Moya

<p align="left">
  <img src="https://github.com/RicardoMoya.png" alt="Ricardo Moya GitHub avatar" width="120" style="border-radius: 50%;" />
</p>
<p align="left">
  🐙 GitHub: <a href="https://github.com/RicardoMoya">@RicardoMoya</a><br>
  💼 LinkedIn: <a href="https://www.linkedin.com/in/phdricardomoya/">Ricardo Moya, PhD</a>
</p>

## 📧 Contacto

Para preguntas, sugerencias o reportar issues:
- 📝 [GitHub Issues](https://github.com/RicardoMoya/KinielaGPT/issues)
- 💬 [GitHub Discussions](https://github.com/RicardoMoya/KinielaGPT/discussions)

---

⚽ Proyecto creado por Ricardo Moya para que cada quiniela se juegue con cabeza, estrategia y datos.
