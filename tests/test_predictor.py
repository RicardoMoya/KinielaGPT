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
Tests unitarios para la clase KinielaPredictor.

Ejecutar: python -m pytest tests/test_predictor.py -v -s

Este módulo contiene pruebas exhaustivas para todos los métodos privados de la clase KinielaPredictor,
excepto el método predict() que es el punto de entrada público. Las pruebas cubren:

- Estrategias de predicción: conservadora, arriesgada y personalizada
- Análisis contextual de partidos
- Ajuste de probabilidades según contexto
- Generación de justificaciones
- Optimización de distribuciones
- Validación de distribuciones personalizadas
- Cálculo de resúmenes

Las pruebas utilizan datos simulados que representan escenarios realistas de partidos de fútbol
español, incluyendo probabilidades LAE y detalles de clasificación histórica.
"""

import json

from kinielagpt.predictor import KinielaPredictor

# Instancia global del predictor para los tests
predictor = KinielaPredictor()

# Cargar datos de muestra para pruebas
# Nota: Los datos reales de data_source_samples se cargan pero no se usan directamente
# en estos tests para mantener el aislamiento y la simplicidad
with open('tests/data_source_samples/quiniela_probs_lae.xml', 'r', encoding='utf-8') as f:
    # Los datos XML se cargan para referencia pero no se parsean en estos tests
    # En un escenario real, se implementaría un parser XML a dict
    quiniela_probs_raw = f.read()

with open('tests/data_source_samples/match_details_process.json', 'r', encoding='utf-8') as f:
    match_details_raw = json.load(f)


def test_predict_conservative():
    """
    Prueba la estrategia conservadora de predicción.

    La estrategia conservadora selecciona siempre el signo con mayor probabilidad LAE.
    Este test verifica que:
    - Se selecciona correctamente el signo con mayor probabilidad
    - Se asigna el nivel de confianza apropiado
    - Se genera la justificación correcta

    Expected
    --------
    Predicciones correctas: '1' para primer partido, 'X' para segundo
    - Confianza: 'ALTA' para 60%, 'BAJA' para 40%

    Verifications
    -------------
    - El método retorna predicciones válidas
    - Se muestran mensajes de éxito con los resultados
    """
    print("=" * 80)
    print("TEST: test_predict_conservative()")
    print("=" * 80)

    # Datos de prueba: partido con victoria local clara y empate probable
    sample_probs = [
        {'1_Prob': 60.0, 'X_Prob': 25.0, '2_Prob': 15.0, 'partido': 'A | B'},
        {'1_Prob': 30.0, 'X_Prob': 40.0, '2_Prob': 30.0, 'partido': 'C | D'}
    ]
    sample_details = [
        {'clasificacionLocal': 1, 'clasificacionVisitante': 2, 'veces1': 5, 'vecesX': 3, 'veces2': 2},
        {'clasificacionLocal': 2, 'clasificacionVisitante': 1, 'veces1': 2, 'vecesX': 5, 'veces2': 3}
    ]

    preds = predictor._KinielaPredictor__predict_conservative(sample_probs, sample_details)

    # Verificaciones
    assert preds[0]['prediction'] == '1', "❌ Primera predicción debería ser '1'"
    assert preds[1]['prediction'] == 'X', "❌ Segunda predicción debería ser 'X'"
    assert preds[0]['confidence'] == 'ALTA', "❌ Primera confianza debería ser 'ALTA'"
    assert preds[1]['confidence'] == 'BAJA', "❌ Segunda confianza debería ser 'BAJA'"
    assert 'Probabilidad LAE' in preds[0]['reasoning'], "❌ Falta 'Probabilidad LAE' en justificación"

    print("✅ Predicción conservadora: signos correctos")
    print(f"   Partido 1: {preds[0]['prediction']} (confianza: {preds[0]['confidence']})")
    print(f"   Partido 2: {preds[1]['prediction']} (confianza: {preds[1]['confidence']})")
    print("✅ Justificaciones incluyen probabilidades LAE")


def test_predict_risky():
    """
    Prueba la estrategia arriesgada de predicción.

    La estrategia arriesgada ajusta las probabilidades LAE según análisis contextual
    (clasificación, histórico, rachas). Este test verifica que:
    - Se aplican ajustes contextuales
    - Se generan probabilidades ajustadas
    - Se incluyen factores contextuales en la respuesta

    Expected
    --------
    Predicciones con probabilidades ajustadas y factores contextuales

    Verifications
    -------------
    - El método retorna predicciones válidas con ajustes
    - Se muestran mensajes de éxito
    """
    print("=" * 80)
    print("TEST: test_predict_risky()")
    print("=" * 80)

    sample_probs = [
        {'1_Prob': 60.0, 'X_Prob': 25.0, '2_Prob': 15.0, 'partido': 'A | B'},
        {'1_Prob': 30.0, 'X_Prob': 40.0, '2_Prob': 30.0, 'partido': 'C | D'}
    ]
    sample_details = [
        {'clasificacionLocal': 1, 'clasificacionVisitante': 2, 'veces1': 5, 'vecesX': 3, 'veces2': 2},
        {'clasificacionLocal': 2, 'clasificacionVisitante': 1, 'veces1': 2, 'vecesX': 5, 'veces2': 3}
    ]

    preds = predictor._KinielaPredictor__predict_risky(sample_probs, sample_details)

    # Verificaciones
    assert len(preds) == 2, "❌ Deberían haber 2 predicciones"
    assert all('prediction' in p for p in preds), "❌ Todas las predicciones deben tener 'prediction'"
    assert all('adjusted_probabilities' in p for p in preds), "❌ Todas deben tener 'adjusted_probabilities'"
    assert all('context_factors' in p for p in preds), "❌ Todas deben tener 'context_factors'"
    assert all('reasoning' in p for p in preds), "❌ Todas deben tener 'reasoning'"

    print("✅ Estrategia arriesgada: predicciones con ajustes contextuales")
    print(f"   Número de predicciones: {len(preds)}")
    print(f"   Todas incluyen probabilidades ajustadas: {all('adjusted_probabilities' in p for p in preds)}")
    print(f"   Todas incluyen factores contextuales: {all('context_factors' in p for p in preds)}")


def test_predict_custom():
    """
    Prueba la estrategia personalizada de predicción.

    La estrategia personalizada optimiza la asignación de signos para alcanzar
    una distribución específica de 1s, Xs y 2s. Este test verifica que:
    - Se respeta la distribución objetivo
    - Se optimiza según scores contextuales
    - Se asignan signos a todos los partidos
    """
    print("=" * 80)
    print("TEST: test_predict_custom()")
    print("=" * 80)

    sample_probs = [
        {'1_Prob': 60.0, 'X_Prob': 25.0, '2_Prob': 15.0, 'partido': 'A | B'},
        {'1_Prob': 30.0, 'X_Prob': 40.0, '2_Prob': 30.0, 'partido': 'C | D'}
    ]
    sample_details = [
        {'clasificacionLocal': 1, 'clasificacionVisitante': 2, 'veces1': 5, 'vecesX': 3, 'veces2': 2},
        {'clasificacionLocal': 2, 'clasificacionVisitante': 1, 'veces1': 2, 'vecesX': 5, 'veces2': 3}
    ]
    custom_dist = {'1': 1, 'X': 1, '2': 0}  # 1 uno, 1 empate, 0 doses

    preds = predictor._KinielaPredictor__predict_custom(sample_probs, sample_details, custom_dist)

    # Verificaciones
    assert len(preds) == 2, "❌ Deberían haber 2 predicciones"
    assert sum(1 for p in preds if p['prediction'] == '1') == 1, "❌ Debería haber 1 predicción '1'"
    assert sum(1 for p in preds if p['prediction'] == 'X') == 1, "❌ Debería haber 1 predicción 'X'"
    assert sum(1 for p in preds if p['prediction'] == '2') == 0, "❌ Debería haber 0 predicciones '2'"
    assert all('score' in p for p in preds), "❌ Todas las predicciones deben tener 'score'"

    print("✅ Predicción personalizada: distribución correcta")
    print(f"   Distribución objetivo: {custom_dist}")
    obtained = {'1': sum(1 for p in preds if p['prediction'] == '1'),
                'X': sum(1 for p in preds if p['prediction'] == 'X'),
                '2': sum(1 for p in preds if p['prediction'] == '2')}
    print(f"   Distribución obtenida: {obtained}")
    print("✅ Todas las predicciones incluyen scores")


def test_analyze_context():
    """
    Prueba el análisis contextual de un partido.

    El método __analyze_context evalúa factores como clasificación, histórico
    y rachas para generar scores de ajuste. Este test verifica que:
    - Se devuelven todos los factores contextuales requeridos
    - Los scores son numéricos razonables
    - Se maneja correctamente la información histórica
    """
    print("=" * 80)
    print("TEST: test_analyze_context()")
    print("=" * 80)

    detail = {
        'clasificacionLocal': 1,
        'clasificacionVisitante': 2,
        'veces1': 5, 'vecesX': 3, 'veces2': 2
    }

    context = predictor._KinielaPredictor__analyze_context(detail)

    # Verificaciones
    assert isinstance(context, dict), "❌ El contexto debe ser un diccionario"
    required_keys = ['local_strength', 'visitor_strength', 'draw_tendency',
                    'recent_form_local', 'recent_form_visitor']
    assert all(key in context for key in required_keys), f"❌ Faltan claves requeridas: {required_keys}"
    assert all(isinstance(context[key], (int, float, str)) for key in context), \
           "❌ Todos los valores deben ser numéricos o string"

    print("✅ Análisis contextual: factores correctos")
    print(f"   Claves encontradas: {list(context.keys())}")
    print(f"   Local strength: {context.get('local_strength', 'N/A')}")
    print(f"   Visitor strength: {context.get('visitor_strength', 'N/A')}")


def test_adjust_probabilities():
    """
    Prueba el ajuste de probabilidades según contexto.

    El método __adjust_probabilities modifica las probabilidades LAE aplicando
    factores contextuales y normaliza el resultado. Este test verifica que:
    - Las probabilidades ajustadas suman aproximadamente 100%
    - Se aplican correctamente los factores de ajuste
    - Los valores resultantes son coherentes

    Parameters
    ----------
    predictor : KinielaPredictor
        Instancia del predictor proporcionada por el fixture.
    """
    probs = {'1': 50.0, 'X': 30.0, '2': 20.0}
    context = {
        'local_strength': 10,
        'visitor_strength': -5,
        'draw_tendency': 0,
        'recent_form_local': 'neutral',
        'recent_form_visitor': 'neutral'
    }

    adjusted = predictor._KinielaPredictor__adjust_probabilities(probs, context)

    # Verificaciones
    assert abs(sum(adjusted.values()) - 100) < 1e-6  # Suma normalizada
    assert all(isinstance(v, float) for v in adjusted.values())
    assert all(v >= 0 for v in adjusted.values())  # No negativas
    # Con local_strength=10, la prob de 1 debería aumentar
    assert adjusted['1'] > probs['1']


def test_generate_reasoning():
    """
    Prueba la generación de justificaciones para predicciones.

    El método __generate_reasoning crea explicaciones textuales que detallan
    por qué se seleccionó un signo particular. Este test verifica que:
    - Se genera una justificación coherente
    - Se incluyen probabilidades base y ajustes
    - Se mencionan factores contextuales relevantes
    """
    print("=" * 80)
    print("TEST: test_generate_reasoning()")
    print("=" * 80)

    original_probs = {'1': 50.0, 'X': 30.0, '2': 20.0}
    adjusted_probs = {'1': 60.0, 'X': 25.0, '2': 15.0}
    context = {
        'local_strength': 20,
        'visitor_strength': -10,
        'draw_tendency': 0,
        'recent_form_local': 'neutral',
        'recent_form_visitor': 'neutral'
    }

    reasoning = predictor._KinielaPredictor__generate_reasoning('1', original_probs, adjusted_probs, context)

    # Verificaciones
    assert isinstance(reasoning, str), "❌ La justificación debe ser un string"
    assert len(reasoning) > 0, "❌ La justificación no debe estar vacía"
    assert 'Probabilidad LAE' in reasoning, "❌ Debe mencionar 'Probabilidad LAE'"
    assert 'ajustada' in reasoning, "❌ Debe mencionar el ajuste"

    print("✅ Generación de justificación: contenido correcto")
    print(f"   Longitud: {len(reasoning)} caracteres")
    print("✅ Incluye probabilidades LAE y ajustes")


def test_optimize_distribution():
    """
    Prueba la optimización de distribución de signos.

    El método __optimize_distribution asigna signos a partidos usando un algoritmo
    greedy para maximizar la calidad mientras respeta cuotas. Este test verifica que:
    - Se respeta la distribución objetivo
    - Se asignan signos a todos los partidos
    - Se priorizan los scores más altos
    """
    print("=" * 80)
    print("TEST: test_optimize_distribution()")
    print("=" * 80)

    match_scores = [
        {'match_id': 1, 'match': 'A | B', '1': 60.0, 'X': 25.0, '2': 15.0,
         'probabilities': {'1': 60.0, 'X': 25.0, '2': 15.0}, 'context': {}},
        {'match_id': 2, 'match': 'C | D', '1': 30.0, 'X': 40.0, '2': 30.0,
         'probabilities': {'1': 30.0, 'X': 40.0, '2': 30.0}, 'context': {}}
    ]

    preds = predictor._KinielaPredictor__optimize_distribution(match_scores, 1, 1, 0)

    # Verificaciones
    assert len(preds) == 2, "❌ Deberían haber 2 predicciones"
    assert sum(1 for p in preds if p['prediction'] == '1') == 1, "❌ Debería haber 1 predicción '1'"
    assert sum(1 for p in preds if p['prediction'] == 'X') == 1, "❌ Debería haber 1 predicción 'X'"
    assert sum(1 for p in preds if p['prediction'] == '2') == 0, "❌ Debería haber 0 predicciones '2'"
    # El partido 1 debería tener el score más alto para '1', el 2 para 'X'
    assert preds[0]['match_id'] == 1 and preds[0]['prediction'] == '1', "❌ Partido 1 debería ser '1'"
    assert preds[1]['match_id'] == 2 and preds[1]['prediction'] == 'X', "❌ Partido 2 debería ser 'X'"

    print("✅ Optimización de distribución: asignaciones correctas")
    count_1 = sum(1 for p in preds if p['prediction'] == '1')
    count_x = sum(1 for p in preds if p['prediction'] == 'X')
    count_2 = sum(1 for p in preds if p['prediction'] == '2')
    print(f"   Distribución: 1={count_1}, X={count_x}, 2={count_2}")
    print("✅ Priorización de scores altos")


def test_validate_custom_distribution():
    """
    Prueba la validación de distribuciones personalizadas.

    El método __validate_custom_distribution verifica que una distribución
    personalizada tenga las claves correctas y sume 15. Este test verifica que:
    - Se aceptan distribuciones válidas
    - Se rechazan distribuciones inválidas
    - Se requiere la presencia de todas las claves
    """
    print("=" * 80)
    print("TEST: test_validate_custom_distribution()")
    print("=" * 80)

    # Distribuciones válidas
    valid_distributions = [
        {'1': 7, 'X': 4, '2': 4},  # Distribución por defecto
        {'1': 8, 'X': 4, '2': 3},  # Otra distribución válida
        {'1': 5, 'X': 5, '2': 5},  # Distribución equilibrada
    ]

    # Distribuciones inválidas
    invalid_distributions = [
        {'1': 8, 'X': 4, '2': 2},  # Suma 14
        {'1': 10, 'X': 3, '2': 3},  # Suma 16
        {'1': 7, 'X': 4},  # Falta clave '2'
        {'1': 7, '2': 4},  # Falta clave 'X'
        {'X': 4, '2': 4},  # Falta clave '1'
    ]

    # Verificaciones
    for valid in valid_distributions:
        assert predictor._KinielaPredictor__validate_custom_distribution(valid), \
               f"❌ Distribución válida rechazada: {valid}"

    for invalid in invalid_distributions:
        assert not predictor._KinielaPredictor__validate_custom_distribution(invalid), \
               f"❌ Distribución inválida aceptada: {invalid}"

    print("✅ Validación de distribuciones: correctas")
    print(f"   Distribuciones válidas probadas: {len(valid_distributions)}")
    print(f"   Distribuciones inválidas probadas: {len(invalid_distributions)}")


def test_calculate_summary():
    """
    Prueba el cálculo del resumen de predicciones.

    El método __calculate_summary cuenta las ocurrencias de cada signo
    en una lista de predicciones. Este test verifica que:
    - Se cuentan correctamente los signos
    - Se incluyen todos los signos posibles
    - Los valores son numéricos enteros

    Parameters
    ----------
    predictor : KinielaPredictor
        Instancia del predictor proporcionada por el fixture.
    """
    preds = [
        {'prediction': '1'},
        {'prediction': 'X'},
        {'prediction': '2'},
        {'prediction': '1'}
    ]

    summary = predictor._KinielaPredictor__calculate_summary(preds)

    # Verificaciones
    expected = {'1': 2, 'X': 1, '2': 1}
    assert summary == expected, f"❌ Resumen esperado {expected}, obtenido {summary}"
    assert all(isinstance(count, int) for count in summary.values()), "❌ Todos los conteos deben ser enteros"
    assert all(count >= 0 for count in summary.values()), "❌ Todos los conteos deben ser no negativos"

    print("✅ Cálculo de resumen: conteo correcto")
    print(f"   Resumen esperado: {expected}")
    print(f"   Resumen obtenido: {summary}")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTS DE PREDICTOR - KinielaPredictor")
    print("=" * 80)
    
    test_predict_conservative()
    test_predict_risky()
    test_predict_custom()
    test_analyze_context()
    test_adjust_probabilities()
    test_generate_reasoning()
    test_optimize_distribution()
    test_validate_custom_distribution()
    test_calculate_summary()
    
    print("\n" + "=" * 80)
    print("✅ TODOS LOS TESTS DEL PREDICTOR COMPLETADOS EXITOSAMENTE")
    print("=" * 80)
