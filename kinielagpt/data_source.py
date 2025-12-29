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

import time

import pandas as pd
import requests
import xmltodict

URL_BASE = "https://www.quinielista.es/xml2/porcentajes.asp"
URL_LAE = "https://www.quinielista.es/xml2/porcentajes_lae.asp?jornada={}&temporada={}"
URL_QUINI = "https://www.quinielista.es/xml2/porcentajes.asp?jornada={}&temporada={}"
URL_DETAILS_BASE = "https://www.eduardolosilla.es/"
URL_DETAILS = "https://api.eduardolosilla.es/detallePartido"

HEADERS_BASE = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-language": "es-ES,es;q=0.9,en;q=0.8",
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
}

HEADER_DETAIL = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "es-ES,es;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "origin": "https://www.eduardolosilla.es",
    "pragma": "no-cache",
    "referer": "https://www.eduardolosilla.es/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
}


def get_xml_as_json(url: str) -> dict | None:
    """
    Obtiene XML desde una URL y lo convierte a formato diccionario.

    Realiza una petición HTTP GET a la URL especificada, recupera el contenido XML de la API quinielista.es y lo parsea
    en una estructura de diccionario usando la librería xmltodict con prefijo de atributos personalizado.

    Parameters
    ----------
    url : str
        URL desde la que obtener el XML. Puede ser URL_BASE, URL_LAE o URL_QUINI.

    Returns
    -------
    dict or None
        Diccionario con los datos XML convertidos a formato JSON, o None si la petición falla.

    Raises
    ------
    requests.exceptions.RequestException
        Si la petición HTTP falla o devuelve un código de estado de error.
    Exception
        Si el parseo del XML falla.

    """
    try:
        print(f"Fetching XML from {url}...")
        response = requests.get(url=url, headers=HEADERS_BASE)
        response.raise_for_status()
        
        # Parse XML and convert to dictionary (attr_prefix='' removes @ from attributes)
        result = xmltodict.parse(response.content, attr_prefix='')
        
        print("XML converted to JSON successfully")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching XML: {e}")
        return None
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return None

def get_last_kiniela() -> tuple:
    """
    Obtiene la información de la última quiniela disponible.

    Recupera los datos de la quiniela más reciente desde la URL base de quinielista.es y extrae el número de jornada, 
    año de temporada y lista de partidos con su información básica.

    Returns
    -------
    tuple
        Una tupla que contiene (info, jornada, temporada, partidos):
        - info (str or None): Cadena formateada con información de jornada y temporada.
        - jornada (int or None): Número de jornada.
        - temporada (int or None): Año de temporada.
        - partidos (list or None): Lista de partidos con campos id y partido.

    """
    json_data = get_xml_as_json(url=URL_BASE)
    jornada = int(json_data['quinielista']['porcentajes']['jornada']) if json_data else None
    temporada = int(json_data['quinielista']['porcentajes']['temporada']) if json_data else None
    info = (f"Quiniela de la jornada {jornada} de la temporada {temporada-1}/{temporada}" 
            if temporada is not None and jornada is not None else None)
    partidos = [{'id': int(i['num']), 'partido': f"{i['local']} | {i['visitante']}"} 
                for i in json_data['quinielista']['porcentajes']['partido']] if json_data else None

    return info, jornada, temporada, partidos

def get_kiniela(jornada: int, temporada: int) -> tuple:
    """
    Obtiene la información de quiniela para una jornada y temporada específicas.

    Recupera los datos de quiniela desde el endpoint LAE de quinielista.es para la jornada y temporada especificadas, 
    devolviendo información formateada sobre los partidos y sus identificadores.

    Parameters
    ----------
    jornada : int
        Número de jornada a consultar.
    temporada : int
        Año de temporada a consultar.

    Returns
    -------
    tuple
        Una tupla que contiene (info, jornada, temporada, partidos):
        - info (str or None): Cadena formateada con información de jornada y temporada.
        - jornada (int or None): Número de jornada (devuelto).
        - temporada (int or None): Año de temporada (devuelto).
        - partidos (list or None): Lista de partidos con campos id y partido.

    """
    json_data = get_xml_as_json(url=URL_LAE.format(jornada, temporada))

    if not json_data:
        print("No ha sido posible obtener información de la jornada solicitada.")
        return None, None, None, None
    else:
        info = (f"Quiniela de la jornada {jornada} de la temporada {temporada-1}/{temporada}" 
                if temporada is not None and jornada is not None else None)
        partidos = [{'id': int(i['num']), 'partido': f"{i['local']} | {i['visitante']}"} 
                    for i in json_data['quinielista']['porcentajes']['partido']] if json_data else None

        return info, jornada, temporada, partidos
    
def get_kiniela_probabilities(jornada: int, temporada: int) -> list | None:
    """
    Obtiene las probabilidades de quiniela para una jornada y temporada específicas.

    Recupera datos de las fuentes LAE y Quiniela, los fusiona usando operaciones de pandas DataFramey calcula 
    probabilidades normalizadas para los resultados de partido (1, X, 2) y predicciones de goles tanto para equipos 
    locales como visitantes. Las probabilidades se normalizan para sumar 100% por grupo.

    Parameters
    ----------
    jornada : int
        Número de jornada a consultar.
    temporada : int
        Año de temporada a consultar.

    Returns
    -------
    list or None
        Lista de probabilidades de partido con valores normalizados, o None si no hay datos disponibles.
        Cada partido contiene campos id, partido y probabilidades (1_Prob, X_Prob, 2_Prob, probabilidades de goles 
        para equipos local y visitante). Valores redondeados a 1 decimal.

    Process Detail
    --------------
    1. Obtiene datos XML de los endpoints LAE y Quiniela.
    2. Convierte el XML a pandas DataFrame para cada fuente.
    3. Concatena ambos DataFrames y convierte las columnas de porcentajes a numérico.
    4. Agrupa por número de partido ('num') y agrega: máximo para nombres de equipos, media para probabilidades.
    5. Normaliza grupos de probabilidades para sumar 100% (resultado partido, goles local, goles visitante).
    6. Filtra valores cero y redondea a 1 decimal.

    """
    json_lae = get_xml_as_json(url=URL_LAE.format(jornada, temporada))
    json_quini = get_xml_as_json(url=URL_QUINI.format(jornada, temporada))

    pdf_lae = (pd.DataFrame(data=json_lae['quinielista']['porcentajes']['partido']).fillna(value=0.0) 
               if json_lae else None)
    pdf_quini = (pd.DataFrame(data=json_quini['quinielista']['porcentajes']['partido']).fillna(value=0.0) 
                 if json_quini else None)

    if pdf_lae is not None and pdf_quini is not None:
        # Unión de ambos DataFrames
        pdf_union = pd.concat(objs=[pdf_lae, pdf_quini], ignore_index=True)
        
        # Convertir columna 'num' a entero y columnas de porcentajes a numéricas
        pdf_union['num'] = (pd.to_numeric(arg=pdf_union['num'], errors='coerce')
                            .fillna(value=0).astype(dtype=int))
        porc_cols = [col for col in pdf_union.columns if col.startswith('porc_')]
        pdf_union[porc_cols] = (pdf_union[porc_cols]
                                .apply(pd.to_numeric, errors='coerce')
                                .fillna(value=0.0))
        
        # Agrupar por 'num' y agregar: máximo para textos, media para porcentajes
        agg_dict = ({'local': 'max', 'visitante': 'max'} | {col: 'mean' for col in porc_cols})
        pdf = pdf_union.groupby(by='num').agg(func=agg_dict).reset_index()
        
        # Crear campo partido combinando local y visitante
        pdf['partido'] = pdf.apply(lambda row: f"{row['local']} | {row['visitante']}", axis=1)
        pdf = pdf.drop(columns=['local', 'visitante'])
        
        # Renombrar columnas de goles
        pdf = pdf.rename(columns={
            'porc_1': '1_Prob', 
            'porc_X': 'X_Prob', 
            'porc_2': '2_Prob',
            'porc_15L_0': '0_Goles_Local_Prob',
            'porc_15L_1': '1_Goles_Local_Prob',
            'porc_15L_2': '2_Goles_Local_Prob',
            'porc_15L_M': 'Mas_Goles_Local_Prob',
            'porc_15V_0': '0_Goles_Visitante_Prob',
            'porc_15V_1': '1_Goles_Visitante_Prob',
            'porc_15V_2': '2_Goles_Visitante_Prob',
            'porc_15V_M': 'Mas_Goles_Visitante_Prob'
        })
        
        # Normalizar grupos de columnas en base 100 (salvo si todas son 0)
        col_groups = [
            ['1_Prob', 'X_Prob', '2_Prob'],
            ['0_Goles_Local_Prob', '1_Goles_Local_Prob', '2_Goles_Local_Prob', 
             'Mas_Goles_Local_Prob'],
            ['0_Goles_Visitante_Prob', '1_Goles_Visitante_Prob', '2_Goles_Visitante_Prob', 
             'Mas_Goles_Visitante_Prob']
        ]
        
        for cols in col_groups:
            if all(col in pdf.columns for col in cols):
                row_sums = pdf[cols].sum(axis=1)
                mask = row_sums != 0
                pdf.loc[mask, cols] = pdf.loc[mask, cols].div(other=row_sums[mask], axis=0) * 100
        
        # Ordenar por 'num' y convertir a JSON eliminando claves con valor 0 y redondeando a 1 decimal
        pdf = pdf.sort_values(by='num').reset_index(drop=True)
        pdf = pdf.rename(columns={'num': 'id'})
        return [{k: round(number=v, ndigits=1) if isinstance(v, float) 
                 else v for k, v in row.items() if v != 0 and v != 0.0} for row in pdf.to_dict(orient='records')]
    
    return None

def get_kiniela_matches_details(jornada: int, temporada: int) -> list | None:
    """
    Obtiene información detallada de partidos incluyendo datos históricos y comparativa para una jornada específica.

    Establece una sesión con la API eduardolosilla.es, obtiene detalles completos de partidos incluyendo
    clasificaciones de equipos, tendencias de evolución, resultados históricos de los últimos 10 años, datos
    destacados y análisis comparativo del rendimiento reciente de equipos usando la función privada
    _procesar_comparativa.

    Parameters
    ----------
    jornada : int
        Número de jornada a consultar.
    temporada : int
        Año de temporada a consultar.

    Returns
    -------
    list or None
        Lista de diccionarios con información detallada de partidos, o None si la petición falla.
        Cada partido contiene: id, partido, division, clasificacionLocal, clasificacionVisitante,
        evolucionClasificacionLocal, evolucionClasificacionVisitante, historico_10_years, veces1, vecesX, veces2, 
        datosDestacados y comparativa procesada.

    Raises
    ------
    requests.exceptions.RequestException
        Si falla la inicialización de sesión o la petición a la API.

    """
    session = requests.Session()   
  
    try:
        print("Initializing session at www.eduardolosilla.es...")
        response = session.get(url=URL_DETAILS_BASE, headers=HEADERS_BASE)
        response.raise_for_status() # Verify that the request was successful: Status code 200-299
    except requests.exceptions.RequestException as e:
        print(f"Error initializing session: {e}")
        return None

    
    # Request parameters
    params = {"jornada": jornada, "temporada": temporada, "uts": int(time.time() * 1000)}

    try:
        # Make GET request using the session
        response = session.get(url=URL_DETAILS, params=params, headers=HEADER_DETAIL)
        response.raise_for_status() # Verify that the request was successful: Status code 200-299
        data = response.json()['detallePartidos']
        
        # Filtrar campos relevantes de cada partido
        partidos_filtrados = []
        for dt in data:
            historico_10 = (dt.get('historico', []) or [])[:10]

            # Local English-named wrapper for comparativa processing,
            # delegating to the existing implementation.
            def __process_comparison(*, ultimos_partidos, equipo_local, equipo_visitante):
                return __procesar_ultimos_partidos(
                    ultimos_partidos=ultimos_partidos,
                    equipo_local=equipo_local,
                    equipo_visitante=equipo_visitante,
                )

            # Procesar comparativa / Process comparison
            ultimos_partidos_procesado = __process_comparison(
                ultimos_partidos=dt.get('comparativa', {}),
                equipo_local=dt.get('local'),
                equipo_visitante=dt.get('visitante')
            )

            # Calcular rachas en un solo pase para optimizar
            rachas = {
                'local': [p['cod_resultado'] for p in ultimos_partidos_procesado 
                         if p.get('cod_resultado') and p.get('tipo') in ['local_como_local', 'local_como_visitante']],
                'visitante': [p['cod_resultado'] for p in ultimos_partidos_procesado 
                             if p.get('cod_resultado') and 
                             p.get('tipo') in ['visitante_como_local', 'visitante_como_visitante']],
                'local_como_local': [p['cod_resultado'] for p in ultimos_partidos_procesado 
                                    if p.get('cod_resultado') and p.get('tipo') == 'local_como_local'],
                'visitante_como_visitante': [p['cod_resultado'] for p in ultimos_partidos_procesado 
                                            if p.get('cod_resultado') and p.get('tipo') == 'visitante_como_visitante']
            }
            
            loc = rachas['local'][-5:] if rachas['local'] else []
            vist = rachas['visitante'][-5:] if rachas['visitante'] else []
            loc_as_loc = rachas['local_como_local'][-5:] if rachas['local_como_local'] else []
            vist_as_vist = rachas['visitante_como_visitante'][-5:] if rachas['visitante_como_visitante'] else []

            partido_filtrado = {
                'id': dt.get('orden'),
                'partido': f"{dt.get('local')} | {dt.get('visitante')}",
                'division': dt.get('division'),
                'clasificacion_local': dt.get('clasificacionLocal'),
                'clasificacion_visitante': dt.get('clasificacionVisitante'),
                'evolucion_clasificacion_local': dt.get('evolucionLocal'),
                'evolucion_clasificacion_visitante': dt.get('evolucionVisitante'),
                'historico_10_years': historico_10,
                'veces1': sum(1 for h in historico_10 if h.get('signo') == '1'),
                'vecesX': sum(1 for h in historico_10 if h.get('signo') == 'X'),
                'veces2': sum(1 for h in historico_10 if h.get('signo') == '2'),
                'datos_destacados': dt.get('datosDestacados'),
                'ultimos_partidos': ultimos_partidos_procesado,
                'racha_local_ultimos_5_partidos': loc,
                'racha_visitante_ultimos_5_partidos': vist,
                'racha_local_como_local_ultimos_5_partidos': loc_as_loc,
                'racha_visitante_como_visitante_ultimos_5_partidos': vist_as_vist
            }
            partidos_filtrados.append(partido_filtrado)
        
        return partidos_filtrados

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def __procesar_ultimos_partidos(ultimos_partidos: dict, equipo_local: str, equipo_visitante: str) -> list:
    """
    Procesa los datos de ultimos_partidos para extraer resultados históricos de partidos de ambos equipos.

    Transforma la estructura anidada de ultimos_partidos (vuelta1/vuelta2 con partidos_local/partidos_visitante) 
    en una lista plana de partidos ordenada por jornada.
    Muestra cómo cada equipo ha actuado en partidos recientes, filtrando sólo partidos completados (status=100)
    y resultados válidos.

    Parameters
    ----------
    ultimos_partidos : dict
        Diccionario que contiene claves vuelta1 y vuelta2 con listas partidos_local y partidos_visitante.
        Cada partido incluye: jornada, rival, resultado_casa, resultado_fuera, status.
    equipo_local : str
        Nombre del equipo local para el partido actual.
    equipo_visitante : str
        Nombre del equipo visitante para el partido actual.

    Returns
    -------
    list
        Lista plana de partidos ordenada por jornada, cada uno conteniendo:
        - jornada (str): Número de jornada.
        - partido (str): Partido formateado como "LOCAL | VISITANTE".
        - resultado (str): Resultado del partido (ej., "2-1", "0-0").
        - cod_resultado (str): Código del resultado para quiniela: 'VICTORIA', 'EMPATE' y 'DERROTA'.

    Process Detail
    --------------
    1. Itera a través de vuelta1 y vuelta2 en el diccionario comparativa (las vueltas no importan).
    2. Procesa partidos_local: partidos jugados por equipo_local contra rival.
       - Si resultado_casa válido: partido es "equipo_local | rival"
       - Si resultado_fuera válido: partido es "rival | equipo_local"
    3. Procesa partidos_visitante: partidos jugados por equipo_visitante contra rival.
       - Si resultado_casa válido: partido es "equipo_visitante | rival"
       - Si resultado_fuera válido: partido es "rival | equipo_visitante"
    4. Filtra partidos con status=100 y resultados válidos (no vacíos tras strip, no '-').
    5. Agrupa partidos por jornada, ordenando por equipo (local primero, visitante después).
    6. Ordena la lista final por jornada (numérico) y orden interno.

    Notes
    -----
    Esta es una función privada (prefijo __) usada internamente por get_kiniela_matches_details.
    El campo orden se usa para ordenación interna y se elimina de la salida final.

    """
    if not ultimos_partidos:
        return []
    
    def __resultado_valido(resultado: str) -> bool:
        """Comprueba si el resultado es válido (no vacío tras strip, no '-')."""
        if not resultado:
            return False
        resultado_clean = resultado.strip()
        return bool(resultado_clean and resultado_clean != '-')
    
    partidos_por_jornada = {}
    
    for vuelta in ['vuelta1', 'vuelta2']:
        if vuelta not in ultimos_partidos:
            continue
        
        # Partidos del EQUIPO LOCAL (partidos_local)
        # El equipo_local juega contra rival
        for p in ultimos_partidos[vuelta].get('partidos_local', []):
            if p.get('status') != 100:
                continue
            
            resultado_casa = p.get('resultado_casa', '').strip()
            resultado_fuera = p.get('resultado_fuera', '').strip()
            rival = p.get('rival', '')
            jornada = p.get('jornada')
            
            # Si hay resultado_casa válido: equipo_local | rival
            if __resultado_valido(resultado=resultado_casa):
                if jornada not in partidos_por_jornada:
                    partidos_por_jornada[jornada] = []
                orden = len(partidos_por_jornada[jornada])
                try:
                    goles_local, goles_rival = map(int, resultado_casa.split('-'))
                except Exception:
                    goles_local, goles_rival = None, None
                if goles_local is not None and goles_rival is not None:
                    if goles_local > goles_rival:
                        signo = 'VICTORIA'
                    elif goles_local == goles_rival:
                        signo = 'EMPATE'
                    else:
                        signo = 'DERROTA'
                else:
                    signo = ''
                partidos_por_jornada[jornada].append({
                    'jornada': jornada,
                    'partido': f"{equipo_local} | {rival}",
                    'resultado': resultado_casa,
                    'cod_resultado': signo,
                    'tipo': 'local_como_local',
                    'orden': orden
                })
            # Si hay resultado_fuera válido: rival | equipo_local
            if __resultado_valido(resultado=resultado_fuera):
                if jornada not in partidos_por_jornada:
                    partidos_por_jornada[jornada] = []
                orden = len(partidos_por_jornada[jornada])
                try:
                    goles_rival, goles_local = map(int, resultado_fuera.split('-'))
                except Exception:
                    goles_rival, goles_local = None, None
                if goles_local is not None and goles_rival is not None:
                    if goles_local > goles_rival:
                        signo = 'VICTORIA'
                    elif goles_local == goles_rival:
                        signo = 'EMPATE'
                    else:
                        signo = 'DERROTA'
                else:
                    signo = ''
                partidos_por_jornada[jornada].append({
                    'jornada': jornada,
                    'partido': f"{rival} | {equipo_local}",
                    'resultado': resultado_fuera,
                    'cod_resultado': signo,
                    'tipo': 'local_como_visitante',
                    'orden': orden
                })
        
        # Partidos del EQUIPO VISITANTE (partidos_visitante)
        # El equipo_visitante juega contra rival
        for p in ultimos_partidos[vuelta].get('partidos_visitante', []):
            if p.get('status') != 100:
                continue
            
            resultado_casa = p.get('resultado_casa', '').strip()
            resultado_fuera = p.get('resultado_fuera', '').strip()
            rival = p.get('rival', '')
            jornada = p.get('jornada')
            
            # Si hay resultado_casa válido: equipo_visitante | rival
            if __resultado_valido(resultado=resultado_casa):
                if jornada not in partidos_por_jornada:
                    partidos_por_jornada[jornada] = []
                orden = len(partidos_por_jornada[jornada])
                try:
                    goles_visitante, goles_rival = map(int, resultado_casa.split('-'))
                except Exception:
                    goles_visitante, goles_rival = None, None
                if goles_visitante is not None and goles_rival is not None:
                    if goles_visitante > goles_rival:
                        signo = 'VICTORIA'
                    elif goles_visitante == goles_rival:
                        signo = 'EMPATE'
                    else:
                        signo = 'DERROTA'
                else:
                    signo = ''
                partidos_por_jornada[jornada].append({
                    'jornada': jornada,
                    'partido': f"{equipo_visitante} | {rival}",
                    'resultado': resultado_casa,
                    'cod_resultado': signo,
                    'tipo': 'visitante_como_local',
                    'orden': orden
                })
            # Si hay resultado_fuera válido: rival | equipo_visitante
            if __resultado_valido(resultado=resultado_fuera):
                if jornada not in partidos_por_jornada:
                    partidos_por_jornada[jornada] = []
                orden = len(partidos_por_jornada[jornada])
                try:
                    goles_rival, goles_visitante = map(int, resultado_fuera.split('-'))
                except Exception:
                    goles_rival, goles_visitante = None, None
                if goles_visitante is not None and goles_rival is not None:
                    if goles_visitante > goles_rival:
                        signo = 'VICTORIA'
                    elif goles_visitante == goles_rival:
                        signo = 'EMPATE'
                    else:
                        signo = 'DERROTA'
                else:
                    signo = ''
                partidos_por_jornada[jornada].append({
                    'jornada': jornada,
                    'partido': f"{rival} | {equipo_visitante}",
                    'resultado': resultado_fuera,
                    'cod_resultado': signo,
                    'tipo': 'visitante_como_visitante',
                    'orden': orden
                })
    
    # Ordenar por jornada y luego por orden
    todos_partidos = []
    for jornada in sorted(partidos_por_jornada.keys(), key=lambda x: int(x) if x.isdigit() else 0):
        partidos_jornada = sorted(partidos_por_jornada[jornada], key=lambda x: x['orden'])
        todos_partidos.extend(
            [{'jornada': p['jornada'], 
              'partido': p['partido'], 
              'resultado': p['resultado'], 
              'cod_resultado': p['cod_resultado'],
              'tipo': p['tipo']}
             for p in partidos_jornada]
        )
    
    return todos_partidos
