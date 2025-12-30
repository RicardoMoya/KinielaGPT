# 🎯 Módulo `predictor`

El módulo `predictor` implementa algoritmos avanzados de predicción de quiniela, con tres estrategias: conservadora, arriesgada y personalizada.

---

## Clase Principal: `KinielaPredictor`

### Método `predict`

<div class="api-method-signature">predict(jornada, temporada, strategy="conservadora", custom_distribution=None)</div>

Genera una predicción completa de quiniela usando la estrategia especificada.

#### Parámetros

| Nombre               | Tipo   | Descripción                                                                 |
|----------------------|--------|-----------------------------------------------------------------------------|
| `jornada`            | int    | Número de jornada                                                           |
| `temporada`          | int    | Año de la temporada                                                         |
| `strategy`           | str    | Estrategia: "conservadora", "arriesgada", "personalizada" (por defecto: conservadora) |
| `custom_distribution`| dict   | Solo para estrategia personalizada. Ej: `{"1": 7, "X": 4, "2": 4}`         |

#### return

`dict` con predicción completa y estadísticas (ver ejemplo de estructura más abajo).

---

## Estrategias de Predicción

### 🎯 Conservadora
Selecciona siempre el signo con mayor probabilidad LAE. Máxima fiabilidad estadística, menos riesgo de sorpresas.

### 🎲 Arriesgada
Balancea probabilidades LAE con análisis contextual (rachas, histórico, clasificación). Ajusta probabilidades según forma actual y momentum de equipos.

### ⚙️ Personalizada
Optimiza la distribución de signos según especificaciones del usuario (`custom_distribution`).

---

## Ejemplos de Uso Programático

```{note}
Los valores de `jornada` y `temporada` en los siguientes ejemplos son ilustrativos. Para probar su funcionamiento, actualiza estos valores con datos actuales, ya que las APIs no proporcionan datos históricos.
```

### Predicción Conservadora
```python
import json
from kinielagpt.predictor import KinielaPredictor

predictor = KinielaPredictor()
result = predictor.predict(jornada=32, temporada=2026)
print(json.dumps(result, indent=2, ensure_ascii=False))
```

<details>
<summary><b>Resultado</b></summary>

```json
{
  "jornada": 32,
  "temporada": 2026,
  "strategy": "conservadora",
  "predictions": [
    {
      "match_id": 1,
      "match": "CELTA | VALENCIA",
      "prediction": "1",
      "confidence": "MEDIA",
      "reasoning": "Probabilidad LAE del 1: 56.0% (la más alta)",
      "probabilities": {
        "1": 56.0,
        "X": 28.4,
        "2": 15.6
      }
    },
    {
      "match_id": 2,
      "match": "OSASUNA | ATH.CLUB",
      "prediction": "2",
      "confidence": "BAJA",
      "reasoning": "Probabilidad LAE del 2: 40.6% (la más alta)",
      "probabilities": {
        "1": 25.7,
        "X": 33.6,
        "2": 40.6
      }
    },
    {
      "match_id": 3,
      "match": "ELCHE | VILLARREAL",
      "prediction": "2",
      "confidence": "MEDIA",
      "reasoning": "Probabilidad LAE del 2: 58.2% (la más alta)",
      "probabilities": {
        "1": 16.1,
        "X": 25.6,
        "2": 58.2
      }
    },
    {
      "match_id": 4,
      "match": "ESPANYOL | BARCELONA",
      "prediction": "2",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE del 2: 65.6% (la más alta)",
      "probabilities": {
        "1": 10.8,
        "X": 23.6,
        "2": 65.6
      }
    },
    {
      "match_id": 5,
      "match": "SEVILLA | LEVANTE",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE del 1: 74.0% (la más alta)",
      "probabilities": {
        "1": 74.0,
        "X": 18.0,
        "2": 8.0
      }
    },
    {
      "match_id": 6,
      "match": "R.MADRID | BETIS",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE del 1: 77.5% (la más alta)",
      "probabilities": {
        "1": 77.5,
        "X": 15.8,
        "2": 6.7
      }
    },
    {
      "match_id": 7,
      "match": "ALAVÉS | R.OVIEDO",
      "prediction": "1",
      "confidence": "MEDIA",
      "reasoning": "Probabilidad LAE del 1: 59.3% (la más alta)",
      "probabilities": {
        "1": 59.3,
        "X": 26.9,
        "2": 13.8
      }
    },
    {
      "match_id": 8,
      "match": "MALLORCA | GIRONA",
      "prediction": "1",
      "confidence": "MEDIA",
      "reasoning": "Probabilidad LAE del 1: 45.8% (la más alta)",
      "probabilities": {
        "1": 45.8,
        "X": 32.1,
        "2": 22.1
      }
    },
    {
      "match_id": 9,
      "match": "CASTELLÓN | HUESCA",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE del 1: 63.5% (la más alta)",
      "probabilities": {
        "1": 63.5,
        "X": 26.2,
        "2": 10.4
      }
    },
    {
      "match_id": 10,
      "match": "VALLADOLID | RACING S.",
      "prediction": "2",
      "confidence": "BAJA",
      "reasoning": "Probabilidad LAE del 2: 39.4% (la más alta)",
      "probabilities": {
        "1": 30.4,
        "X": 30.2,
        "2": 39.4
      }
    },
    {
      "match_id": 11,
      "match": "CÓRDOBA | BURGOS",
      "prediction": "1",
      "confidence": "BAJA",
      "reasoning": "Probabilidad LAE del 1: 42.2% (la más alta)",
      "probabilities": {
        "1": 42.2,
        "X": 36.9,
        "2": 20.9
      }
    },
    {
      "match_id": 12,
      "match": "SPORTING | MÁLAGA",
      "prediction": "1",
      "confidence": "MEDIA",
      "reasoning": "Probabilidad LAE del 1: 57.1% (la más alta)",
      "probabilities": {
        "1": 57.1,
        "X": 29.7,
        "2": 13.2
      }
    },
    {
      "match_id": 13,
      "match": "R.ZARAGOZA | LAS PALMAS",
      "prediction": "2",
      "confidence": "BAJA",
      "reasoning": "Probabilidad LAE del 2: 44.8% (la más alta)",
      "probabilities": {
        "1": 24.5,
        "X": 30.7,
        "2": 44.8
      }
    },
    {
      "match_id": 14,
      "match": "DEPORTIVO | CÁDIZ",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE del 1: 64.5% (la más alta)",
      "probabilities": {
        "1": 64.5,
        "X": 24.5,
        "2": 11.0
      }
    },
    {
      "match_id": 15,
      "match": "R.SOCIEDAD | AT.MADRID",
      "prediction": "1-2",
      "confidence": "N/A",
      "reasoning": "Marcador más probable basado en probabilidades de goles",
      "probabilities": {
        "id": 15,
        "0_Goles_Local_Prob": 28.3,
        "1_Goles_Local_Prob": 54.9,
        "2_Goles_Local_Prob": 12.9,
        "Mas_Goles_Local_Prob": 3.9,
        "0_Goles_Visitante_Prob": 8.4,
        "1_Goles_Visitante_Prob": 37.2,
        "2_Goles_Visitante_Prob": 40.1,
        "Mas_Goles_Visitante_Prob": 14.3,
        "partido": "R.SOCIEDAD | AT.MADRID"
      }
    }
  ],
  "summary": {
    "1": 9,
    "X": 0,
    "2": 5
  }
}
```
</details>

---

### Predicción Arriesgada
```python
import json
from kinielagpt.predictor import KinielaPredictor

predictor = KinielaPredictor()
result = predictor.predict(jornada=32, temporada=2026, strategy="arriesgada")
print(json.dumps(result, indent=2, ensure_ascii=False))
```

<details>
<summary><b>Resultado</b></summary>

```json
{
  "jornada": 32,
  "temporada": 2026,
  "strategy": "arriesgada",
  "predictions": [
    {
      "match_id": 1,
      "match": "CELTA | VALENCIA",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE 1: 56.0%.",
      "probabilities": {
        "1": 56.0,
        "X": 28.4,
        "2": 15.6
      },
      "adjusted_probabilities": {
        "1": 56.950476114586245,
        "X": 27.184748396350457,
        "2": 15.864775489063309
      },
      "context_factors": {
        "local_strength": 2.1,
        "visitor_strength": 2.1,
        "draw_tendency": -3.9000000000000004,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 2,
      "match": "OSASUNA | ATH.CLUB",
      "prediction": "2",
      "confidence": "MEDIA",
      "reasoning": "Probabilidad LAE 2: 40.6%.",
      "probabilities": {
        "1": 25.7,
        "X": 33.6,
        "2": 40.6
      },
      "adjusted_probabilities": {
        "1": 25.254316110537644,
        "X": 30.01877065590205,
        "2": 44.7269132335603
      },
      "context_factors": {
        "local_strength": -0.9000000000000008,
        "visitor_strength": 11.099999999999998,
        "draw_tendency": -9.9,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 3,
      "match": "ELCHE | VILLARREAL",
      "prediction": "2",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE 2: 58.2%.",
      "probabilities": {
        "1": 16.1,
        "X": 25.6,
        "2": 58.2
      },
      "adjusted_probabilities": {
        "1": 17.6858334102134,
        "X": 26.36562147502038,
        "2": 55.948545114766226
      },
      "context_factors": {
        "local_strength": 6.766666666666667,
        "visitor_strength": -6.566666666666667,
        "draw_tendency": 0.09999999999999898,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 4,
      "match": "ESPANYOL | BARCELONA",
      "prediction": "2",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE 2: 65.6%.",
      "probabilities": {
        "1": 10.8,
        "X": 23.6,
        "2": 65.6
      },
      "adjusted_probabilities": {
        "1": 9.290433454267712,
        "X": 23.00515562344854,
        "2": 67.70441092228374
      },
      "context_factors": {
        "local_strength": -9.9,
        "visitor_strength": 8.1,
        "draw_tendency": 2.1,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 5,
      "match": "SEVILLA | LEVANTE",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE 1: 74.0%.",
      "probabilities": {
        "1": 74.0,
        "X": 18.0,
        "2": 8.0
      },
      "adjusted_probabilities": {
        "1": 75.07142857142858,
        "X": 17.73938223938224,
        "2": 7.1891891891891895
      },
      "context_factors": {
        "local_strength": 5.1,
        "visitor_strength": -6.9,
        "draw_tendency": 2.1,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 6,
      "match": "R.MADRID | BETIS",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE 1: 77.5%.",
      "probabilities": {
        "1": 77.5,
        "X": 15.8,
        "2": 6.7
      },
      "adjusted_probabilities": {
        "1": 77.80634820743771,
        "X": 15.862455505516332,
        "2": 6.331196287045959
      },
      "context_factors": {
        "local_strength": 2.1,
        "visitor_strength": -3.9000000000000004,
        "draw_tendency": 2.1,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 7,
      "match": "ALAVÉS | R.OVIEDO",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE 1: 59.3%. ajustada a 64.9% por análisis contextual. ventaja del local por clasificación/histórico.",
      "probabilities": {
        "1": 59.3,
        "X": 26.9,
        "2": 13.8
      },
      "adjusted_probabilities": {
        "1": 64.94724929385136,
        "X": 23.423464711274065,
        "2": 11.629285994874579
      },
      "context_factors": {
        "local_strength": 17.1,
        "visitor_strength": -9.9,
        "draw_tendency": -6.9,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 8,
      "match": "MALLORCA | GIRONA",
      "prediction": "1",
      "confidence": "MEDIA",
      "reasoning": "Probabilidad LAE 1: 45.8%.",
      "probabilities": {
        "1": 45.8,
        "X": 32.1,
        "2": 22.1
      },
      "adjusted_probabilities": {
        "1": 48.09120115394702,
        "X": 31.601199842643585,
        "2": 20.307599003409386
      },
      "context_factors": {
        "local_strength": 6.766666666666667,
        "visitor_strength": -6.566666666666667,
        "draw_tendency": 0.09999999999999898,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 9,
      "match": "CASTELLÓN | HUESCA",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE 1: 63.5%.",
      "probabilities": {
        "1": 63.5,
        "X": 26.2,
        "2": 10.4
      },
      "adjusted_probabilities": {
        "1": 60.29448804459053,
        "X": 27.638499695964065,
        "2": 12.0670122594454
      },
      "context_factors": {
        "local_strength": -9.9,
        "visitor_strength": 10.099999999999998,
        "draw_tendency": 0.09999999999999898,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 10,
      "match": "VALLADOLID | RACING S.",
      "prediction": "2",
      "confidence": "BAJA",
      "reasoning": "Probabilidad LAE 2: 39.4%.",
      "probabilities": {
        "1": 30.4,
        "X": 30.2,
        "2": 39.4
      },
      "adjusted_probabilities": {
        "1": 31.944649963006654,
        "X": 29.016976944150052,
        "2": 39.03837309284329
      },
      "context_factors": {
        "local_strength": 5.1,
        "visitor_strength": -0.9000000000000008,
        "draw_tendency": -3.9000000000000004,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 11,
      "match": "CÓRDOBA | BURGOS",
      "prediction": "1",
      "confidence": "MEDIA",
      "reasoning": "Probabilidad LAE 1: 42.2%.",
      "probabilities": {
        "1": 42.2,
        "X": 36.9,
        "2": 20.9
      },
      "adjusted_probabilities": {
        "1": 44.380942999737336,
        "X": 36.38386524822694,
        "2": 19.23519175203572
      },
      "context_factors": {
        "local_strength": 6.766666666666667,
        "visitor_strength": -6.566666666666667,
        "draw_tendency": 0.09999999999999898,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 12,
      "match": "SPORTING | MÁLAGA",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE 1: 57.1%.",
      "probabilities": {
        "1": 57.1,
        "X": 29.7,
        "2": 13.2
      },
      "adjusted_probabilities": {
        "1": 59.04668667289812,
        "X": 28.082550302553255,
        "2": 12.870763024548628
      },
      "context_factors": {
        "local_strength": 5.1,
        "visitor_strength": -0.9000000000000008,
        "draw_tendency": -3.9000000000000004,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 13,
      "match": "R.ZARAGOZA | LAS PALMAS",
      "prediction": "2",
      "confidence": "MEDIA",
      "reasoning": "Probabilidad LAE 2: 44.8%.",
      "probabilities": {
        "1": 24.5,
        "X": 30.7,
        "2": 44.8
      },
      "adjusted_probabilities": {
        "1": 25.055842139530228,
        "X": 30.473982070416188,
        "2": 44.47017579005359
      },
      "context_factors": {
        "local_strength": 2.1,
        "visitor_strength": -0.9000000000000008,
        "draw_tendency": -0.9000000000000008,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 14,
      "match": "DEPORTIVO | CÁDIZ",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Probabilidad LAE 1: 64.5%. ventaja del local por clasificación/histórico.",
      "probabilities": {
        "1": 64.5,
        "X": 24.5,
        "2": 11.0
      },
      "adjusted_probabilities": {
        "1": 67.69910250354275,
        "X": 22.93764761454889,
        "2": 9.363249881908361
      },
      "context_factors": {
        "local_strength": 11.099999999999998,
        "visitor_strength": -9.9,
        "draw_tendency": -0.9000000000000008,
        "recent_form_local": "neutral",
        "recent_form_visitor": "neutral"
      }
    },
    {
      "match_id": 15,
      "match": "R.SOCIEDAD | AT.MADRID",
      "prediction": "1-2",
      "confidence": "N/A",
      "reasoning": "Marcador más probable basado en probabilidades de goles",
      "probabilities": {
        "id": 15,
        "0_Goles_Local_Prob": 28.3,
        "1_Goles_Local_Prob": 54.9,
        "2_Goles_Local_Prob": 12.9,
        "Mas_Goles_Local_Prob": 3.9,
        "0_Goles_Visitante_Prob": 8.4,
        "1_Goles_Visitante_Prob": 37.2,
        "2_Goles_Visitante_Prob": 40.1,
        "Mas_Goles_Visitante_Prob": 14.3,
        "partido": "R.SOCIEDAD | AT.MADRID"
      }
    }
  ],
  "summary": {
    "1": 9,
    "X": 0,
    "2": 5
  }
}
```
</details>

---

### Predicción Personalizada
```python
import json
from kinielagpt.predictor import KinielaPredictor

predictor = KinielaPredictor()
custom_dist = {"1": 7, "X": 4, "2": 4}
result = predictor.predict(jornada=32, temporada=2026, strategy="personalizada", custom_distribution=custom_dist)
print(json.dumps(result, indent=2, ensure_ascii=False))
```

<details>
<summary><b>Resultado</b></summary>

```json
{
  "jornada": 32,
  "temporada": 2026,
  "strategy": "personalizada",
  "predictions": [
    {
      "match_id": 1,
      "match": "CELTA | VALENCIA",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Optimizado para distribución personalizada. Score: 57.2",
      "probabilities": {
        "1": 56.0,
        "X": 28.4,
        "2": 15.6
      },
      "score": 57.175999999999995
    },
    {
      "match_id": 2,
      "match": "OSASUNA | ATH.CLUB",
      "prediction": "2",
      "confidence": "MEDIA",
      "reasoning": "Optimizado para distribución personalizada. Score: 45.1",
      "probabilities": {
        "1": 25.7,
        "X": 33.6,
        "2": 40.6
      },
      "score": 45.1066
    },
    {
      "match_id": 3,
      "match": "ELCHE | VILLARREAL",
      "prediction": "2",
      "confidence": "ALTA",
      "reasoning": "Optimizado para distribución personalizada. Score: 54.4",
      "probabilities": {
        "1": 16.1,
        "X": 25.6,
        "2": 58.2
      },
      "score": 54.37820000000001
    },
    {
      "match_id": 4,
      "match": "ESPANYOL | BARCELONA",
      "prediction": "2",
      "confidence": "ALTA",
      "reasoning": "Optimizado para distribución personalizada. Score: 70.9",
      "probabilities": {
        "1": 10.8,
        "X": 23.6,
        "2": 65.6
      },
      "score": 70.91359999999999
    },
    {
      "match_id": 5,
      "match": "SEVILLA | LEVANTE",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Optimizado para distribución personalizada. Score: 77.8",
      "probabilities": {
        "1": 74.0,
        "X": 18.0,
        "2": 8.0
      },
      "score": 77.774
    },
    {
      "match_id": 6,
      "match": "R.MADRID | BETIS",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Optimizado para distribución personalizada. Score: 79.1",
      "probabilities": {
        "1": 77.5,
        "X": 15.8,
        "2": 6.7
      },
      "score": 79.1275
    },
    {
      "match_id": 7,
      "match": "ALAVÉS | R.OVIEDO",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Optimizado para distribución personalizada. Score: 69.4",
      "probabilities": {
        "1": 59.3,
        "X": 26.9,
        "2": 13.8
      },
      "score": 69.4403
    },
    {
      "match_id": 8,
      "match": "MALLORCA | GIRONA",
      "prediction": "X",
      "confidence": "BAJA",
      "reasoning": "Optimizado para distribución personalizada. Score: 32.1",
      "probabilities": {
        "1": 45.8,
        "X": 32.1,
        "2": 22.1
      },
      "score": 32.1321
    },
    {
      "match_id": 9,
      "match": "CASTELLÓN | HUESCA",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Optimizado para distribución personalizada. Score: 57.2",
      "probabilities": {
        "1": 63.5,
        "X": 26.2,
        "2": 10.4
      },
      "score": 57.2135
    },
    {
      "match_id": 10,
      "match": "VALLADOLID | RACING S.",
      "prediction": "X",
      "confidence": "BAJA",
      "reasoning": "Optimizado para distribución personalizada. Score: 29.0",
      "probabilities": {
        "1": 30.4,
        "X": 30.2,
        "2": 39.4
      },
      "score": 29.022199999999998
    },
    {
      "match_id": 11,
      "match": "CÓRDOBA | BURGOS",
      "prediction": "X",
      "confidence": "MEDIA",
      "reasoning": "Optimizado para distribución personalizada. Score: 36.9",
      "probabilities": {
        "1": 42.2,
        "X": 36.9,
        "2": 20.9
      },
      "score": 36.936899999999994
    },
    {
      "match_id": 12,
      "match": "SPORTING | MÁLAGA",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Optimizado para distribución personalizada. Score: 60.0",
      "probabilities": {
        "1": 57.1,
        "X": 29.7,
        "2": 13.2
      },
      "score": 60.0121
    },
    {
      "match_id": 13,
      "match": "R.ZARAGOZA | LAS PALMAS",
      "prediction": "2",
      "confidence": "MEDIA",
      "reasoning": "Optimizado para distribución personalizada. Score: 44.4",
      "probabilities": {
        "1": 24.5,
        "X": 30.7,
        "2": 44.8
      },
      "score": 44.3968
    },
    {
      "match_id": 14,
      "match": "DEPORTIVO | CÁDIZ",
      "prediction": "1",
      "confidence": "ALTA",
      "reasoning": "Optimizado para distribución personalizada. Score: 71.7",
      "probabilities": {
        "1": 64.5,
        "X": 24.5,
        "2": 11.0
      },
      "score": 71.6595
    },
    {
      "match_id": 15,
      "match": "R.SOCIEDAD | AT.MADRID",
      "prediction": "1-2",
      "confidence": "N/A",
      "reasoning": "Marcador más probable basado en probabilidades de goles",
      "probabilities": {
        "id": 15,
        "0_Goles_Local_Prob": 28.3,
        "1_Goles_Local_Prob": 54.9,
        "2_Goles_Local_Prob": 12.9,
        "Mas_Goles_Local_Prob": 3.9,
        "0_Goles_Visitante_Prob": 8.4,
        "1_Goles_Visitante_Prob": 37.2,
        "2_Goles_Visitante_Prob": 40.1,
        "Mas_Goles_Visitante_Prob": 14.3,
        "partido": "R.SOCIEDAD | AT.MADRID"
      }
    }
  ],
  "summary": {
    "1": 7,
    "X": 3,
    "2": 4
  }
}
```
</details>

---

## Validación de Distribución Personalizada

La estrategia personalizada valida que:

- La suma de signos sea exactamente 15
- Cada signo tenga al menos 0 y máximo 15
- Las claves sean exactamente "1", "X", "2"

```python
# Ejemplos válidos
{"1": 7, "X": 4, "2": 4}  # Suma = 15
{"1": 10, "X": 3, "2": 2}  # Suma = 15

# Ejemplos inválidos
{"1": 8, "X": 4, "2": 4}  # Suma = 16
{"1": 7, "X": 4}          # Falta "2"
```

---

## Comparación de Estrategias

| Aspecto            | Conservadora   | Arriesgada   | Personalizada         |
|--------------------|----------------|--------------|-----------------------|
| **Base**           | Probabilidades | + Contexto   | Distribución objetivo |
| **Riesgo**         | Bajo           | Medio        | Variable              |
| **Personalización**| Ninguna        | Automática   | Total                 |
| **Uso típico**     | Validación     | Predicción   | Optimización          |

---

## Consejos de Uso

- **Conservadora**: Ideal para principiantes o validación
- **Arriesgada**: Recomendada para predicciones reales
- **Personalizada**: Para usuarios avanzados con estrategias específicas

Todas las estrategias incluyen justificaciones detalladas para cada predicción.
