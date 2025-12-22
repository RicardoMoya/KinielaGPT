# 🧩 API Reference

Esta sección contiene la documentación técnica completa de las herramientas MCP disponibles en KinielaGPT.


## Módulos Principales

| Módulo | Descripción |
|--------|-------------|
|🧠 [analyzer](analyzer) | Proporciona herramientas para el análisis detallado de partidos individuales y el rendimiento completo de equipos.|
|🗄️[data_source](data_source) | Maneja la obtención y procesamiento de datos desde APIs externas de fútbol español. |
|🚨 [detector](detector) | Identifica partidos con posibles sorpresas basándose en inconsistencias entre probabilidades LAE y factores contextuales. |
|🎯 [predictor](predictor) | Algoritmos avanzados de predicción de quiniela, con tres estrategias: conservadora, arriesgada y personalizada. |
|🖥️ [server](server) | Servidor MCP (Model Context Protocol) que expone las funcionalidades de KinielaGPT como herramientas para clientes MCP. |

---

## Parámetros utilizados
- `jornada`: Número entero (mínimo 1)
- `temporada`: Año entero (mínimo 2000)
- `match_id`: ID del partido (1-15)
- `team_name`: Nombre del equipo
- `strategy`: "conservadora", "arriesgada", o "personalizada"
- `threshold`: Número decimal 0-100 (default 30.0)

---

## Respuestas
Todas las respuestas están en formato JSON estructurado con campos consistentes.

---

## Errores
Los errores se devuelven con códigos HTTP estándar y mensajes descriptivos.



```{toctree}
:hidden:
:includehidden:
:maxdepth: 1

analyzer
data_source
detector
predictor
server
```
