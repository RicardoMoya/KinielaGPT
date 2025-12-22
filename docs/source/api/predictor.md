# 🎯 Módulo `predictor`

El módulo `predictor` implementa algoritmos avanzados de predicción de quiniela, con tres estrategias: conservadora, arriesgada y personalizada.

---

## Clase Principal: `KinielaPredictor`


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

## Ejemplos de Uso

### Predicción Conservadora
```python
import json
from kinielagpt.predictor import KinielaPredictor

predictor = KinielaPredictor()
result = predictor.predict(jornada=26, temporada=2026)
print(json.dumps(result, indent=2, ensure_ascii=False))
```

### Predicción Arriesgada
```python
import json
from kinielagpt.predictor import KinielaPredictor

predictor = KinielaPredictor()
result = predictor.predict(jornada=26, temporada=2026, strategy="arriesgada")
print(json.dumps(result, indent=2, ensure_ascii=False))
```

### Predicción Personalizada
```python
import json
from kinielagpt.predictor import KinielaPredictor

predictor = KinielaPredictor()
custom_dist = {"1": 7, "X": 4, "2": 4}
result = predictor.predict(jornada=26, temporada=2026, strategy="personalizada", custom_distribution=custom_dist)
print(json.dumps(result, indent=2, ensure_ascii=False))
```

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
