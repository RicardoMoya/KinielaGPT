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
Tests para el módulo data_source.

Ejecutar: python -m pytest tests/test_data_source.py -v
"""

import json

import kinielagpt.data_source as ds_module
from kinielagpt import data_source

URL_TEST_1 = "https://www.quinielista.es/xml2/porcentajes_lae.asp?jornada=28&temporada=2026"
URL_TEST_2 = "https://www.quinielista.es/xml2/porcentajes.asp?jornada=28&temporada=2026"
JORNADA_TEST = 28
TEMPORADA_TEST = 2026


def test_get_xml_as_json() -> None:
    """
    Prueba la función get_xml_as_json validando la obtención y conversión de XML a JSON.

    Verifica que la función puede realizar peticiones HTTP GET a la API de quinielista.es,
    parsear el XML recibido y convertirlo a formato diccionario. Valida la estructura completa
    del JSON resultante incluyendo campos de jornada, temporada, partidos y probabilidades.

    Raises
    ------
    AssertionError
        Si la estructura del JSON no coincide con la esperada o faltan campos requeridos.

    Examples
    --------
    >>> test_get_xml_as_json()
    ================================================================================
    TEST: get_xml_as_json()
    ================================================================================
    ✅ Jornada: 28, Temporada: 2026
    ✅ Se obtuvieron 15 partidos
    ✅ Primer partido tiene todas las claves requeridas
    ✅ Partido 15 tiene todas las claves de goles requeridas
    """
    print("=" * 80)
    print("TEST: get_xml_as_json()")
    print("=" * 80)

    result = data_source.get_xml_as_json(url=URL_TEST_1)
    
    assert result is not None,       "❌ No se pudo obtener el XML"
    assert isinstance(result, dict), "❌ El resultado debe ser un diccionario"
    
    # Comprobar que porcentajes contiene las claves requeridas
    porcentajes = result['quinielista']['porcentajes']
    assert 'jornada' in porcentajes,    "❌ Falta la clave 'jornada' en porcentajes"
    assert 'temporada' in porcentajes,  "❌ Falta la clave 'temporada' en porcentajes"
    assert 'partido' in porcentajes,    "❌ Falta la clave 'partido' en porcentajes"
    print(f"✅ Jornada: {porcentajes['jornada']}, Temporada: {porcentajes['temporada']}")
    
    # Comprobar que existe el campo partido y es una lista con 15 elementos
    partidos = porcentajes['partido']
    assert isinstance(partidos, list), "❌ El campo 'partido' debe ser una lista"
    assert len(partidos) == 15,       f"❌ Se esperaban 15 partidos, se obtuvieron {len(partidos)}"
    print(f"✅ Se obtuvieron {len(partidos)} partidos")
    
    # Comprobar que el primer elemento es un diccionario con las claves esperadas
    primer_partido = partidos[0]
    assert isinstance(primer_partido, dict), "❌ El primer partido debe ser un diccionario"
    assert 'num' in primer_partido,          "❌ Falta la clave 'num'"
    assert 'local' in primer_partido,        "❌ Falta la clave 'local'"
    assert 'visitante' in primer_partido,    "❌ Falta la clave 'visitante'"
    assert 'porc_1' in primer_partido,       "❌ Falta la clave 'porc_1'"
    assert 'porc_X' in primer_partido,       "❌ Falta la clave 'porc_X'"
    assert 'porc_2' in primer_partido,       "❌ Falta la clave 'porc_2'"
    print("✅ Primer partido tiene todas las claves requeridas")
    
    # Comprobar que el partido 15 tiene las claves de goles
    partido_15 = partidos[14]  # índice 14 = posición 15
    assert isinstance(partido_15, dict),  "❌ El partido 15 debe ser un diccionario"
    assert 'porc_15L_0' in partido_15,    "❌ Falta la clave 'porc_15L_0' en partido 15"
    assert 'porc_15L_1' in partido_15,    "❌ Falta la clave 'porc_15L_1' en partido 15"
    assert 'porc_15L_2' in partido_15,    "❌ Falta la clave 'porc_15L_2' en partido 15"
    assert 'porc_15L_M' in partido_15,    "❌ Falta la clave 'porc_15L_M' en partido 15"
    assert 'porc_15V_0' in partido_15,    "❌ Falta la clave 'porc_15V_0' en partido 15"
    assert 'porc_15V_1' in partido_15,    "❌ Falta la clave 'porc_15V_1' en partido 15"
    assert 'porc_15V_2' in partido_15,    "❌ Falta la clave 'porc_15V_2' en partido 15"
    assert 'porc_15V_M' in partido_15,    "❌ Falta la clave 'porc_15V_M' en partido 15"
    print("✅ Partido 15 tiene todas las claves de goles requeridas")
    print(f"✅ JSON resultante: {json.dumps(result)}")


def test_get_kiniela() -> None:
    """
    Prueba la función get_kiniela para una jornada y temporada específicas.

    Valida que la función puede recuperar información de quiniela desde el endpoint LAE,
    verificando la estructura de datos devuelta incluyendo información formateada, jornada,
    temporada y lista de partidos con formato 'LOCAL | VISITANTE'.

    Parameters
    ----------
    jornada : int, optional
        Número de jornada a probar (por defecto JORNADA_TEST=28).
    temporada : int, optional
        Año de temporada a probar (por defecto TEMPORADA_TEST=2026).

    Raises
    ------
    AssertionError
        Si los datos devueltos no coinciden con jornada/temporada o estructura incorrecta.

    Examples
    --------
    >>> test_get_kiniela(jornada=28, temporada=2026)
    ================================================================================
    TEST: get_kiniela()
    ================================================================================
    ✅ Info: Quiniela de la jornada 28 de la temporada 2025/2026
    ✅ Jornada: 28, Temporada: 2026
    ✅ Se obtuvieron 15 partidos
    """
    print("\n" + "=" * 80)
    print("TEST: get_kiniela()")
    print("=" * 80)

    info, jornada_ret, temporada_ret, partidos = data_source.get_kiniela(jornada=JORNADA_TEST, temporada=TEMPORADA_TEST)
    
    assert info is not None,            "❌ No se pudo obtener info"
    assert jornada_ret == JORNADA_TEST,     f"❌ Jornada esperada: {JORNADA_TEST}, obtenida: {jornada_ret}"
    assert temporada_ret == TEMPORADA_TEST, f"❌ Temporada esperada: {TEMPORADA_TEST}, obtenida: {temporada_ret}"
    assert partidos is not None,        "❌ No se pudieron obtener partidos"
    assert isinstance(partidos, list),  "❌ Partidos debe ser una lista"
    assert len(partidos) == 15,        f"❌ Se esperaban 15 partidos, se obtuvieron {len(partidos)}"
    
    # Comprobar que todos los partidos tienen las claves id y partido
    for partido in partidos:
        assert 'id' in partido,       "❌ Falta la clave 'id' en el partido"
        assert 'partido' in partido,  "❌ Falta la clave 'partido' en el partido"
        assert isinstance(partido['partido'], str), "❌ El valor de 'partido' debe ser un string"
        assert ' | ' in partido['partido'], (
            f"❌ El formato del partido debe ser 'EQUIPO | EQUIPO', obtenido: {partido['partido']}"
        )
        partes = partido['partido'].split(' | ')
        assert len(partes) == 2, (
            f"❌ El partido debe tener exactamente 2 equipos separados por ' | ', "
            f"obtenido: {partido['partido']}"
        )
    
    print(f"✅ Info: {info}")
    print(f"✅ Jornada: {jornada_ret}, Temporada: {temporada_ret}")
    print(f"✅ Se obtuvieron {len(partidos)} partidos")
    print("✅ Partidos Correctamente parseados:")
    for p in partidos:
        print(f"  {p['id']}: {p['partido']}")


def test_get_kiniela_probabilities() -> None:
    """
    Prueba la función get_kiniela_probabilities validando el cálculo de probabilidades normalizadas.

    Verifica que la función fusiona correctamente datos de fuentes LAE y Quiniela, calcula
    probabilidades normalizadas para resultados de partido (1, X, 2) y goles del partido 15,
    asegurando que las probabilidades sumen aproximadamente 100% por grupo.

    Raises
    ------
    AssertionError
        Si las probabilidades no están normalizadas correctamente o falta algún campo.

    Notes
    -----
    El partido 15 incluye campos adicionales de probabilidades de goles tanto para
    equipo local como visitante (0, 1, 2, Más goles).

    Examples
    --------
    >>> test_get_kiniela_probabilities(jornada=28, temporada=2026)
    ================================================================================
    TEST: get_kiniela_probabilities()
    ================================================================================
    ✅ Se obtuvieron probabilidades para 15 partidos
    ✅ Las probabilidades del primer partido suman 100.0%
    """
    print("\n" + "=" * 80)
    print("TEST: get_kiniela_probabilities()")
    print("=" * 80)

    result = data_source.get_kiniela_probabilities(jornada=JORNADA_TEST, temporada=TEMPORADA_TEST)
    
    assert result is not None,       "❌ No se pudieron obtener probabilidades"
    assert isinstance(result, list), "❌ El resultado debe ser una lista"
    assert len(result) == 15,       f"❌ Se esperaban 15 partidos, se obtuvieron {len(result)}"
    print(f"✅ Se obtuvieron probabilidades para {len(result)} partidos")
    
    # Comprobar estructura del primer partido (partidos 1-14)
    primer_partido = result[0]
    assert 'id' in primer_partido,      "❌ Falta la clave 'id'"
    assert 'partido' in primer_partido, "❌ Falta la clave 'partido'"
    assert '1_Prob' in primer_partido,  "❌ Falta la clave '1_Prob'"
    assert 'X_Prob' in primer_partido,  "❌ Falta la clave 'X_Prob'"
    assert '2_Prob' in primer_partido,  "❌ Falta la clave '2_Prob'"
    print("✅ Estructura del primer partido es correcta")
    
    # Verificar que las probabilidades suman ~100%
    suma = primer_partido['1_Prob'] + primer_partido['X_Prob'] + primer_partido['2_Prob']
    assert 99.0 <= suma <= 101.0, f"❌ Las probabilidades no suman 100%: {suma}"
    print(f"✅ Las probabilidades del primer partido suman {suma:.1f}%")
    
    # Comprobar estructura del partido 15 (con probabilidades de goles)
    partido_15 = result[14]
    assert '0_Goles_Local_Prob' in partido_15,       "❌ Falta la clave '0_Goles_Local_Prob'"
    assert '1_Goles_Local_Prob' in partido_15,       "❌ Falta la clave '1_Goles_Local_Prob'"
    assert '2_Goles_Local_Prob' in partido_15,       "❌ Falta la clave '2_Goles_Local_Prob'"
    assert 'Mas_Goles_Local_Prob' in partido_15,     "❌ Falta la clave 'Mas_Goles_Local_Prob'"
    assert '0_Goles_Visitante_Prob' in partido_15,   "❌ Falta la clave '0_Goles_Visitante_Prob'"
    assert '1_Goles_Visitante_Prob' in partido_15,   "❌ Falta la clave '1_Goles_Visitante_Prob'"
    assert '2_Goles_Visitante_Prob' in partido_15,   "❌ Falta la clave '2_Goles_Visitante_Prob'"
    assert 'Mas_Goles_Visitante_Prob' in partido_15, "❌ Falta la clave 'Mas_Goles_Visitante_Prob'"
    print("✅ Estructura del partido 15 es correcta")
    
    print(f"✅ Se obtuvieron {len(result)} partidos con probabilidades correctas")
    print(f"Primer partido: {primer_partido['partido']}")
    print(f"  1: {primer_partido['1_Prob']:.1f}%")
    print(f"  X: {primer_partido['X_Prob']:.1f}%")
    print(f"  2: {primer_partido['2_Prob']:.1f}%")
    print(f"Partido 15: {partido_15['partido']}")
    print(f"  Goles Local: 0={partido_15.get('0_Goles_Local_Prob', 0):.1f}%, "
          f"1={partido_15.get('1_Goles_Local_Prob', 0):.1f}%, "
          f"2={partido_15.get('2_Goles_Local_Prob', 0):.1f}%, "
          f"M={partido_15.get('Mas_Goles_Local_Prob', 0):.1f}%")
    print(f"  Goles Visitante: 0={partido_15.get('0_Goles_Visitante_Prob', 0):.1f}%, "
          f"1={partido_15.get('1_Goles_Visitante_Prob', 0):.1f}%, "
          f"2={partido_15.get('2_Goles_Visitante_Prob', 0):.1f}%, "
          f"M={partido_15.get('Mas_Goles_Visitante_Prob', 0):.1f}%")


def test_procesar_comparativa() -> None:
    """
    Prueba la función __procesar_comparativa comparando resultados con datos esperados.

    Carga datos raw de match_details_raw.json, procesa la comparativa del primer partido
    usando la función privada __procesar_comparativa y compara el resultado obtenido
    con los datos procesados previamente guardados en match_details_process.json.
    Valida que jornada, partido y resultado coincidan exactamente.

    Raises
    ------
    AssertionError
        Si los datos procesados no coinciden con los esperados o falta algún campo.

    Notes
    -----
    Esta prueba utiliza acceso a función privada mediante getattr para verificar
    el procesamiento correcto de datos de comparativa de partidos históricos.

    Process Detail
    --------------
    1. Carga datos raw desde match_details_raw.json con comparativa sin procesar.
    2. Carga datos esperados desde match_details_process.json.
    3. Extrae comparativa, equipo_local y equipo_visitante del primer partido.
    4. Invoca __procesar_comparativa con los datos extraídos.
    5. Compara resultado obtenido con comparativa esperada campo por campo.
    6. Verifica que número de partidos, jornadas, equipos y resultados coincidan.

    Examples
    --------
    >>> test_procesar_comparativa()
    ================================================================================
    TEST: __procesar_comparativa()
    ================================================================================
    ✅ Se cargaron 15 partidos del JSON raw
    ✅ Se cargaron 15 partidos del JSON process
    ✅ Partido: AT.MADRID vs VALENCIA
    ✅ Se obtuvieron 12 partidos procesados
    ✅ Número de partidos coincide: 12
    ✅ Todos los partidos procesados coinciden con los esperados
    """
    print("\n" + "=" * 80)
    print("TEST: __procesar_comparativa()")
    print("=" * 80)
    
    # Cargar datos raw
    json_raw_path = "tests/data_source_samples/match_details_raw.json"
    with open(json_raw_path, encoding="utf-8") as f:
        data_raw = json.load(f)
    
    # Cargar datos procesados esperados
    json_process_path = "tests/data_source_samples/match_details_process.json"
    with open(json_process_path, encoding="utf-8") as f:
        data_process = json.load(f)
    
    assert 'detallePartidos' in data_raw, "❌ No se encontró 'detallePartidos' en el JSON raw"
    partidos_raw = data_raw['detallePartidos']
    partidos_process = data_process
    assert len(partidos_raw) > 0, "❌ No hay partidos en el JSON raw"
    assert len(partidos_process) > 0, "❌ No hay partidos en el JSON process"
    print(f"✅ Se cargaron {len(partidos_raw)} partidos del JSON raw")
    print(f"✅ Se cargaron {len(partidos_process)} partidos del JSON process")
    
    # Probar con el primer partido
    primer_partido_raw = partidos_raw[0]
    primer_partido_process = partidos_process[0]
    
    comparativa = primer_partido_raw.get('comparativa', {})
    equipo_local = primer_partido_raw.get('local')
    equipo_visitante = primer_partido_raw.get('visitante')
    
    assert comparativa, "❌ No hay comparativa en el primer partido"
    assert equipo_local, "❌ No hay equipo local"
    assert equipo_visitante, "❌ No hay equipo visitante"
    print(f"✅ Partido: {equipo_local} vs {equipo_visitante}")
    
    # Acceder a la función privada __procesar_comparativa
    procesar_func = getattr(ds_module, '_data_source__procesar_comparativa', None)
    
    if procesar_func is None:
        procesar_func = getattr(ds_module, '__procesar_comparativa', None)
    
    assert procesar_func is not None, "❌ No se pudo acceder a __procesar_comparativa"
    
    # Procesar comparativa
    result = procesar_func(
        comparativa=comparativa,
        equipo_local=equipo_local,
        equipo_visitante=equipo_visitante
    )
    
    assert result is not None, "❌ El resultado no debe ser None"
    assert isinstance(result, list), "❌ El resultado debe ser una lista"
    print(f"✅ Se obtuvieron {len(result)} partidos procesados")
    
    # Verificar estructura de los partidos procesados
    if len(result) > 0:
        primer_resultado = result[0]
        assert 'jornada' in primer_resultado, "❌ Falta la clave 'jornada'"
        assert 'partido' in primer_resultado, "❌ Falta la clave 'partido'"
        assert 'resultado' in primer_resultado, "❌ Falta la clave 'resultado'"
        print("✅ Estructura correcta de partidos procesados")
    
    # Comparar resultado obtenido con el esperado (process.json)
    comparativa_esperada = primer_partido_process.get('comparativa', [])
    
    assert len(result) == len(comparativa_esperada), (
        f"❌ Número de partidos procesados no coincide: "
        f"obtenido={len(result)}, esperado={len(comparativa_esperada)}"
    )
    print(f"✅ Número de partidos coincide: {len(result)}")
    
    # Comparar cada partido procesado
    for i, (obtenido, esperado) in enumerate(zip(result, comparativa_esperada)):
        assert obtenido['jornada'] == esperado['jornada'], (
            f"❌ Jornada no coincide en partido {i}: "
            f"obtenido={obtenido['jornada']}, esperado={esperado['jornada']}"
        )
        assert obtenido['partido'] == esperado['partido'], (
            f"❌ Partido no coincide en posición {i}: "
            f"obtenido={obtenido['partido']}, esperado={esperado['partido']}"
        )
        assert obtenido['resultado'] == esperado['resultado'], (
            f"❌ Resultado no coincide en posición {i}: "
            f"obtenido={obtenido['resultado']}, esperado={esperado['resultado']}"
        )
    
    print("✅ Todos los partidos procesados coinciden con los esperados")


if __name__ == "__main__":
    test_get_xml_as_json()
    test_get_kiniela()
    test_get_kiniela_probabilities()
    test_procesar_comparativa()
