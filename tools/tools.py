import random
import requests

def buscar_estadisticas_monstruo(nombre_criatura: str) -> str:
    """
    Busca las estadísticas oficiales de un monstruo en la API gratuita del SRD de D&D 5e.
    Útil para las skills 'bestiario-cazador' y 'rastreador-cazador'.
    """
    # La API usa minúsculas y guiones (ej: 'adult-black-dragon')
    query = nombre_criatura.strip().lower().replace(" ", "-")
    url = f"https://www.dnd5eapi.co/api/monsters/{query}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            tipo = data.get("type", "desconocido")
            cr = data.get("challenge_rating", 0)
            ac = data.get("armor_class", [{}])[0].get("value", 10)
            vulnerabilidades = ", ".join(data.get("damage_vulnerabilities", [])) or "Ninguna"
            inmunidades = ", ".join(data.get("damage_immunities", [])) or "Ninguna"
            
            # Devuelve datos crudos; el Agente Tabaxi se encarga de narrarlos en personaje.
            return f"[{data['name']}] Tipo: {tipo} | CR: {cr} | CA: {ac} | Vulnerable a: {vulnerabilidades} | Inmune a: {inmunidades}"
        else:
            return f"No encontré estadísticas exactas para '{nombre_criatura}' en el manual básico. Deberás deducirlo por su tipo."
    except Exception as e:
        return f"Error al consultar el bestiario: {str(e)}"

def tirar_dados(cantidad: int, caras: int, modificador: int = 0) -> str:
    """
    Realiza una tirada de dados (ej. 1d20 + 3 para Supervivencia o Naturaleza).
    El agente puede usar esto para determinar si el NPC nota un detalle oculto.
    """
    if cantidad <= 0 or caras <= 0:
        return "Tirada inválida."
        
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