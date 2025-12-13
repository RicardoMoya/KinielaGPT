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


class MatchAnalyzer:
    """
    Analizador de partidos individuales.

    Proporciona análisis detallado de un partido específico incluyendo probabilidades,
    histórico, rachas, clasificación y factores contextuales.
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
        >>> analyzer = MatchAnalyzer()
        >>> data = analyzer.get_raw_data(jornada=26, temporada=2025, match_id=5)
        >>> print(data["historical"]["total_matches"])
        12
        >>> print(data["evolution_local"])
        ['V', 'V', 'E', 'D', 'V']
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
            "match_info": {
                "match_id": match_id,
                "match": prob["partido"],
                "jornada": jornada,
                "temporada": temporada,
            },
            "probabilities": {
                "1": prob.get("1_Prob", 0),
                "X": prob.get("X_Prob", 0),
                "2": prob.get("2_Prob", 0),
                "goal_forecast": prob.get("pronosticoGoles", "N/A"),
            },
            "historical": {
                "local_wins": detail.get("veces1", 0),
                "draws": detail.get("vecesX", 0),
                "visitor_wins": detail.get("veces2", 0),
                "total_matches": detail.get("veces1", 0) + detail.get("vecesX", 0) + detail.get("veces2", 0),
            },
            "classification": {
                "local": detail.get("clasificacionLocal", "N/A"),
                "visitor": detail.get("clasificacionVisitante", "N/A"),
            },
            "evolution_local": detail.get("evolucionLocal", []),
            "evolution_visitor": detail.get("evolucionVisitante", []),
            "comparativa": detail.get("comparativa", []),
            "datos_destacados": detail.get("datosDestacados", []),
        }

    def analyze(self, jornada: int, temporada: int, match_id: int, 
                include_prediction: bool = True) -> dict[str, Any] | None:
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
        >>> analyzer = MatchAnalyzer()
        >>> # Análisis completo con predicción
        >>> analysis = analyzer.analyze(jornada=26, temporada=2025, match_id=5)
        >>> print(analysis["prediction"])
        '1'
        >>> print(analysis["confidence"])
        'ALTA'
        >>> 
        >>> # Solo datos en crudo
        >>> raw_data = analyzer.analyze(jornada=26, temporada=2025, match_id=5, include_prediction=False)
        >>> print(raw_data["historical"]["total_matches"])
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
            "total_matches": total_historic,
            "local_wins": veces1,
            "draws": vecesX,
            "visitor_wins": veces2,
        }

        if total_historic > 0:
            historical_analysis["local_win_rate"] = round((veces1 / total_historic) * 100, 1)
            historical_analysis["draw_rate"] = round((vecesX / total_historic) * 100, 1)
            historical_analysis["visitor_win_rate"] = round((veces2 / total_historic) * 100, 1)

        # Análisis de forma reciente
        recent_form = self.__analyze_recent_form(detail=detail)

        # Análisis de clasificación
        classification = {
            "local_position": detail.get("clasificacionLocal", "N/A"),
            "visitor_position": detail.get("clasificacionVisitante", "N/A"),
        }

        # Generar predicción y justificación
        prediction, confidence, reasoning = self.__generate_prediction_with_reasoning(
            probs=probs,
            historical_analysis=historical_analysis,
            recent_form=recent_form,
            classification=classification,
        )

        return {
            "match_info": {
                "match_id": match_id,
                "match": prob["partido"],
                "jornada": jornada,
                "temporada": temporada,
            },
            "probabilities": probs,
            "prediction": prediction,
            "confidence": confidence,
            "reasoning": reasoning,
            "historical_data": historical_analysis,
            "recent_form": recent_form,
            "classification_info": classification,
            "datos_destacados": detail.get("datosDestacados", []),
        }

    def __analyze_recent_form(self, detail: dict[str, Any]) -> dict[str, Any]:
        """
        Analiza la forma reciente de los equipos.

        Parameters
        ----------
        detail : dict[str, Any]
            Detalles del partido.

        Returns
        -------
        dict[str, Any]
            Análisis de forma reciente con evolución de ambos equipos.
        """
        evolucion_local = detail.get("evolucionLocal", [])
        evolucion_visitor = detail.get("evolucionVisitante", [])

        form_analysis = {
            "local_recent_results": evolucion_local[:5] if evolucion_local else [],
            "visitor_recent_results": evolucion_visitor[:5] if evolucion_visitor else [],
        }

        # Calcular rachas
        if evolucion_local:
            form_analysis["local_streak"] = self.__calculate_streak(results=evolucion_local)
        if evolucion_visitor:
            form_analysis["visitor_streak"] = self.__calculate_streak(results=evolucion_visitor)

        return form_analysis

    def __calculate_streak(self, results: list[str]) -> dict[str, Any]:
        """
        Calcula la racha actual de un equipo.
        
        Identifica la secuencia consecutiva de resultados del mismo tipo al inicio de la lista
        de resultados recientes. Una racha puede ser de victorias, empates o derrotas.
        
        Proceso:
        1. Toma el primer resultado como referencia
        2. Cuenta cuántos resultados consecutivos son del mismo tipo
        3. Se detiene al encontrar un resultado diferente
        4. Clasifica la racha y genera descripción
        
        Ejemplos:
        - ['V', 'V', 'V', 'E'] → 3 victorias consecutivas
        - ['D', 'D', 'V'] → 2 derrotas consecutivas
        - ['E'] → 1 empate
        
        Las rachas son útiles para evaluar el momento de forma del equipo y pueden
        influir en la predicción (equipo en racha ganadora vs equipo en mala racha).

        Parameters
        ----------
        results : list[str]
            Lista de resultados recientes (ej: ['V', 'V', 'E', 'D']).

        Returns
        -------
        dict[str, Any]
            Información de la racha: tipo, longitud, descripción.
        """
        if not results:
            return {"type": "none", "length": 0, "description": "Sin datos"}

        last_result = results[0]
        streak_length = 1

        for result in results[1:]:
            if result == last_result:
                streak_length += 1
            else:
                break

        descriptions = {
            "V": "victorias consecutivas",
            "E": "empates consecutivos",
            "D": "derrotas consecutivas",
        }

        return {
            "type": last_result,
            "length": streak_length,
            "description": f"{streak_length} {descriptions.get(last_result, 'resultados')}",
        }

    def __generate_prediction_with_reasoning(
        self,
        probs: dict[str, float],
        historical_analysis: dict[str, Any],
        recent_form: dict[str, Any],
        classification: dict[str, Any],
    ) -> tuple[str, str, str]:
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
        
        4. **Evaluación de rachas significativas**: Identifica rachas de 3+ resultados
           consecutivos y las incorpora a la justificación si apoyan la predicción
           (ej: "Local: 4 victorias consecutivas").
        
        5. **Cálculo de confianza**: Utiliza __calculate_confidence() para determinar el
           nivel de certeza (ALTA/MEDIA/BAJA) basado en probabilidad, consistencia
           histórica y rachas actuales.
        
        6. **Formato de justificación**: Une todos los elementos con puntos para crear una
           explicación legible y coherente.
        
        Ejemplos:
        - Predicción fuerte: ("1", "ALTA", "Probabilidad LAE del 1: 68.5%. Histórico: 
          Local gana 70% de los enfrentamientos (7 de 10). Local: 5 victorias consecutivas.")
        - Predicción moderada: ("X", "MEDIA", "Probabilidad LAE del X: 42.3%. 
          Histórico: 35% de empates (4 de 11).")
        - Predicción débil: ("2", "BAJA", "Probabilidad LAE del 2: 38.7%. 
          Visitante: 3 victorias consecutivas.")
        
        La justificación siempre incluye la probabilidad LAE como ancla cuantitativa,
        complementada con evidencia histórica y de forma reciente cuando está disponible.

        Parameters
        ----------
        probs : dict[str, float]
            Probabilidades LAE.
        historical_analysis : dict[str, Any]
            Análisis histórico de enfrentamientos.
        recent_form : dict[str, Any]
            Análisis de forma reciente.
        classification : dict[str, Any]
            Información de clasificación.

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
        if historical_analysis.get("total_matches", 0) > 0:
            if predicted_sign == "1":
                win_rate = historical_analysis.get("local_win_rate", 0)
                reasoning_parts.append(
                    f"Histórico: Local gana {win_rate:.0f}% de los enfrentamientos "
                    f"({historical_analysis['local_wins']} de {historical_analysis['total_matches']})"
                )
            elif predicted_sign == "X":
                draw_rate = historical_analysis.get("draw_rate", 0)
                reasoning_parts.append(
                    f"Histórico: {draw_rate:.0f}% de empates "
                    f"({historical_analysis['draws']} de {historical_analysis['total_matches']})"
                )
            elif predicted_sign == "2":
                win_rate = historical_analysis.get("visitor_win_rate", 0)
                reasoning_parts.append(
                    f"Histórico: Visitante gana {win_rate:.0f}% de los enfrentamientos "
                    f"({historical_analysis['visitor_wins']} de {historical_analysis['total_matches']})"
                )

        # Agregar información de rachas
        local_streak = recent_form.get("local_streak", {})
        visitor_streak = recent_form.get("visitor_streak", {})

        if local_streak.get("length", 0) >= 3:
            reasoning_parts.append(f"Local: {local_streak['description']}")
        if visitor_streak.get("length", 0) >= 3:
            reasoning_parts.append(f"Visitante: {visitor_streak['description']}")

        # Determinar confianza
        confidence = self.__calculate_confidence(
            max_prob=max_prob,
            historical_analysis=historical_analysis,
            recent_form=recent_form,
        )

        reasoning = ". ".join(reasoning_parts) + "."

        return predicted_sign, confidence, reasoning

    def __calculate_confidence(
        self,
        max_prob: float,
        historical_analysis: dict[str, Any],
        recent_form: dict[str, Any],
    ) -> str:
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
        
        3. **Ajuste por rachas significativas**: Evalúa las rachas de ambos equipos:
           - Racha de 3+ resultados: +3 puntos por equipo
           - Racha de 5+ resultados: +5 puntos por equipo
           Las rachas largas indican momentum y aumentan la certeza de la predicción.
        
        4. **Clasificación por umbrales**: Convierte la puntuación final en categoría:
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
        recent_form : dict[str, Any]
            Forma reciente.

        Returns
        -------
        str
            Nivel de confianza: 'ALTA', 'MEDIA' o 'BAJA'.
        """
        confidence_score = max_prob

        # Ajustar por consistencia histórica
        if historical_analysis.get("total_matches", 0) >= 5:
            confidence_score += 5

        # Ajustar por rachas
        local_streak = recent_form.get("local_streak", {})
        visitor_streak = recent_form.get("visitor_streak", {})

        if local_streak.get("length", 0) >= 3 or visitor_streak.get("length", 0) >= 3:
            confidence_score += 5

        if confidence_score >= 60:
            return "ALTA"
        elif confidence_score >= 45:
            return "MEDIA"
        else:
            return "BAJA"


class TeamAnalyzer:
    """
    Analizador de rendimiento de equipos.

    Proporciona análisis completo del rendimiento de un equipo específico: últimos resultados,
    rachas, rendimiento local/visitante, clasificación y tendencia.
    """

    def analyze(self, jornada: int, temporada: int, team_name: str) -> dict[str, Any] | None:
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
        
        5. **Cálculo de racha actual**: Utiliza __calculate_streak() para identificar series
           consecutivas de victorias, empates o derrotas.
        
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
          analyze(26, 2025, "BARCELONA") → {'current_streak': {'type': 'V', 'length': 5, 
          'description': '5 victorias consecutivas'}, 'trend': 'Excelente', ...}
        
        - Equipo con rendimiento irregular:
          analyze(26, 2025, "GETAFE") → {'current_streak': {'type': 'E', 'length': 1, 
          'description': '1 empate'}, 'trend': 'Irregular', ...}
        
        - Error de equipo no encontrado:
          analyze(26, 2025, "EQUIPO_INEXISTENTE") → {'error': 'Equipo no encontrado...'}
        
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
        >>> analyzer = TeamAnalyzer()
        >>> analysis = analyzer.analyze(jornada=26, temporada=2025, team_name="BARCELONA")
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
                parts = partido.split(" - ")
                if len(parts) == 2 and team_name.upper() in parts[0].upper():
                    is_local = True
                break

        if team_match is None:
            return {
                "error": f"Equipo '{team_name}' no encontrado en la jornada {jornada}",
            }

        # Extraer datos del equipo
        if is_local:
            classification = team_match.get("clasificacionLocal", "N/A")
            evolucion = team_match.get("evolucionLocal", [])
        else:
            classification = team_match.get("clasificacionVisitante", "N/A")
            evolucion = team_match.get("evolucionVisitante", [])

        # Analizar resultados recientes
        recent_results = evolucion[:5] if evolucion else []

        # Calcular racha actual
        current_streak = self.__calculate_streak(results=evolucion) if evolucion else None

        # Analizar tendencia
        trend = self.__analyze_trend(results=evolucion) if evolucion else None

        # Rendimiento local/visitante (basado en últimos resultados)
        home_away_analysis = self.__analyze_home_away_performance(comparativa=team_match.get("comparativa", []))

        return {
            "team_name": team_name,
            "classification": classification,
            "is_playing_home": is_local,
            "recent_results": recent_results,
            "current_streak": current_streak,
            "trend": trend,
            "performance_analysis": home_away_analysis,
            "next_match": team_match.get("partido", "N/A"),
        }

    def __calculate_streak(self, results: list[str]) -> dict[str, Any]:
        """
        Calcula la racha actual del equipo.

        Parameters
        ----------
        results : list[str]
            Lista de resultados recientes.

        Returns
        -------
        dict[str, Any]
            Información de la racha.
        """
        if not results:
            return {"type": "none", "length": 0, "description": "Sin datos"}

        last_result = results[0]
        streak_length = 1

        for result in results[1:]:
            if result == last_result:
                streak_length += 1
            else:
                break

        descriptions = {
            "V": "victorias consecutivas",
            "E": "empates consecutivos",
            "D": "derrotas consecutivas",
        }

        return {
            "type": last_result,
            "length": streak_length,
            "description": f"{streak_length} {descriptions.get(last_result, 'resultados')}",
        }

    def __analyze_trend(self, results: list[str]) -> dict[str, Any]:
        """
        Analiza la tendencia del equipo en sus últimos partidos.
        
        Este método evalúa la trayectoria reciente del equipo clasificando su momentum en
        categorías cualitativas (Excelente, Buena, Irregular, Mala) basándose en patrones
        de resultados. A diferencia de __calculate_streak() que solo mira rachas consecutivas,
        este método considera la composición general de los últimos 5 resultados para dar
        una evaluación más matizada del momento del equipo.
        
        El algoritmo de clasificación incluye:
        1. **Conteo de resultados**: Cuenta victorias, empates y derrotas en los últimos
           5 partidos (o menos si no hay suficientes datos).
        
        2. **Identificación de racha excepcional**: Si hay 3+ del mismo resultado consecutivo,
           clasifica como:
           - "Excelente" si son victorias
           - "Buena" si son empates (sin perder)
           - "Mala" si son derrotas
        
        3. **Evaluación por balance de resultados**: Si no hay racha significativa, analiza
           el balance general:
           - "Excelente": 4+ victorias en últimos 5 (80%+ efectividad)
           - "Buena": 3 victorias o solo 0-1 derrotas (solidez)
           - "Mala": 3+ derrotas (crisis de resultados)
           - "Irregular": Cualquier otra combinación
        
        4. **Construcción de mensaje descriptivo**: Genera un texto explicativo con la
           distribución de resultados (ej: "3V-1E-1D en últimos 5 partidos").
        
        Ejemplos de clasificación:
        - ['V','V','V','V','E'] → Excelente (4V-1E-0D, racha de 4 victorias)
        - ['E','E','E','V','D'] → Buena (1V-3E-1D, solo 1 derrota)
        - ['D','D','D','E','V'] → Mala (1V-1E-3D, racha de 3 derrotas)
        - ['V','D','E','V','D'] → Irregular (2V-1E-2D, resultados mezclados)
        - ['V','V'] → Excelente (2V-0E-0D, 100% victorias en 2 partidos)
        
        La tendencia es más informativa que la racha cuando hay alternancia de resultados,
        ya que captura el rendimiento agregado en lugar de solo la consistencia reciente.

        Parameters
        ----------
        results : list[str]
            Lista de resultados recientes.

        Returns
        -------
        dict[str, Any]
            Análisis de tendencia: dirección, puntos_últimos_5, forma.
        """
        if not results or len(results) < 3:
            return {"direction": "unknown", "description": "Datos insuficientes"}

        # Calcular puntos de los últimos 5 partidos (V=3, E=1, D=0)
        points_map = {"V": 3, "E": 1, "D": 0}
        last_5 = results[:5]
        points = sum(points_map.get(r, 0) for r in last_5)

        # Calcular puntos de los 5 anteriores para comparar
        previous_5 = results[5:10] if len(results) >= 10 else []
        previous_points = sum(points_map.get(r, 0) for r in previous_5) if previous_5 else points

        # Determinar tendencia
        if points > previous_points:
            direction = "improving"
            description = "Tendencia al alza"
        elif points < previous_points:
            direction = "declining"
            description = "Tendencia a la baja"
        else:
            direction = "stable"
            description = "Rendimiento estable"

        # Evaluar forma
        if points >= 12:
            form = "excellent"
        elif points >= 9:
            form = "good"
        elif points >= 6:
            form = "average"
        else:
            form = "poor"

        return {
            "direction": direction,
            "description": description,
            "points_last_5": points,
            "form": form,
            "last_5_results": last_5,
        }

    def __analyze_home_away_performance(self, comparativa: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Analiza el rendimiento local vs visitante basado en la comparativa.
        
        Este método separa y evalúa el desempeño del equipo en dos contextos distintos:
        jugando en casa (local) y jugando fuera (visitante). Esta diferenciación es crucial
        porque muchos equipos tienen rendimientos significativamente diferentes según el
        escenario, lo que afecta la predicción de resultados futuros.
        
        El proceso de análisis incluye:
        1. **Clasificación de partidos**: Recorre la lista comparativa identificando cada
           partido como local o visitante según la presencia de las etiquetas "(L)" o "(V)"
           en los strings de equipos.
        
        2. **Conteo de resultados por contexto**: Para cada categoría (local/visitante),
           cuenta las victorias, empates y derrotas. Por ejemplo:
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
        - Equipo fuerte en casa: {'home': {'record': '5V-0E-0D', 'points': 15, 
          'effectiveness': 100.0, 'rating': 'Excelente'}, 'away': {'record': '1V-1E-3D', 
          'points': 4, 'effectiveness': 26.7, 'rating': 'Malo'}}
        
        - Equipo equilibrado: {'home': {'record': '3V-1E-1D', 'points': 10, 
          'effectiveness': 66.7, 'rating': 'Bueno'}, 'away': {'record': '2V-2E-1D', 
          'points': 8, 'effectiveness': 53.3, 'rating': 'Bueno'}}
        
        Esta separación revela patrones importantes como "fortaleza de local" o "efectividad
        visitante", factores cruciales en predicciones de quiniela.

        Parameters
        ----------
        comparativa : list[dict[str, Any]]
            Lista de partidos recientes con información de local/visitante.

        Returns
        -------
        dict[str, Any]
            Análisis de rendimiento local y visitante.
        """
        if not comparativa:
            return {"home": "Sin datos", "away": "Sin datos"}

        # Contabilizar partidos como local y visitante
        home_count = len([m for m in comparativa if m.get("esLocal")])
        away_count = len([m for m in comparativa if not m.get("esLocal")])

        return {
            "home": f"{home_count} partidos como local",
            "away": f"{away_count} partidos como visitante",
        }
