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
Motor de predicción de quiniela con múltiples estrategias.

Este módulo implementa las tres estrategias de predicción:
- Conservadora: Selecciona siempre el signo con mayor probabilidad
- Arriesgada: Balancea probabilidades con análisis contextual
- Personalizada: Optimiza según distribución de signos especificada por el usuario
"""

from typing import Any

from kinielagpt import data_source


class KinielaPredictor:
    """
    Predictor de quiniela con soporte para múltiples estrategias.

    Attributes
    ----------
    _strategies : dict
        Diccionario mapeando nombres de estrategias a métodos de predicción.
    """

    def __init__(self) -> None:
        """
        Inicializa el predictor con las estrategias disponibles.
        """
        self.__strategies = {
            "conservadora": self.__predict_conservative,
            "arriesgada": self.__predict_risky,
            "personalizada": self.__predict_custom,
        }

    def predict(
        self,
        jornada: int,
        temporada: int,
        strategy: str = "conservadora",
        custom_distribution: dict[str, int] | None = None,
    ) -> dict[str, Any] | None:
        """
        Genera una predicción completa de quiniela.
        
        Este método es el punto de entrada principal para generar predicciones. Coordina la obtención
        de datos (probabilidades LAE y detalles de partidos), valida los parámetros de entrada, ejecuta
        la estrategia de predicción seleccionada y genera un resumen de la distribución de signos.
        
        El proceso incluye:
        1. Validación de la estrategia y parámetros
        2. Obtención de probabilidades LAE y detalles de partidos
        3. Ejecución de la estrategia seleccionada (conservadora, arriesgada o personalizada)
        4. Cálculo del resumen con distribución final de signos
        5. Retorno del resultado completo con predicciones y metadatos

        Parameters
        ----------
        jornada : int
            Número de jornada a predecir.
        temporada : int
            Año de la temporada.
        strategy : str, optional
            Estrategia de predicción: "conservadora", "arriesgada" o "personalizada" (default: "conservadora").
        custom_distribution : dict[str, int] | None, optional
            Distribución personalizada para strategy="personalizada". Debe contener claves:
            "1", "X", "2". Si no se proporciona, usa distribución por defecto: {"1": 7, "X": 4, "2": 4}.
            Ejemplo: {"1": 8, "X": 4, "2": 3}.

        Returns
        -------
        dict[str, Any] | None
            Diccionario con la predicción completa:
            - jornada: Número de jornada
            - temporada: Año de temporada
            - strategy: Estrategia utilizada
            - predictions: Lista de 15 predicciones, cada una con match_id, match, prediction, confidence, reasoning, 
                           probabilities
            - summary: Resumen con distribución de signos
            Retorna None si hay algún error.

        Raises
        ------
        ValueError
            Si la estrategia no es válida o custom_distribution es inválida.

        Examples
        --------
        >>> predictor = KinielaPredictor()
        >>> # Predicción conservadora
        >>> pred = predictor.predict(jornada=26, temporada=2025, strategy="conservadora")
        >>> print(pred["summary"])
        {'1': 9, 'X': 3, '2': 3}
        >>>
        >>> # Predicción personalizada
        >>> pred = predictor.predict(
        ...     jornada=26,
        ...     temporada=2025,
        ...     strategy="personalizada",
        ...     custom_distribution={"1": 8, "X": 4, "2": 3}
        ... )
        """
        if strategy not in self.__strategies:
            raise ValueError(f"Estrategia desconocida: {strategy}. Opciones: {list(self.__strategies.keys())}")

        if strategy == "personalizada":
            if custom_distribution is not None and not self.__validate_custom_distribution(
                distribution=custom_distribution
            ):
                raise ValueError("custom_distribution inválida. Debe sumar 15 y contener claves '1', 'X', '2'")

        # Obtener datos necesarios
        probabilities = data_source.get_kiniela_probabilities(jornada=jornada, temporada=temporada)
        details = data_source.get_kiniela_matches_details(jornada=jornada, temporada=temporada)

        if probabilities is None or details is None:
            return None

        # Ejecutar estrategia seleccionada
        predictions = self.__strategies[strategy](
            probabilities=probabilities,
            details=details,
            custom_distribution=custom_distribution,
        )

        # Calcular resumen
        summary = self.__calculate_summary(predictions=predictions)

        return {
            "jornada": jornada,
            "temporada": temporada,
            "strategy": strategy,
            "predictions": predictions,
            "summary": summary,
        }

    def __predict_conservative(self, probabilities: list[dict[str, Any]], 
                               details: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Estrategia conservadora: Selecciona siempre el signo con mayor probabilidad.
        
        Esta estrategia minimiza el riesgo siguiendo únicamente las probabilidades LAE oficiales.
        Para cada partido, identifica el signo (1, X, 2) con la probabilidad más alta y lo selecciona
        como predicción. Es ideal para maximizar el número esperado de aciertos.
        
        El algoritmo:
        1. Para cada partido, extrae las probabilidades de 1, X y 2
        2. Identifica el signo con la probabilidad máxima
        3. Asigna nivel de confianza según el valor de la probabilidad:
           - ALTA: >= 60%
           - MEDIA: 45% - 60%
           - BAJA: < 45%
        4. Genera una justificación simple basada en la probabilidad LAE

        Parameters
        ----------
        probabilities : list[dict[str, Any]]
            Lista de probabilidades de cada partido.
        details : list[dict[str, Any]]
            Lista de detalles de cada partido.

        Returns
        -------
        list[dict[str, Any]]
            Lista de predicciones para los 15 partidos.
        """
        predictions = []

        for i, (prob, detail) in enumerate(iterable=zip(probabilities, details), start=1):
            # Determinar signo con mayor probabilidad
            probs = {
                "1": prob.get("1_Prob", 0),
                "X": prob.get("X_Prob", 0),
                "2": prob.get("2_Prob", 0),
            }
            predicted_sign = max(probs, key=lambda k: probs[k])
            max_prob = probs[predicted_sign]

            # Determinar nivel de confianza basado en probabilidad
            if max_prob >= 60:
                confidence = "ALTA"
            elif 45 <= max_prob < 60:
                confidence = "MEDIA"
            else:
                confidence = "BAJA"

            # Generar justificación
            reasoning = f"Probabilidad LAE del {predicted_sign}: {max_prob:.1f}% (la más alta)"

            predictions.append(
                {
                    "match_id": i,
                    "match": prob["partido"],
                    "prediction": predicted_sign,
                    "confidence": confidence,
                    "reasoning": reasoning,
                    "probabilities": probs,
                }
            )

        return predictions

    def __predict_risky(self, probabilities: list[dict[str, Any]], 
                        details: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Estrategia arriesgada: Balancea probabilidades con análisis contextual.

        Esta estrategia va más allá de las probabilidades LAE, incorporando análisis contextual profundo
        para identificar situaciones donde el contexto sugiere un resultado diferente al más probable.
        Puede generar predicciones más arriesgadas pero potencialmente más rentables.
        
        El proceso incluye:
        1. Análisis del contexto de cada partido (clasificación, histórico, rachas)
        2. Ajuste de las probabilidades LAE según factores contextuales:
           - Fortaleza local/visitante basada en clasificación
           - Tendencia histórica en enfrentamientos directos
           - Rendimiento reciente de ambos equipos
        3. Selección del signo con mayor probabilidad ajustada
        4. Asignación de confianza con umbrales más estrictos (55%/40%)
        5. Generación de justificación detallada explicando ajustes contextuales
        
        Factores considerados:
        - Rachas recientes de ambos equipos
        - Histórico de enfrentamientos (últimos 10 años)
        - Diferencia de clasificación
        - Rendimiento local/visitante

        Parameters
        ----------
        probabilities : list[dict[str, Any]]
            Lista de probabilidades de cada partido.
        details : list[dict[str, Any]]
            Lista de detalles de cada partido.

        Returns
        -------
        list[dict[str, Any]]
            Lista de predicciones para los 15 partidos.
        """
        predictions = []

        for i, (prob, detail) in enumerate(iterable=zip(probabilities, details), start=1):
            probs = {"1": prob.get("1_Prob", 0), "X": prob.get("X_Prob", 0), "2": prob.get("2_Prob", 0)}

            # Análisis contextual
            context_analysis = self.__analyze_context(detail=detail)

            # Ajustar probabilidades según contexto
            adjusted_probs = self.__adjust_probabilities(probs=probs, context=context_analysis)

            # Seleccionar signo con mayor probabilidad ajustada
            predicted_sign = max(adjusted_probs, key=lambda k: adjusted_probs[k])
            final_prob = adjusted_probs[predicted_sign]

            # Determinar confianza
            if final_prob >= 55:
                confidence = "ALTA"
            elif 40 <= final_prob < 55:
                confidence = "MEDIA"
            else:
                confidence = "BAJA"

            # Generar justificación detallada
            reasoning = self.__generate_reasoning(
                predicted_sign=predicted_sign,
                original_probs=probs,
                adjusted_probs=adjusted_probs,
                context=context_analysis,
            )

            predictions.append(
                {
                    "match_id": i,
                    "match": prob["partido"],
                    "prediction": predicted_sign,
                    "confidence": confidence,
                    "reasoning": reasoning,
                    "probabilities": probs,
                    "adjusted_probabilities": adjusted_probs,
                    "context_factors": context_analysis,
                }
            )

        return predictions

    def __predict_custom(self, probabilities: list[dict[str, Any]], details: list[dict[str, Any]],
                         custom_distribution: dict[str, int] | None = None) -> list[dict[str, Any]]:
        """
        Estrategia personalizada: Optimiza para alcanzar la distribución especificada.

        Esta estrategia permite al usuario definir exactamente cuántos 1s, Xs y 2s desea en su quiniela,
        y el sistema optimiza la asignación de signos para maximizar la calidad de las predicciones
        dentro de esas restricciones. Útil cuando se tiene una intuición sobre la distribución de resultados
        o se quiere controlar el nivel de riesgo.
        
        El algoritmo de optimización:
        1. Calcula un score ajustado para cada posible asignación (partido-signo):
           - Score base: probabilidad LAE del signo
           - Multiplicado por factor contextual (fortaleza local/visitante/empate)
        2. Crea 45 asignaciones posibles (15 partidos × 3 signos)
        3. Ordena todas las asignaciones por score descendente
        4. Asigna signos usando algoritmo greedy:
           - Selecciona la mejor asignación disponible
           - Respeta las cuotas de cada signo (ej: 7 unos, 4 equis, 4 doses)
           - Asegura que cada partido recibe exactamente un signo
        5. Retorna predicciones ordenadas por ID de partido
        
        Distribución por defecto si no se especifica: {"1": 7, "X": 4, "2": 4}

        Parameters
        ----------
        probabilities : list[dict[str, Any]]
            Lista de probabilidades de cada partido.
        details : list[dict[str, Any]]
            Lista de detalles de cada partido.
        custom_distribution : dict[str, int] | None
            Distribución deseada: {"1": N, "X": M, "2": K}.
            Si es None, usa distribución por defecto: {"1": 7, "X": 4, "2": 4}.

        Returns
        -------
        list[dict[str, Any]]
            Lista de predicciones para los 15 partidos.
        """
        if custom_distribution is None:
            # Distribución por defecto: 7 locales, 4 empates, 4 visitantes
            custom_distribution = {"1": 7, "X": 4, "2": 4}

        target_1 = custom_distribution["1"]
        target_X = custom_distribution["X"]
        target_2 = custom_distribution["2"]

        # Calcular scores para cada partido y cada signo
        match_scores = []
        for i, (prob, detail) in enumerate(iterable=zip(probabilities, details), start=1):
            context = self.__analyze_context(detail=detail)
            scores = {
                "match_id": i,
                "match": prob["partido"],
                "1": prob.get("1_Prob", 0) * (1 + context.get("local_strength", 0) / 100),
                "X": prob.get("X_Prob", 0) * (1 + context.get("draw_tendency", 0) / 100),
                "2": prob.get("2_Prob", 0) * (1 + context.get("visitor_strength", 0) / 100),
                "probabilities": {
                    "1": prob.get("1_Prob", 0),
                    "X": prob.get("X_Prob", 0),
                    "2": prob.get("2_Prob", 0),
                },
                "context": context,
            }
            match_scores.append(scores)

        # Asignar signos optimizando para la distribución deseada
        predictions = self.__optimize_distribution(
            match_scores=match_scores,
            target_1=target_1,
            target_X=target_X,
            target_2=target_2)

        return predictions

    def __analyze_context(self, detail: dict[str, Any]) -> dict[str, Any]:
        """
        Analiza el contexto de un partido para ajustar probabilidades.
        
        Este método evalúa múltiples factores contextuales que pueden influir en el resultado
        de un partido más allá de las probabilidades LAE. Genera scores de ajuste que luego
        se utilizan para modificar las probabilidades base.
        
        Análisis realizado:
        1. **Clasificación**: Compara posiciones de los equipos
           - +2 puntos de fortaleza local por cada posición de ventaja
           - Ej: Local 3º vs Visitante 8º → +10 puntos fortaleza local
        
        2. **Histórico de enfrentamientos**: Analiza últimos 10 años
           - Calcula % de victorias locales, empates y visitantes
           - Ajusta ±30 puntos según desviación del 33.3% esperado
           - Ej: 50% victorias locales → +15 puntos fortaleza local
        
        Los scores de ajuste se devuelven en rango -100 a +100 y se utilizan como
        multiplicadores porcentuales en las probabilidades.

        Parameters
        ----------
        detail : dict[str, Any]
            Diccionario con detalles del partido.

        Returns
        -------
        dict[str, Any]
            Análisis contextual con factores como:
            - local_strength: Fortaleza del equipo local (-100 a +100)
            - visitor_strength: Fortaleza del equipo visitante (-100 a +100)
            - draw_tendency: Tendencia al empate (-100 a +100)
            - recent_form_local: Forma reciente del local
            - recent_form_visitor: Forma reciente del visitante
        """
        context = {
            "local_strength": 0,
            "visitor_strength": 0,
            "draw_tendency": 0,
            "recent_form_local": "neutral",
            "recent_form_visitor": "neutral",
        }

        # Analizar clasificación (si disponible)
        try:
            pos_local_raw = detail.get("clasificacionLocal", "10")
            pos_visitor_raw = detail.get("clasificacionVisitante", "10")
            
            # Convertir a string si es int
            if isinstance(pos_local_raw, int):
                pos_local = pos_local_raw
            else:
                pos_local = int(str(pos_local_raw).split("º")[0])
            
            if isinstance(pos_visitor_raw, int):
                pos_visitor = pos_visitor_raw
            else:
                pos_visitor = int(str(pos_visitor_raw).split("º")[0])
            
            diff_positions = pos_visitor - pos_local
            context["local_strength"] += diff_positions * 2  # +2 puntos por cada posición de ventaja
        except (ValueError, IndexError, AttributeError):
            pass

        # Analizar histórico
        veces1 = detail.get("veces1", 0)
        vecesX = detail.get("vecesX", 0)
        veces2 = detail.get("veces2", 0)
        total_historic = veces1 + vecesX + veces2
        if total_historic > 0:
            context["local_strength"] += (veces1 / total_historic - 0.33) * 30
            context["visitor_strength"] += (veces2 / total_historic - 0.33) * 30
            context["draw_tendency"] += (vecesX / total_historic - 0.33) * 30

        return context

    def __adjust_probabilities(self, probs: dict[str, float], context: dict[str, Any]) -> dict[str, float]:
        """
        Ajusta probabilidades LAE según análisis contextual.
        
        Aplica los factores contextuales (fortaleza local/visitante/empate) a las probabilidades LAE
        base para generar probabilidades ajustadas que reflejen mejor el contexto del partido.
        
        Proceso de ajuste:
        1. Multiplica cada probabilidad por (1 + factor_contextual/100)
           - Ej: Prob LAE 1 = 50%, fortaleza_local = +20 → 50% × 1.20 = 60%
        2. Normaliza las tres probabilidades para que sumen exactamente 100%
           - Mantiene la coherencia probabilística
        3. Retorna probabilidades ajustadas listas para usar en predicción
        
        Los ajustes reflejan ventajas contextuales sin eliminar completamente la información
        de las probabilidades LAE base.

        Parameters
        ----------
        probs : dict[str, float]
            Probabilidades originales ("1", "X", "2").
        context : dict[str, Any]
            Análisis contextual del partido.

        Returns
        -------
        dict[str, float]
            Probabilidades ajustadas, normalizadas para sumar 100%.
        """
        adjusted = {
            "1": probs["1"] * (1 + context["local_strength"] / 100),
            "X": probs["X"] * (1 + context["draw_tendency"] / 100),
            "2": probs["2"] * (1 + context["visitor_strength"] / 100),
        }

        # Normalizar para que sumen 100%
        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: (v / total) * 100 for k, v in adjusted.items()}

        return adjusted

    def __generate_reasoning(self, predicted_sign: str, original_probs: dict[str, float], 
                             adjusted_probs: dict[str, float], context: dict[str, Any]) -> str:
        """
        Genera justificación textual de una predicción.
        
        Crea una explicación en lenguaje natural que detalla por qué se seleccionó un signo particular,
        incluyendo la probabilidad base, ajustes contextuales aplicados y factores relevantes considerados.
        
        Estructura de la justificación:
        1. Probabilidad LAE base del signo predicho
        2. Ajuste contextual si es significativo (>5% de cambio)
           - Menciona la probabilidad ajustada final
        3. Factores relevantes que influyeron:
           - Ventaja/desventaja del local por clasificación o histórico
           - Solo menciona factores con impacto > 10 puntos
        
        La justificación es concisa pero informativa, permitiendo al usuario entender
        el razonamiento detrás de cada predicción.

        Parameters
        ----------
        predicted_sign : str
            Signo predicho ("1", "X", "2").
        original_probs : dict[str, float]
            Probabilidades LAE originales.
        adjusted_probs : dict[str, float]
            Probabilidades ajustadas por contexto.
        context : dict[str, Any]
            Factores contextuales considerados.

        Returns
        -------
        str
            Justificación en texto legible.
        """
        reasoning_parts = []

        # Probabilidad base
        orig_prob = original_probs[predicted_sign]
        adj_prob = adjusted_probs[predicted_sign]
        reasoning_parts.append(f"Probabilidad LAE {predicted_sign}: {orig_prob:.1f}%")

        # Mencionar ajuste si es significativo
        adjustment = adj_prob - orig_prob
        if abs(adjustment) > 5:
            reasoning_parts.append(f"ajustada a {adj_prob:.1f}% por análisis contextual")

        # Mencionar factores relevantes
        if abs(context["local_strength"]) > 10:
            if context["local_strength"] > 0:
                reasoning_parts.append("ventaja del local por clasificación/histórico")
            else:
                reasoning_parts.append("desventaja del local por clasificación/histórico")

        return ". ".join(reasoning_parts) + "."

    def __optimize_distribution(self, match_scores: list[dict[str, Any]], target_1: int, target_X: int, 
                                target_2: int) -> list[dict[str, Any]]:
        """
        Optimiza la asignación de signos para alcanzar la distribución objetivo.

        Utiliza un algoritmo greedy que maximiza la calidad global de las predicciones
        mientras respeta estrictamente las cuotas de cada signo especificadas por el usuario.
        
        Algoritmo greedy de optimización:
        1. Crea 45 asignaciones candidatas (15 partidos × 3 signos posibles)
        2. Cada asignación tiene un score = probabilidad_ajustada_por_contexto
        3. Ordena todas las asignaciones por score descendente
        4. Itera sobre asignaciones de mayor a menor score:
           - Si el partido aún no tiene signo asignado
           - Y queda cuota disponible para ese signo
           - Asigna ese signo a ese partido
        5. Continúa hasta asignar los 15 partidos
        6. Ordena resultado final por match_id
        
        Este enfoque greedy no garantiza la solución óptima global, pero genera
        resultados de alta calidad en tiempo lineal O(n log n).

        Parameters
        ----------
        match_scores : list[dict[str, Any]]
            Scores de cada partido para cada signo.
        target_1 : int
            Cantidad objetivo de 1s.
        target_X : int
            Cantidad objetivo de Xs.
        target_2 : int
            Cantidad objetivo de 2s.

        Returns
        -------
        list[dict[str, Any]]
            Lista de predicciones optimizadas.
        """
        # Crear lista de asignaciones con sus scores
        assignments = []
        for match in match_scores:
            for sign in ["1", "X", "2"]:
                assignments.append(
                    {
                        "match_id": match["match_id"],
                        "match": match["match"],
                        "sign": sign,
                        "score": match[sign],
                        "probabilities": match["probabilities"],
                        "context": match["context"],
                    }
                )

        # Ordenar por score descendente
        assignments.sort(key=lambda x: x["score"], reverse=True)

        # Asignar signos respetando cuotas
        assigned_matches = set()
        predictions = []
        remaining = {"1": target_1, "X": target_X, "2": target_2}

        for assignment in assignments:
            match_id = assignment["match_id"]
            sign = assignment["sign"]

            # Si el partido ya tiene asignación o se acabó la cuota, saltar
            if match_id in assigned_matches or remaining[sign] <= 0:
                continue

            # Asignar
            assigned_matches.add(match_id)
            remaining[sign] -= 1

            confidence = "ALTA" if assignment["score"] >= 50 else "MEDIA" if assignment["score"] >= 35 else "BAJA"

            predictions.append(
                {
                    "match_id": match_id,
                    "match": assignment["match"],
                    "prediction": sign,
                    "confidence": confidence,
                    "reasoning": f"Optimizado para distribución personalizada. Score: {assignment['score']:.1f}",
                    "probabilities": assignment["probabilities"],
                    "score": assignment["score"],
                }
            )

            # Si ya asignamos los 15 partidos, terminar
            if len(predictions) == 15:
                break

        # Ordenar por match_id
        predictions.sort(key=lambda x: x["match_id"])

        return predictions

    def __validate_custom_distribution(self, distribution: dict[str, int]) -> bool:
        """
        Valida que una distribución personalizada sea correcta.
        
        Verifica que la distribución proporcionada por el usuario cumple los requisitos:
        - Contiene las tres claves obligatorias: "1", "X", "2"
        - La suma de valores es exactamente 15 (número de partidos en una quiniela)
        
        Esta validación previene errores de usuario como distribuciones incompletas
        (ej: {"1": 8, "X": 7}) o sumas incorrectas (ej: {"1": 10, "X": 3, "2": 3} = 16).

        Parameters
        ----------
        distribution : dict[str, int]
            Distribución a validar con claves "1", "X", "2".

        Returns
        -------
        bool
            True si es válida (suma 15 y todas las claves presentes), False en caso contrario.
        """
        required_keys = {"1", "X", "2"}
        if not all(key in distribution for key in required_keys):
            return False

        total = distribution["1"] + distribution["X"] + distribution["2"]
        return total == 15

    def __calculate_summary(self, predictions: list[dict[str, Any]]) -> dict[str, int]:
        """
        Calcula el resumen de distribución de signos en las predicciones.
        
        Recorre todas las predicciones y cuenta cuántas veces aparece cada signo (1, X, 2).
        El resumen permite al usuario ver rápidamente la distribución final sin revisar
        partido por partido, facilitando la evaluación del balance de la quiniela.
        
        Útil para verificar que:
        - Estrategia personalizada cumplió la distribución solicitada
        - Estrategias conservadora/arriesgada generaron distribución razonable
        - No hay sesgo excesivo hacia un solo resultado

        Parameters
        ----------
        predictions : list[dict[str, Any]]
            Lista de predicciones.

        Returns
        -------
        dict[str, int]
            Diccionario con conteo: {"1": N, "X": M, "2": K}.
        """
        summary = {"1": 0, "X": 0, "2": 0}

        for pred in predictions:
            sign = pred["prediction"]
            if sign == "1":
                summary["1"] += 1
            elif sign == "X":
                summary["X"] += 1
            elif sign == "2":
                summary["2"] += 1

        return summary
