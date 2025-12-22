# 🗄️ Módulo `data_source`

Maneja la obtención y procesamiento de datos desde APIs externas de fútbol español.

---

## Funciones Principales

| Función                                           | Parámetros                         | Retorno                                |
| ------------------------------------------------- | ---------------------------------- | -------------------------------------- |
| `get_last_kiniela()`                              | Ninguno                            | `(jornada, temporada, lista_partidos)` |
| `get_kiniela(jornada, temporada)`                 | `jornada (int)`, `temporada (int)` | `(jornada, temporada, lista_partidos)` |
| `get_kiniela_probabilities(jornada, temporada)`   | `jornada (int)`, `temporada (int)` | `list[dict]` o `None` |
| `get_kiniela_matches_details(jornada, temporada)` | `jornada (int)`, `temporada (int)` | `list[dict]` o `None` |


---

## Ejemplos de Uso

```python
from kinielagpt import data_source

# Última quiniela
descripcion, jornada, temporada, partidos = data_source.get_last_kiniela()
print(descripcion)
print(f"Partidos de la jornada:")
for i, partido in enumerate(partidos, 1):
    print(f"Partido: {partido['id']} - {partido['partido']}")


# Probabilidades de jornada específica
probs = data_source.get_kiniela_probabilities(jornada=26, temporada=2026)
for i, prob in enumerate(probs, 1):
    if i != 15:
        print(f"Partido {i}: {prob['partido']} - 1_Prob: {prob['1_Prob']} | X_Prob: {prob['X_Prob']} | 2_Prob: {prob['2_Prob']} ")
```