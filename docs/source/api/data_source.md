# 🗄️ Módulo `data_source`

Maneja la obtención y procesamiento de datos desde APIs externas de fútbol español.

---

## Funciones Principales

| Método                                           | Return                                | Descripción |
| ------------------------------------------------- | ------------------------------------- | ----------- |
| `get_last_kiniela()`                              | `(jornada, temporada, lista_partidos)` | Obtiene información de la última quiniela disponible. Devuelve jornada, temporada y lista de partidos |
| `get_kiniela(jornada, temporada)`                 | `(jornada, temporada, lista_partidos)` | Obtiene información de una quiniela específica. Devuelve jornada, temporada y lista de partidos |
| `get_kiniela_probabilities(jornada, temporada)`   | `list[dict]` o `None`                 | Obtiene las probabilidades LAE para todos los partidos de una jornada. Devuelve lista de diccionarios con probabilidades o None si hay error |
| `get_kiniela_matches_details(jornada, temporada)` | `list[dict]` o `None`                 | Obtiene detalles detallados de todos los partidos de una jornada. Devuelve lista de diccionarios con información completa de partidos o None si hay error |


---

## Ejemplo de Uso Programático

```{note}
Los valores de `jornada` y `temporada` en los siguientes ejemplos son ilustrativos. Para probar su funcionamiento, actualiza estos valores con datos actuales, ya que las APIs no proporcionan datos históricos.
```

```python
import json
from kinielagpt import data_source

# Última quiniela
descripcion, jornada, temporada, partidos = data_source.get_last_kiniela()
print(descripcion)
print(json.dumps(partidos, indent=2, ensure_ascii=False))

# Probabilidades de jornada específica
print('==========================================')
print('=              PROBABILIDADES            =')
print('==========================================')
probs = data_source.get_kiniela_probabilities(jornada=jornada, temporada=temporada)
print(json.dumps(probs, indent=2, ensure_ascii=False))
```

<details>
<summary><b>Resultado</b></summary>

```
Quiniela de la jornada 32 de la temporada 2025/2026
[
  {
    "id": 1,
    "partido": "CELTA | VALENCIA"
  },
  {
    "id": 2,
    "partido": "OSASUNA | ATH.CLUB"
  },
  {
    "id": 3,
    "partido": "ELCHE | VILLARREAL"
  },
  {
    "id": 4,
    "partido": "ESPANYOL | BARCELONA"
  },
  {
    "id": 5,
    "partido": "SEVILLA | LEVANTE"
  },
  {
    "id": 6,
    "partido": "R.MADRID | BETIS"
  },
  {
    "id": 7,
    "partido": "ALAVÉS | R.OVIEDO"
  },
  {
    "id": 8,
    "partido": "MALLORCA | GIRONA"
  },
  {
    "id": 9,
    "partido": "CASTELLÓN | HUESCA"
  },
  {
    "id": 10,
    "partido": "VALLADOLID | RACING S."
  },
  {
    "id": 11,
    "partido": "CÓRDOBA | BURGOS"
  },
  {
    "id": 12,
    "partido": "SPORTING | MÁLAGA"
  },
  {
    "id": 13,
    "partido": "R.ZARAGOZA | LAS PALMAS"
  },
  {
    "id": 14,
    "partido": "DEPORTIVO | CÁDIZ"
  },
  {
    "id": 15,
    "partido": "R.SOCIEDAD | AT.MADRID"
  }
]
==========================================
=              PROBABILIDADES            =
==========================================
[
  {
    "id": 1,
    "1_Prob": 55.9,
    "X_Prob": 28.4,
    "2_Prob": 15.6,
    "partido": "CELTA | VALENCIA"
  },
  {
    "id": 2,
    "1_Prob": 25.7,
    "X_Prob": 33.6,
    "2_Prob": 40.6,
    "partido": "OSASUNA | ATH.CLUB"
  },
  {
    "id": 3,
    "1_Prob": 16.1,
    "X_Prob": 25.6,
    "2_Prob": 58.3,
    "partido": "ELCHE | VILLARREAL"
  },
  {
    "id": 4,
    "1_Prob": 10.8,
    "X_Prob": 23.7,
    "2_Prob": 65.5,
    "partido": "ESPANYOL | BARCELONA"
  },
  {
    "id": 5,
    "1_Prob": 74.0,
    "X_Prob": 18.0,
    "2_Prob": 8.0,
    "partido": "SEVILLA | LEVANTE"
  },
  {
    "id": 6,
    "1_Prob": 77.4,
    "X_Prob": 15.9,
    "2_Prob": 6.7,
    "partido": "R.MADRID | BETIS"
  },
  {
    "id": 7,
    "1_Prob": 59.3,
    "X_Prob": 27.0,
    "2_Prob": 13.7,
    "partido": "ALAVÉS | R.OVIEDO"
  },
  {
    "id": 8,
    "1_Prob": 45.8,
    "X_Prob": 32.2,
    "2_Prob": 22.1,
    "partido": "MALLORCA | GIRONA"
  },
  {
    "id": 9,
    "1_Prob": 63.4,
    "X_Prob": 26.3,
    "2_Prob": 10.4,
    "partido": "CASTELLÓN | HUESCA"
  },
  {
    "id": 10,
    "1_Prob": 30.4,
    "X_Prob": 30.3,
    "2_Prob": 39.3,
    "partido": "VALLADOLID | RACING S."
  },
  {
    "id": 11,
    "1_Prob": 42.3,
    "X_Prob": 36.9,
    "2_Prob": 20.9,
    "partido": "CÓRDOBA | BURGOS"
  },
  {
    "id": 12,
    "1_Prob": 57.2,
    "X_Prob": 29.7,
    "2_Prob": 13.2,
    "partido": "SPORTING | MÁLAGA"
  },
  {
    "id": 13,
    "1_Prob": 24.6,
    "X_Prob": 30.7,
    "2_Prob": 44.8,
    "partido": "R.ZARAGOZA | LAS PALMAS"
  },
  {
    "id": 14,
    "1_Prob": 64.5,
    "X_Prob": 24.6,
    "2_Prob": 10.9,
    "partido": "DEPORTIVO | CÁDIZ"
  },
  {
    "id": 15,
    "0_Goles_Local_Prob": 28.4,
    "1_Goles_Local_Prob": 54.9,
    "2_Goles_Local_Prob": 12.9,
    "Mas_Goles_Local_Prob": 3.9,
    "0_Goles_Visitante_Prob": 8.4,
    "1_Goles_Visitante_Prob": 37.4,
    "2_Goles_Visitante_Prob": 39.9,
    "Mas_Goles_Visitante_Prob": 14.3,
    "partido": "R.SOCIEDAD | AT.MADRID"
  }
]
```
</details>