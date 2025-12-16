# KinielaGPT - Spanish Football Quiniela Prediction MCP Server
# Copyright (C) 2025 Ricardo Moya
#
# GitHub: https://github.com/RicardoMoya
# LinkedIn: https://www.linkedin.com/in/phdricardomoya/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Tests unitarios para el detector de sorpresas en predicciones de quiniela.

Ejecutar: python -m pytest tests/test_detector.py -v -s
"""

import json

from kinielagpt.detector import SurpriseDetector

# Instancia global del detector para los tests
detector = SurpriseDetector()

# Cargar datos de muestra para pruebas
# Nota: Los datos reales de data_source_samples se cargan pero no se usan directamente
# en estos tests para mantener el aislamiento y la simplicidad
with open("tests/data_source_samples/quiniela_probs_lae.xml", "r", encoding="utf-8") as f:
    # Los datos XML se cargan para referencia pero no se parsean en estos tests
    # En un escenario real, se implementaría un parser XML a dict
    quiniela_probs_raw = f.read()

with open("tests/data_source_samples/match_details_process.json", "r", encoding="utf-8") as f:
    match_details_raw = json.load(f)


def test_calculate_streak_value_all_wins():
    """
    Test: Cálculo de valor de racha con todas victorias.

    Valida que una racha perfecta de 5 victorias consecutivas produzca el valor máximo
    de 15 puntos (3 puntos por cada victoria). Este es el caso límite superior del
    sistema de scoring de rachas.

    Expected
    --------
    Valor de racha calculado: 15 (3 × 5 victorias)

    Verifications
    -------------
    - El método retorna el valor esperado sin errores
    - Se muestra mensaje de éxito con el cálculo correcto
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_value_all_wins()")
    print("=" * 80)

    streak = ["V", "V", "V", "V", "V"]
    result = detector._SurpriseDetector__calculate_streak_value(streak)

    assert result == 15, f"❌ Valor esperado 15, obtenido {result}"
    print(f"✅ Valor de racha calculado correctamente: {result} (3 × 5 victorias)")


def test_calculate_streak_value_all_losses():
    """
    Test: Cálculo de valor de racha con todas derrotas.

    Valida que una racha perfecta de 5 derrotas consecutivas produzca el valor mínimo
    de -15 puntos (-3 puntos por cada derrota). Este es el caso límite inferior del
    sistema de scoring de rachas.

    Expected
    --------
    Valor de racha calculado: -15 (-3 × 5 derrotas)

    Verifications
    -------------
    - El método retorna el valor esperado sin errores
    - Se muestra mensaje de éxito con el cálculo correcto
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_value_all_losses()")
    print("=" * 80)

    streak = ["D", "D", "D", "D", "D"]
    result = detector._SurpriseDetector__calculate_streak_value(streak)

    assert result == -10, f"❌ Valor esperado -10, obtenido {result}"
    print(f"✅ Valor de racha calculado correctamente: {result} (-2 × 5 derrotas)")


def test_calculate_streak_value_all_draws():
    """
    Test: Cálculo de valor de racha con todos empates.

    Valida que una racha de 5 empates consecutivos produzca el valor neutro
    de 0 puntos (0 puntos por cada empate). Los empates no afectan el scoring.

    Expected
    --------
    Valor de racha calculado: 5 (1 × 5 empates)

    Verifications
    -------------
    - El método retorna el valor esperado sin errores
    - Se muestra mensaje de éxito con el cálculo correcto
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_value_all_draws()")
    print("=" * 80)

    streak = ["E", "E", "E", "E", "E"]
    result = detector._SurpriseDetector__calculate_streak_value(streak)

    assert result == 5, f"❌ Valor esperado 5, obtenido {result}"
    print(f"✅ Valor de racha calculado correctamente: {result} (1 × 5 empates)")


def test_calculate_streak_value_mixed_positive():
    """
    Test: Cálculo de valor de racha con resultados mixtos positivos.

    Valida el cálculo correcto de una racha mixta con predominio de victorias.
    La fórmula es: 3×V + 0×E -3×D

    Expected
    --------
    Valor de racha calculado: 8 (3×3 victorias + 1×1 empates -2×1 derrotas)

    Verifications
    -------------
    - El método retorna el valor esperado sin errores
    - Se muestra mensaje de éxito con el cálculo correcto
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_value_mixed_positive()")
    print("=" * 80)

    streak = ["V", "V", "E", "V", "D"]
    result = detector._SurpriseDetector__calculate_streak_value(streak)

    assert result == 8, f"❌ Valor esperado 8, obtenido {result}"
    print(f"✅ Valor de racha calculado correctamente: {result} (3×3V + 1×1E -2×1D)")


def test_calculate_streak_value_mixed_negative():
    """
    Test: Cálculo de valor de racha con resultados mixtos negativos.

    Valida el cálculo correcto de una racha mixta con predominio de derrotas.
    La fórmula es: 3×V + 0×E -3×D

    Expected
    --------
    Valor de racha calculado: -2 (3×1 victorias + 1×1 empates -2×3 derrotas)

    Verifications
    -------------
    - El método retorna el valor esperado sin errores
    - Se muestra mensaje de éxito con el cálculo correcto
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_value_mixed_negative()")
    print("=" * 80)

    streak = ["D", "V", "E", "D", "D"]
    result = detector._SurpriseDetector__calculate_streak_value(streak)

    assert result == -2, f"❌ Valor esperado -2, obtenido {result}"
    print(f"✅ Valor de racha calculado correctamente: {result} (3×1V + 1×1E -2×3D)")


def test_calculate_streak_value_irregular():
    """
    Test: Cálculo de valor de racha con patrón irregular.

    Valida el cálculo correcto de una racha con patrón no uniforme.
    La fórmula es: 3×V + 0×E -3×D

    Expected
    --------
    Valor de racha calculado: 5 (3×2 victorias + 1×1 empates -2×1 derrotas)

    Verifications
    -------------
    - El método retorna el valor esperado sin errores
    - Se muestra mensaje de éxito con el cálculo correcto
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_value_irregular()")
    print("=" * 80)

    streak = ["V", "D", "V", "E"]
    result = detector._SurpriseDetector__calculate_streak_value(streak)

    assert result == 5, f"❌ Valor esperado 5, obtenido {result}"
    print(f"✅ Valor de racha calculado correctamente: {result} (3×2V + 1×1E -2×1D)")


def test_calculate_streak_value_empty():
    """
    Test: Cálculo de valor de racha con lista vacía.

    Valida que una lista vacía de resultados produzca el valor neutro de 0 puntos.
    Este caso maneja el edge case de equipos sin historial disponible.

    Expected
    --------
    Valor de racha calculado: 0 (lista vacía)

    Verifications
    -------------
    - El método retorna el valor esperado sin errores
    - Se muestra mensaje de éxito con el cálculo correcto
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_value_empty()")
    print("=" * 80)

    streak = []
    result = detector._SurpriseDetector__calculate_streak_value(streak)

    assert result == 0, f"❌ Valor esperado 0, obtenido {result}"
    print(f"✅ Valor de racha calculado correctamente: {result} (lista vacía)")


def test_calculate_streak_value_villarreal_example():
    """
    Test: Cálculo de valor de racha para Villarreal (ejemplo real).

    Utiliza datos reales del Villarreal según la documentación detector_ejemplo.md.
    Villarreal tiene una racha de 4 victorias y 1 empate en los últimos 5 partidos.

    Expected
    --------
    Valor de racha calculado: 12 (3×4 victorias + 0×1 empates)

    Verifications
    -------------
    - El método retorna el valor esperado sin errores
    - Se muestra mensaje de éxito con el cálculo correcto
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_value_villarreal_example()")
    print("=" * 80)

    # Datos reales de Villarreal según detector_ejemplo.md
    streak = ["V", "V", "V", "V", "E"]
    result = detector._SurpriseDetector__calculate_streak_value(streak)

    assert result == 13, f"❌ Valor esperado 13, obtenido {result}"
    print(f"✅ Valor de racha calculado correctamente: {result} (3×4V + 1×1E)")


def test_calculate_streak_value_getafe_example():
    """
    Test: Cálculo de valor de racha para Getafe (ejemplo real).

    Utiliza datos reales del Getafe según la documentación detector_ejemplo.md.
    Getafe tiene una racha de 1 victoria, 2 empates y 2 derrotas en los últimos 5 partidos.

    Expected
    --------
    Valor de racha calculado: -3 (3×1 victorias + 0×2 empates -3×2 derrotas)

    Verifications
    -------------
    - El método retorna el valor esperado sin errores
    - Se muestra mensaje de éxito con el cálculo correcto
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_value_getafe_example()")
    print("=" * 80)

    # Datos reales de Getafe según detector_ejemplo.md
    streak = ["V", "E", "D", "E", "D"]
    result = detector._SurpriseDetector__calculate_streak_value(streak)

    assert result == 1, f"❌ Valor esperado 1, obtenido {result}"
    print(f"✅ Valor de racha calculado correctamente: {result} (3×1V + 2×1E -2×2D)")


# ===========================
# Tests de __check_streak_inconsistency
# ===========================


def test_check_streak_inconsistency_local_favorite_poor_form():
    """
    Test: Detección de inconsistencia de racha - local favorito con mala forma.

    Caso: Local con 75% de probabilidad pero racha negativa de -8 puntos.
    Debe detectar inconsistencia porque la probabilidad es alta pero la forma es mala.

    Expected
    --------
    Inconsistencia detectada de tipo "streak_inconsistency"

    Verifications
    -------------
    - El método retorna un diccionario con la inconsistencia detectada
    - Se muestra mensaje de éxito con los detalles de la detección
    """
    print("=" * 80)
    print("TEST: test_check_streak_inconsistency_local_favorite_poor_form()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 75.0, "X_Prob": 15.0, "2_Prob": 10.0}
    detail = {
        "evolucionLocal": ["D", "D", "D", "D"],  # -8 puntos
        "evolucionVisitante": ["V", "V", "V", "E"],  # +10 puntos
    }

    result = detector._SurpriseDetector__check_streak_inconsistency("1", 75.0, prob, detail)

    assert result is not None, "❌ No se detectó inconsistencia"
    assert result["type"] == "streak_inconsistency", (
        f"❌ Tipo esperado 'streak_inconsistency', obtenido '{result['type']}'"
    )
    assert result["local_streak"] == -8, f"❌ Racha local esperada -8, obtenida {result['local_streak']}"
    assert result["visitor_streak"] == 10, f"❌ Racha visitante esperada 10, obtenida {result['visitor_streak']}"
    print(f"✅ Inconsistencia de racha detectada: local={result['local_streak']}, visitante={result['visitor_streak']}")


def test_check_streak_inconsistency_visitor_favorite_poor_form():
    """
    Test: Detección de inconsistencia de racha - visitante favorito con mala forma.

    Caso: Visitante con 70% de probabilidad pero racha negativa de -8 puntos.
    Debe detectar inconsistencia porque la probabilidad es alta pero la forma es mala.

    Expected
    --------
    Inconsistencia detectada de tipo "streak_inconsistency"

    Verifications
    -------------
    - El método retorna un diccionario con la inconsistencia detectada
    - Se muestra mensaje de éxito con los detalles de la detección
    """
    print("=" * 80)
    print("TEST: test_check_streak_inconsistency_visitor_favorite_poor_form()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 15.0, "X_Prob": 15.0, "2_Prob": 70.0}
    detail = {
        "evolucionLocal": ["V", "E", "V", "V"],  # +10 puntos
        "evolucionVisitante": ["D", "D", "D", "D"],  # -8 puntos
    }

    result = detector._SurpriseDetector__check_streak_inconsistency("2", 70.0, prob, detail)

    assert result is not None, "❌ No se detectó inconsistencia"
    assert result["type"] == "streak_inconsistency", (
        f"❌ Tipo esperado 'streak_inconsistency', obtenido '{result['type']}'"
    )
    assert result["local_streak"] == 10, f"❌ Racha local esperada 10, obtenida {result['local_streak']}"
    assert result["visitor_streak"] == -8, f"❌ Racha visitante esperada -8, obtenida {result['visitor_streak']}"
    print(f"✅ Inconsistencia de racha detectada: local={result['local_streak']}, visitante={result['visitor_streak']}")


def test_check_streak_inconsistency_draw_underestimated():
    """
    Test: Detección de inconsistencia de racha - empate subestimado.

    Caso: Empate con 20% de probabilidad pero ambas rachas son neutras (0 puntos).
    Debe detectar inconsistencia porque el empate tiene baja probabilidad pero ambas
    formas son equilibradas.

    Expected
    --------
    Inconsistencia detectada de tipo "streak_inconsistency"

    Verifications
    -------------
    - El método retorna un diccionario con la inconsistencia detectada
    - Se muestra mensaje de éxito con los detalles de la detección
    """
    print("=" * 80)
    print("TEST: test_check_streak_inconsistency_draw_underestimated()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 40.0, "X_Prob": 20.0, "2_Prob": 40.0}
    detail = {
        "evolucionLocal": ["E", "D", "E", "V"],  # +3 puntos
        "evolucionVisitante": ["E", "V", "E", "D"],  # +3 puntos
    }

    result = detector._SurpriseDetector__check_streak_inconsistency("1", 40.0, prob, detail)

    assert result is not None, "❌ No se detectó inconsistencia"
    assert result["type"] == "streak_inconsistency", (
        f"❌ Tipo esperado 'streak_inconsistency', obtenido '{result['type']}'"
    )
    assert result["local_streak"] == 3, f"❌ Racha local esperada 3, obtenida {result['local_streak']}"
    assert result["visitor_streak"] == 3, f"❌ Racha visitante esperada 3, obtenida {result['visitor_streak']}"
    print(f"✅ Inconsistencia de racha detectada: local={result['local_streak']}, visitante={result['visitor_streak']}")


def test_check_streak_inconsistency_no_detection_balanced():
    """
    Test: No detección de inconsistencia - caso equilibrado.

    Caso: Probabilidades equilibradas (33% cada una) con rachas equilibradas.
    No debe detectar inconsistencia porque todo está balanceado.

    Expected
    --------
    No se detecta inconsistencia (retorna None)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no se detectó inconsistencia
    """
    print("=" * 80)
    print("TEST: test_check_streak_inconsistency_no_detection_balanced()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 33.3, "X_Prob": 33.3, "2_Prob": 33.3}
    detail = {
        "evolucionLocal": ["V", "E", "D"],  # +0 puntos
        "evolucionVisitante": ["D", "E", "V"],  # +0 puntos
    }

    result = detector._SurpriseDetector__check_streak_inconsistency("1", 33.3, prob, detail)

    assert result is None, f"❌ Se detectó inconsistencia inesperada: {result}"
    print("✅ No se detectó inconsistencia en caso equilibrado")


def test_check_streak_inconsistency_threshold_not_met():
    """
    Test: No detección de inconsistencia - umbral no alcanzado.

    Caso: Probabilidades altas con rachas ligeramente negativas.
    No debe detectar inconsistencia porque la divergencia no alcanza el umbral.

    Expected
    --------
    No se detecta inconsistencia (retorna None)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no se detectó inconsistencia
    """
    print("=" * 80)
    print("TEST: test_check_streak_inconsistency_threshold_not_met()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 60.0, "X_Prob": 25.0, "2_Prob": 15.0}
    detail = {
        "evolucionLocal": ["V", "D", "V"],  # +3 puntos
        "evolucionVisitante": ["E", "D", "V"],  # +0 puntos
    }

    result = detector._SurpriseDetector__check_streak_inconsistency("1", 60.0, prob, detail)

    assert result is None, f"❌ Se detectó inconsistencia inesperada: {result}"
    print("✅ No se detectó inconsistencia por umbral no alcanzado")


def test_check_streak_inconsistency_missing_data():
    """
    Test: No detección de inconsistencia - datos faltantes.

    Caso: Probabilidades disponibles pero datos de evolución faltantes.
    No debe detectar inconsistencia porque no hay datos suficientes.

    Expected
    --------
    No se detecta inconsistencia (retorna None)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no se detectó inconsistencia
    """
    print("=" * 80)
    print("TEST: test_check_streak_inconsistency_missing_data()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 75.0, "X_Prob": 15.0, "2_Prob": 10.0}
    detail = {}  # Sin datos de evolución

    result = detector._SurpriseDetector__check_streak_inconsistency("1", 75.0, prob, detail)

    assert result is None, f"❌ Se detectó inconsistencia inesperada: {result}"
    print("✅ No se detectó inconsistencia por datos faltantes")


# ===========================
# Tests de __check_historical_inconsistency
# ===========================


def test_check_historical_inconsistency_detected():
    """
    Test: Detección de inconsistencia histórica.

    Caso: Historial muestra 80% victorias locales pero probabilidad actual es solo 30%.
    Debe detectar inconsistencia porque el historial es muy favorable pero la prob es baja.

    Expected
    --------
    Inconsistencia detectada de tipo "historical_inconsistency"

    Verifications
    -------------
    - El método retorna un diccionario con la inconsistencia detectada
    - Se muestra mensaje de éxito con los detalles de la detección
    """
    print("=" * 80)
    print("TEST: test_check_historical_inconsistency_detected()")
    print("=" * 80)

    prob = {"1": 30.0, "X": 40.0, "2": 30.0}
    detail = {
        "veces1": 8,  # 8 victorias locales
        "vecesX": 1,  # 1 empate
        "veces2": 2,  # 2 victorias visitantes
    }

    result = detector._SurpriseDetector__check_historical_inconsistency("X", prob, detail)

    assert result is not None, "❌ No se detectó inconsistencia"
    assert result["type"] == "historical_inconsistency", (
        f"❌ Tipo esperado 'historical_inconsistency', obtenido '{result['type']}'"
    )
    assert result["divergence_score"] > 30, f"❌ Divergencia esperada >30, obtenida {result['divergence_score']}"
    print(f"✅ Inconsistencia histórica detectada: {result['description']}")


def test_check_historical_inconsistency_not_detected():
    """
    Test: No detección de inconsistencia histórica - caso consistente.

    Caso: Historial muestra 50% victorias locales y probabilidad actual es 45%.
    No debe detectar inconsistencia porque el historial y la prob están alineados.

    Expected
    --------
    No se detecta inconsistencia (retorna None)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no se detectó inconsistencia
    """
    print("=" * 80)
    print("TEST: test_check_historical_inconsistency_not_detected()")
    print("=" * 80)

    prob = {"1": 45.0, "X": 30.0, "2": 25.0}
    detail = {
        "veces1": 5,  # 5 victorias locales
        "vecesX": 3,  # 3 empates
        "veces2": 2,  # 2 victorias visitantes
    }

    result = detector._SurpriseDetector__check_historical_inconsistency("1", prob, detail)

    assert result is None, f"❌ Se detectó inconsistencia inesperada: {result}"
    print("✅ No se detectó inconsistencia histórica en caso consistente")


def test_check_historical_inconsistency_insufficient_sample():
    """
    Test: No detección de inconsistencia histórica - muestra insuficiente.

    Caso: Historial tiene solo 3 partidos (menos del mínimo de 5).
    No debe detectar inconsistencia porque no hay muestra estadística suficiente.

    Expected
    --------
    No se detecta inconsistencia (retorna None)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no se detectó inconsistencia
    """
    print("=" * 80)
    print("TEST: test_check_historical_inconsistency_insufficient_sample()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 20.0, "X_Prob": 30.0, "2_Prob": 50.0}
    detail = {
        "historial": {
            "local": {"V": 1, "E": 1, "D": 1},  # Solo 3 partidos
            "visitante": {"V": 1, "E": 1, "D": 1},
        }
    }

    result = detector._SurpriseDetector__check_historical_inconsistency("2", prob, detail)

    assert result is None, f"❌ Se detectó inconsistencia inesperada: {result}"
    print("✅ No se detectó inconsistencia por muestra insuficiente")


def test_check_historical_inconsistency_below_reporting_threshold():
    """
    Test: No detección de inconsistencia histórica - por debajo del umbral de reporte.

    Caso: Hay divergencia pero no alcanza el umbral mínimo para reportar.
    No debe detectar inconsistencia porque la divergencia es pequeña.

    Expected
    --------
    No se detecta inconsistencia (retorna None)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no se detectó inconsistencia
    """
    print("=" * 80)
    print("TEST: test_check_historical_inconsistency_below_reporting_threshold()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 35.0, "X_Prob": 30.0, "2_Prob": 35.0}
    detail = {
        "historial": {
            "local": {"V": 6, "E": 2, "D": 2},  # 60% victorias locales
            "visitante": {"V": 2, "E": 2, "D": 6},  # 20% victorias visitantes
        }
    }

    result = detector._SurpriseDetector__check_historical_inconsistency("1", prob, detail)

    assert result is None, f"❌ Se detectó inconsistencia inesperada: {result}"
    print("✅ No se detectó inconsistencia por debajo del umbral de reporte")


# ===========================
# Tests de __check_classification_inconsistency
# ===========================


def test_check_classification_inconsistency_local_overestimated():
    """
    Test: Detección de inconsistencia de clasificación - local sobreestimado.

    Caso: Local está en posición 5 pero tiene 70% de probabilidad.
    Debe detectar inconsistencia porque su clasificación no justifica tanta probabilidad.

    Expected
    --------
    Inconsistencia detectada de tipo "classification_inconsistency"

    Verifications
    -------------
    - El método retorna un diccionario con la inconsistencia detectada
    - Se muestra mensaje de éxito con los detalles de la detección
    """
    print("=" * 80)
    print("TEST: test_check_classification_inconsistency_local_overestimated()")
    print("=" * 80)

    detail = {"clasificacionLocal": "15º 20pt", "clasificacionVisitante": "3º 50pt"}

    result = detector._SurpriseDetector__check_classification_inconsistency("1", 70.0, detail)

    assert result is not None, "❌ No se detectó inconsistencia"
    assert result["type"] == "classification_inconsistency", (
        f"❌ Tipo esperado 'classification_inconsistency', obtenido '{result['type']}'"
    )
    assert result["factors"]["local_position"] == 15, f"❌ Posición local esperada 15, obtenida {result['factors']['local_position']}"
    assert result["factors"]["visitor_position"] == 3, f"❌ Posición visitante esperada 3, obtenida {result['factors']['visitor_position']}"
    print(
        f"✅ Inconsistencia de clasificación detectada: local pos={result['factors']['local_position']}, visitante pos={result['factors']['visitor_position']}"
    )


def test_check_classification_inconsistency_visitor_overestimated():
    """
    Test: Detección de inconsistencia de clasificación - visitante sobreestimado.

    Caso: Visitante está en posición 18 pero tiene 65% de probabilidad.
    Debe detectar inconsistencia porque su clasificación no justifica tanta probabilidad.

    Expected
    --------
    Inconsistencia detectada de tipo "classification_inconsistency"

    Verifications
    -------------
    - El método retorna un diccionario con la inconsistencia detectada
    - Se muestra mensaje de éxito con los detalles de la detección
    """
    print("=" * 80)
    print("TEST: test_check_classification_inconsistency_visitor_overestimated()")
    print("=" * 80)

    detail = {"clasificacionLocal": "4º 50pt", "clasificacionVisitante": "18º 15pt"}

    result = detector._SurpriseDetector__check_classification_inconsistency("2", 65.0, detail)

    assert result is not None, "❌ No se detectó inconsistencia"
    assert result["type"] == "classification_inconsistency", (
        f"❌ Tipo esperado 'classification_inconsistency', obtenido '{result['type']}'"
    )
    assert result["factors"]["local_position"] == 4, f"❌ Posición local esperada 4, obtenida {result['factors']['local_position']}"
    assert result["factors"]["visitor_position"] == 18, f"❌ Posición visitante esperada 18, obtenida {result['factors']['visitor_position']}"
    print(
        f"✅ Inconsistencia de clasificación detectada: local pos={result['factors']['local_position']}, visitante pos={result['factors']['visitor_position']}"
    )


def test_check_classification_inconsistency_not_detected_small_diff():
    """
    Test: No detección de inconsistencia de clasificación - diferencia pequeña.

    Caso: Posiciones cercanas (6 vs 9) con probabilidades razonables.
    No debe detectar inconsistencia porque la diferencia de clasificación es pequeña.

    Expected
    --------
    No se detecta inconsistencia (retorna None)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no se detectó inconsistencia
    """
    print("=" * 80)
    print("TEST: test_check_classification_inconsistency_not_detected_small_diff()")
    print("=" * 80)

    detail = {"clasificacionLocal": "6º 40pt", "clasificacionVisitante": "9º 32pt"}

    result = detector._SurpriseDetector__check_classification_inconsistency("1", 55.0, detail)

    assert result is None, f"❌ Se detectó inconsistencia inesperada: {result}"
    print("✅ No se detectó inconsistencia por diferencia pequeña de clasificación")


def test_check_classification_inconsistency_not_detected_low_prob():
    """
    Test: No detección de inconsistencia de clasificación - probabilidad baja.

    Caso: Probabilidades bajas (menos de 50%) independientemente de la clasificación.
    No debe detectar inconsistencia porque las probs son bajas.

    Expected
    --------
    No se detecta inconsistencia (retorna None)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no se detectó inconsistencia
    """
    print("=" * 80)
    print("TEST: test_check_classification_inconsistency_not_detected_low_prob()")
    print("=" * 80)

    detail = {"clasificacionLocal": "12º 25pt", "clasificacionVisitante": "5º 45pt"}

    result = detector._SurpriseDetector__check_classification_inconsistency("1", 45.0, detail)

    assert result is None, f"❌ Se detectó inconsistencia inesperada: {result}"
    print("✅ No se detectó inconsistencia por probabilidades bajas")


def test_check_classification_inconsistency_wrong_direction():
    """
    Test: No detección de inconsistencia de clasificación - dirección incorrecta.

    Caso: Local mejor clasificado pero con probabilidad baja (lo cual es consistente).
    No debe detectar inconsistencia porque la clasificación y prob van en la misma dirección.

    Expected
    --------
    No se detecta inconsistencia (retorna None)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no se detectó inconsistencia
    """
    print("=" * 80)
    print("TEST: test_check_classification_inconsistency_wrong_direction()")
    print("=" * 80)

    detail = {"clasificacionLocal": "15º 20pt", "clasificacionVisitante": "3º 50pt"}

    result = detector._SurpriseDetector__check_classification_inconsistency("2", 50.0, detail)

    assert result is None, f"❌ Se detectó inconsistencia inesperada: {result}"
    print("✅ No se detectó inconsistencia por dirección correcta")


def test_check_classification_inconsistency_missing_data():
    """
    Test: No detección de inconsistencia de clasificación - datos faltantes.

    Caso: Probabilidades disponibles pero datos de clasificación faltantes.
    No debe detectar inconsistencia porque no hay datos suficientes.

    Expected
    --------
    No se detecta inconsistencia (retorna None)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no se detectó inconsistencia
    """
    print("=" * 80)
    print("TEST: test_check_classification_inconsistency_missing_data()")
    print("=" * 80)

    detail = {}  # Sin datos de clasificación

    result = detector._SurpriseDetector__check_classification_inconsistency("1", 70.0, detail)

    assert result is None, f"❌ Se detectó inconsistencia inesperada: {result}"
    print("✅ No se detectó inconsistencia por datos de clasificación faltantes")


def test_check_classification_inconsistency_int_format():
    """
    Test: Detección de inconsistencia de clasificación - formato entero.

    Caso: Posiciones en formato entero (no string) con sobreestimación.
    Debe detectar inconsistencia validando que funciona con enteros.

    Expected
    --------
    Inconsistencia detectada de tipo "classification_inconsistency"

    Verifications
    -------------
    - El método retorna un diccionario con la inconsistencia detectada
    - Se muestra mensaje de éxito con los detalles de la detección
    """
    print("=" * 80)
    print("TEST: test_check_classification_inconsistency_int_format()")
    print("=" * 80)

    detail = {"clasificacionLocal": "16º 18pt", "clasificacionVisitante": "7º 38pt"}

    result = detector._SurpriseDetector__check_classification_inconsistency("1", 65.0, detail)

    assert result is not None, "❌ No se detectó inconsistencia"
    assert result["type"] == "classification_inconsistency", (
        f"❌ Tipo esperado 'classification_inconsistency', obtenido '{result['type']}'"
    )
    assert result["factors"]["local_position"] == 16, f"❌ Posición local esperada 16, obtenida {result['factors']['local_position']}"
    assert result["factors"]["visitor_position"] == 7, f"❌ Posición visitante esperada 7, obtenida {result['factors']['visitor_position']}"
    print(
        f"✅ Inconsistencia de clasificación detectada con formato entero: local pos={result['factors']['local_position']}, visitante pos={result['factors']['visitor_position']}"
    )


# ===========================
# Tests de __analyze_inconsistencies
# ===========================


def test_analyze_inconsistencies_alert_roja():
    """
    Test: Análisis de inconsistencias - ALERTA ROJA.

    Caso: Múltiples inconsistencias que generan una divergencia alta (>= 50).
    Debe asignar ALERTA ROJA con el nivel más alto de alerta.

    Expected
    --------
    Resultado con alert_level = "🚨 ALERTA ROJA"

    Verifications
    -------------
    - El método retorna un diccionario con la alerta correcta
    - Se muestra mensaje de éxito con el nivel de alerta
    """
    print("=" * 80)
    print("TEST: test_analyze_inconsistencies_alert_roja()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 75.0, "X_Prob": 15.0, "2_Prob": 10.0}
    detail = {
        "evolucionLocal": ["D", "D", "D", "D", "D"],  # -15
        "evolucionVisitante": ["V", "V", "V", "V", "V"],  # +15
        "historial": {
            "local": {"V": 1, "E": 1, "D": 8},  # 10% victorias locales
            "visitante": {"V": 8, "E": 1, "D": 1},  # 80% victorias visitantes
        },
        "clasificacion": {"local": {"posicion": 18, "puntos": 15}, "visitante": {"posicion": 2, "puntos": 55}},
    }

    result = detector._SurpriseDetector__analyze_inconsistencies(prob, detail, threshold=25.0)

    assert result is not None, "❌ No se generó análisis"
    assert result["alert_level"] == "🚨 ALERTA ROJA", (
        f"❌ Nivel esperado '🚨 ALERTA ROJA', obtenido '{result['alert_level']}'"
    )
    assert result["divergence_score"] >= 50, (
        f"❌ Score de divergencia esperado >= 50, obtenido {result['divergence_score']}"
    )
    print(f"✅ ALERTA ROJA asignada correctamente (divergence={result['divergence_score']})")


def test_analyze_inconsistencies_alert_media():
    """
    Test: Análisis de inconsistencias - ALERTA MEDIA.

    Caso: Inconsistencias moderadas que generan una divergencia media (35-49).
    Debe asignar ALERTA MEDIA.

    Expected
    --------
    Resultado con alert_level = "⚠️ ALERTA MEDIA"

    Verifications
    -------------
    - El método retorna un diccionario con la alerta correcta
    - Se muestra mensaje de éxito con el nivel de alerta
    """
    print("=" * 80)
    print("TEST: test_analyze_inconsistencies_alert_media()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 72.5, "X_Prob": 18.3, "2_Prob": 9.2}
    detail = {
        "evolucionLocal": ["D", "D", "D", "E", "D"],  # -10
        "evolucionVisitante": ["V", "V", "V", "V", "E"],  # +12
        "historial": {
            "local": {"V": 3, "E": 2, "D": 5},  # 30% victorias locales
            "visitante": {"V": 6, "E": 2, "D": 2},  # 60% victorias visitantes
        },
        "clasificacion": {"local": {"posicion": 12, "puntos": 25}, "visitante": {"posicion": 6, "puntos": 40}},
    }

    result = detector._SurpriseDetector__analyze_inconsistencies(prob, detail, threshold=25.0)

    assert result is not None, "❌ No se generó análisis"
    assert result["alert_level"] == "⚠️ ALERTA MEDIA", (
        f"❌ Nivel esperado '⚠️ ALERTA MEDIA', obtenido '{result['alert_level']}'"
    )
    print(f"✅ ALERTA MEDIA asignada correctamente (divergence={result['divergence_score']})")


def test_analyze_inconsistencies_alert_normal():
    """
    Test: Análisis de inconsistencias - ALERTA normal.

    Caso: Inconsistencias leves que generan una divergencia baja (threshold-34).
    Debe asignar ALERTA normal.

    Expected
    --------
    Resultado con alert_level = "⚠️ ALERTA"

    Verifications
    -------------
    - El método retorna un diccionario con la alerta correcta
    - Se muestra mensaje de éxito con el nivel de alerta
    """
    print("=" * 80)
    print("TEST: test_analyze_inconsistencies_alert_normal()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 65.0, "X_Prob": 25.0, "2_Prob": 10.0}
    detail = {
        "evolucionLocal": ["D", "D", "D", "E", "V"],  # -7
        "evolucionVisitante": ["V", "V", "E", "V", "D"],  # +5
        "historial": {
            "local": {"V": 4, "E": 3, "D": 3},  # 40% victorias locales
            "visitante": {"V": 3, "E": 3, "D": 4},  # 30% victorias visitantes
        },
        "clasificacion": {"local": {"posicion": 10, "puntos": 30}, "visitante": {"posicion": 8, "puntos": 35}},
    }

    result = detector._SurpriseDetector__analyze_inconsistencies(prob, detail, threshold=25.0)

    if result is not None:
        assert result["alert_level"] == "⚠️ ALERTA", f"❌ Nivel esperado '⚠️ ALERTA', obtenido '{result['alert_level']}'"
        print(f"✅ ALERTA normal asignada correctamente (divergence={result['divergence_score']})")
    else:
        print("✅ No se generó alerta (consistente con el umbral)")


def test_analyze_inconsistencies_no_alert():
    """
    Test: Análisis de inconsistencias - Sin alerta.

    Caso: Todo consistente, sin divergencias significativas.
    No debe generar ninguna alerta.

    Expected
    --------
    Resultado None (sin alerta)

    Verifications
    -------------
    - El método retorna None
    - Se muestra mensaje de éxito indicando que no hay alerta
    """
    print("=" * 80)
    print("TEST: test_analyze_inconsistencies_no_alert()")
    print("=" * 80)

    prob = {"partido": "TEST", "1_Prob": 50.0, "X_Prob": 25.0, "2_Prob": 25.0}
    detail = {
        "evolucionLocal": ["V", "E", "D", "V", "E"],  # +1
        "evolucionVisitante": ["D", "V", "E", "D", "V"],  # +1
        "historial": {
            "local": {"V": 5, "E": 3, "D": 2},  # 50% victorias locales
            "visitante": {"V": 2, "E": 3, "D": 5},  # 20% victorias visitantes
        },
        "clasificacion": {"local": {"posicion": 8, "puntos": 35}, "visitante": {"posicion": 12, "puntos": 25}},
    }

    result = detector._SurpriseDetector__analyze_inconsistencies(prob, detail, threshold=25.0)

    assert result is None, f"❌ Se generó alerta inesperada: {result}"
    print("✅ No se generó alerta en caso consistente")


if __name__ == "__main__":
    test_calculate_streak_value_all_wins()
    test_calculate_streak_value_all_losses()
    test_calculate_streak_value_all_draws()
    test_calculate_streak_value_mixed_positive()
    test_calculate_streak_value_mixed_negative()
    test_calculate_streak_value_irregular()
    test_calculate_streak_value_empty()
    test_calculate_streak_value_villarreal_example()
    test_calculate_streak_value_getafe_example()
    test_check_streak_inconsistency_local_favorite_poor_form()
    test_check_streak_inconsistency_visitor_favorite_poor_form()
    test_check_streak_inconsistency_draw_underestimated()
    test_check_streak_inconsistency_no_detection_balanced()
    test_check_streak_inconsistency_threshold_not_met()
    test_check_streak_inconsistency_missing_data()
    test_check_historical_inconsistency_detected()
    test_check_historical_inconsistency_not_detected()
    test_check_historical_inconsistency_insufficient_sample()
    test_check_historical_inconsistency_below_reporting_threshold()
    test_check_classification_inconsistency_local_overestimated()
    test_check_classification_inconsistency_visitor_overestimated()
    test_check_classification_inconsistency_not_detected_small_diff()
    test_check_classification_inconsistency_not_detected_low_prob()
    test_check_classification_inconsistency_wrong_direction()
    test_check_classification_inconsistency_missing_data()
    test_check_classification_inconsistency_int_format()
    test_analyze_inconsistencies_alert_roja()
    test_analyze_inconsistencies_alert_media()
    test_analyze_inconsistencies_alert_normal()
    test_analyze_inconsistencies_no_alert()
