# 🖥️ Módulo `server`

El módulo `server` implementa el servidor MCP (Model Context Protocol) que expone las funcionalidades de KinielaGPT como herramientas para clientes MCP.

---

## Arquitectura MCP

- Comunicación bidireccional via stdio
- Protocolo JSON-RPC 2.0
- Integración nativa con Claude Desktop, VS Code, etc.

---

## Herramientas Disponibles

| Herramienta       | Descripción | Parámetros principales  | Respuesta principal |
|-------------------|-------------|-------------------------|---------------------|
| `get_last_quiniela` | Última quiniela disponible | Ninguno | Lista de partidos de la última quiniela  |
| `get_quiniela`      | Info completa de una jornada | `jornada`, `temporada` | Lista de partidos de una quiniela en particular |
| `get_probabilities` | Probabilidades LAE para todos los partidos | `jornada` (int), `temporada` (int) | Lista de partidos con probabilidades|
| `predict_quiniela`  | Predicción completa de quiniela | `jornada`, `temporada`, `strategy`, `custom_distribution` | Ver módulo `predictor` |
| `detect_surprises`  | Detecta posibles sorpresas | `jornada`, `temporada`, `threshold` | Ver módulo `detector` |
| `analyze_match`     | Análisis detallado de un partido | `jornada`, `temporada`, `match_id` | Ver módulo `analyzer` |
| `analyze_team`      | Análisis completo de un equipo | `jornada`, `temporada`, `team_name` | Ver módulo `analyzer` |
