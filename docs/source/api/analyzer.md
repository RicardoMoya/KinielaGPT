# 🧠 Módulo `analyzer`

Proporciona herramientas para el análisis detallado de partidos individuales y el rendimiento completo de equipos.

---

## Clases Principales


<div class="api-method-signature">MatchAnalyzer</div>
Analiza partidos individuales considerando probabilidades, histórico, rachas y factores contextuales.

#### Métodos

| Método                                      | Descripción                                                                 |
|---------------------------------------------|-----------------------------------------------------------------------------|
| `get_raw_data(jornada, temporada, match_id)` | Obtiene información en crudo de un partido específico                       |
| `analyze(jornada, temporada, match_id, include_prediction=True)` | Analiza un partido, con o sin predicción justificada                        |

#### Parámetros Comunes

| Nombre             | Tipo   | Descripción                        |
|--------------------|--------|------------------------------------|
| `jornada`          | int    | Número de jornada                  |
| `temporada`        | int    | Año de la temporada                |
| `match_id`         | int    | ID del partido (1-15)              |
| `include_prediction`| bool  | Incluir predicción (default: True) |

#### return

- **Con predicción:** Predicción, nivel de confianza (ALTA/MEDIA/BAJA), justificación detallada
- **Sin predicción:** Datos en crudo del partido

---


<div class="api-method-signature">TeamAnalyzer</div>
Analiza el rendimiento completo de un equipo específico.

#### Método

| Método                                  | Descripción                                  |
|-----------------------------------------|----------------------------------------------|
| `analyze(jornada, temporada, team_name)`| Analiza el rendimiento completo de un equipo |

| Nombre      | Tipo   | Descripción             |
|-------------|--------|-------------------------|
| `jornada`   | int    | Número de jornada       |
| `temporada` | int    | Año de la temporada     |
| `team_name` | str    | Nombre exacto del equipo|

#### return

`dict` con análisis completo: últimos resultados, rachas actuales, rendimiento local/visitante, clasificación y tendencia (Excelente/Buena/Irregular/Mala)

---

## Métricas Analizadas

- **Rendimiento General:** Victorias, empates, derrotas, goles a favor/en contra, puntos obtenidos
- **Rachas Actuales:** Racha de victorias/derrotas, sin perder, sin marcar
- **Rendimiento Local/Visitante:** Estadísticas como local y visitante, comparación
- **Tendencias:** Evolución reciente, posición en clasificación, comparación con temporada anterior

---

## Ejemplos de Uso

### Análisis de Partido
```python
import json
from kinielagpt.analyzer import MatchAnalyzer

analyzer = MatchAnalyzer()

raw_data = analyzer.get_raw_data(jornada=26, temporada=2026, match_id=5)
print(json.dumps(raw_data, indent=2, ensure_ascii=False))

analysis = analyzer.analyze(jornada=26, temporada=2026, match_id=5)
print(json.dumps(analysis, indent=2, ensure_ascii=False))

```

### Análisis de Equipo
```python
import json
from kinielagpt.analyzer import TeamAnalyzer

analyzer = TeamAnalyzer()
team_analysis = analyzer.analyze(jornada=26, temporada=2026, team_name="RAYO")
print(json.dumps(team_analysis, indent=2, ensure_ascii=False))
```