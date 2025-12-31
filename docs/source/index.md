# Kiniela Game Prediction Tool

<p align="left">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"/></a>
  <a href="https://pypi.org/project/kinielagpt/"><img src="https://img.shields.io/pypi/v/kinielagpt.svg?color=purple" alt="PyPI version"/></a>
  <a href="https://modelcontextprotocol.io"><img src="https://img.shields.io/badge/MCP-compatible-green.svg" alt="MCP"/></a>
  <a href="https://www.gnu.org/licenses/agpl-3.0"><img src="https://img.shields.io/badge/License-AGPL%20v3-red.svg" alt="License: AGPL v3"/></a>
  <a href="https://ricardomoya.github.io/KinielaGPT/"><img src="https://img.shields.io/badge/docs-sphinx-orange.svg" alt="Documentation"/></a>
</p>

<div class="hero-section">
  <p class="hero-description">
    <strong>KinielaGPT</strong> es un servidor MCP (Model Context Protocol) diseñado para potenciar tus predicciones de la Quiniela mediante un análisis avanzado de datos. Combina las probabilidades oficiales de LAE con un análisis contextual profundo: histórico de enfrentamientos, rachas recientes, clasificación y rendimiento como local o visitante. Ofrece tres estrategias de predicción, detección de sorpresas y un análisis pormenorizado partido a partido.
  </p>
</div>

## 🎯 Características Principales

<ul class="features-list">
  <li>
    <div class="feature-content">
      <div class="feature-header">
        <strong>🎲 Predicción de Resultados</strong>
      </div>
      <div class="feature-description">
        <p>Genera pronósticos mediante tres estrategias: conservadora, arriesgada o totalmente personalizada.</p>
      </div>
    </div>
  </li>
  <li>
    <div class="feature-content">
      <div class="feature-header">
        <strong>📊 Análisis Integral de Partidos</strong>
      </div>
      <div class="feature-description">
        <p>Integra probabilidades de LAE, histórico de duelos, rachas, clasificación y contexto para ofrecer una predicción razonada.</p>
      </div>
    </div>
  </li>
  <li>
    <div class="feature-content">
      <div class="feature-header">
        <strong>🔍 Detección de Sorpresas</strong>
      </div>
      <div class="feature-description">
        <p>Detecta discrepancias entre las probabilidades oficiales y el rendimiento real (rachas, histórico, forma) para anticipar posibles sorpresas.</p>
      </div>
    </div>
  </li>
  <li>
    <div class="feature-content">
      <div class="feature-header">
        <strong>👥 Estado de Forma de Equipos</strong>
      </div>
      <div class="feature-description">
        <p>Evalúa el rendimiento detallado: últimos marcadores, rachas vigentes, desempeño local/visitante y tendencias clasificatorias.</p>
      </div>
    </div>
  </li>
  <li>
    <div class="feature-content">
      <div class="feature-header">
        <strong>📈 Consulta Flexible de Datos</strong>
      </div>
      <div class="feature-description">
        <p>Accede tanto a análisis interpretados como a los datos en bruto para sacar tus propias conclusiones.</p>
      </div>
    </div>
  </li>
  <li>
    <div class="feature-content">
      <div class="feature-header">
        <strong>🔌 Servidor MCP Nativo</strong>
      </div>
      <div class="feature-description">
        <p>Incluye 7 herramientas especializadas, totalmente compatibles con Claude Desktop, VS Code y otros clientes MCP.</p>
      </div>
    </div>
  </li>
</ul>

<br>
<hr>

## 🏁 Pasos para empezar a usar KinielaGPT

Sigue estos pasos para tener KinielaGPT listo y funcionando en tu equipo:

1. [Instala UV o Python 3.10+](quickstart.md) en tu PC.
2. [Instala](installation.md) KinielaGPT.
3. [Configura](configuration.md) el servidor MCP, eligiendo Claude o VS Code como cliente.

Una vez completados estos pasos, ¡ya puedes empezar a hacer predicciones y análisis con KinielaGPT!

<br>
<hr>


```{include} quickstart.md
```

<br>
<hr>

```{include} installation.md
```

<br>
<hr>

```{include} configuration.md
```

<br>
<hr>

```{include} usage.md
```

<br>
<hr>

⚽ Proyecto creado por **Ricardo Moya** para que cada quiniela se juegue con cabeza, estrategia y datos.

<div align="left">
  <div style="display: flex; align-items: center;">
    <img src="https://github.com/RicardoMoya.png" alt="Ricardo Moya GitHub avatar" width="180" style="border-radius: 90px; margin-right: 24px;"/>
    <div style="font-size:1.5em;">
      🐙 GitHub: <a href="https://github.com/RicardoMoya" target="_blank">@RicardoMoya</a><br>
      💼 LinkedIn: <a href="https://www.linkedin.com/in/phdricardomoya/" target="_blank">Ricardo Moya, PhD</a>
    </div>
  </div>
</div>


```{toctree}
:hidden:
:includehidden:
:maxdepth: 2
:caption: Contenido

quickstart
installation
configuration
usage
api/index
contributing
license
```
