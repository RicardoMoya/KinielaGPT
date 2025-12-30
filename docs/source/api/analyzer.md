# 🧠 Módulo `analyzer`

Proporciona herramientas para el análisis detallado de partidos individuales y el rendimiento completo de equipos.

---

## Clase Principal

<div class="api-method-signature">Analyzer</div>
Analizador de partidos y equipos para KinielaGPT. Proporciona herramientas avanzadas para analizar partidos individuales y el rendimiento de equipos específicos utilizando datos de probabilidades LAE, histórico de enfrentamientos, evolución reciente y clasificaciones.

#### Funciones Principales

| Método                                      | Return | Descripción |
|---------------------------------------------|-----------------|-------------|
| `get_raw_data(jornada, temporada, match_id)` | `dict` | Obtiene información en crudo de un partido específico. Retorna datos en crudo del partido (probabilidades, histórico, clasificaciones, evoluciones, rachas, datos destacados) |
| `analyze_match(jornada, temporada, match_id)` | `dict` | Analiza un partido con predicción justificada. Retorna análisis completo con predicción, confianza (ALTA/MEDIA/BAJA) y razonamiento detallado |
| `analyze_team(jornada, temporada, team_name)` | `dict` | Analiza el rendimiento completo de un equipo. Retorna análisis completo del equipo (clasificación, últimos partidos, tendencias, rendimiento local/visitante) |

#### Parámetros

| Nombre             | Tipo   | Descripción                        |
|--------------------|--------|------------------------------------|
| `jornada`          | int    | Número de jornada                  |
| `temporada`        | int    | Año de la temporada                |
| `match_id`         | int    | ID del partido (1-15)              |
| `team_name`        | str    | Nombre exacto del equipo           |

---

## Métricas Analizadas

- **Rendimiento General:** Victorias, empates, derrotas, puntos obtenidos, porcentaje de efectividad
- **Tendencias:** Dirección (mejorando/empeorando/estable), forma (excelente/buena/regular/mala)
- **Rendimiento Local/Visitante:** Estadísticas diferenciadas, comparación de efectividad
- **Histórico:** Victorias locales/visitantes/empates, porcentajes
- **Clasificación:** Posición actual, evolución reciente

---

## Ejemplos de Uso Programático

```{note}
Los valores de `jornada` y `temporada` en los siguientes ejemplos son ilustrativos. Para probar su funcionamiento, actualiza estos valores con datos actuales, ya que las APIs no proporcionan datos históricos.
```

### Datos en Crudo de Partido


```python
import json
from kinielagpt.analyzer import Analyzer

analyzer = Analyzer()

raw_data = analyzer.get_raw_data(jornada=32, temporada=2026, match_id=4)
print(json.dumps(raw_data, indent=2, ensure_ascii=False))
```

<details>
<summary><b>Resultado</b></summary>

```json
{
  "info_partido": {
    "id_partido": 4,
    "partido": "ESPANYOL | BARCELONA",
    "jornada": 32,
    "temporada": 2026
  },
  "probabilidades": {
    "1": 10.8,
    "X": 23.2,
    "2": 66.0,
    "pronostico_goles": "N/A"
  },
  "historico": {
    "victorias_local": 0,
    "empates": 4,
    "victorias_visitante": 6,
    "total_partidos": 10
  },
  "clasificacion": {
    "local": 5,
    "visitante": 1
  },
  "evolucion_clasificacion_local": [6, 7, 5, 3, 4, 4, 7, 9, 6, 5, 6, 6, 6, 6, 5, 5, 5, 5 ],
  "evolucion_clasificacion_visitante": [1, 3, 4, 2, 2, 2, 1, 2,2, 2, 2, 2, 2, 1, 1, 1, 1, 1],
  "ultimos_partidos": [
    {
      "jornada": "1",
      "partido": "ESPANYOL | Atlético",
      "resultado": "2-1",
      "cod_resultado": "VICTORIA",
      "tipo": "local_como_local"
    },
    {
      "jornada": "1",
      "partido": "Mallorca | BARCELONA",
      "resultado": "0-3",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "2",
      "partido": "Real Sociedad | ESPANYOL",
      "resultado": "2-2",
      "cod_resultado": "EMPATE",
      "tipo": "local_como_visitante"
    },
    {
      "jornada": "2",
      "partido": "Levante | BARCELONA",
      "resultado": "2-3",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "3",
      "partido": "ESPANYOL | Osasuna",
      "resultado": "1-0",
      "cod_resultado": "VICTORIA",
      "tipo": "local_como_local"
    },
    {
      "jornada": "3",
      "partido": "Rayo Vallecano | BARCELONA",
      "resultado": "1-1",
      "cod_resultado": "EMPATE",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "4",
      "partido": "ESPANYOL | Mallorca",
      "resultado": "3-2",
      "cod_resultado": "VICTORIA",
      "tipo": "local_como_local"
    },
    {
      "jornada": "4",
      "partido": "BARCELONA | Valencia",
      "resultado": "6-0",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "5",
      "partido": "Real Madrid | ESPANYOL",
      "resultado": "2-0",
      "cod_resultado": "DERROTA",
      "tipo": "local_como_visitante"
    },
    {
      "jornada": "5",
      "partido": "BARCELONA | Getafe",
      "resultado": "3-0",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "6",
      "partido": "ESPANYOL | Valencia",
      "resultado": "2-2",
      "cod_resultado": "EMPATE",
      "tipo": "local_como_local"
    },
    {
      "jornada": "6",
      "partido": "Real Oviedo | BARCELONA",
      "resultado": "1-3",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "7",
      "partido": "Girona | ESPANYOL",
      "resultado": "0-0",
      "cod_resultado": "EMPATE",
      "tipo": "local_como_visitante"
    },
    {
      "jornada": "7",
      "partido": "BARCELONA | Real Sociedad",
      "resultado": "2-1",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "8",
      "partido": "ESPANYOL | Real Betis",
      "resultado": "1-2",
      "cod_resultado": "DERROTA",
      "tipo": "local_como_local"
    },
    {
      "jornada": "8",
      "partido": "Sevilla | BARCELONA",
      "resultado": "4-1",
      "cod_resultado": "DERROTA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "9",
      "partido": "Real Oviedo | ESPANYOL",
      "resultado": "0-2",
      "cod_resultado": "VICTORIA",
      "tipo": "local_como_visitante"
    },
    {
      "jornada": "9",
      "partido": "BARCELONA | Girona",
      "resultado": "2-1",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "10",
      "partido": "ESPANYOL | Elche",
      "resultado": "1-0",
      "cod_resultado": "VICTORIA",
      "tipo": "local_como_local"
    },
    {
      "jornada": "10",
      "partido": "Real Madrid | BARCELONA",
      "resultado": "2-1",
      "cod_resultado": "DERROTA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "11",
      "partido": "Deportivo Alavés | ESPANYOL",
      "resultado": "2-1",
      "cod_resultado": "DERROTA",
      "tipo": "local_como_visitante"
    },
    {
      "jornada": "11",
      "partido": "BARCELONA | Elche",
      "resultado": "3-1",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "12",
      "partido": "ESPANYOL | Villarreal",
      "resultado": "0-2",
      "cod_resultado": "DERROTA",
      "tipo": "local_como_local"
    },
    {
      "jornada": "12",
      "partido": "Celta | BARCELONA",
      "resultado": "2-4",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "13",
      "partido": "ESPANYOL | Sevilla",
      "resultado": "2-1",
      "cod_resultado": "VICTORIA",
      "tipo": "local_como_local"
    },
    {
      "jornada": "13",
      "partido": "BARCELONA | Athletic",
      "resultado": "4-0",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "14",
      "partido": "Celta | ESPANYOL",
      "resultado": "0-1",
      "cod_resultado": "VICTORIA",
      "tipo": "local_como_visitante"
    },
    {
      "jornada": "14",
      "partido": "BARCELONA | Deportivo Alavés",
      "resultado": "3-1",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "15",
      "partido": "ESPANYOL | Rayo Vallecano",
      "resultado": "1-0",
      "cod_resultado": "VICTORIA",
      "tipo": "local_como_local"
    },
    {
      "jornada": "15",
      "partido": "Real Betis | BARCELONA",
      "resultado": "3-5",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "16",
      "partido": "Getafe | ESPANYOL",
      "resultado": "0-1",
      "cod_resultado": "VICTORIA",
      "tipo": "local_como_visitante"
    },
    {
      "jornada": "16",
      "partido": "BARCELONA | Osasuna",
      "resultado": "2-0",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "17",
      "partido": "Athletic | ESPANYOL",
      "resultado": "1-2",
      "cod_resultado": "VICTORIA",
      "tipo": "local_como_visitante"
    },
    {
      "jornada": "17",
      "partido": "Villarreal | BARCELONA",
      "resultado": "0-2",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "19",
      "partido": "BARCELONA | Atlético de Madrid",
      "resultado": "3-1",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    }
  ],
  "rachas": {
    "racha_local_ultimos_5_partidos": ["VICTORIA", "VICTORIA", "VICTORIA", "VICTORIA", "VICTORIA"],
    "racha_visitante_ultimos_5_partidos": ["VICTORIA", "VICTORIA", "VICTORIA", "VICTORIA", "VICTORIA"],
    "racha_local_como_local_ultimos_5_partidos": ["DERROTA", "VICTORIA", "DERROTA", "VICTORIA", "VICTORIA"],
    "racha_visitante_como_visitante_ultimos_5_partidos": ["DERROTA", "DERROTA", "VICTORIA", "VICTORIA", "VICTORIA"]
  },
  "datos_destacados": [
    "El ESPANYOL lleva 5 partidos seguidos ganando",
    "El BARCELONA lleva 8 partidos seguidos ganando",
    "El ESPANYOL lleva 10 partidos seguidos sin empatar",
    "El BARCELONA lleva 15 partidos seguidos sin empatar",
    "El BARCELONA lleva 8 partidos seguidos sin perder",
    "El BARCELONA lleva 6 partidos seguidos sin empatar fuera"
  ]
}
```
</details>
   
---

### Análisis Completo de Partido

```python
import json
from kinielagpt.analyzer import Analyzer

analyzer = Analyzer()

analysis = analyzer.analyze_match(jornada=32, temporada=2026, match_id=4)
print(json.dumps(analysis, indent=2, ensure_ascii=False))
```

<details>
<summary><b>Resultado</b></summary>

```json
{
  "info_partido": {
    "id_partido": 4,
    "partido": "ESPANYOL | BARCELONA",
    "jornada": 32,
    "temporada": 2026
  },
  "probabilidades": {
    "1": 10.8,
    "X": 23.2,
    "2": 66.0
  },
  "datos_historicos": {
    "total_partidos": 10,
    "victorias_local": 0,
    "empates": 4,
    "victorias_visitante": 6,
    "porcentaje_victorias_local": 0.0,
    "porcentaje_empates": 40.0,
    "porcentaje_victorias_visitante": 60.0
  },
  "prediccion": "2",
  "confianza": "ALTA",
  "razonamiento": "Probabilidad LAE del 2: 66.0%. Histórico: Visitante gana 60% de los enfrentamientos (6 de 10).",
  "info_clasificacion": {
    "clasificacion_local": 5,
    "clasificacion_visitante": 1,
    "evolucion_clasificacion_local": [6, 7, 5, 3, 4, 4, 7, 9, 6, 5, 6, 6, 6, 6, 5, 5, 5, 5],
    "evolucion_clasificacion_visitante": [1, 3, 4, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
  },
  "tendencias_local": {
    "tendencia_general": {
      "direccion": "mejorando",
      "descripcion": "Tendencia al alza",
      "puntos_ultimos_partidos": 15,
      "porcentaje_puntos_ultimos_partidos": 100.0,
      "forma": "excelente",
      "ultimos_resultados": ["VICTORIA", "VICTORIA", "VICTORIA", "VICTORIA", "VICTORIA"]
    },
    "tendencia_local_como_local": {
      "direccion": "estable",
      "descripcion": "Rendimiento estable",
      "puntos_ultimos_partidos": 9,
      "porcentaje_puntos_ultimos_partidos": 60.0,
      "forma": "buena",
      "ultimos_resultados": ["DERROTA", "VICTORIA", "DERROTA", "VICTORIA", "VICTORIA"]
    }
  },
  "tendencias_visitante": {
    "tendencia_general": {
      "direccion": "mejorando",
      "descripcion": "Tendencia al alza",
      "puntos_ultimos_partidos": 15,
      "porcentaje_puntos_ultimos_partidos": 100.0,
      "forma": "excelente",
      "ultimos_resultados": ["VICTORIA", "VICTORIA", "VICTORIA", "VICTORIA", "VICTORIA"]
    },
    "tendencia_visitante_como_visitante": {
      "direccion": "estable",
      "descripcion": "Rendimiento estable",
      "puntos_ultimos_partidos": 9,
      "porcentaje_puntos_ultimos_partidos": 60.0,
      "forma": "buena",
      "ultimos_resultados": ["DERROTA", "DERROTA", "VICTORIA", "VICTORIA", "VICTORIA"]
    }
  },
  "analisis_rendimiento_del_local_vs_visitante": {
    "local": {
      "registro": "10V-3E-4D (33pts)",
      "puntos": 33,
      "porcentaje_puntos_conseguidos": 64.7,
      "calificacion": "Bueno"
    },
    "visitante": {
      "registro": "15V-1E-2D (46pts)",
      "puntos": 46,
      "porcentaje_puntos_conseguidos": 85.2,
      "calificacion": "Excelente"
    },
    "comparacion": "Mejor visitante"
  },
  "datos_destacados": [
    "El ESPANYOL lleva 5 partidos seguidos ganando",
    "El BARCELONA lleva 8 partidos seguidos ganando",
    "El ESPANYOL lleva 10 partidos seguidos sin empatar",
    "El BARCELONA lleva 15 partidos seguidos sin empatar",
    "El BARCELONA lleva 8 partidos seguidos sin perder",
    "El BARCELONA lleva 6 partidos seguidos sin empatar fuera"
  ]
}
```
</details>

---

### Análisis de Equipo
```python
import json
from kinielagpt.analyzer import Analyzer

analyzer = Analyzer()
team_analysis = analyzer.analyze_team(jornada=32, temporada=2026, team_name="BETIS")
print(json.dumps(team_analysis, indent=2, ensure_ascii=False))
```

<details>
<summary><b>Resultado</b></summary>

```json
{
  "equipo": "BETIS",
  "clasificacion": 6,
  "evolucion_clasificacion": [10, 6, 10, 11, 8, 8, 6, 4, 5, 6, 5, 5, 5, 5, 6, 6, 6, 6],
  "juega_en_casa": false,
  "ultimos_5_partidos": [
    {
      "jornada": "13",
      "partido": "BETIS | Girona FC",
      "resultado": "1-1",
      "cod_resultado": "EMPATE",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "14",
      "partido": "Sevilla | BETIS",
      "resultado": "0-2",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "15",
      "partido": "BETIS | FC Barcelona",
      "resultado": "3-5",
      "cod_resultado": "DERROTA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "16",
      "partido": "Rayo Vallecano | BETIS",
      "resultado": "0-0",
      "cod_resultado": "EMPATE",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "17",
      "partido": "BETIS | Getafe",
      "resultado": "4-0",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    }
  ],
  "ultimos_5_partidos_como_local": [
    {
      "jornada": "10",
      "partido": "BETIS | Atlético",
      "resultado": "0-2",
      "cod_resultado": "DERROTA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "11",
      "partido": "BETIS | Mallorca",
      "resultado": "3-0",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "13",
      "partido": "BETIS | Girona FC",
      "resultado": "1-1",
      "cod_resultado": "EMPATE",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "15",
      "partido": "BETIS | FC Barcelona",
      "resultado": "3-5",
      "cod_resultado": "DERROTA",
      "tipo": "visitante_como_local"
    },
    {
      "jornada": "17",
      "partido": "BETIS | Getafe",
      "resultado": "4-0",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_local"
    }
  ],
  "ultimos_5_partidos_como_visitante": [
    {
      "jornada": "8",
      "partido": "Espanyol | BETIS",
      "resultado": "1-2",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "9",
      "partido": "Villarreal | BETIS",
      "resultado": "2-2",
      "cod_resultado": "EMPATE",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "12",
      "partido": "Valencia | BETIS",
      "resultado": "1-1",
      "cod_resultado": "EMPATE",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "14",
      "partido": "Sevilla | BETIS",
      "resultado": "0-2",
      "cod_resultado": "VICTORIA",
      "tipo": "visitante_como_visitante"
    },
    {
      "jornada": "16",
      "partido": "Rayo Vallecano | BETIS",
      "resultado": "0-0",
      "cod_resultado": "EMPATE",
      "tipo": "visitante_como_visitante"
    }
  ],
  "racha_ultimos_5_partidos": ["EMPATE", "VICTORIA", "DERROTA", "EMPATE", "VICTORIA"],
  "racha_como_local_ultimos_5_partidos": ["DERROTA", "VICTORIA", "EMPATE", "DERROTA", "VICTORIA"],
  "racha_como_visitante_ultimos_5_partidos": ["VICTORIA", "EMPATE", "EMPATE", "VICTORIA", "EMPATE"],
  "tendencia_global": {
    "direccion": "estable",
    "descripcion": "Rendimiento estable",
    "puntos_ultimos_partidos": 8,
    "porcentaje_puntos_ultimos_partidos": 53.3,
    "forma": "regular",
    "ultimos_resultados": ["EMPATE", "VICTORIA", "DERROTA", "EMPATE", "VICTORIA"]
  },
  "tendencia_como_local": {
    "direccion": "estable",
    "descripcion": "Rendimiento estable",
    "puntos_ultimos_partidos": 7,
    "porcentaje_puntos_ultimos_partidos": 46.7,
    "forma": "regular",
    "ultimos_resultados": ["DERROTA", "VICTORIA", "EMPATE", "DERROTA", "VICTORIA"]
  },
  "tendencia_como_visitante": {
    "direccion": "estable",
    "descripcion": "Rendimiento estable",
    "puntos_ultimos_partidos": 9,
    "porcentaje_puntos_ultimos_partidos": 60.0,
    "forma": "buena",
    "ultimos_resultados": ["VICTORIA", "EMPATE", "EMPATE", "VICTORIA", "EMPATE"]
  },
  "analisis_rendimiento_como_local_y_como_visitante": {
    "local": {
      "registro": "5V-1E-3D (16pts)",
      "puntos": 16,
      "porcentaje_puntos_conseguidos": 59.3,
      "calificacion": "Bueno"
    },
    "visitante": {
      "registro": "2V-6E-0D (12pts)",
      "puntos": 12,
      "porcentaje_puntos_conseguidos": 50.0,
      "calificacion": "Bueno"
    },
    "comparacion": "Equilibrado Local/Visitante"
  },
  "proximo_partido": "R.MADRID | BETIS"
}
```
</details>
