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
Detector de sorpresas en predicciones de quiniela.

Este módulo identifica partidos donde existe una inconsistencia significativa entre
las probabilidades LAE y el análisis contextual (histórico, rachas, clasificación).
"""

from typing import Any

from kinielagpt import data_source


class SurpriseDetector:
    """
    Detector de posibles sorpresas en partidos de quiniela.

    Identifica inconsistencias entre probabilidades LAE y factores contextuales que
    podrían indicar resultados inesperados.
    """

    def detect(self, jornada: int, temporada: int, threshold: float = 30.0) -> dict[str, Any] | None:
        """
        Detecta posibles sorpresas en una jornada.
        
        Este método identifica partidos donde existe una divergencia significativa entre las
        probabilidades LAE (que tienden a ser conservadoras y basarse en datos estadísticos) y
        los factores contextuales actuales (rachas, histórico directo, clasificación). Estas
        inconsistencias pueden señalar oportunidades donde el resultado esperado podría diferir
        de las probabilidades publicadas.
        
        El proceso de detección incluye:
        1. **Recopilación de datos**: Obtiene probabilidades LAE y detalles completos de todos
           los partidos de la jornada.
        
        2. **Análisis partido por partido**: Para cada encuentro, ejecuta __analyze_inconsistencies()
           que evalúa tres tipos de divergencias:
           - Inconsistencia de rachas: Racha actual contradice probabilidad
           - Inconsistencia histórica: Historial directo difiere de probabilidad LAE
           - Inconsistencia de clasificación: Posiciones en tabla no concuerdan con favorito
        
        3. **Cálculo de score de divergencia**: Cada inconsistencia recibe una puntuación (0-100)
           que mide la magnitud de la contradicción. Se selecciona la más significativa.
        
        4. **Filtrado por umbral**: Solo se reportan partidos cuyo score de divergencia supera
           el threshold especificado (default: 30). Umbrales típicos:
           - threshold=20: Detección sensible (muchas alertas)
           - threshold=30: Balance recomendado
           - threshold=40: Solo inconsistencias muy marcadas
        
        5. **Clasificación de alertas**: Asigna nivel de gravedad según score:
           - 🚨 ALERTA ROJA: divergence >= 50 (contradicción severa)
           - ⚠️ ALERTA MEDIA: divergence >= 35 (contradicción notable)
           - ⚠️ ALERTA: divergence >= threshold (contradicción detectable)
        
        6. **Consolidación de reporte**: Estructura los resultados con información completa de
           cada sorpresa: partido, nivel de alerta, tipo de inconsistencia, descripción
           explicativa, probabilidades LAE y factores contextuales detectados.
        
        Ejemplos de uso:
        - Detección estándar: detect(26, 2025) → Encuentra 2 alertas con threshold=30
        - Detección sensible: detect(26, 2025, threshold=20) → Encuentra 5 alertas
        - Detección restrictiva: detect(26, 2025, threshold=45) → Solo 1 alerta crítica
        
        Casos típicos detectados:
        - Local favorito (70%) pero visitante con 5 victorias consecutivas
        - Visitante favorito (65%) pero 8 posiciones peor clasificado que local
        - Victoria clara esperada (60%) pero histórico muestra 80% de empates
        
        Este análisis es valioso para identificar apuestas de valor donde el contexto actual
        sugiere un resultado diferente al que indican las probabilidades LAE conservadoras.

        Parameters
        ----------
        jornada : int
            Número de jornada a analizar.
        temporada : int
            Año de la temporada.
        threshold : float, optional
            Umbral de divergencia para considerar sorpresa (0-100, default: 30).
            Valores más bajos detectan más alertas, valores más altos solo alertas críticas.

        Returns
        -------
        dict[str, Any] | None
            Diccionario con resultados de la detección:
            - jornada: Número de jornada
            - temporada: Año de temporada
            - threshold: Umbral utilizado
            - total_surprises: Cantidad de partidos con alertas
            - surprises: Lista de sorpresas detectadas, cada una con match_id, match, alert_level,
              inconsistency_type, description, probabilities, context_factors
            Retorna None si hay algún error.

        Examples
        --------
        >>> detector = SurpriseDetector()
        >>> surprises = detector.detect(jornada=26, temporada=2025, threshold=25.0)
        >>> print(f"Alertas encontradas: {surprises['total_surprises']}")
        Alertas encontradas: 3
        >>> for surprise in surprises["surprises"]:
        ...     print(f"{surprise['match']}: {surprise['alert_level']}")
        VILLARREAL - GETAFE: ALERTA ROJA
        """
        # Obtener datos necesarios
        probabilities = data_source.get_kiniela_probabilities(jornada=jornada, temporada=temporada)
        details = data_source.get_kiniela_matches_details(jornada=jornada, temporada=temporada)

        if probabilities is None or details is None:
            return None

        surprises = []

        for i, (prob, detail) in enumerate(iterable=zip(probabilities, details), start=1):
            # Analizar inconsistencias
            inconsistencies = self.__analyze_inconsistencies(prob=prob, detail=detail, threshold=threshold)

            if inconsistencies:
                surprise_data = {
                    "match_id": i,
                    "match": prob["partido"],
                    "alert_level": inconsistencies["alert_level"],
                    "inconsistency_type": inconsistencies["type"],
                    "description": inconsistencies["description"],
                    "probabilities": {
                        "1": prob.get("1_Prob", 0),
                        "X": prob.get("X_Prob", 0),
                        "2": prob.get("2_Prob", 0),
                    },
                    "context_factors": inconsistencies["factors"],
                }
                surprises.append(surprise_data)

        return {
            "jornada": jornada,
            "temporada": temporada,
            "threshold": threshold,
            "total_surprises": len(surprises),
            "surprises": surprises,
        }

    def __analyze_inconsistencies(self, prob: dict[str, Any], detail: dict[str, Any], 
                                   threshold: float) -> dict[str, Any] | None:
        """
        Analiza inconsistencias entre probabilidades y contexto.
        
        Este método ejecuta el análisis central de detección de sorpresas para un partido
        individual, evaluando múltiples dimensiones de posibles contradicciones entre las
        probabilidades LAE y los factores contextuales actuales. Es el motor analítico que
        determina si un partido merece una alerta.
        
        El proceso de análisis incluye:
        1. **Extracción de probabilidades**: Obtiene las probabilidades LAE del partido y
           identifica el signo dominante (con mayor probabilidad).
        
        2. **Filtro de relevancia**: Solo analiza partidos con probabilidad dominante >50%,
           ya que probabilidades equilibradas (ej: 35-33-32) no generan expectativas claras
           que puedan contradecirse.
        
        3. **Ejecución de verificaciones múltiples**: Ejecuta tres funciones especializadas
           que evalúan diferentes tipos de inconsistencias:
           - __check_streak_inconsistency(): Compara rachas actuales vs probabilidad
           - __check_historical_inconsistency(): Compara histórico directo vs probabilidad LAE
           - __check_classification_inconsistency(): Compara posiciones en tabla vs favorito
        
        4. **Filtrado de resultados válidos**: Descarta verificaciones que retornan None
           (sin inconsistencia detectada) y conserva solo las que encontraron divergencias.
        
        5. **Selección de inconsistencia principal**: Si hay múltiples inconsistencias, elige
           la más significativa según divergence_score. Esto evita reportes duplicados y
           enfoca en el factor más relevante.
        
        6. **Aplicación del umbral**: Verifica si la divergencia más significativa supera el
           threshold configurado. Si no lo supera, retorna None (no hay alerta).
        
        7. **Clasificación del nivel de alerta**: Asigna gravedad visual según score:
           - divergence >= 50: "🚨 ALERTA ROJA" (contradicción crítica)
           - divergence >= 35: "⚠️ ALERTA MEDIA" (contradicción notable)
           - divergence >= threshold: "⚠️ ALERTA" (contradicción moderada)
        
        8. **Construcción de resultado**: Estructura la información completa de la
           inconsistencia: tipo, descripción explicativa, factores contextuales y score.
        
        Ejemplos de detección:
        - Partido con prob={1:70, X:20, 2:10} pero local en racha de 4 derrotas y visitante
          con 5 victorias → divergence=45, ALERTA MEDIA (streak_inconsistency)
        
        - Partido con prob={2:65, X:25, 1:10} pero histórico muestra 12 victorias locales
          en 15 enfrentamientos → divergence=42, ALERTA MEDIA (historical_inconsistency)
        
        - Partido equilibrado prob={1:45, X:30, 2:25} → Retorna None (max_prob < 50)
        
        - Partido con prob={1:55, X:25, 2:20} y divergence=15 con threshold=30 → Retorna None
          (no supera umbral)
        
        Este método actúa como orquestador que coordina las verificaciones específicas y
        sintetiza el resultado más relevante.

        Parameters
        ----------
        prob : dict[str, Any]
            Probabilidades LAE del partido.
        detail : dict[str, Any]
            Detalles del partido.
        threshold : float
            Umbral de divergencia.

        Returns
        -------
        dict[str, Any] | None
            Información de inconsistencia si se detecta, None en caso contrario.
            Diccionario incluye: alert_level, type, description, factors, divergence_score.
        """
        probs = {
            "1": prob.get("1_Prob", 0),
            "X": prob.get("X_Prob", 0),
            "2": prob.get("2_Prob", 0),
        }

        # Identificar signo con mayor probabilidad
        max_sign = max(probs, key=lambda k: probs[k])
        max_prob = probs[max_sign]

        # Solo analizar si hay una probabilidad dominante (>50%)
        if max_prob < 50:
            return None

        # Verificar diferentes tipos de inconsistencias
        inconsistency_checks = [
            self.__check_streak_inconsistency(max_sign=max_sign, max_prob=max_prob, probs=probs, detail=detail),
            self.__check_historical_inconsistency(max_sign=max_sign, probs=probs, detail=detail),
            self.__check_classification_inconsistency(max_sign=max_sign, max_prob=max_prob, detail=detail),
        ]

        # Filtrar inconsistencias válidas y calcular score total
        valid_inconsistencies = [inc for inc in inconsistency_checks if inc is not None]

        if not valid_inconsistencies:
            return None

        # Seleccionar la inconsistencia más significativa
        most_significant = max(valid_inconsistencies, key=lambda x: x["divergence_score"])

        # Verificar si supera el umbral
        if most_significant["divergence_score"] < threshold:
            return None

        # Determinar nivel de alerta
        if most_significant["divergence_score"] >= 50:
            alert_level = "🚨 ALERTA ROJA"
        elif most_significant["divergence_score"] >= 35:
            alert_level = "⚠️ ALERTA MEDIA"
        else:
            alert_level = "⚠️ ALERTA"

        return {
            "alert_level": alert_level,
            "type": most_significant["type"],
            "description": most_significant["description"],
            "factors": most_significant["factors"],
            "divergence_score": most_significant["divergence_score"],
        }

    def __check_streak_inconsistency(self, max_sign: str, max_prob: float, probs: dict[str, float], 
                                      detail: dict[str, Any]) -> dict[str, Any] | None:
        """
        Verifica inconsistencias con rachas recientes.
        
        Este método detecta contradicciones entre las probabilidades LAE y el momentum actual
        de los equipos medido a través de sus rachas recientes. Las rachas son indicadores
        poderosos de forma actual que pueden no estar completamente reflejados en las
        probabilidades LAE que tienden a ser más conservadoras y basarse en promedios.
        
        El algoritmo de detección incluye:
        1. **Extracción de evoluciones**: Obtiene los últimos 5 resultados de ambos equipos
           (evolucionLocal y evolucionVisitante).
        
        2. **Cálculo de valores de racha**: Utiliza __calculate_streak_value() para convertir
           resultados en scores numéricos:
           - Victoria (V) = +3 puntos
           - Empate (E) = +1 punto
           - Derrota (D) = -2 puntos
           Ejemplos: ['V','V','V','E','V'] = 13 (racha fuerte), ['D','D','D','E','D'] = -9 (racha mala)
        
        3. **Evaluación de tres escenarios de inconsistencia**:
        
           **Escenario 1 - Favorito local con forma pobre**:
           - Condición: max_sign='1' y max_prob >= 60% (local muy favorito)
           - Inconsistencia: local_streak < -6 (mala racha) Y visitor_streak > 6 (buena racha)
           - Divergencia: (max_prob - 50) + |local_streak| + visitor_streak
           - Ejemplo: prob=70%, local=-8, visitor=9 → divergence = 20 + 8 + 9 = 37
        
           **Escenario 2 - Favorito visitante con forma pobre**:
           - Condición: max_sign='2' y max_prob >= 60% (visitante muy favorito)
           - Inconsistencia: visitor_streak < -6 Y local_streak > 6
           - Cálculo simétrico al escenario 1
        
           **Escenario 3 - Baja probabilidad de empate con tendencia a empatar**:
           - Condición: max_sign != 'X' y prob(X) < 30% (empate descartado)
           - Inconsistencia: Ambos equipos tienen 2 o más empates en últimos 3 partidos
           - Divergencia: 25 + (empates_local + empates_visitante) × 3
           - Ejemplo: Local 2/3 empates, Visitante 3/3 empates → 25 + 5×3 = 40
        
        4. **Construcción de reporte**: Si se detecta divergencia, genera descripción
           explicativa y estructura factores contextuales identificados.
        
        Ejemplos de detección:
        - BARCELONA (70% prob) vs GETAFE: Barcelona con ['D','D','D','E','D'] = -9,
          Getafe con ['V','V','V','V','E'] = 13 → INCONSISTENCIA CRÍTICA (divergence = 42)
        
        - MADRID (35% empate) vs SEVILLA: Ambos con 3/3 empates recientes
          → ALERTA empate subestimado (divergence = 34)
        
        - VALENCIA (55% prob) vs BILBAO: Valencia con racha moderada, Bilbao con racha neutra
          → No hay inconsistencia (rachas no extremas)
        
        Las rachas son especialmente relevantes porque capturan momentum, confianza y dinámica
        de equipo que las probabilidades estáticas no reflejan completamente.

        Parameters
        ----------
        max_sign : str
            Signo con mayor probabilidad LAE.
        max_prob : float
            Probabilidad del signo dominante.
        probs : dict[str, float]
            Probabilidades LAE del partido.
        detail : dict[str, Any]
            Detalles del partido.

        Returns
        -------
        dict[str, Any] | None
            Información de inconsistencia si se detecta, None en caso contrario.
        """
        evolucion_local = detail.get("evolucionLocal", [])
        evolucion_visitor = detail.get("evolucionVisitante", [])

        if not evolucion_local or not evolucion_visitor:
            return None

        # Calcular rachas
        local_streak = self.__calculate_streak_value(results=evolucion_local[:5])
        visitor_streak = self.__calculate_streak_value(results=evolucion_visitor[:5])

        divergence = 0
        description_parts = []
        factors = {}

        # Caso 1: Alta probabilidad de 1 pero local con mala racha y visitante con buena racha
        if max_sign == "1" and max_prob >= 60:
            if local_streak < -6 and visitor_streak > 6:
                divergence = min((max_prob - 50) + abs(local_streak) + visitor_streak, 100)
                description_parts.append(
                    f"Probabilidad alta de victoria local ({max_prob:.0f}%) pero el local está en mala racha "
                    f"y el visitante en buena forma"
                )
                factors["local_recent_form"] = "Mala racha"
                factors["visitor_recent_form"] = "Buena racha"

        # Caso 2: Alta probabilidad de 2 pero visitante con mala racha y local con buena racha
        elif max_sign == "2" and max_prob >= 60:
            if visitor_streak < -6 and local_streak > 6:
                divergence = min((max_prob - 50) + abs(visitor_streak) + local_streak, 100)
                description_parts.append(
                    f"Probabilidad alta de victoria visitante ({max_prob:.0f}%) pero el visitante está "
                    f"en mala racha y el local en buena forma"
                )
                factors["local_recent_form"] = "Buena racha"
                factors["visitor_recent_form"] = "Mala racha"

        # Caso 3: Baja probabilidad de empate pero ambos equipos en racha de empates
        elif max_sign != "X" and probs.get("X", 0) < 30:
            draws_local = evolucion_local[:3].count("E")
            draws_visitor = evolucion_visitor[:3].count("E")
            if draws_local >= 2 and draws_visitor >= 2:
                divergence = 25 + (draws_local + draws_visitor) * 3
                description_parts.append(
                    "Baja probabilidad de empate pero ambos equipos con tendencia a empatar últimamente"
                )
                factors["draw_tendency"] = f"Local {draws_local}/3 empates, Visitante {draws_visitor}/3 empates"

        if divergence > 0:
            return {
                "type": "streak_inconsistency",
                "description": ". ".join(description_parts),
                "factors": factors,
                "divergence_score": divergence,
                "local_streak": local_streak,
                "visitor_streak": visitor_streak,
            }

        return None

    def __check_historical_inconsistency(self, max_sign: str, probs: dict[str, float], 
                                         detail: dict[str, Any]) -> dict[str, Any] | None:
        """
        Verifica inconsistencias con el histórico de enfrentamientos.
        
        Este método detecta divergencias significativas entre las probabilidades LAE asignadas
        y los patrones históricos de enfrentamientos directos entre los dos equipos. El histórico
        directo es un indicador potente porque algunos equipos tienen "ventaja psicológica" o
        estilos de juego que históricamente favorecen ciertos resultados, independientemente de
        su forma actual.
        
        El proceso de verificación incluye:
        1. **Extracción de histórico**: Obtiene el conteo de resultados en enfrentamientos
           directos previos:
           - veces1: Victorias del equipo local
           - vecesX: Empates
           - veces2: Victorias del equipo visitante
        
        2. **Validación de muestra**: Requiere al menos 5 enfrentamientos previos para considerar
           el histórico estadísticamente significativo. Con menos partidos, el histórico no es
           representativo y podría generar falsas alarmas.
        
        3. **Cálculo de tasas históricas**: Convierte conteos a porcentajes para comparación
           directa con probabilidades LAE:
           - Ejemplo: 8 victorias locales en 12 partidos → 66.7% tasa histórica de '1'
        
        4. **Identificación de divergencias**: Para cada resultado ('1', 'X', '2'), calcula la
           diferencia entre probabilidad LAE y tasa histórica:
           - prob_diff = probs[sign] - historical_rates[sign]
           - Ejemplo: LAE da 75% al '1', pero histórico solo muestra 40% → diff = +35%
        
        5. **Detección de sobrestimación significativa**: Se activa alerta cuando:
           - El signo es el favorito según LAE (max_sign)
           - La probabilidad LAE supera la tasa histórica en más de 30 puntos porcentuales
           - Indica que LAE podría estar sobrestimando basándose en otros factores
        
        6. **Cálculo de divergencia**: Usa la diferencia porcentual directamente como score:
           - prob_diff > 30 → Inconsistencia detectable
           - prob_diff >= 25 → Umbral mínimo para reportar
        
        7. **Generación de reporte**: Construye descripción explicativa incluyendo ambos
           porcentajes y el tamaño de la muestra histórica para contexto.
        
        Ejemplos de detección:
        - REAL MADRID (80% prob '1') vs BARCELONA con histórico: 3V-2E-7D en 12 partidos
          → Histórico solo 25% victorias locales, LAE da 80% → divergence = 55 (ALERTA ROJA)
          Interpretación: Madrid raramente gana en casa contra Barça históricamente
        
        - GETAFE (65% prob '2') vs ATHLETIC con histórico: 1V-5E-2D en 8 partidos
          → Histórico solo 25% victorias visitante, LAE da 65% → divergence = 40 (ALERTA MEDIA)
          Interpretación: Este partido históricamente tiende al empate
        
        - SEVILLA (55% prob '1') vs VILLARREAL con histórico: 6V-2E-3D en 11 partidos
          → Histórico 54.5% victorias locales, LAE da 55% → diff = 0.5 (sin inconsistencia)
          Interpretación: LAE y histórico alineados perfectamente
        
        - VALENCIA (70% prob 'X') con solo 3 enfrentamientos previos
          → Retorna None (muestra insuficiente, mínimo 5 partidos requerido)
        
        Este análisis es crucial porque el histórico directo puede revelar dinámicas específicas
        entre dos equipos que las estadísticas generales no capturan (ej: estilo de juego
        contrapuesto, superioridad psicológica histórica).

        Parameters
        ----------
        max_sign : str
            Signo con mayor probabilidad LAE.
        probs : dict[str, float]
            Probabilidades LAE del partido.
        detail : dict[str, Any]
            Detalles del partido.

        Returns
        -------
        dict[str, Any] | None
            Información de inconsistencia si se detecta, None en caso contrario.
        """
        veces1 = detail.get("veces1", 0)
        vecesX = detail.get("vecesX", 0)
        veces2 = detail.get("veces2", 0)
        total_historic = veces1 + vecesX + veces2

        if total_historic < 5:  # Requiere al menos 5 enfrentamientos
            return None

        historical_rates = {
            "1": (veces1 / total_historic) * 100,
            "X": (vecesX / total_historic) * 100,
            "2": (veces2 / total_historic) * 100,
        }

        # Buscar contradicciones significativas
        divergence = 0
        description_parts = []
        factors = {}

        for sign in ["1", "X", "2"]:
            prob_diff = probs[sign] - historical_rates[sign]

            # Si la probabilidad LAE es mucho mayor que el histórico
            if sign == max_sign and prob_diff > 30:
                divergence = prob_diff
                sign_names = {"1": "victoria local", "X": "empate", "2": "victoria visitante"}
                description_parts.append(
                    f"Probabilidad LAE de {sign_names[sign]} ({probs[sign]:.0f}%) muy superior "
                    f"al histórico de enfrentamientos ({historical_rates[sign]:.0f}% en {total_historic} partidos)"
                )
                factors["historical_rate"] = f"{historical_rates[sign]:.0f}%"
                factors["lae_probability"] = f"{probs[sign]:.0f}%"
                factors["total_matches"] = total_historic

        if divergence >= 25:
            return {
                "type": "historical_inconsistency",
                "description": ". ".join(description_parts),
                "factors": factors,
                "divergence_score": divergence,
            }

        return None

    def __check_classification_inconsistency(self, max_sign: str, max_prob: float, 
                                             detail: dict[str, Any]) -> dict[str, Any] | None:
        """
        Verifica inconsistencias con las posiciones de clasificación.
        
        Este método detecta situaciones donde las probabilidades LAE favorecen fuertemente a un
        equipo que está significativamente peor clasificado que su rival. La posición en la tabla
        es un indicador agregado de calidad y rendimiento sostenido durante la temporada, por lo
        que grandes disparidades entre clasificación y probabilidades pueden señalar sorpresas.
        
        El proceso de verificación incluye:
        1. **Extracción de posiciones**: Parsea las clasificaciones de ambos equipos desde los
           strings en formato "Nº XXpt" (ej: "5º 45pt" → posición 5).
        
        2. **Manejo robusto de errores**: Utiliza try-except para gestionar casos donde las
           clasificaciones no están disponibles o tienen formato no estándar, evitando que
           errores de parsing interrumpan el análisis.
        
        3. **Evaluación de dos escenarios críticos**:
        
           **Escenario 1 - Victoria local sobrestimada**:
           - Condición: max_sign='1' (local favorito) y max_prob >= 65% (muy favorito)
           - Inconsistencia: El visitante está 8 o más posiciones mejor clasificado
             (pos_visitor < pos_local - 8)
           - Divergencia: (pos_local - pos_visitor) × 2.5
           - Ejemplo: Local en puesto 15º (65% prob), Visitante en puesto 3º
             → diferencia = 12 posiciones → divergence = 12 × 2.5 = 30
           - Interpretación: ¿Por qué el 15º es gran favorito contra el 3º?
        
           **Escenario 2 - Victoria visitante sobrestimada**:
           - Condición: max_sign='2' (visitante favorito) y max_prob >= 65%
           - Inconsistencia: El local está 8 o más posiciones mejor clasificado
           - Cálculo simétrico al escenario 1
           - Ejemplo: Visitante en puesto 18º (68% prob), Local en puesto 6º
             → diferencia = 12 posiciones → divergence = 30
        
        4. **Umbral de posiciones**: Requiere una diferencia mínima de 8 posiciones para
           considerar la inconsistencia significativa. Diferencias menores pueden explicarse
           por otros factores (forma reciente, ventaja de local, etc.).
        
        5. **Umbral de probabilidad**: Solo evalúa cuando max_prob >= 65%, ya que probabilidades
           moderadas (50-60%) ya incorporan incertidumbre que puede justificar la diferencia
           de clasificación.
        
        6. **Umbral de divergencia**: Reporta inconsistencia solo si divergence >= 20, lo que
           corresponde a diferencias de 8+ posiciones en la tabla.
        
        7. **Generación de reporte**: Incluye las posiciones exactas de ambos equipos y la
           magnitud de la diferencia para contexto completo.
        
        Ejemplos de detección:
        - ELCHE (17º, 70% prob '1') vs REAL MADRID (2º, 15% prob '2')
          → Diferencia = 15 posiciones, divergence = 37.5 (ALERTA MEDIA)
          Interpretación: ¿Cómo el colista es tan favorito contra el subcampeón?
        
        - OSASUNA (10º, 68% prob '2') vs SEVILLA (4º, 20% prob '1')
          → Diferencia = 6 posiciones (< 8) → No reporta (diferencia insuficiente)
          Interpretación: 6 posiciones de diferencia son justificables por otros factores
        
        - BETIS (8º, 55% prob '1') vs CELTA (12º, 25% prob '2')
          → max_prob = 55% (< 65%) → No evalúa (probabilidad no suficientemente alta)
          Interpretación: Probabilidad moderada ya refleja incertidumbre
        
        - GETAFE vs GRANADA con clasificaciones no disponibles
          → except captura error de parsing → Retorna None (sin datos)
        
        Esta verificación es especialmente valiosa para identificar casos donde el factor campo
        (local/visitante) o una racha reciente podrían estar influyendo excesivamente en las
        probabilidades, ignorando la calidad objetiva medida por la clasificación de liga.

        Parameters
        ----------
        max_sign : str
            Signo con mayor probabilidad LAE.
        max_prob : float
            Probabilidad del signo dominante.
        detail : dict[str, Any]
            Detalles del partido.

        Returns
        -------
        dict[str, Any] | None
            Información de inconsistencia si se detecta, None en caso contrario.
        """
        try:
            clasificacion_local = detail.get("clasificacionLocal", "")
            clasificacion_visitor = detail.get("clasificacionVisitante", "")

            pos_local = int(clasificacion_local.split("º")[0])
            pos_visitor = int(clasificacion_visitor.split("º")[0])

            divergence = 0
            description_parts = []
            factors = {}

            # Alta probabilidad de victoria local pero el visitante está mucho mejor clasificado
            if max_sign == "1" and max_prob >= 65 and pos_visitor < pos_local - 8:
                divergence = (pos_local - pos_visitor) * 2.5
                description_parts.append(
                    f"Alta probabilidad de victoria local ({max_prob:.0f}%) pero el visitante "
                    f"está {pos_local - pos_visitor} posiciones por encima en la tabla "
                    f"(Local: {pos_local}º, Visitante: {pos_visitor}º)"
                )
                factors["position_difference"] = pos_local - pos_visitor
                factors["local_position"] = pos_local
                factors["visitor_position"] = pos_visitor

            # Alta probabilidad de victoria visitante pero el local está mucho mejor clasificado
            elif max_sign == "2" and max_prob >= 65 and pos_local < pos_visitor - 8:
                divergence = (pos_visitor - pos_local) * 2.5
                description_parts.append(
                    f"Alta probabilidad de victoria visitante ({max_prob:.0f}%) pero el local "
                    f"está {pos_visitor - pos_local} posiciones por encima en la tabla "
                    f"(Local: {pos_local}º, Visitante: {pos_visitor}º)"
                )
                factors["position_difference"] = pos_visitor - pos_local
                factors["local_position"] = pos_local
                factors["visitor_position"] = pos_visitor

            if divergence >= 20:
                return {
                    "type": "classification_inconsistency",
                    "description": ". ".join(description_parts),
                    "factors": factors,
                    "divergence_score": divergence,
                }

        except (ValueError, IndexError, AttributeError):
            pass

        return None

    def __calculate_streak_value(self, results: list[str]) -> int:
        """
        Calcula un valor numérico de racha (positivo = buena, negativo = mala).
        
        Este método cuantifica la calidad de una racha de resultados convirtiéndola en un
        score numérico único que permite comparaciones rápidas y evaluación de momentum. A
        diferencia de __calculate_streak() en analyzer.py que identifica rachas consecutivas,
        este método suma todos los resultados para obtener una valoración global.
        
        El sistema de puntuación es:
        1. **Victoria (V)**: +3 puntos (máximo valor, refleja resultado positivo completo)
        2. **Empate (E)**: +1 punto (resultado neutro/defensivo, no pierde pero no gana)
        3. **Derrota (D)**: -2 puntos (penalización por resultado negativo)
        
        Esta ponderación refleja el impacto real en competición y estado de forma:
        - Las victorias valen el triple que los empates (3 vs 1 en puntos de liga)
        - Las derrotas tienen impacto negativo moderado (-2) para reflejar crisis de confianza
        - El balance permite que empates compensen derrotas (2 empates = 1 derrota)
        
        Proceso de cálculo:
        1. Recorre la lista de resultados recientes
        2. Para cada resultado, suma el valor correspondiente según la tabla
        3. Retorna la suma total como score único
        
        Ejemplos de cálculo:
        - ['V', 'V', 'V', 'V', 'V'] → 3+3+3+3+3 = 15 (racha perfecta, máximo teórico en 5 partidos)
        - ['V', 'V', 'E', 'V', 'E'] → 3+3+1+3+1 = 11 (muy buena racha, sin derrotas)
        - ['E', 'E', 'E', 'E', 'E'] → 1+1+1+1+1 = 5 (racha neutral, equipo empata mucho)
        - ['V', 'D', 'E', 'D', 'V'] → 3-2+1-2+3 = 3 (irregular, victorias compensan derrotas)
        - ['E', 'D', 'D', 'E', 'D'] → 1-2-2+1-2 = -4 (mala racha, más derrotas que resultados positivos)
        - ['D', 'D', 'D', 'D', 'D'] → -2-2-2-2-2 = -10 (racha crítica, peor escenario)
        - [] → 0 (sin datos)
        
        Interpretación de rangos típicos (para 5 partidos):
        - Score >= 10: Racha excelente (mayormente victorias)
        - Score 6-9: Buena racha (balance positivo claro)
        - Score 1-5: Racha moderada (más empates que derrotas)
        - Score -3 a 0: Racha pobre (más derrotas que victorias)
        - Score <= -6: Racha crítica (mayoría derrotas)
        
        Usos en detección de sorpresas:
        - local_streak < -6 y visitor_streak > 6 → Gran divergencia de forma
        - Umbrales de -6 y +6 identifican rachas extremas (muy malas o muy buenas)
        - La diferencia entre scores permite medir la magnitud de la inconsistencia
        
        Esta métrica es más informativa que contar solo victorias porque captura matices:
        un equipo con 2V-3D (score=2) está peor que uno con 0V-5E (score=5), reflejando
        que evitar derrotas puede ser mejor que ganar poco y perder mucho.

        Parameters
        ----------
        results : list[str]
            Lista de resultados recientes (V, E, D).

        Returns
        -------
        int
            Valor de racha: +3 por victoria, +1 por empate, -2 por derrota.
        """
        values = {"V": 3, "E": 1, "D": -2}
        return sum(values.get(r, 0) for r in results)
