import random
import requests
import math

def buscar_estadisticas_monstruo(nombre_criatura: str) -> str:
    """
    Busca las estadísticas oficiales de un monstruo en la API gratuita del SRD de D&D 5e.
    Útil para las skills 'bestiario-cazador' y 'rastreador-cazador'.
    """
    if not isinstance(nombre_criatura, str) or not nombre_criatura.strip():
        return "Debes indicar el nombre del monstruo que quieres consultar."

    # La API usa minúsculas y guiones (ej: 'adult-black-dragon')
    query = nombre_criatura.strip().lower().replace(" ", "-")
    url = f"https://www.dnd5eapi.co/api/monsters/{query}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            tipo = data.get("type", "desconocido")
            cr = data.get("challenge_rating", 0)
            armor_class = data.get("armor_class", [])
            ac = armor_class[0].get("value", 10) if isinstance(armor_class, list) and armor_class else 10
            vulnerabilidades = ", ".join(data.get("damage_vulnerabilities", [])) or "Ninguna"
            inmunidades = ", ".join(data.get("damage_immunities", [])) or "Ninguna"
            
            # Devuelve datos crudos; el Agente Tabaxi se encarga de narrarlos en personaje.
            return f"[{data['name']}] Tipo: {tipo} | CR: {cr} | CA: {ac} | Vulnerable a: {vulnerabilidades} | Inmune a: {inmunidades}"
        elif response.status_code == 404:
            return f"No encontré estadísticas exactas para '{nombre_criatura}' en el manual básico. Deberás deducirlo por su tipo."
        return f"No pude consultar el bestiario (respuesta HTTP {response.status_code}). Inténtalo nuevamente."
    except requests.Timeout:
        return "La consulta al bestiario agotó el tiempo de espera. Inténtalo nuevamente."
    except requests.RequestException as e:
        return f"No pude conectar con el bestiario: {str(e)}"

def tirar_dados(cantidad: int, caras: int, modificador: int = 0) -> str:
    """
    Realiza una tirada de dados (ej. 1d20 + 3 para Supervivencia o Naturaleza).
    El agente puede usar esto para determinar si el NPC nota un detalle oculto.
    """
    if (
        isinstance(cantidad, bool)
        or isinstance(caras, bool)
        or isinstance(modificador, bool)
        or not isinstance(cantidad, int)
        or not isinstance(caras, int)
        or not isinstance(modificador, int)
    ):
        return "Tirada inválida: cantidad, caras y modificador deben ser números enteros."
    if cantidad <= 0 or caras <= 0:
        return "Tirada inválida: cantidad y caras deben ser mayores que cero."
    if cantidad > 100 or caras > 1000:
        return "Tirada inválida: usa como máximo 100 dados de hasta 1000 caras."
        
    resultados = [random.randint(1, caras) for _ in range(cantidad)]
    total = sum(resultados) + modificador
    
    detalles = f"[{', '.join(map(str, resultados))}]"
    if modificador != 0:
        signo = "+" if modificador > 0 else "-"
        detalles += f" {signo} {abs(modificador)}"
        
    return f"Resultado de {cantidad}d{caras}: {total} (Dados: {detalles})"

def tasar_botin_monstruo(cr_monstruo: float) -> str:
    """
    Calcula un valor aproximado en piezas de oro (PO) basado en el nivel de desafío (CR).
    Potencia la skill 'botin-cazador'.
    """
    if (
        isinstance(cr_monstruo, bool)
        or not isinstance(cr_monstruo, (int, float))
        or not math.isfinite(float(cr_monstruo))
        or cr_monstruo < 0
    ):
        return "Valoración inválida: el CR debe ser un número mayor o igual que cero."
    if cr_monstruo < 1:
        monedas = random.randint(1, 10)
        return f"Materiales menores. Valor estimado: {monedas} Piezas de Plata (PP)."
    elif cr_monstruo <= 4:
        monedas = random.randint(10, 50)
        return f"Glándulas o cueros útiles. Valor estimado: {monedas} Piezas de Oro (PO)."
    elif cr_monstruo <= 10:
        monedas = random.randint(100, 500)
        return f"Partes raras y exóticas. Valor estimado: {monedas} Piezas de Oro (PO)."
    else:
        monedas = random.randint(1000, 5000)
        return f"Materiales legendarios de altísima demanda. Valor estimado: {monedas} Piezas de Oro (PO)."