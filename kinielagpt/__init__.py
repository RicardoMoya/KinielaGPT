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
KinielaGPT - Servidor MCP para predicción de quiniela española.

Este paquete implementa un servidor Model Context Protocol (MCP) que proporciona
herramientas para analizar y predecir resultados de la quiniela española de fútbol.

Autor: Ricardo Moya
GitHub: https://github.com/RicardoMoya
LinkedIn: https://www.linkedin.com/in/phdricardomoya/
Licencia: AGPL-3.0-or-later
"""

__version__ = "1.0.0"
__author__ = "Ricardo Moya"
__email__ = "contact@ricardomoya.dev"
__license__ = "AGPL-3.0-or-later"
__github__ = "https://github.com/RicardoMoya/kiniela-gpt"

from kinielagpt import data_source
from kinielagpt.analyzer import Analyzer
from kinielagpt.detector import SurpriseDetector
from kinielagpt.predictor import KinielaPredictor

__all__ = [
    "data_source",
    "KinielaPredictor",
    "Analyzer",
    "SurpriseDetector",
]
