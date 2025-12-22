# 🚨 Módulo `detector`

Identifica partidos con posibles sorpresas basándose en inconsistencias entre probabilidades LAE y factores contextuales.

---

## Clase Principal: `SurpriseDetector`


<div class="api-method-signature">detect(jornada, temporada, threshold=30.0)</div>

Detecta posibles sorpresas en una jornada completa.

| Parámetro   | Tipo   | Descripción                                 |
|-------------|--------|---------------------------------------------|
| `jornada`   | int    | Número de jornada                           |
| `temporada` | int    | Año de la temporada                         |
| `threshold` | float  | Umbral de divergencia (0-100, default 30.0) |

**return:** `dict` con lista de alertas de sorpresas (ver ejemplo de estructura más abajo).

---

## Algoritmo de Detección de Sorpresas


El algoritmo de detección de sorpresas evalúa cada partido identificando hasta cuatro tipos de **inconsistencias** que pueden indicar un resultado inesperado:

1. **Inconsistencia base:** Se detecta cuando existe un favorito claro (probabilidad superior al 50%).
2. **Inconsistencia por racha:** Analiza y compara las rachas recientes de ambos equipos, asignando una puntuación según su tendencia positiva o negativa.
3. **Inconsistencia por resultados históricos:** Compara la probabilidad asignada al favorito con la probabilidad real observada en los enfrentamientos previos entre ambos equipos.
4. **Inconsistencia por clasificación:** Considera la diferencia de posiciones en la tabla; solo se aplica si la distancia es mayor a 8 puestos.

Para cada inconsistencia detectada se calcula un **score de divergencia**, que mide la magnitud de la contradicción y permite clasificar la sorpresa en tres niveles:

- 🔴 **ALERTA ROJA**: Divergencia ≥ 50 puntos (contradicción crítica)
- 🟠 **ALERTA MEDIA**: Divergencia ≥ 35 puntos (contradicción notable)
- 🟡 **ALERTA**: Divergencia ≥ threshold (contradicción detectable)

El parámetro *threshold* ajusta la sensibilidad del sistema:

- **threshold=20**: Detección muy sensible (mayor número de alertas)
- **threshold=30**: Configuración equilibrada (recomendada)
- **threshold=40**: Solo se reportan inconsistencias muy marcadas


---

## 🔍 Ejemplo de detección de sorpresas

A continuación se explica el proceso completo de detección de sorpresas desde los datos en bruto hasta el resultado final, usando ejemplo (ficticio) el partido **VILLARREAL - GETAFE** con los siguientes datos:

| Campo | Valor |
|-------|-------|
| **Partido** | VILLARREAL - GETAFE |
| **Threshold** | 25.0 |
| **Prob 1** | 72.5% |
| **Prob X** | 18.3% |
| **Prob 2** | 9.2% |
| **Racha Local** | D-D-D-E-D |
| **Racha Visitante** | V-V-V-V-E |
| **Posición Local** | 12º (28 pts) |
| **Posición Visitante** | 16º (22 pts) |
| **Histórico 1** | 8 victorias locales |
| **Histórico X** | 5 empates |
| **Histórico 2** | 3 victorias visitante |
| **Total Histórico** | 16 partidos |


---

### 1. Cálculo de Divergencia Base

Cuando hay un favorito claro (probabilidad > 50%), se calcula una **divergencia base** que presenta cuánto la probabilidad supera el umbral del 50%:

```python
base_divergence = max_prob - 50
                = 72.5 - 50
                = 22.5 puntos
```

**Interpretación**: Este valor (22.5) será la base para calcular la divergencia total. Representa qué tan favorito es el resultado y se sumará a otros factores (rachas, histórico, clasificación) para determinar si hay inconsistencia.

**Significado**:
- `base_divergence = 0-10`: Favorito débil (50-60% prob)
- `base_divergence = 10-20`: Favorito moderado (60-70% prob)
- `base_divergence = 20-30`: Favorito fuerte (70-80% prob) ← **Caso actual**
- `base_divergence = 30-50`: Favorito muy fuerte (80-100% prob)

---

### 2.- Cálculo de Divergencia por Rachas

Se aplica el siguiente **Sistema de puntuación**:
- Victoria (V) = +3 puntos
- Empate (E) = +1 punto
- Derrota (D) = -2 puntos

**Cálculo para VILLARREAL (local)**:
```python
local_streak = __calculate_streak_value(["D", "D", "D", "E", "D"])
# = -2 + (-2) + (-2) + 1 + (-2)
# = -7 puntos
```

**Cálculo para GETAFE (visitante)**:
```python
visitor_streak = __calculate_streak_value(["V", "V", "V", "V", "E"])
# = 3 + 3 + 3 + 3 + 1
# = 13 puntos
```

**Rangos de interpretación de rachas** (en 5 partidos):
- `streak >= 10`: Racha excelente (mayoría victorias)
- `streak 6-9`: Buena racha
- `streak 1-5`: Racha moderada
- `streak -3 a 0`: Racha pobre
- `streak <= -6`: Racha crítica (mayoría derrotas)


**Resultado**:
- VILLARREAL: **-7 puntos** → Racha crítica (4 derrotas en 5 partidos)
- GETAFE: **+13 puntos** → Racha excelente (4 victorias en 5 partidos)


#### Evaluación de Escenarios

**Escenario evaluado**: Alta probabilidad de victoria local.

El análisis verifica si se cumple la **condición de inconsistencia por rachas**, aplicable cuando hay un favorito claro (probabilidad > 60%).

```python
if max_prob >= 60:
    if local_streak < -6 and visitor_streak > 6:
        # ¡INCONSISTENCIA DETECTADA!
```

**Verificación de condiciones**:
- ✅ `max_prob >= 60` → Verdadero (72.5% >= 60%) - Favorito fuerte
- ✅ `local_streak < -6` → Verdadero (-7 < -6) - Mala racha significativa
- ✅ `visitor_streak > 6` → Verdadero (13 > 6) - Buena racha significativa

**✅ INCONSISTENCIA CONFIRMADA**

**Explicación de umbrales**:
- **60% de probabilidad**: Umbral que distingue favoritos fuertes (>=60%) de favoritos débiles (<60%)
- **-6 puntos en racha**: Umbral de mala forma (típicamente 3-4 derrotas recientes)
- **+6 puntos en racha**: Umbral de buena forma (típicamente 2-3 victorias recientes)

Estos umbrales aseguran que solo se detecten inconsistencias cuando hay una **contradicción real** entre ser favorito fuerte y tener forma muy pobre, mientras el rival tiene forma muy buena.

#### Cálculo de Score de Divergencia

Una vez confirmada la inconsistencia, se calcula el **score de divergencia total** que mide la magnitud de la contradicción:

```python
divergence = min((max_prob - 50) + abs(local_streak) + abs(visitor_streak), 100)
           = min((72.5 - 50) + abs(-7) + 13, 100)
           = min(22.5 + 7 + 13, 100)
           = min(42.5, 100)
           = 42.5 puntos
```

1. **Divergencia base** = `(max_prob - 50)` = 22.5

2. **Magnitud racha local** = `abs(local_streak)` = 7
   - Usa valor absoluto porque queremos la magnitud, no el signo
   - Penaliza por tener mala racha siendo favorito

3. **Magnitud racha visitante** = `abs(visitor_streak)` = 13
   - Penaliza por ignorar la buena racha del rival

4. **Suma total** = 22.5 + 7 + 13 = **42.5 puntos**

5. **Límite máximo** = `min(42.5, 100)` = 42.5
   - El score se limita a 100 para evitar valores extremos
   - En este caso, 42.5 < 100, así que no se aplica el límite

**Interpretación del score 42.5**:
- Es un valor **alto-moderado** que indica inconsistencia notable
- Supera claramente el threshold de 25.0 configurado
- Se acerca al umbral de 50 para ALERTA ROJA
- Refleja una contradicción significativa pero no extrema

#### Generación del Reporte

```python
return {
    "type": "streak_inconsistency",
    "description": "Probabilidad alta de victoria local (72%) pero el local está en mala racha y el visitante en buena forma",
    "factors": {
        "local_recent_form": "Mala racha",
        "visitor_recent_form": "Buena racha"
    },
    "divergence_score": 42.5
}
```

---

### 3.- Cálculo de Divergencia por Historico

Tenemos un históricos de 16 encuentros entre el **VILLARREAL - GETAFE** con los siguientes resultados:

```python
veces1 = 8   # Victorias locales
vecesX = 5   # Empates
veces2 = 3   # Victorias visitante
total_historic = 16  # Total de enfrentamientos
```

#### Validación de Muestra

Este tipo de inconsistencia se calcula si se han jugamos a lo largo de la historia mas de 5 partidos:

```python
if total_historic < 5:
    return None  # Muestra insuficiente
```

**✅ Cumple**: 16 >= 5 → Muestra estadísticamente significativa

#### Cálculo de Tasas Históricas

```python
historical_rates = {
    "1": (8 / 16) * 100 = 50.0%,
    "X": (5 / 16) * 100 = 31.25%,
    "2": (3 / 16) * 100 = 18.75%
}
```

#### Cálculo de Divergencia

La **divergencia por histórico** mide cuánto se aleja la probabilidad del encuentro del patrón histórico real de enfrentamientos directos:


```python
if max_prob >= 50:
    divergencie = max_prob - historical_rate
    # divergence = 72.5 - 50 = 22.5
```

**Interpretación**:
- **Probabilidad**: 72.5% de victoria local
- **Histórico real**: 50.0% de victorias locales (8 de 16 partidos)
- **Divergencia**: 22.5 puntos más al local de lo que indica su histórico


**Interpretación de rangos**:

| Rango de Divergencia | Interpretación | Acción |
|---------------------|----------------|--------|
| `divergence > 50` | Discrepancia extrema | Las probabilidades ignoran el patrón histórico claro, sorpresa muy probable |
| `divergence 35-50` | Discrepancia alta | Histórico sugiere resultado diferente, analizar con detalle |
| `divergence 25-35` | Discrepancia moderada | Diferencia notable pero no crítica |
| `divergence < 25` | Sin inconsistencia | Diferencia explicable por otros factores, no reportar |

#### Evaluación del Umbral


**Verificación**:
- ❌ `divergencia_historico > 25` → Falso (22.5 < 25)

**❌ NO SE DETECTA INCONSISTENCIA HISTÓRICA**

**Explicación del umbral de 25 puntos**:
- Se requiere una diferencia de **más de 25 puntos porcentuales** para considerar inconsistencia
- En este caso: 22.5 < 25 → La diferencia no es suficientemente grande
- **Interpretación**: Aunque la probabilidad (72.5%) es mayor que la del histórico (50%), la diferencia es aceptable
- Factores como ventaja de local, forma actual o clasificación pueden justificar esta diferencia de 22.5 puntos

**Ejemplo de inconsistencia histórica que SÍ se detectaría**:
```
Si histórico fuera 35% y la probabilidad diera 72.5%:
divergencia = 72.5 - 35.0 = 37.5 > 25 ✅ ALERTA DETECTADA -> DISCREPANCIA ALTA
Interpretación: Las probabilidades ignoran que históricamente este partido tiende al empate/derrota local
```

---

### 4.- Cálculo de Divergencia por Clasificación

**Escenario evaluado**: Victoria local sobrestimada (probabilidad > 65%) con visitante mejor clasificado

```python
if max_prob >= 65 and pos_visitor < pos_local - 8:
    # Detectar inconsistencia
```

**Verificación**:
- ✅ `max_prob >= 65` → Verdadero (72.5% >= 65%)
- ❌ `pos_visitor < pos_local - 8` → Falso (16 no es < 12 - 8 = 4)

**Interpretación**: Getafe está **peor** clasificado (16º vs 12º) pero no hay una diferencia de más de 8 posiciones. No hay contradicción con la clasificación.

**❌ NO SE DETECTA INCONSISTENCIA DE CLASIFICACIÓN**

**Interpretación por diferencia de posiciones**:

| Posiciones de Diferencia | Divergencia Resultante | Interpretación |
|--------------------------|------------------------|----------------|
| <8 posiciones | 0 puntos | Diferencia no reportable |
| 8 posiciones | 20 puntos | Diferencia notable (umbral mínimo) |
| 10 posiciones | 25 puntos | Diferencia significativa |
| 12 posiciones | 30 puntos | Diferencia crítica |
| 15+ posiciones | 37.5+ puntos | Diferencia extrema (favorito muy mal clasificado) |

**Nota**: Diferencias < 8 posiciones no se reportan (justificables por ventaja de campo u otros factores).

---

**Ejemplo con 10 posiciones de diferencia**:

Supongamos un partido **SEVILLA (14º) vs REAL MADRID (4º)** con las siguientes características:

```python
# Datos del partido
max_prob = 68.0  # 68% probabilidad victoria local (victoria del SEVILLA)
pos_local = 14   # Sevilla en 14º posición
pos_visitor = 4  # Real Madrid en 4º posición
```

**Verificación de condiciones**:
```python
if max_prob >= 65 and pos_visitor < pos_local - 8:
    # Calcular divergencia
```

- ✅ `max_prob >= 65` → Verdadero (68% >= 65%)
- ✅ `pos_visitor < pos_local - 8` → Verdadero (4 < 14 - 8 = 6)

**✅ INCONSISTENCIA DE CLASIFICACIÓN DETECTADA**

**Cálculo de divergencia**:
```python
divergence = (pos_local - pos_visitor) * 2.5
           = (14 - 4) * 2.5
           = 10 * 2.5
           = 25.0 puntos
```

**Interpretación**:
- Sevilla está 10 posiciones **por debajo** de Real Madrid en la tabla (14º vs 4º)
- Las probabilidades dan a Sevilla 68% de victoria local
- Esta es una **diferencia significativa**: ¿por qué un equipo 10 puestos peor es tan favorito?
- Posibles factores: ventaja de campo muy fuerte, mala racha del Madrid, lesiones clave del visitante
- **Divergencia de 25 puntos** → Si se combina con divergencia base (18 pts), score total = 43 pts → **⚠️ ALERTA MEDIA**


---


## 🎚️ Niveles de Alerta


Una vez detectadas las inconsistencia más significativa, se aplican estos umbrales globales:

| Nivel de Alerta | Rango de Divergencia | Interpretación | Recomendación |
|-----------------|---------------------|----------------|---------------|
| **🔴 ALERTA ROJA** | `divergence >= 50` | Contradicción crítica entre Probabilidad y contexto | Alta probabilidad de sorpresa, analizar con detalle |
| **🟠 ALERTA MEDIA** | `35 <= divergence < 50` | Contradicción notable y significativa | Sorpresa posible, considerar factores adicionales |
| **🟡 ALERTA** | `threshold <= divergence < 35` | Contradicción detectable pero moderada | Monitorear, puede haber valor oculto |
| 🟢 *Sin alerta* | `divergence < threshold` | Sin inconsistencia significativa | No se reporta |


**Ajuste de sensibilidad con el parámetro `threshold`**: en función del umbral (`threshold`) definido se pueden detectar más o menos alertas:

| Threshold | Tipo de Detección | Alertas Esperadas | Uso Recomendado |
|-----------|-------------------|-------------------|-----------------|
| `threshold = 20` | Sensible | Muchas alertas | Exploración amplia, análisis exhaustivo |
| `threshold = 25` | Estándar | Balance óptimo | **Recomendado** (default) |
| `threshold = 30` | Conservador | Menos alertas | Solo inconsistencias claras |
| `threshold = 40` | Restrictivo | Pocas alertas | Solo casos muy críticos |


---

## 📊 Resultado Final

A continuación se muestra el resultado que devolveria el proceso de detección de sorpresas:

```python
return {
    "jornada": 19,
    "temporada": 2026,
    "threshold": 25.0,
    "total_surprises": 3,  # Este partido + 2 más
    "surprises": [
        # ... otros partidos ...
        {
            "match": "VILLARREAL - GETAFE",
            "alert_level": "🟠 ALERTA MEDIA",
            "inconsistency_type": "streak_inconsistency",
            "description": "Probabilidad alta de victoria local (72%) pero el local está en mala racha y el visitante en buena forma",
            "probabilities": {
                "1": 72.5,
                "X": 18.3,
                "2": 9.2
            },
            "context_factors": {
                "local_recent_form": "Mala racha",
                "visitor_recent_form": "Buena racha"
            },
            "divergence_analysis": {
                "divergence_base": 22.5,
                "divergence_streak": 20.0,
                "divergence_historical": 22.5,
                "divergence_classification": null,
                "total_score": 42.5,
                "selected_inconsistency": "streak_inconsistency",
            }
        }
    ]
}
```

**Desglose del análisis de divergencias**:

- **`divergence_base`** (22.5): Calculada en punto 1 como `max_prob - 50 = 72.5 - 50`
- **`divergence_streak`** (20.0): Calculada en punto 2 como `abs(-7) + 13 = 7 + 13`
  - Esta se suma a la base porque cumplió todas las condiciones (prob≥60%, racha<-6, racha>6)
- **`divergence_historical`** (22.5): Calculada en punto 3 como `72.5 - 50.0`
  - NO se usó porque 22.5 < 25 (umbral de inconsistencia histórica)
- **`divergence_classification`** (null): punto 4 no detectó inconsistencia
  - Getafe está peor clasificado (16º vs 12º), consistente con favorito local
- **`total_score`** (42.5): `divergence_base + divergence_streak = 22.5 + 20.0`
  - Solo incluye las divergencias que se activaron
- **`selected_inconsistency`** ("streak_inconsistency"): La única que cumplió todos los criterios
- **`threshold_used`** (25.0): Umbral configurado en la llamada al detector
- **`exceeded_threshold`** (true): 42.5 ≥ 25.0, por eso se reporta la alerta

---

## 🔑 Puntos Clave del Análisis

#### ¿Por qué se detectó esta sorpresa?

La detección se activó porque se cumplieron **todas las condiciones necesarias**:

1. **Favorito claro identificado**: 
   - Probabilidad del "1" (72.5%) > 50% → Hay un resultado favorito
   - Divergencia base: 72.5 - 50 = 22.5 puntos

2. **Favorito fuerte con mala forma**:
   - Probabilidad >= 60% (72.5%) → Favorito fuerte
   - Racha local = -7 puntos (< -6) → Mala racha significativa (4D-1E)

3. **Rival con excelente forma**:
   - Racha visitante = +13 puntos (> +6) → Buena racha significativa (4V-1E)

4. **Score de divergencia alto**:
   - Cálculo: (72.5 - 50) + |-7| + 13 = 42.5 puntos
   - Supera el threshold de 25.0 configurado
   - Alcanza nivel de ALERTA MEDIA (35 <= 42.5 < 50)

5. **Magnitud extrema de rachas**:
   - Diferencia total: -7 (local) vs +13 (visitante) = 20 puntos de separación
   - Esto representa una contradicción muy marcada en el momentum actual

#### ¿Qué no activó alertas?

1. **Inconsistencia histórica** (no detectada):
   - Tasa histórica local: 8/16 = 50%
   - Probabilidad: 72.5%
   - Diferencia: 22.5 puntos porcentuales
   - ❌ No supera el umbral de 25 puntos requerido
   - **Conclusión**: El histórico sugiere leve favorito local, consistente con probabilidades

2. **Inconsistencia de clasificación** (no detectada):
   - Villarreal: 12º posición
   - Getafe: 16º posición (4 puestos peor)
   - ❌ No cumple condición: visitante NO está 8+ posiciones mejor clasificado
   - **Conclusión**: La clasificación respalda a Villarreal como favorito

#### Interpretación práctica

Esta alerta sugiere que:

1. **Sobrevalorización del factor campo**: 
   - Las probabilidades podrían estar dando demasiado peso al hecho de que Villarreal juega en casa
   - El 72.5% parece no considerar suficientemente el pésimo momento de Villarreal

2. **Momento actual vs datos históricos**:
   - El **momentum reciente** de Getafe (4 victorias) contradice su posición de tabla (16º)
   - La **mala racha** de Villarreal (4 derrotas) contradice su probabilidad de favorito

3. **Oportunidad de apuesta de valor**:
   - La victoria del Getafe o el empate podrían tener más probabilidad real
   - El mercado podría estar infravalorando la forma actual de Getafe
   - Posible partido para apostar contra el favorito (Villarreal)

4. **Contexto relevante**:
   - La forma reciente (últimos 5 partidos) pesa más que la posición en tabla
   - 4 derrotas consecutivas indican problemas actuales graves (lesiones, crisis, cambio técnico)
   - 4 victorias consecutivas indican equipo en racha ascendente

---

## 📝 Conclusión

El proceso de detección de sorpresas es un análisis multi-dimensional que:

1. ✅ Recopila datos de múltiples fuentes (probabilidades + detalles de partidos)
2. ✅ Calcula métricas cuantitativas (rachas, tasas históricas, posiciones)
3. ✅ Evalúa múltiples dimensiones de inconsistencia (forma, histórico, clasificación)
4. ✅ Pondera la magnitud de las contradicciones (divergence_score)
5. ✅ Filtra por relevancia (threshold configurable)
6. ✅ Clasifica la gravedad (ALERTA ROJA/MEDIA/NORMAL)

Este enfoque sistemático permite identificar **oportunidades de valor** donde el contexto actual sugiere resultados diferentes a las probabilidades publicadas.
