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

from kinielagpt.analyzer import MatchAnalyzer, TeamAnalyzer

# Instancias globales para los tests
match_analyzer = MatchAnalyzer()
team_analyzer = TeamAnalyzer()


def test_calculate_streak_victorias_consecutivas() -> None:
    """
    Prueba el cálculo de una racha de victorias consecutivas.
    
    Verifica que __calculate_streak identifica correctamente una secuencia de 3 victorias
    consecutivas al inicio de una lista de resultados, clasificándola apropiadamente y
    generando la descripción textual correcta.
    
    Raises
    ------
    AssertionError
        Si el tipo de racha, longitud o descripción no coinciden con lo esperado.
    
    Examples
    --------
    >>> Input: ['V', 'V', 'V', 'E', 'D']
    >>> Output: {'type': 'V', 'length': 3, 'description': '3 victorias consecutivas'}
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_victorias_consecutivas()")
    print("=" * 80)
    
    results = ['V', 'V', 'V', 'E', 'D']
    
    # Acceder al método privado usando name mangling
    streak = match_analyzer._MatchAnalyzer__calculate_streak(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {streak}")
    print("Estructura: {{'type': str, 'length': int, 'description': str}}")
    
    assert streak['type'] == 'V', "❌ Tipo de racha incorrecto"
    assert streak['length'] == 3, "❌ Longitud de racha incorrecta"
    assert streak['description'] == '3 victorias consecutivas', "❌ Descripción incorrecta"
    print("✅ Racha de 3 victorias consecutivas calculada correctamente")


def test_calculate_streak_derrotas_consecutivas() -> None:
    """
    Prueba el cálculo de una racha de derrotas consecutivas.
    
    Verifica que __calculate_streak identifica correctamente 2 derrotas consecutivas
    seguidas de otros resultados.
    
    Raises
    ------
    AssertionError
        Si el tipo, longitud o descripción de la racha no coinciden con lo esperado.
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_derrotas_consecutivas()")
    print("=" * 80)
    
    results = ['D', 'D', 'V', 'E']
    
    streak = match_analyzer._MatchAnalyzer__calculate_streak(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {streak}")
    
    assert streak['type'] == 'D', "❌ Tipo de racha incorrecto"
    assert streak['length'] == 2, "❌ Longitud de racha incorrecta"
    assert streak['description'] == '2 derrotas consecutivas', "❌ Descripción incorrecta"
    print("✅ Racha de 2 derrotas consecutivas calculada correctamente")


def test_calculate_streak_empates_consecutivos() -> None:
    """
    Prueba el cálculo de una racha de empates consecutivos.
    
    Verifica que __calculate_streak identifica 4 empates consecutivos correctamente.
    
    Raises
    ------
    AssertionError
        Si la racha no se calcula correctamente.
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_empates_consecutivos()")
    print("=" * 80)
    
    results = ['E', 'E', 'E', 'E', 'V']
    
    streak = match_analyzer._MatchAnalyzer__calculate_streak(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {streak}")
    
    assert streak['type'] == 'E', "❌ Tipo de racha incorrecto"
    assert streak['length'] == 4, "❌ Longitud de racha incorrecta"
    assert streak['description'] == '4 empates consecutivos', "❌ Descripción incorrecta"
    print("✅ Racha de 4 empates consecutivos calculada correctamente")


def test_calculate_streak_sin_racha() -> None:
    """
    Prueba el cálculo con un solo resultado.
    
    Verifica que __calculate_streak maneja correctamente casos con un único resultado.
    
    Raises
    ------
    AssertionError
        Si no identifica correctamente que solo hay 1 resultado.
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_sin_racha()")
    print("=" * 80)
    
    results = ['V']
    
    streak = match_analyzer._MatchAnalyzer__calculate_streak(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {streak}")
    
    assert streak['type'] == 'V', "❌ Tipo de racha incorrecto"
    assert streak['length'] == 1, "❌ Longitud de racha incorrecta"
    assert '1' in streak['description'], "❌ Descripción incorrecta"
    print("✅ Racha con un solo resultado calculada correctamente")


def test_calculate_streak_lista_vacia() -> None:
    """
    Prueba el cálculo con lista vacía.
    
    Verifica que __calculate_streak maneja correctamente el caso sin datos de entrada.
    
    Raises
    ------
    AssertionError
        Si no retorna la estructura esperada para datos vacíos.
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_lista_vacia()")
    print("=" * 80)
    
    results = []
    
    streak = match_analyzer._MatchAnalyzer__calculate_streak(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {streak}")
    
    assert streak['type'] == 'none', "❌ Tipo de racha incorrecto"
    assert streak['length'] == 0, "❌ Longitud de racha incorrecta"
    assert streak['description'] == 'Sin datos', "❌ Descripción incorrecta"
    print("✅ Racha con lista vacía calculada correctamente")


def test_analyze_recent_form() -> None:
    """
    Prueba el análisis de forma reciente con datos completos.
    
    Verifica que __analyze_recent_form procesa correctamente la evolución de ambos equipos
    y calcula las rachas actuales de local y visitante.
    
    Raises
    ------
    AssertionError
        Si la estructura o los cálculos de rachas no son correctos.
    """
    print("=" * 80)
    print("TEST: test_analyze_recent_form()")
    print("=" * 80)
    
    detail = {
        'evolucionLocal': ['V', 'V', 'E', 'D', 'V', 'V', 'E'],
        'evolucionVisitante': ['D', 'D', 'E', 'V', 'D']
    }
    
    form = match_analyzer._MatchAnalyzer__analyze_recent_form(detail)  # type: ignore
    
    print(f"Input evolucionLocal: {detail['evolucionLocal']}")
    print(f"Input evolucionVisitante: {detail['evolucionVisitante']}")
    print(f"Output: {form}")
    print(
        "Estructura: {{'local_recent_results': list, 'visitor_recent_results': list, "
        "'local_streak': dict, 'visitor_streak': dict}}"
    )
    
    assert 'local_recent_results' in form, "❌ Falta local_recent_results"
    assert 'visitor_recent_results' in form, "❌ Falta visitor_recent_results"
    assert 'local_streak' in form, "❌ Falta local_streak"
    assert 'visitor_streak' in form, "❌ Falta visitor_streak"
    assert len(form['local_recent_results']) == 5, "❌ Longitud local_recent_results incorrecta"
    assert len(form['visitor_recent_results']) == 5, "❌ Longitud visitor_recent_results incorrecta"
    assert form['local_streak']['type'] == 'V', "❌ Tipo de racha local incorrecto"
    assert form['local_streak']['length'] == 2, "❌ Longitud de racha local incorrecta"
    assert form['visitor_streak']['type'] == 'D', "❌ Tipo de racha visitante incorrecto"
    assert form['visitor_streak']['length'] == 2, "❌ Longitud de racha visitante incorrecta"
    print("✅ Análisis de forma reciente calculado correctamente")


def test_analyze_recent_form_sin_datos() -> None:
    """
    Prueba el análisis de forma reciente sin datos.
    
    Verifica que __analyze_recent_form maneja correctamente casos sin información disponible.
    
    Raises
    ------
    AssertionError
        Si no retorna listas vacías correctamente.
    """
    print("=" * 80)
    print("TEST: test_analyze_recent_form_sin_datos()")
    print("=" * 80)
    
    detail = {}
    
    form = match_analyzer._MatchAnalyzer__analyze_recent_form(detail)  # type: ignore
    
    print(f"Input: {detail}")
    print(f"Output: {form}")
    
    assert form['local_recent_results'] == [], "❌ local_recent_results no es lista vacía"
    assert form['visitor_recent_results'] == [], "❌ visitor_recent_results no es lista vacía"
    print("✅ Análisis de forma reciente sin datos manejado correctamente")


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
    recent_form = {
        'local_streak': {'type': 'V', 'length': 5},
        'visitor_streak': {'type': 'D', 'length': 2}
    }
    
    confidence = match_analyzer._MatchAnalyzer__calculate_confidence(  # type: ignore
        max_prob=max_prob,
        historical_analysis=historical_analysis,
        recent_form=recent_form
    )
    
    print(f"Input max_prob: {max_prob}")
    print(f"Input historical_analysis: {historical_analysis}")
    print(f"Input recent_form: {recent_form}")
    print(f"Output: {confidence}")
    print(f"Cálculo: {max_prob} + 5 (histórico) + 5 (racha) = {max_prob + 10}")
    
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
    recent_form = {
        'local_streak': {'type': 'E', 'length': 2},
        'visitor_streak': {'type': 'V', 'length': 1}
    }
    
    confidence = match_analyzer._MatchAnalyzer__calculate_confidence(  # type: ignore
        max_prob=max_prob,
        historical_analysis=historical_analysis,
        recent_form=recent_form
    )
    
    print(f"Input max_prob: {max_prob}")
    print(f"Input historical_analysis: {historical_analysis}")
    print(f"Input recent_form: {recent_form}")
    print(f"Output: {confidence}")
    print(f"Cálculo: {max_prob} + 0 (sin histórico suficiente) + 0 (sin racha significativa) = {max_prob}")
    
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
    recent_form = {
        'local_streak': {'type': 'D', 'length': 2},
        'visitor_streak': {'type': 'E', 'length': 1}
    }
    
    confidence = match_analyzer._MatchAnalyzer__calculate_confidence(  # type: ignore
        max_prob=max_prob,
        historical_analysis=historical_analysis,
        recent_form=recent_form
    )
    
    print(f"Input max_prob: {max_prob}")
    print(f"Input historical_analysis: {historical_analysis}")
    print(f"Input recent_form: {recent_form}")
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
    recent_form = {
        'local_streak': {'type': 'V', 'length': 4, 'description': '4 victorias consecutivas'},
        'visitor_streak': {'type': 'D', 'length': 1, 'description': '1 derrota'}
    }
    classification = {
        'local_position': '3º',
        'visitor_position': '15º'
    }
    
    prediction, confidence, reasoning = match_analyzer._MatchAnalyzer__generate_prediction_with_reasoning(  # type: ignore
        probs=probs,
        historical_analysis=historical_analysis,
        recent_form=recent_form,
        classification=classification
    )
    
    print(f"Input probs: {probs}")
    print(f"Input historical_analysis: {historical_analysis}")
    print(f"Input recent_form: {recent_form}")
    print(f"Input classification: {classification}")
    print(f"\nOutput prediction: {prediction}")
    print(f"Output confidence: {confidence}")
    print(f"Output reasoning: {reasoning}")
    print("\nEstructura: (str, str, str) -> (prediction, confidence, reasoning)")
    
    assert prediction == '1', "❌ Predicción incorrecta"
    assert confidence == 'ALTA', "❌ Confianza incorrecta"
    assert 'Probabilidad LAE del 1' in reasoning, "❌ Reasoning no contiene probabilidad"
    assert '70%' in reasoning or '70.0%' in reasoning, "❌ Reasoning no contiene porcentaje histórico"
    assert '4 victorias consecutivas' in reasoning, "❌ Reasoning no contiene racha local"
    print("✅ Predicción con razonamiento generada correctamente")


def test_calculate_streak_team() -> None:
    """
    Prueba el cálculo de racha para un equipo.
    
    Verifica que __calculate_streak de TeamAnalyzer identifica correctamente rachas consecutivas.
    
    Raises
    ------
    AssertionError
        Si la racha no se calcula correctamente.
    """
    print("=" * 80)
    print("TEST: test_calculate_streak_team()")
    print("=" * 80)
    
    results = ['V', 'V', 'V', 'V', 'V', 'E', 'D']
    
    streak = team_analyzer._TeamAnalyzer__calculate_streak(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {streak}")
    
    assert streak['type'] == 'V', "❌ Tipo de racha incorrecto"
    assert streak['length'] == 5, "❌ Longitud de racha incorrecta"
    assert streak['description'] == '5 victorias consecutivas', "❌ Descripción incorrecta"
    print("✅ Racha de equipo calculada correctamente")


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
    
    results = ['V', 'V', 'V', 'V', 'E']
    
    trend = team_analyzer._TeamAnalyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {trend}")
    print("Estructura: {{'direction': str, 'description': str, 'points_last_5': int, "
          "'form': str, 'last_5_results': list}}")
    print(f"Puntos calculados: 4V*3 + 1E*1 = {4*3 + 1*1}")
    
    assert 'direction' in trend, "❌ Falta direction"
    assert 'description' in trend, "❌ Falta description"
    assert 'points_last_5' in trend, "❌ Falta points_last_5"
    assert 'form' in trend, "❌ Falta form"
    assert 'last_5_results' in trend, "❌ Falta last_5_results"
    assert trend['points_last_5'] == 13, "❌ Puntos incorrectos"
    assert trend['form'] == 'excellent', "❌ Forma incorrecta"
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
    
    results = ['V', 'V', 'E', 'E', 'V']
    
    trend = team_analyzer._TeamAnalyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {trend}")
    print(f"Puntos calculados: 3V*3 + 2E*1 = {3*3 + 2*1}")
    
    assert trend['points_last_5'] == 11, "❌ Puntos incorrectos"
    assert trend['form'] == 'good', "❌ Forma incorrecta"
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
    
    results = ['V', 'E', 'D', 'V', 'E']
    
    trend = team_analyzer._TeamAnalyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {trend}")
    print(f"Puntos calculados: 2V*3 + 2E*1 + 1D*0 = {2*3 + 2*1}")
    
    assert trend['points_last_5'] == 8, "❌ Puntos incorrectos"
    assert trend['form'] == 'average', "❌ Forma incorrecta"
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
    
    results = ['D', 'D', 'D', 'E', 'V']
    
    trend = team_analyzer._TeamAnalyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {trend}")
    print(f"Puntos calculados: 1V*3 + 1E*1 + 3D*0 = {1*3 + 1*1}")
    
    assert trend['points_last_5'] == 4, "❌ Puntos incorrectos"
    assert trend['form'] == 'poor', "❌ Forma incorrecta"
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
    
    # Últimos 5: V,V,E,D,D (8 puntos)
    # Anteriores 5: D,D,D,D,E (1 punto)
    results = ['V', 'V', 'E', 'D', 'D', 'D', 'D', 'D', 'D', 'E']
    
    trend = team_analyzer._TeamAnalyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input (últimos 10): {results}")
    print(f"Últimos 5: {results[:5]}")
    print(f"Anteriores 5: {results[5:10]}")
    print(f"Output: {trend}")
    print(f"Puntos últimos 5: {trend['points_last_5']}")
    
    assert trend['points_last_5'] == 7, "❌ Puntos incorrectos"
    assert trend['direction'] == 'improving', "❌ Dirección incorrecta"
    assert 'alza' in trend['description'].lower(), "❌ Descripción no indica alza"
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
    
    trend = team_analyzer._TeamAnalyzer__analyze_trend(results)  # type: ignore
    
    print(f"Input: {results}")
    print(f"Output: {trend}")
    
    assert trend['direction'] == 'unknown', "❌ Dirección incorrecta"
    assert 'insuficiente' in trend['description'].lower(), "❌ Descripción no indica insuficiente"
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
    
    comparativa = [
        {'esLocal': True, 'partido': 'EQUIPO1 | RIVAL1'},
        {'esLocal': True, 'partido': 'EQUIPO1 | RIVAL2'},
        {'esLocal': True, 'partido': 'EQUIPO1 | RIVAL3'},
        {'esLocal': False, 'partido': 'RIVAL4 | EQUIPO1'},
        {'esLocal': False, 'partido': 'RIVAL5 | EQUIPO1'},
    ]
    
    performance = team_analyzer._TeamAnalyzer__analyze_home_away_performance(comparativa)  # type: ignore
    
    print(f"Input comparativa ({len(comparativa)} partidos):")
    for p in comparativa:
        print(f"  - esLocal={p['esLocal']}: {p['partido']}")
    print(f"Output: {performance}")
    print("Estructura: {{'home': str, 'away': str}}")
    
    assert 'home' in performance, "❌ Falta home"
    assert 'away' in performance, "❌ Falta away"
    assert '3 partidos como local' in performance['home'], "❌ Conteo local incorrecto"
    assert '2 partidos como visitante' in performance['away'], "❌ Conteo visitante incorrecto"
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
    
    comparativa = []
    
    performance = team_analyzer._TeamAnalyzer__analyze_home_away_performance(comparativa)  # type: ignore
    
    print(f"Input: {comparativa}")
    print(f"Output: {performance}")
    
    assert performance['home'] == 'Sin datos', "❌ Home no es 'Sin datos'"
    assert performance['away'] == 'Sin datos', "❌ Away no es 'Sin datos'"
    print("✅ Rendimiento sin datos manejado correctamente")


if __name__ == "__main__":
    print("="*80)
    print("TESTS PARA KINIELAGPT ANALYZER")
    print("="*80)
    
    # Tests de MatchAnalyzer
    print("\n" + "="*80)
    print("TESTS DE MATCHANALYZER")
    print("="*80)
    
    test_calculate_streak_victorias_consecutivas()
    test_calculate_streak_derrotas_consecutivas()
    test_calculate_streak_empates_consecutivos()
    test_calculate_streak_sin_racha()
    test_calculate_streak_lista_vacia()
    test_analyze_recent_form()
    test_analyze_recent_form_sin_datos()
    test_calculate_confidence_alta()
    test_calculate_confidence_media()
    test_calculate_confidence_baja()
    test_generate_prediction_with_reasoning()
    
    # Tests de TeamAnalyzer
    print("\n" + "="*80)
    print("TESTS DE TEAMANALYZER")
    print("="*80)
    
    test_calculate_streak_team()
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
