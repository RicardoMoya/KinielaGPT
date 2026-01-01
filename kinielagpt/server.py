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
Módulo principal del servidor MCP para KinielaGPT.

Este módulo implementa el servidor MCP que expone herramientas para obtener información,
generar predicciones y analizar partidos de la quiniela española.
"""

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from kinielagpt import data_source
from kinielagpt.analyzer import Analyzer
from kinielagpt.detector import SurpriseDetector
from kinielagpt.predictor import KinielaPredictor

# Crear instancia del servidor MCP
app = Server(name="kiniela-gpt")

# Instanciar componentes del sistema
predictor = KinielaPredictor()
analyzer = Analyzer()
surprise_detector = SurpriseDetector()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Lista todas las herramientas disponibles en el servidor MCP.

    Returns
    -------
    list[Tool]
        Lista de herramientas MCP con sus descripciones y esquemas de parámetros.
    """
    return [
        Tool(
            name="get_last_quiniela",
            description=(
                "Obtiene la información de la última quiniela disponible, incluyendo jornada, "
                "temporada y lista de partidos."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_quiniela",
            description=(
                "Obtiene la información de una jornada específica de quiniela, incluyendo todos "
                "los partidos programados."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "jornada": {
                        "type": "integer",
                        "description": "Número de jornada",
                        "minimum": 1,
                    },
                    "temporada": {
                        "type": "integer",
                        "description": "Año de la temporada",
                        "minimum": 2026,
                    },
                },
                "required": ["jornada", "temporada"],
            },
        ),
        Tool(
            name="get_probabilities",
            description=(
                "Obtiene las probabilidades LAE para cada partido de una jornada específica. "
                "Incluye probabilidades de 1, X, 2 y pronósticos de goles."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "jornada": {
                        "type": "integer",
                        "description": "Número de jornada",
                        "minimum": 1,
                    },
                    "temporada": {
                        "type": "integer",
                        "description": "Año de la temporada",
                        "minimum": 2026,
                    },
                },
                "required": ["jornada", "temporada"],
            },
        ),
        Tool(
            name="predict_quiniela",
            description=(
                "Genera una predicción completa de quiniela utilizando diferentes estrategias: "
                "conservadora (mayor probabilidad), arriesgada (balancea probabilidad y contexto) "
                "o personalizada (con distribución específica de 1-X-2)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "jornada": {
                        "type": "integer",
                        "description": "Número de jornada",
                        "minimum": 1,
                    },
                    "temporada": {
                        "type": "integer",
                        "description": "Año de la temporada",
                        "minimum": 2000,
                    },
                    "strategy": {
                        "type": "string",
                        "enum": ["conservadora", "arriesgada", "personalizada"],
                        "description": (
                            "Estrategia de predicción: "
                            "    'conservadora' (máxima probabilidad), "
                            "    'arriesgada' (balancea probabilidad y contexto), "
                            "    'personalizada' (distribución personalizada)"
                        ),
                        "default": "conservadora",
                    },
                    "custom_distribution": {
                        "type": "object",
                        "description": (
                            "Solo para strategy='custom': distribución deseada de signos. "
                            'Ejemplo: {"1": 8, "X": 4, "2": 3}'
                        ),
                        "properties": {
                            "1": {
                                "type": "integer",
                                "description": "Cantidad de 1s deseados",
                                "minimum": 0,
                                "maximum": 15,
                            },
                            "X": {
                                "type": "integer",
                                "description": "Cantidad de Xs deseadas",
                                "minimum": 0,
                                "maximum": 15,
                            },
                            "2": {
                                "type": "integer",
                                "description": "Cantidad de 2s deseados",
                                "minimum": 0,
                                "maximum": 15,
                            },
                        },
                        "required": ["1", "X", "2"],
                    },
                },
                "required": ["jornada", "temporada", "strategy"],
            },
        ),
        Tool(
            name="detect_surprises",
            description=(
                "Identifica partidos donde existe una inconsistencia significativa entre las "
                "probabilidades LAE y el análisis contextual (rachas, histórico, forma reciente). "
                "Útil para detectar posibles sorpresas."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "jornada": {
                        "type": "integer",
                        "description": "Número de jornada",
                        "minimum": 1,
                    },
                    "temporada": {
                        "type": "integer",
                        "description": "Año de la temporada",
                        "minimum": 2026,
                    },
                    "threshold": {
                        "type": "number",
                        "description": "Umbral de divergencia para considerar sorpresa (0-100, default: 30)",
                        "minimum": 0,
                        "maximum": 100,
                        "default": 30.0,
                    },
                },
                "required": ["jornada", "temporada"],
            },
        ),
        Tool(
            name="analyze_match",
            description=(
                "Analiza un partido específico con opciones flexibles: puede proporcionar análisis completo "
                "con predicción justificada (por defecto) o solo información en crudo del partido. "
                "\n\n**Con predicción (include_prediction=true)**: Genera predicción, nivel de confianza y "
                "justificación basada en probabilidades LAE, histórico, rachas y clasificación.\n\n"
                "**Sin predicción (include_prediction=false)**: Retorna únicamente datos en crudo como "
                "histórico de enfrentamientos, evolución reciente de ambos equipos, clasificaciones actuales, "
                "comparativa de últimos partidos y datos destacados. Útil para consultas específicas como: "
                "'muéstrame el histórico entre estos equipos', 'cuáles son los últimos resultados', etc."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "jornada": {
                        "type": "integer",
                        "description": "Número de jornada",
                        "minimum": 1,
                    },
                    "temporada": {
                        "type": "integer",
                        "description": "Año de la temporada",
                        "minimum": 2026,
                    },
                    "match_id": {
                        "type": "integer",
                        "description": "ID del partido dentro de la jornada (1-15 típicamente)",
                        "minimum": 1,
                        "maximum": 15,
                    },
                    "include_prediction": {
                        "type": "boolean",
                        "description": (
                            "Si true (default), incluye análisis completo con predicción justificada. "
                            "Si false, retorna solo datos en crudo sin predicción ni interpretación."
                        ),
                        "default": True,
                    },
                },
                "required": ["jornada", "temporada", "match_id"],
            },
        ),
        Tool(
            name="analyze_team",
            description=(
                "Analiza el rendimiento completo de un equipo: últimos resultados, rachas actuales, "
                "rendimiento como local/visitante, clasificación y tendencia."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "jornada": {
                        "type": "integer",
                        "description": "Número de jornada",
                        "minimum": 1,
                    },
                    "temporada": {
                        "type": "integer",
                        "description": "Año de la temporada",
                        "minimum": 2000,
                    },
                    "team_name": {
                        "type": "string",
                        "description": (
                            "Nombre del equipo a analizar (debe coincidir con el nombre usado en los datos)"
                        ),
                    },
                },
                "required": ["jornada", "temporada", "team_name"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Maneja las llamadas a las herramientas del servidor MCP.

    Parameters
    ----------
    name : str
        Nombre de la herramienta a ejecutar.
    arguments : Any
        Argumentos de la herramienta en formato de diccionario.

    Returns
    -------
    list[TextContent]
        Lista con el contenido de texto resultante de la ejecución.

    Raises
    ------
    ValueError
        Si la herramienta solicitada no existe o los argumentos son inválidos.
    """
    try:
        if name == "get_last_quiniela":
            result = data_source.get_last_kiniela()
            if result is None:
                return [TextContent(type="text", text="Error: No se pudo obtener la última quiniela.")]

            info, jornada, temporada, partidos = result
            response = {"info": info, "jornada": jornada, "temporada": temporada, "partidos": partidos}
            return [TextContent(type="text", text=json.dumps(obj=response, ensure_ascii=False, indent=2))]

        elif name == "get_quiniela":
            jornada = arguments["jornada"]
            temporada = arguments["temporada"]
            result = data_source.get_kiniela(jornada=jornada, temporada=temporada)

            if result is None:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: No se pudo obtener información de la jornada {jornada}, temporada {temporada}.",
                    )
                ]
            else:
                info, jornada, temporada, partidos = result
                response = {"info": info, "jornada": jornada, "temporada": temporada, "partidos": partidos}
                return [TextContent(type="text", text=json.dumps(obj=response, ensure_ascii=False, indent=2))]

        elif name == "get_probabilities":
            jornada = arguments["jornada"]
            temporada = arguments["temporada"]
            probabilities = data_source.get_kiniela_probabilities(jornada=jornada, temporada=temporada)

            if probabilities is None:
                error_msg = (
                    f"Error: No se pudieron obtener probabilidades para jornada {jornada}, temporada {temporada}."
                )
                return [TextContent(type="text", text=error_msg)]
            else:
                return [TextContent(type="text", text=json.dumps(obj=probabilities, ensure_ascii=False, indent=2))]

        elif name == "predict_quiniela":
            jornada = arguments["jornada"]
            temporada = arguments["temporada"]
            strategy = arguments.get("strategy", "conservadora")
            custom_dist = arguments.get("custom_distribution")

            prediction = predictor.predict(
                jornada=jornada,
                temporada=temporada,
                strategy=strategy,
                custom_distribution=custom_dist,
            )

            if prediction is None:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: No se pudo generar predicción para jornada {jornada}, temporada {temporada}.",
                    )
                ]

            return [TextContent(type="text", text=json.dumps(obj=prediction, ensure_ascii=False, indent=2))]

        elif name == "detect_surprises":
            jornada = arguments["jornada"]
            temporada = arguments["temporada"]
            threshold = arguments.get("threshold", 30.0)

            surprises = surprise_detector.detect(jornada=jornada, temporada=temporada, threshold=threshold)

            if surprises is None:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: No se pudieron detectar sorpresas para jornada {jornada}, temporada {temporada}.",
                    )
                ]

            return [TextContent(type="text", text=json.dumps(obj=surprises, ensure_ascii=False, indent=2))]

        elif name == "analyze_match":
            jornada = arguments["jornada"]
            temporada = arguments["temporada"]
            match_id = arguments["match_id"]

            analysis = analyzer.analyze_match(jornada=jornada, temporada=temporada, match_id=match_id)

            if analysis is None:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: No se pudo analizar el partido {match_id} de la jornada {jornada}.",
                    )
                ]

            return [TextContent(type="text", text=json.dumps(obj=analysis, ensure_ascii=False, indent=2))]

        elif name == "analyze_team":
            jornada = arguments["jornada"]
            temporada = arguments["temporada"]
            team_name = arguments["team_name"]

            analysis = analyzer.analyze_team(jornada=jornada, temporada=temporada, team_name=team_name)

            if analysis is None:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: No se pudo analizar el equipo '{team_name}' en la jornada {jornada}.",
                    )
                ]

            return [TextContent(type="text", text=json.dumps(obj=analysis, ensure_ascii=False, indent=2))]

        else:
            raise ValueError(f"Herramienta desconocida: {name}")

    except Exception as e:
        error_msg = f"Error al ejecutar {name}: {str(e)}"
        return [TextContent(type="text", text=error_msg)]


async def main() -> None:
    """
    Punto de entrada principal del servidor MCP.

    Inicia el servidor utilizando stdio (entrada/salida estándar) para comunicarse
    con el cliente MCP.
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream=read_stream,
            write_stream=write_stream,
            initialization_options=app.create_initialization_options(),
        )


def run() -> None:
    """
    Función síncrona que ejecuta el servidor MCP.
    
    Esta es la función de punto de entrada definida en pyproject.toml
    para el script `kinielagpt`.
    """
    asyncio.run(main())


if __name__ == "__main__":
    run()
