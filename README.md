# Agent ADK Laprida Fernando

Agente de cazarrecompensas Tabaxi para D&D 5e desarrollado con Python y Google Agent Development Kit (ADK). Interpreta solicitudes en español, mantiene el personaje y selecciona herramientas para identificar criaturas, realizar pruebas de dados y estimar el botín de un monstruo.

## Características

- Identificación y análisis de criaturas a partir de una descripción o rastros.
- Consulta del bestiario oficial de D&D 5e a través de la API pública del SRD.
- Traducción de estadísticas mecánicas a consejos narrativos.
- Resolución de tiradas de dados, incluyendo modificadores.
- Estimación aleatoria de valor y partes aprovechables según el Nivel de Desafío (CR).
- Bloque final fuera de personaje con datos mecánicos para el Dungeon Master.
- Manejo de nombres vacíos, tiradas inválidas, valores de CR inválidos y respuestas vacías o de error de la API.

## Herramientas

| Herramienta | Responsabilidad | Ejemplos de entrada |
| --- | --- | --- |
| `buscar_estadisticas_monstruo` | Consulta estadísticas del bestiario SRD por nombre normalizado | `adult black dragon`, `owlbear`, `kobold` |
| `tirar_dados` | Genera tiradas aleatorias y aplica un modificador | `cantidad=1, caras=20, modificador=3` |
| `tasar_botin_monstruo` | Estima piezas de plata/oro y el tipo de materiales según el CR | `CR 14`, `CR 3`, `CR 0.5` |

El agente usa LiteLLM para conectarse a Ollama; el modelo configurado es `qwen2.5:3b`.

## Requisitos

- Windows o cualquier sistema compatible con Python 3.10 o superior.
- Python y `pip`.
- Ollama instalado y ejecutándose.
- Conexión a Internet para consultar `https://www.dnd5eapi.co`.

## Instalación

Desde la raíz del repositorio:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Descarga el modelo usado por el agente:

```powershell
ollama pull qwen2.5:3b
```

Comprueba que Ollama responde:

```powershell
ollama list
```

No es necesario configurar una clave de API para este modelo local.

## Ejecutar el agente

Con Ollama activo, inicia la interfaz web de ADK desde la raíz del proyecto:

```powershell
adk web
```

Luego abre la dirección mostrada por la terminal, normalmente `http://127.0.0.1:8000`, selecciona `agent` y prueba ejemplos como:

- “Encontré huellas grandes con garras cerca del campamento. ¿Qué criatura podría ser?”
- “Identifica a un adult black dragon y dime cómo sobrevivir.”
- “Haz una tirada de 1d20 más 3 para Supervivencia.”
- “Acabo de cazar un dragón de CR 14. ¿Qué partes puedo despiezar y cuánto valen?”

## Selección y uso de herramientas

El modelo decide qué herramienta invocar según la intención del mensaje:

1. Si solicita identificar o consultar una criatura, usa `buscar_estadisticas_monstruo`.
2. Si necesita resolver una tirada explícita o una prueba para el personaje, usa `tirar_dados`.
3. Si posee el CR de una criatura y pide tasar el botín, usa `tasar_botin_monstruo`.

Las herramientas devuelven texto estructurado al agente. Este convierte los datos en narrativa en personaje y añade mecánicas reales en el bloque citado del DM.

## Ejemplo de respuestas

### Consulta de bestiario

```text
Usuario: ¿Qué puedo hacer contra un adult black dragon?

Agente:
Su escamas, como mi pelaje cuando estoy entre arbustos,
desvían armas ordinarias, pero su aliento ácido perfora
armaduras y carne por igual. Mantén distancia y busca
cobertura para no quedar atrapado en el baño corrosivo.

> Bloque del DM: Adult Black Dragon | CR 14 | CA 19 |
> Tipo: dragon | Vulnerable a: Ninguna | Inmune a: acid
```

### Tirada

```text
Usuario: Haz una tirada de percepción con 1d20 + 2.

> Resultado generado por tirar_dados: 1d20 + 2
```

## Validaciones

- `buscar_estadisticas_monstruo` rechaza nombres vacíos y distingue criatura inexistente, errores HTTP y problemas de conexión.
- `tirar_dados` exige valores enteros, cantidad y caras positivas, como máximo 100 dados y 1000 caras.
- `tasar_botin_monstruo` rechaza CR negativos, valores no numéricos o infinitos.

## Ejecución alternativa

Para probar las herramientas sin iniciar la interfaz web:

```powershell
python -c "from tools.tools import buscar_estadisticas_monstruo, tirar_dados, tasar_botin_monstruo; print(buscar_estadisticas_monstruo('owlbear')); print(tirar_dados(1,20,3)); print(tasar_botin_monstruo(14))"
```

## Resolución de problemas

- **`adk` no se reconoce:** activa el entorno virtual y reinstala `google-adk`.
- **No se puede conectar a Ollama:** verifica que el servicio esté iniciado con `ollama serve` y que el modelo exista con `ollama list`.
- **Modelo no encontrado:** ejecuta `ollama pull qwen2.5:3b`.
- **Error al consultar el bestiario:** comprueba la conexión a Internet y vuelve a intentar con el nombre en inglés de la criatura.

## Autor

Laprida Fernando