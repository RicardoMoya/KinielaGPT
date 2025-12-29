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
Tests para el módulo analyzer.

Estos tests verifican la lógica de cálculo de las funciones privadas de MatchAnalyzer
y TeamAnalyzer, sin realizar llamadas a servicios externos. Validan el correcto funcionamiento
de los algoritmos de análisis de rachas, tendencias, confianza y predicciones.

Ejecutar: python -m pytest tests/test_analyzer.py -v -s
"""

from kinielagpt.analyzer import Analyzer

# Instancias globales para los tests
analyzer = Analyzer()


def test_calculate_confidence_alta() -> None:
    """
    Prueba el cálculo de nivel de confianza ALTA.
    
    Verifica que __calculate_confidence asigna confianza ALTA cuando hay probabilidad alta,
    histórico suficiente y racha significativa.
    
    Raises
    ------
    AssertionError
        Si no calcula ALTA cuando debería.
    """
    print("=" * 80)
    print("TEST: test_calculate_confidence_alta()")
    print("=" * 80)
    
    max_prob = 68.5
    historical_analysis = {'total_matches': 10}
    
    confidence = analyzer._Analyzer__calculate_confidence(  # type: ignore
        max_prob=max_prob,
        historical_analysis=historical_analysis
    )
    
    print(f"Input max_prob: {max_prob}")
    print(f"Input historical_analysis: {historical_analysis}")
    print(f"Output: {confidence}")
    print(f"Cálculo: {max_prob} + 5 (histórico >=5) = {max_prob + 5}")
    
    assert confidence == 'ALTA', "❌ Confianza no es ALTA"
    print("✅ Confianza ALTA calculada correctamente")


def test_calculate_confidence_media() -> None:
    """
    Prueba el cálculo de nivel de confianza MEDIA.
    
    Verifica que __calculate_confidence asigna confianza MEDIA cuando hay probabilidad moderada
    y contexto equilibrado.
    
    Raises
    ------
    AssertionError
        Si no calcula MEDIA cuando debería.
    """
    print("=" * 80)
    print("TEST: test_calculate_confidence_media()")
    print("=" * 80)
    
    max_prob = 48.0
    historical_analysis = {'total_matches': 3}
    
    confidence = analyzer._Analyzer__calculate_confidence(  # type: ignore
        max_prob=max_prob,
        historical_analysis=historical_analysis
    )
    
    print(f"Input max_prob: {max_prob}")
    print(f"Input historical_analysis: {historical_analysis}")
    print(f"Output: {confidence}")
    print(f"Cálculo: {max_prob} + 0 (histórico <5) = {max_prob}")
    
    assert confidence == 'MEDIA', "❌ Confianza no es MEDIA"
    print("✅ Confianza MEDIA calculada correctamente")


def test_calculate_confidence_baja() -> None:
    """
    Prueba el cálculo de nivel de confianza BAJA.
    
    Verifica que __calculate_confidence asigna confianza BAJA cuando la probabilidad es baja
    o no hay suficiente contexto histórico.
    
    Raises
    ------
    AssertionError
        Si no calcula BAJA cuando debería.
    """
    print("=" * 80)
    print("TEST: test_calculate_confidence_baja()")
    print("=" * 80)
    
    max_prob = 38.0
    historical_analysis = {'total_matches': 2}
    
    confidence = analyzer._Analyzer__calculate_confidence(  # type: ignore
        max_prob=max_prob,
        historical_analysis=historical_analysis
    )
    
    print(f"Input max_prob: {max_prob}")
    print(f"Input historical_analysis: {historical_analysis}")
    print(f"Output: {confidence}")
    
    assert confidence == 'BAJA', "❌ Confianza no es BAJA"
    print("✅ Confianza BAJA calculada correctamente")


def test_generate_prediction_with_reasoning() -> None:
    """
    Prueba la generación completa de predicción con razonamiento.
    
    Verifica que __generate_prediction_with_reasoning integra probabilidades, histórico,
    rachas y clasificación para generar predicción, confianza y justificación.
    
    Raises
    ------
    AssertionError
        Si no genera la estructura completa o los valores no son válidos.
    """
    print("=" * 80)
    print("TEST: test_generate_prediction_with_reasoning()")
    print("=" * 80)
    
    probs = {'1': 65.5, 'X': 22.3, '2': 12.2}
    historical_analysis = {
        'total_matches': 10,
        'local_wins': 7,
        'draws': 2,
        'visitor_wins': 1,
        'local_win_rate': 70.0,
        'draw_rate': 20.0,
        'visitor_win_rate': 10.0
    }
    
    prediction, confidence, reasoning = analyzer._Analyzer__generate_prediction_with_reasoning(  # type: ignore
        probs=probs,
        historical_analysis=historical_analysis
    )
    
    print(f"Input probs: {probs}")
    print(f"Input historical_analysis: {historical_analysis}")
    print(f"\nOutput prediction: {prediction}")
    print(f"Output confidence: {confidence}")
    print(f"Output reasoning: {reasoning}")
    print("\nEstructura: (str, str, str) -> (prediction, confidence, reasoning)")
    
    assert prediction == '1', "❌ Predicción incorrecta"
    assert confidence == 'ALTA', "❌ Confianza incorrecta"
    assert 'Probabilidad LAE del 1' in reasoning, "❌ Reasoning no contiene probabilidad"
    print("✅ Predicción con razonamiento generada correctamente")


def test_analyze_trend_excelente() -> None:
    """
    Prueba el análisis de tendencia excelente.
    
    Verifica que __analyze_trend calcula correctamente una tendencia excelente (11-15 puntos).
    
    Raises
    ------
    AssertionError
        Si no identifica correctamente una tendencia excelente.
    """
    print("=" * 80)
    print("TEST: test_analyze_trend_excelente()")
    print("=" * 80)
    
    results = ['VICTORIA', 'VICTORIA', 'VICTORIA', 'VICTORIA', 'EMPATE']
    
    trend = analyzer._Analyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {trend}")
    print("Estructura: {{'direccion': str, 'descripcion': str, 'puntos_ultimos_partidos': int, "
          "'forma': str, 'ultimos_resultados': list}}")
    print(f"Puntos calculados: 4V*3 + 1E*1 = {4*3 + 1*1}")
    
    assert 'direccion' in trend, "❌ Falta direccion"
    assert 'descripcion' in trend, "❌ Falta descripcion"
    assert 'puntos_ultimos_partidos' in trend, "❌ Falta puntos_ultimos_partidos"
    assert 'forma' in trend, "❌ Falta forma"
    assert 'ultimos_resultados' in trend, "❌ Falta ultimos_resultados"
    assert trend['puntos_ultimos_partidos'] == 13, "❌ Puntos incorrectos"
    assert trend['forma'] == 'excelente', "❌ Forma incorrecta"
    print("✅ Tendencia EXCELENTE analizada correctamente")


def test_analyze_trend_buena() -> None:
    """
    Prueba el análisis de tendencia buena.
    
    Verifica que __analyze_trend calcula correctamente una tendencia buena (8-10 puntos).
    
    Raises
    ------
    AssertionError
        Si no identifica correctamente una tendencia buena.
    """
    print("=" * 80)
    print("TEST: test_analyze_trend_buena()")
    print("=" * 80)
    
    results = ['VICTORIA', 'VICTORIA', 'EMPATE', 'EMPATE', 'VICTORIA']
    
    trend = analyzer._Analyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {trend}")
    print(f"Puntos calculados: 3V*3 + 2E*1 = {3*3 + 2*1}")
    
    assert trend['puntos_ultimos_partidos'] == 11, "❌ Puntos incorrectos"
    assert trend['forma'] == 'buena', "❌ Forma incorrecta"
    print("✅ Tendencia BUENA analizada correctamente")


def test_analyze_trend_regular() -> None:
    """
    Prueba el análisis de tendencia regular.
    
    Verifica que __analyze_trend calcula correctamente una tendencia regular (5-7 puntos).
    
    Raises
    ------
    AssertionError
        Si no identifica correctamente una tendencia regular.
    """
    print("=" * 80)
    print("TEST: test_analyze_trend_regular()")
    print("=" * 80)
    
    results = ['VICTORIA', 'EMPATE', 'DERROTA', 'VICTORIA', 'EMPATE']
    
    trend = analyzer._Analyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {trend}")
    print(f"Puntos calculados: 2V*3 + 2E*1 + 1D*0 = {2*3 + 2*1}")
    
    assert trend['puntos_ultimos_partidos'] == 8, "❌ Puntos incorrectos"
    assert trend['forma'] == 'regular', "❌ Forma incorrecta"
    print("✅ Tendencia REGULAR analizada correctamente")


def test_analyze_trend_mala() -> None:
    """
    Prueba el análisis de tendencia mala.
    
    Verifica que __analyze_trend calcula correctamente una tendencia mala (<5 puntos).
    
    Raises
    ------
    AssertionError
        Si no identifica correctamente una tendencia mala.
    """
    print("=" * 80)
    print("TEST: test_analyze_trend_mala()")
    print("=" * 80)
    
    results = ['DERROTA', 'DERROTA', 'DERROTA', 'EMPATE', 'VICTORIA']
    
    trend = analyzer._Analyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {trend}")
    print(f"Puntos calculados: 1V*3 + 1E*1 + 3D*0 = {1*3 + 1*1}")
    
    assert trend['puntos_ultimos_partidos'] == 4, "❌ Puntos incorrectos"
    assert trend['forma'] == 'mala', "❌ Forma incorrecta"
    print("✅ Tendencia MALA analizada correctamente")


def test_analyze_trend_comparacion_periodos() -> None:
    """
    Prueba el análisis de tendencia comparando períodos.
    
    Verifica que __analyze_trend identifica mejoras al comparar últimos 5 partidos con anteriores 5.
    
    Raises
    ------
    AssertionError
        Si no detecta correctamente la mejora en el rendimiento.
    """
    print("=" * 80)
    print("TEST: test_analyze_trend_comparacion_periodos()")
    print("=" * 80)
    
    # Últimos 5: VICTORIA,VICTORIA,VICTORIA,VICTORIA,VICTORIA (15 puntos)
    # Anteriores 5: DERROTA,DERROTA,DERROTA,DERROTA,EMPATE (1 punto)
    results = ['DERROTA', 'DERROTA', 'DERROTA', 'DERROTA', 'EMPATE', 'VICTORIA', 'VICTORIA', 'VICTORIA', 'VICTORIA', 
               'VICTORIA']
    
    trend = analyzer._Analyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input (últimos 10): {results}")
    print(f"Últimos 5: {results[-5:]}")
    print(f"Anteriores 5: {results[-10:-5]}")
    print(f"Output: {trend}")
    print(f"Puntos últimos 5: {trend['puntos_ultimos_partidos']}")
    
    assert trend['puntos_ultimos_partidos'] == 15, "❌ Puntos incorrectos"
    assert trend['direccion'] == 'mejorando', "❌ Dirección incorrecta"
    assert 'alza' in trend['descripcion'].lower(), "❌ Descripción no indica alza"
    print("✅ Comparación de tendencias analizada correctamente")


def test_analyze_trend_datos_insuficientes() -> None:
    """
    Prueba el análisis de tendencia con datos insuficientes.
    
    Verifica que __analyze_trend maneja correctamente casos con pocos resultados disponibles.
    
    Raises
    ------
    AssertionError
        Si no identifica correctamente la situación de datos insuficientes.
    """
    print("=" * 80)
    print("TEST: test_analyze_trend_datos_insuficientes()")
    print("=" * 80)
    
    results = ['V', 'E']
    
    trend = analyzer._Analyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {trend}")
    
    assert trend['direccion'] == 'unknown', "❌ Dirección incorrecta"
    assert 'insuficiente' in trend['descripcion'].lower(), "❌ Descripción no indica insuficiente"
    print("✅ Tendencia con datos insuficientes manejada correctamente")


def test_analyze_home_away_performance() -> None:
    """
    Prueba el análisis de rendimiento local vs visitante.
    
    Verifica que __analyze_home_away_performance identifica correctamente la cantidad
    de partidos jugados como local y visitante.
    
    Raises
    ------
    AssertionError
        Si no cuenta correctamente los partidos según su condición de local/visitante.
    """
    print("=" * 80)
    print("TEST: test_analyze_home_away_performance()")
    print("=" * 80)
    
    resultados_local = ['VICTORIA', 'EMPATE', 'DERROTA']
    resultados_visitante = ['VICTORIA', 'DERROTA']
    
    performance = analyzer._Analyzer__analyze_home_away_performance(resultados_local, resultados_visitante)  # type: ignore
    
    print(f"Input resultados_local: {resultados_local}")
    print(f"Input resultados_visitante: {resultados_visitante}")
    print(f"Output: {performance}")
    print("Estructura: {{'local': dict, 'visitante': dict, 'comparacion': str}}")
    
    assert 'local' in performance, "❌ Falta local"
    assert 'visitante' in performance, "❌ Falta visitante"
    assert 'comparacion' in performance, "❌ Falta comparacion"
    assert performance['local']['registro'] == '1V-1E-1D (4pts)', "❌ Registro local incorrecto"
    assert performance['visitante']['registro'] == '1V-0E-1D (3pts)', "❌ Registro visitante incorrecto"
    assert performance['comparacion'] == 'Equilibrado Local/Visitante', "❌ Comparacion incorrecta"
    print("✅ Rendimiento local vs visitante analizado correctamente")


def test_analyze_home_away_performance_sin_datos() -> None:
    """
    Prueba el análisis de rendimiento sin datos.
    
    Verifica que __analyze_home_away_performance maneja correctamente casos sin información.
    
    Raises
    ------
    AssertionError
        Si no retorna 'Sin datos' para ambas condiciones.
    """
    print("=" * 80)
    print("TEST: test_analyze_home_away_performance_sin_datos()")
    print("=" * 80)
    
    resultados_local = []
    resultados_visitante = []
    
    performance = analyzer._Analyzer__analyze_home_away_performance(resultados_local, resultados_visitante)  # type: ignore
    
    print(f"Input resultados_local: {resultados_local}")
    print(f"Input resultados_visitante: {resultados_visitante}")
    print(f"Output: {performance}")
    
    assert performance == {}, "❌ Debe retornar diccionario vacío sin datos"
    print("✅ Rendimiento sin datos manejado correctamente")


if __name__ == "__main__":
    print("="*80)
    print("TESTS PARA KINIELAGPT ANALYZER")
    print("="*80)
    
    # Tests de MatchAnalyzer
    print("\n" + "="*80)
    print("TESTS DE MATCHANALYZER")
    print("="*80)
    
    test_calculate_confidence_alta()
    test_calculate_confidence_media()
    test_calculate_confidence_baja()
    test_generate_prediction_with_reasoning()
    
    # Tests de TeamAnalyzer
    print("\n" + "="*80)
    print("TESTS DE TEAMANALYZER")
    print("="*80)
    
    test_analyze_trend_excelente()
    test_analyze_trend_buena()
    test_analyze_trend_regular()
    test_analyze_trend_mala()
    test_analyze_trend_comparacion_periodos()
    test_analyze_trend_datos_insuficientes()
    test_analyze_home_away_performance()
    test_analyze_home_away_performance_sin_datos()
    
    print("\n" + "="*80)
    print("✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
    print("="*80)
