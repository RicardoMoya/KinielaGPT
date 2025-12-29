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
Analizadores de partidos y equipos para KinielaGPT.

Este módulo proporciona herramientas para analizar partidos individuales y el rendimiento
de equipos específicos, generando informes detallados con justificaciones.
"""

from typing import Any

from kinielagpt import data_source


class Analyzer:
    """
    Analizador de partidos y equipos para KinielaGPT.

    Esta clase proporciona herramientas avanzadas para analizar partidos individuales
    y el rendimiento de equipos específicos en el contexto de la quiniela española.
    Utiliza datos de probabilidades LAE, histórico de enfrentamientos, evolución
    reciente y clasificaciones para generar análisis detallados y predicciones
    justificadas.

    Funcionalidades principales:
    - Análisis de partidos con o sin predicción
    - Análisis completo del rendimiento de equipos
    - Evaluación de tendencias y formas recientes
    - Comparación de rendimiento local vs visitante
    - Cálculo de niveles de confianza en predicciones

    Los métodos están diseñados para ser utilizados tanto de forma independiente
    como integrados en flujos de trabajo más complejos de predicción deportiva.
    """

    def get_raw_data(self, jornada: int, temporada: int, match_id: int) -> dict[str, Any] | None:
        """
        Obtiene información en crudo de un partido específico sin análisis ni predicción.

        Este método proporciona acceso directo a los datos brutos del partido sin procesamiento
        adicional, útil para consultas específicas como histórico de enfrentamientos, evolución
        reciente, clasificaciones actuales, o comparativa de últimos partidos. Es ideal cuando
        solo necesitas información factual sin interpretación.

        Datos disponibles en crudo:
        - Información básica del partido (equipos, jornada, temporada)
        - Probabilidades LAE completas (1, X, 2, pronóstico de goles)
        - Histórico de enfrentamientos directos (últimos 10 años)
        - Evolución reciente de ambos equipos (últimos resultados)
        - Clasificaciones actuales de ambos equipos
        - Comparativa de últimos 5 partidos
        - Datos destacados del enfrentamiento

        Casos de uso típicos:
        - "¿Cuál es el histórico entre Barcelona y Real Madrid?"
        - "¿Cuáles son los últimos resultados del Atlético?"
        - "¿Qué posición ocupa cada equipo en la clasificación?"
        - "¿Cuántos empates ha habido históricamente entre estos equipos?"

        Parameters
        ----------
        jornada : int
            Número de jornada.
        temporada : int
            Año de la temporada.
        match_id : int
            ID del partido dentro de la jornada (1-15).

        Returns
        -------
        dict[str, Any] | None
            Datos en crudo del partido con toda la información disponible sin procesar.
            Retorna None si hay algún error o el partido no existe.

        Examples
        --------
        >>> analyzer = Analyzer()
        >>> data = analyzer.get_raw_data(jornada=26, temporada=2025, match_id=5)
        >>> print(data["historico"]["total_partidos"])
        12
        """
        # Obtener datos del partido
        probabilities = data_source.get_kiniela_probabilities(jornada=jornada, temporada=temporada)
        details = data_source.get_kiniela_matches_details(jornada=jornada, temporada=temporada)

        if probabilities is None or details is None:
            return None

        if match_id < 1 or match_id > len(probabilities):
            return None

        prob = probabilities[match_id - 1]
        detail = details[match_id - 1]

        # Retornar datos en crudo sin procesamiento
        return {
            "info_partido": {
                "id_partido": match_id,
                "partido": prob["partido"],
                "jornada": jornada,
                "temporada": temporada,
            },
            "probabilidades": {
                "1": prob.get("1_Prob", 0),
                "X": prob.get("X_Prob", 0),
                "2": prob.get("2_Prob", 0),
                "pronostico_goles": prob.get("pronosticoGoles", "N/A"),
            },
            "historico": {
                "victorias_local": detail.get("veces1", 0),
                "empates": detail.get("vecesX", 0),
                "victorias_visitante": detail.get("veces2", 0),
                "total_partidos": detail.get("veces1", 0) + detail.get("vecesX", 0) + detail.get("veces2", 0),
            },
            "clasificacion": {
                "local": detail.get("clasificacion_local", "N/A"),
                "visitante": detail.get("clasificacion_visitante", "N/A"),
            },
            "evolucion_clasificacion_local": detail.get("evolucion_clasificacion_local", []),
            "evolucion_clasificacion_visitante": detail.get("evolucion_clasificacion_visitante", []),
            "ultimos_partidos": detail.get("ultimos_partidos", []),
            "rachas": {
                "racha_local_ultimos_5_partidos": detail.get("racha_local_ultimos_5_partidos", []),
                "racha_visitante_ultimos_5_partidos": detail.get("racha_visitante_ultimos_5_partidos", []),
                "racha_local_como_local_ultimos_5_partidos": detail.get(
                    "racha_local_como_local_ultimos_5_partidos", []
                ),
                "racha_visitante_como_visitante_ultimos_5_partidos": detail.get(
                    "racha_visitante_como_visitante_ultimos_5_partidos", []
                ),
            },
            "datos_destacados": detail.get("datos_destacados", []),
        }

    def analyze_match(
        self, jornada: int, temporada: int, match_id: int, include_prediction: bool = True
    ) -> dict[str, Any] | None:
        """
        Analiza un partido específico con opción de incluir predicción o solo datos en crudo.

        Este método unificado permite obtener tanto análisis completo con predicción justificada
        como información en crudo del partido. Es la herramienta principal para consultar cualquier
        aspecto de un partido específico.

        Modos de operación:

        **Con predicción (include_prediction=True, por defecto)**:
        Realiza un análisis exhaustivo combinando múltiples fuentes de datos y generando una
        predicción justificada con nivel de confianza. Integra probabilidades LAE, histórico
        de enfrentamientos, forma reciente, clasificación y factores contextuales.

        Proceso de análisis con predicción:
        1. Obtención de datos: probabilidades LAE y detalles del partido
        2. Análisis histórico: Revisa últimos 10 años de enfrentamientos directos
        3. Análisis de forma: Evalúa últimos 5 partidos de cada equipo
        4. Análisis de clasificación: Compara posiciones y tendencias
        5. Evaluación contextual: Identifica factores relevantes (racha, local/visitante)
        6. Generación de predicción: Combina todos los factores con ponderación
        7. Asignación de confianza: ALTA (>=60%), MEDIA (45-60%), BAJA (<45%)
        8. Justificación detallada: Explica el razonamiento completo

        **Sin predicción (include_prediction=False)**:
        Retorna únicamente los datos en crudo del partido sin análisis ni interpretación.
        Útil para consultas específicas sobre histórico, evolución, clasificaciones, etc.

        Casos de uso:
        - Con predicción: "¿Qué resultado es más probable en el partido 5?"
        - Sin predicción: "Muéstrame el histórico de enfrentamientos del partido 3"
        - Sin predicción: "¿Cuáles son los últimos resultados de ambos equipos en el partido 8?"

        Parameters
        ----------
        jornada : int
            Número de jornada.
        temporada : int
            Año de la temporada.
        match_id : int
            ID del partido dentro de la jornada (1-15).
        include_prediction : bool, optional
            Si True (default), incluye análisis completo con predicción.
            Si False, retorna solo datos en crudo sin predicción.

        Returns
        -------
        dict[str, Any] | None
            Si include_prediction=True: Análisis completo con predicción, confianza y razonamiento.
            Si include_prediction=False: Datos en crudo del partido sin procesamiento.
            Retorna None si hay algún error.

        Examples
        --------
        >>> analyzer = Analyzer()
        >>> # Análisis completo con predicción
        >>> analysis = analyzer.analyze_match(jornada=26, temporada=2025, match_id=5)
        >>> print(analysis["prediccion"])
        '1'
        >>> print(analysis["confianza"])
        'ALTA'
        >>>
        >>> # Solo datos en crudo
        >>> raw_data = analyzer.analyze_match(jornada=26, temporada=2026, match_id=5, include_prediction=False)
        >>> print(raw_data["historico"]["total_partidos"])
        12
        """
        # Si no se solicita predicción, retornar solo datos en crudo
        if not include_prediction:
            return self.get_raw_data(jornada=jornada, temporada=temporada, match_id=match_id)

        # Obtener datos del partido
        probabilities = data_source.get_kiniela_probabilities(jornada=jornada, temporada=temporada)
        details = data_source.get_kiniela_matches_details(jornada=jornada, temporada=temporada)

        if probabilities is None or details is None:
            return None

        if match_id < 1 or match_id > len(probabilities):
            return None

        prob = probabilities[match_id - 1]
        detail = details[match_id - 1]

        # Extraer probabilidades
        probs = {
            "1": prob.get("1_Prob", 0),
            "X": prob.get("X_Prob", 0),
            "2": prob.get("2_Prob", 0),
        }

        # Análisis histórico
        veces1 = detail.get("veces1", 0)
        vecesX = detail.get("vecesX", 0)
        veces2 = detail.get("veces2", 0)
        total_historic = veces1 + vecesX + veces2

        historical_analysis = {
            "total_partidos": total_historic,
            "victorias_local": veces1,
            "empates": vecesX,
            "victorias_visitante": veces2,
        }

        if total_historic > 0:
            historical_analysis["porcentaje_victorias_local"] = round((veces1 / total_historic) * 100, 1)
            historical_analysis["porcentaje_empates"] = round((vecesX / total_historic) * 100, 1)
            historical_analysis["porcentaje_victorias_visitante"] = round((veces2 / total_historic) * 100, 1)

        # Análisis de clasificación
        classification = {
            "clasificacion_local": detail.get("clasificacion_local", "N/A"),
            "clasificacion_visitante": detail.get("clasificacion_visitante", "N/A"),
            "evolucion_clasificacion_local": detail.get("evolucion_clasificacion_local", []),
            "evolucion_clasificacion_visitante": detail.get("evolucion_clasificacion_visitante", []),
        }

        # Obtener últimos resultados
        matches = detail.get("ultimos_partidos", [])
        last_matches = {
            "local": [p for p in matches if p.get("tipo") in ["local_como_local", "local_como_visitante"]],
            "visitante": [p for p in matches if p.get("tipo") in ["visitante_como_local", "visitante_como_visitante"]],
            "local_como_local": [p for p in matches if p.get("tipo") == "local_como_local"],
            "local_como_visitante": [p for p in matches if p.get("tipo") == "local_como_visitante"],
            "visitante_como_local": [p for p in matches if p.get("tipo") == "visitante_como_local"],
            "visitante_como_visitante": [p for p in matches if p.get("tipo") == "visitante_como_visitante"],
        }

        racha_local = {
            "racha_general": [p["cod_resultado"] for p in last_matches["local"]],
            "racha_local_como_local": [p["cod_resultado"] for p in last_matches["local_como_local"]],
            "racha_local_como_visitante": [p["cod_resultado"] for p in last_matches["local_como_visitante"]],
        }

        racha_visitante = {
            "racha_general": [p["cod_resultado"] for p in last_matches["visitante"]],
            "racha_visitante_como_local": [p["cod_resultado"] for p in last_matches["visitante_como_local"]],
            "racha_visitante_como_visitante": [p["cod_resultado"] for p in last_matches["visitante_como_visitante"]],
        }

        # Generar predicción y justificación
        prediction, confidence, reasoning = self.__generate_prediction_with_reasoning(
            probs=probs,
            historical_analysis=historical_analysis
        )

        return {
            "info_partido": {
                "id_partido": match_id,
                "partido": prob["partido"],
                "jornada": jornada,
                "temporada": temporada,
            },
            "probabilidades": probs,
            "datos_historicos": historical_analysis,
            "prediccion": prediction,
            "confianza": confidence,
            "razonamiento": reasoning,
            "info_clasificacion": classification,
            "tendencias_local": {
                "tendencia_general": self.__analyze_trend(last_results=racha_local["racha_general"]),
                "tendencia_local_como_local": self.__analyze_trend(last_results=racha_local["racha_local_como_local"]),
            },
            "tendencias_visitante": {
                "tendencia_general": self.__analyze_trend(last_results=racha_visitante["racha_general"]),
                "tendencia_visitante_como_visitante": self.__analyze_trend(
                    last_results=racha_visitante["racha_visitante_como_visitante"]
                ),
            },
            "analisis_rendimiento_del_local_vs_visitante": self.__analyze_home_away_performance(
                resultados_local=racha_local["racha_general"], resultados_visitante=racha_visitante["racha_general"]
            ),
            "datos_destacados": detail.get("datos_destacados", []),
        }

    def analyze_team(self, jornada: int, temporada: int, team_name: str) -> dict[str, Any] | None:
        """
        Analiza el rendimiento completo de un equipo.

        Este método proporciona un análisis exhaustivo del rendimiento de un equipo específico,
        evaluando su trayectoria reciente, clasificación actual, rachas y desempeño diferenciado
        como local y visitante. Es especialmente útil para entender el contexto de un equipo
        antes de hacer predicciones o para responder consultas sobre su estado de forma.

        El proceso de análisis incluye:
        1. **Recuperación de datos**: Obtiene los detalles de todos los partidos de la jornada
           especificada mediante get_kiniela_matches_details().

        2. **Localización del equipo**: Busca el equipo en los partidos de la jornada comparando
           nombres (case-insensitive). Determina si juega como local o visitante analizando la
           posición en el string "EQUIPO1 - EQUIPO2".

        3. **Extracción de datos contextuales**: Según la condición (local/visitante), extrae:
           - Clasificación actual (posición en tabla)
           - Evolución reciente (lista de resultados: 'V', 'E', 'D')

        4. **Análisis de resultados recientes**: Procesa la lista de evolución para obtener los
           últimos 5 resultados del equipo, proporcionando visión de corto plazo.

        5. **Cálculo de racha actual**: Identifica series consecutivas de victorias,
           empates o derrotas basándose en los últimos resultados.

        6. **Evaluación de rendimiento local/visitante**: Analiza la evolución separando
           partidos en casa y fuera para calcular estadísticas específicas de cada escenario.

        7. **Determinación de tendencia**: Clasifica el momento del equipo como:
           - "Excelente": Racha de 3+ victorias
           - "Buena": Racha de 2+ sin derrotar
           - "Irregular": Mezcla de resultados
           - "Mala": Racha de 2+ derrotas

        8. **Consolidación del informe**: Estructura toda la información en un diccionario
           completo con secciones claramente organizadas.

        Ejemplos de uso:
        - Análisis de equipo en racha:
          analyze_team(26, 2025, "BARCELONA") → {'current_streak': {'type': 'V', 'length': 5,
          'description': '5 victorias consecutivas'}, 'trend': 'Excelente', ...}

        - Equipo con rendimiento irregular:
          analyze_team(26, 2025, "GETAFE") → {'current_streak': {'type': 'E', 'length': 1,
          'description': '1 empate'}, 'trend': 'Irregular', ...}

        - Error de equipo no encontrado:
          analyze_team(26, 2025, "EQUIPO_INEXISTENTE") → {'error': 'Equipo no encontrado...'}

        Este análisis es fundamental para evaluar contextos antes de predicciones y para
        responder preguntas específicas sobre el estado de forma de cualquier equipo.

        Parameters
        ----------
        jornada : int
            Número de jornada.
        temporada : int
            Año de la temporada.
        team_name : str
            Nombre del equipo a analizar.

        Returns
        -------
        dict[str, Any] | None
            Análisis completo del equipo con claves: team_name, classification, recent_results,
            current_streak, home_performance, away_performance, trend.
            Retorna None si hay algún error o el equipo no se encuentra.

        Examples
        --------
        >>> analyzer = Analyzer()
        >>> analysis = analyzer.analyze_team(jornada=26, temporada=2025, team_name="BARCELONA")
        >>> print(analysis["current_streak"])
        {'type': 'V', 'length': 5, 'description': '5 victorias consecutivas'}
        """
        # Obtener detalles de todos los partidos
        details = data_source.get_kiniela_matches_details(jornada=jornada, temporada=temporada)

        if details is None:
            return None

        # Buscar el equipo en los partidos
        team_match = None
        is_local = False

        for detail in details:
            partido = detail.get("partido", "")
            if team_name.upper() in partido.upper():
                team_match = detail
                # Determinar si es local o visitante
                parts = partido.split(" | ")
                if len(parts) == 2 and team_name.upper() in parts[0].upper():
                    is_local = True
                break

        if team_match is None:
            return {
                "error": f"Equipo '{team_name}' no encontrado en la jornada {jornada}",
            }

        # Extraer datos del equipo
        if is_local:
            classification = team_match.get("clasificacion_local", "N/A")
            classification_evol = team_match.get("evolucion_clasificacion_local", [])
        else:
            classification = team_match.get("clasificacion_visitante", "N/A")
            classification_evol = team_match.get("evolucion_clasificacion_visitante", [])

        # Obtener últimos resultados
        matches = team_match.get("ultimos_partidos", [])
        last_matches = {
            "local": [p for p in matches if p.get("tipo") in ["local_como_local", "local_como_visitante"]],
            "visitante": [p for p in matches if p.get("tipo") in ["visitante_como_local", "visitante_como_visitante"]],
            "local_como_local": [p for p in matches if p.get("tipo") == "local_como_local"],
            "local_como_visitante": [p for p in matches if p.get("tipo") == "local_como_visitante"],
            "visitante_como_local": [p for p in matches if p.get("tipo") == "visitante_como_local"],
            "visitante_como_visitante": [p for p in matches if p.get("tipo") == "visitante_como_visitante"],
        }
        recent_results_last_matches = last_matches["local"] if is_local else last_matches["visitante"]
        recent_results_last_matches_as_local = (
            last_matches["local_como_local"] if is_local else last_matches["visitante_como_local"]
        )
        recent_results_last_matches_as_visitor = (
            last_matches["local_como_visitante"] if is_local else last_matches["visitante_como_visitante"]
        )

        # Analizar tendencia
        global_trend = self.__analyze_trend(last_results=[p["cod_resultado"] for p in recent_results_last_matches])
        local_trend = self.__analyze_trend(
            last_results=[p["cod_resultado"] for p in recent_results_last_matches_as_local]
        )
        visitor_trend = self.__analyze_trend(
            last_results=[p["cod_resultado"] for p in recent_results_last_matches_as_visitor]
        )

        # Rendimiento local/visitante (basado en últimos resultados)
        resultados_local = [p["cod_resultado"] for p in recent_results_last_matches_as_local]
        resultados_visitante = [p["cod_resultado"] for p in recent_results_last_matches_as_visitor]
        home_away_analysis = self.__analyze_home_away_performance(
            resultados_local=resultados_local, resultados_visitante=resultados_visitante
        )

        return {
            "equipo": team_name,
            "clasificacion": classification,
            "evolucion_clasificacion": classification_evol,
            "juega_en_casa": is_local,
            "ultimos_5_partidos": recent_results_last_matches[-5:],
            "ultimos_5_partidos_como_local": recent_results_last_matches_as_local[-5:],
            "ultimos_5_partidos_como_visitante": recent_results_last_matches_as_visitor[-5:],
            "racha_ultimos_5_partidos": [p["cod_resultado"] for p in recent_results_last_matches][-5:],
            "racha_como_local_ultimos_5_partidos": [p["cod_resultado"] for p in recent_results_last_matches_as_local][
                -5:
            ],
            "racha_como_visitante_ultimos_5_partidos": [
                p["cod_resultado"] for p in recent_results_last_matches_as_visitor
            ][-5:],
            "tendencia_global": global_trend,
            "tendencia_como_local": local_trend,
            "tendencia_como_visitante": visitor_trend,
            "analisis_rendimiento_como_local_y_como_visitante": home_away_analysis,
            "proximo_partido": team_match.get("partido", "N/A"),
        }

    def __generate_prediction_with_reasoning(self, probs: dict[str, float],
                                             historical_analysis: dict[str, Any]) -> tuple[str, str, str]:
        """
        Genera predicción con justificación detallada.

        Este método crea una predicción completa combinando probabilidades LAE con análisis
        contextual, generando una justificación transparente basada en todos los factores
        considerados. El proceso sintetiza información cuantitativa y cualitativa para
        producir una predicción explicable.

        El proceso de generación incluye:
        1. **Selección de signo base**: Identifica el resultado con mayor probabilidad LAE
           como predicción inicial (puede ser '1', 'X' o '2').

        2. **Construcción de justificación base**: Inicia con la probabilidad LAE del signo
           seleccionado como primer argumento (ej: "Probabilidad LAE del 1: 65.3%").

        3. **Incorporación de contexto histórico**: Si existe historial de enfrentamientos
           (>=1 partido), añade estadísticas de victorias/empates del equipo favorecido
           (ej: "Histórico: Local gana 60% de los enfrentamientos (3 de 5)").

        4. **Cálculo de confianza**: Utiliza __calculate_confidence() para determinar el
           nivel de certeza (ALTA/MEDIA/BAJA) basado en probabilidad y consistencia
           histórica.

        5. **Formato de justificación**: Une todos los elementos con puntos para crear una
           explicación legible y coherente.

        Ejemplos:
        - Predicción fuerte: ("1", "ALTA", "Probabilidad LAE del 1: 68.5%. Histórico:
          Local gana 70% de los enfrentamientos (7 de 10).")
        - Predicción moderada: ("X", "MEDIA", "Probabilidad LAE del X: 42.3%.
          Histórico: 35% de empates (4 de 11).")
        - Predicción débil: ("2", "BAJA", "Probabilidad LAE del 2: 38.7%.")

        La justificación siempre incluye la probabilidad LAE como ancla cuantitativa,
        complementada con evidencia histórica y de forma reciente cuando está disponible.

        Parameters
        ----------
        probs : dict[str, float]
            Probabilidades LAE.
        historical_analysis : dict[str, Any]
            Análisis histórico de enfrentamientos.

        Returns
        -------
        tuple[str, str, str]
            Tupla con (predicción, confianza, justificación).
        """
        # Determinar signo base por probabilidad
        predicted_sign = max(probs, key=lambda k: probs[k])
        max_prob = probs[predicted_sign]

        # Construir justificación
        reasoning_parts = [f"Probabilidad LAE del {predicted_sign}: {max_prob:.1f}%"]

        # Agregar información histórica
        if historical_analysis.get("total_partidos", 0) > 0:
            if predicted_sign == "1":
                win_rate = historical_analysis.get("porcentaje_victorias_local", 0)
                reasoning_parts.append(
                    f"Histórico: Local gana {win_rate:.0f}% de los enfrentamientos "
                    f"({historical_analysis['victorias_local']} de {historical_analysis['total_partidos']})"
                )
            elif predicted_sign == "X":
                draw_rate = historical_analysis.get("porcentaje_empates", 0)
                reasoning_parts.append(
                    f"Histórico: {draw_rate:.0f}% de empates "
                    f"({historical_analysis['empates']} de {historical_analysis['total_partidos']})"
                )
            elif predicted_sign == "2":
                win_rate = historical_analysis.get("porcentaje_victorias_visitante", 0)
                reasoning_parts.append(
                    f"Histórico: Visitante gana {win_rate:.0f}% de los enfrentamientos "
                    f"({historical_analysis['victorias_visitante']} de {historical_analysis['total_partidos']})"
                )

        # Agregar información de rachas
        local_streak = {}
        visitor_streak = {}

        if local_streak.get("longitud", 0) >= 3:
            reasoning_parts.append(f"Local: {local_streak['descripcion']}")
        if visitor_streak.get("longitud", 0) >= 3:
            reasoning_parts.append(f"Visitante: {visitor_streak['descripcion']}")

        # Determinar confianza
        confidence = self.__calculate_confidence(max_prob=max_prob, historical_analysis=historical_analysis)

        reasoning = ". ".join(reasoning_parts) + "."

        return predicted_sign, confidence, reasoning

    def __calculate_confidence(self, max_prob: float, historical_analysis: dict[str, Any]) -> str:
        """
        Calcula el nivel de confianza de una predicción.

        Este método evalúa la certeza de una predicción mediante un sistema de puntuación
        que combina la probabilidad LAE base con ajustes contextuales derivados del
        historial de enfrentamientos y las rachas actuales de ambos equipos. El resultado
        es una clasificación cualitativa (ALTA/MEDIA/BAJA) que refleja la fiabilidad
        esperada de la predicción.

        El algoritmo de cálculo incluye:
        1. **Inicialización con probabilidad LAE**: Comienza con la probabilidad máxima
           como puntuación base (ej: max_prob=65.5 → confidence_score=65.5).

        2. **Ajuste por consistencia histórica**: Si existen 5+ enfrentamientos previos,
           incrementa la puntuación en 5 puntos. Esto refleja mayor confianza cuando hay
           evidencia estadística suficiente.

        3. **Clasificación por umbrales**: Convierte la puntuación final en categoría:
           - ALTA: confidence_score >= 60 (alta probabilidad + contexto favorable)
           - MEDIA: 45 <= confidence_score < 60 (probabilidad moderada o contexto mixto)
           - BAJA: confidence_score < 45 (probabilidad baja o contexto desfavorable)

        Ejemplos de cálculo:
        - Caso favorable: max_prob=68 + histórico(5) + racha_local(5) = 78 → ALTA
        - Caso moderado: max_prob=52 + histórico(5) + racha_visitor(3) = 60 → ALTA
        - Caso débil: max_prob=42 + histórico(0) + rachas(0) = 42 → BAJA
        - Caso límite: max_prob=55 + histórico(5) = 60 → ALTA (justo en umbral)

        La puntuación máxima teórica es ~110 (probabilidad 100 + histórico 5 + rachas 10),
        pero valores realistas oscilan entre 35-85.

        Parameters
        ----------
        max_prob : float
            Probabilidad máxima LAE.
        historical_analysis : dict[str, Any]
            Análisis histórico.

        Returns
        -------
        str
            Nivel de confianza: 'ALTA', 'MEDIA' o 'BAJA'.
        """
        confidence_score = max_prob

        # Ajustar por consistencia histórica
        if historical_analysis.get("total_partidos", 0) >= 5:
            confidence_score += 5

        # Ajustar por rachas
        local_streak = {}
        visitor_streak = {}

        if local_streak.get("longitud", 0) >= 3 or visitor_streak.get("longitud", 0) >= 3:
            confidence_score += 5

        if confidence_score >= 60:
            return "ALTA"
        elif confidence_score >= 45:
            return "MEDIA"
        else:
            return "BAJA"

    def __analyze_trend(self, last_results: list[str]) -> dict[str, Any]:
        """
        Analiza la tendencia del equipo en sus últimos partidos.

        Este método evalúa la trayectoria reciente del equipo clasificando su momentum en
        categorías cualitativas (Excelente, Buena, Regular, Mala) basándose en patrones
        de resultados. A diferencia de análisis que solo miran rachas consecutivas,
        este método considera la composición general de los últimos resultados para dar
        una evaluación más matizada del momento del equipo.

        El algoritmo de clasificación incluye:
        1. **Conteo de resultados**: Cuenta victorias, empates y derrotas en los últimos
           partidos disponibles (mínimo 3).

        2. **Identificación de racha excepcional**: Si hay 3+ del mismo resultado consecutivo,
           clasifica como:
           - "Excelente" si son victorias
           - "Buena" si son empates (sin perder)
           - "Mala" si son derrotas

        3. **Evaluación por balance de resultados**: Si no hay racha significativa, analiza
           el balance general basado en efectividad porcentual:
           - "Excelente": ≥80% efectividad
           - "Buena": 60-80% efectividad
           - "Regular": 40-60% efectividad
           - "Mala": <40% efectividad

        4. **Construcción de mensaje descriptivo**: Genera un texto explicativo con la
           distribución de resultados.

        Ejemplos de clasificación:
        - ['VICTORIA','VICTORIA','VICTORIA','VICTORIA','EMPATE'] → Excelente (4V-1E-0D, racha de 4 victorias)
        - ['EMPATE','EMPATE','EMPATE','VICTORIA','DERROTA'] → Buena (1V-3E-1D, solo 1 derrota)
        - ['DERROTA','DERROTA','DERROTA','EMPATE','VICTORIA'] → Mala (1V-1E-3D, racha de 3 derrotas)
        - ['VICTORIA','DERROTA','EMPATE','VICTORIA','DERROTA'] → Regular (2V-1E-2D, resultados mezclados)
        - ['VICTORIA','VICTORIA','EMPATE'] → Buena (2V-1E-0D, 78% efectividad)

        La tendencia es más informativa que la racha cuando hay alternancia de resultados,
        ya que captura el rendimiento agregado en lugar de solo la consistencia reciente.

        Parameters
        ----------
        results : list[str]
            Lista de resultados recientes con valores: 'VICTORIA', 'EMPATE', 'DERROTA'.

        Returns
        -------
        dict[str, Any]
            Análisis de tendencia: dirección (mejorando/empeorando/estable),
            puntos_últimos_partidos, forma (excelente/buena/regular/mala).
        """
        if not last_results or len(last_results) < 3:
            return {"direccion": "unknown", "descripcion": "Datos insuficientes"}

        # Calcular puntos de los últimos partidos disponibles
        points_map = {"VICTORIA": 3, "EMPATE": 1, "DERROTA": 0}
        last_n = last_results[-5:] if len(last_results) >= 5 else last_results  # Usar todos si menos de 5
        points = sum(points_map.get(r, 0) for r in last_n)

        # Calcular efectividad porcentual
        max_points = len(last_n) * 3
        effectiveness = (points / max_points * 100) if max_points > 0 else 0.0

        # Calcular puntos de los partidos anteriores para comparar
        previous_n = last_results[-10:-5] if len(last_results) >= 10 else []
        previous_points = sum(points_map.get(r, 0) for r in previous_n) if previous_n else points

        # Determinar tendencia
        if points > previous_points:
            direction = "mejorando"
            description = "Tendencia al alza"
        elif points < previous_points:
            direction = "empeorando"
            description = "Tendencia a la baja"
        else:
            direction = "estable"
            description = "Rendimiento estable"

        # Evaluar forma basada en efectividad porcentual
        if effectiveness >= 80:
            form = "excelente"
        elif effectiveness >= 60:
            form = "buena"
        elif effectiveness >= 40:
            form = "regular"
        else:
            form = "mala"

        return {
            "direccion": direction,
            "descripcion": description,
            "puntos_ultimos_partidos": points,
            "porcentaje_puntos_ultimos_partidos": round(effectiveness, 1),
            "forma": form,
            "ultimos_resultados": last_n,
        }

    def __analyze_home_away_performance(
        self, resultados_local: list[str], resultados_visitante: list[str]
    ) -> dict[str, Any]:
        """
        Analiza el rendimiento local vs visitante basado en listas de resultados.

        Este método separa y evalúa el desempeño del equipo en dos contextos distintos:
        jugando en casa (local) y jugando fuera (visitante). Esta diferenciación es crucial
        porque muchos equipos tienen rendimientos significativamente diferentes según el
        escenario, lo que afecta la predicción de resultados futuros.

        El proceso de análisis incluye:
        1. **Procesamiento de resultados**: Para cada contexto (local/visitante), procesa
           la lista de resultados ('VICTORIA', 'EMPATE', 'DERROTA').

        2. **Conteo de resultados por contexto**: Cuenta las victorias, empates y derrotas.
           Por ejemplo:
           - Local: 4V, 1E, 0D
           - Visitante: 1V, 2E, 2D

        3. **Cálculo de puntos**: Asigna puntos según la fórmula estándar (V=3, E=1, D=0)
           para obtener métricas cuantitativas comparables:
           - Local: 4×3 + 1×1 + 0×0 = 13 puntos
           - Visitante: 1×3 + 2×1 + 2×0 = 5 puntos

        4. **Cálculo de efectividad**: Determina el porcentaje de puntos obtenidos sobre
           el máximo posible (partidos × 3):
           - Local: 13/(5×3) = 86.7% efectividad
           - Visitante: 5/(5×3) = 33.3% efectividad

        5. **Clasificación cualitativa**: Evalúa el rendimiento según efectividad:
           - "Excelente": ≥70% (muy fuerte en ese contexto)
           - "Bueno": 50-70% (rendimiento sólido)
           - "Regular": 30-50% (desempeño moderado)
           - "Malo": <30% (dificultades en ese escenario)

        6. **Generación de descriptores**: Crea textos informativos como "4V-1E-0D (13pts)"
           para cada contexto, facilitando la interpretación rápida.

        Ejemplos de análisis:
        - Equipo fuerte en casa: {'local': {'registro': '5V-0E-0D', 'puntos': 15,
          'porcentaje_puntos_conseguidos': 100.0, 'calificacion': 'Excelente'},
          'visitante': {'registro': '1V-1E-3D', 'puntos': 4, 'porcentaje_puntos_conseguidos': 26.7,
          'calificacion': 'Malo'}, 'comparacion': 'Mejor local'}

        - Equipo equilibrado: {'local': {'registro': '3V-1E-1D', 'puntos': 10,
          'porcentaje_puntos_conseguidos': 66.7, 'calificacion': 'Bueno'},
          'visitante': {'registro': '2V-2E-1D', 'puntos': 8, 'porcentaje_puntos_conseguidos': 53.3,
          'calificacion': 'Bueno'}, 'comparacion': 'Equilibrado'}

        Esta separación revela patrones importantes como "fortaleza de local" o "efectividad
        visitante", factores cruciales en predicciones de quiniela.

        Parameters
        ----------
        resultados_local : list[str]
            Lista de resultados como local ('VICTORIA', 'EMPATE', 'DERROTA').
        resultados_visitante : list[str]
            Lista de resultados como visitante ('VICTORIA', 'EMPATE', 'DERROTA').

        Returns
        -------
        dict[str, Any]
            Análisis de rendimiento local y visitante con métricas detalladas y comparación.
            Incluye 'local', 'visitante' con métricas individuales, y 'comparacion'
            indicando si el equipo rinde mejor en casa, fuera o equilibradamente.
            Retorna diccionario vacío si no hay suficientes datos.
        """
        # Verificar que ambas listas tengan al menos 1 elemento
        if not resultados_local or not resultados_visitante:
            return {}

        def analyze_context(results: list[str]) -> dict[str, Any]:
            """Analiza resultados para un contexto específico."""
            if not results:
                return {
                    "registro": "Sin datos",
                    "puntos": 0,
                    "porcentaje_puntos_conseguidos": 0.0,
                    "calificacion": "Sin datos",
                }

            # Contar resultados
            wins = results.count("VICTORIA")
            draws = results.count("EMPATE")
            losses = results.count("DERROTA")
            total_matches = len(results)

            # Calcular puntos
            points = wins * 3 + draws * 1 + losses * 0

            # Calcular efectividad
            max_points = total_matches * 3
            effectiveness = (points / max_points * 100) if max_points > 0 else 0.0

            # Clasificar rendimiento
            if effectiveness >= 70:
                rating = "Excelente"
            elif effectiveness >= 50:
                rating = "Bueno"
            elif effectiveness >= 30:
                rating = "Regular"
            else:
                rating = "Malo"

            # Generar record
            record = f"{wins}V-{draws}E-{losses}D ({points}pts)"

            return {
                "registro": record,
                "puntos": points,
                "porcentaje_puntos_conseguidos": round(effectiveness, 1),
                "calificacion": rating,
            }

        home_analysis = analyze_context(resultados_local)
        away_analysis = analyze_context(resultados_visitante)

        # Comparar rendimiento local vs visitante
        home_effectiveness = home_analysis["porcentaje_puntos_conseguidos"]
        away_effectiveness = away_analysis["porcentaje_puntos_conseguidos"]

        if home_effectiveness > away_effectiveness + 10:
            comparison = "Mejor local"
        elif away_effectiveness > home_effectiveness + 10:
            comparison = "Mejor visitante"
        else:
            comparison = "Equilibrado Local/Visitante"

        return {"local": home_analysis, "visitante": away_analysis, "comparacion": comparison}
