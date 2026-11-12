import json
import os
import ollama

# ================= CONFIGURACIÓN =================
ARCHIVO_ENTRADA = "original.json"      # Cambia esto al nombre exacto de tu JSON
ARCHIVO_SALIDA = "traducido.json"      # Aquí se guardará el resultado
TAMANO_LOTE = 20                       # Lotes de 20 líneas para ir fluidos en local
MODELO_OLLAMA = "llama3:8b"            # El modelo local de Ollama a utilizar

GLOSARIO = """
- Mantén el tono literario, melancólico e inmersivo de una novela visual.
- Conserva exactamente los saltos de línea (\\n) y símbolos como ―――.
- No traduzcas nombres propios inventados o de personajes a menos que tengan traducción oficial.
"""
# =================================================

def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def traducir_lote(lote_dict):
    prompt = f"""
Traduce del inglés al español los valores de este objeto JSON correspondiente a diálogos y narración de una novela visual.

REGLAS ESTRICTAS:
1. Devuelve ÚNICAMENTE un objeto JSON válido (comenzando con {{ y terminando con }}) con exactamente las mismas claves numéricas ("0", "1", etc.).
2. NO agregues explicaciones, texto extra, ni bloques de código markdown fuera del JSON.
3. Conserva los saltos de línea (\\n) dentro de cada frase aproximadamente en la misma proporción para que no desborden la caja de texto.
4. {GLOSARIO}

JSON a traducir:
{json.dumps(lote_dict, ensure_ascii=False)}
"""

    for intento in range(3):
        try:
            response = ollama.chat(
                model=MODELO_OLLAMA,
                messages=[{'role': 'user', 'content': prompt}],
                options={
                    'temperature': 0.3,
                }
            )
            
            texto_respuesta = response['message']['content'].strip()
            
            # Limpieza por si el modelo incluye bloques de markdown tipo ```json ... ```
            if texto_respuesta.startswith("```"):
                texto_respuesta = texto_respuesta.split("```")[1]
                if texto_respuesta.startswith("json"):
                    texto_respuesta = texto_respuesta[4:]
            texto_respuesta = texto_respuesta.strip()

            resultado = json.loads(texto_respuesta)
            
            if set(resultado.keys()) == set(lote_dict.keys()):
                return resultado
            else:
                print(f"  [!] Diferencia en claves detectada localmente. Reintentando ({intento+1}/3)...")
        except Exception as e:
            print(f"  [!] Error procesando con Ollama: {e}. Reintentando...")
            
    raise RuntimeError("No se pudo traducir el lote localmente después de 3 intentos.")

def main():
    if not os.path.exists(ARCHIVO_ENTRADA):
        print(f"Error: No se encuentra el archivo {ARCHIVO_ENTRADA}")
        return

    datos_originales = cargar_json(ARCHIVO_ENTRADA)
    total_lineas = len(datos_originales)
    print(f"Total de líneas encontradas: {total_lineas}")

    # Sistema de checkpoint: si ya existe salida previa, retoma
    if os.path.exists(ARCHIVO_SALIDA):
        datos_traducidos = cargar_json(ARCHIVO_SALIDA)
        inicio = len(datos_traducidos)
        print(f"Retomando traducción local desde la línea {inicio}...")
    else:
        datos_traducidos = []
        inicio = 0

    for i in range(inicio, total_lineas, TAMANO_LOTE):
        fin = min(i + TAMANO_LOTE, total_lineas)
        print(f"Traduciendo localmente líneas {i} a {fin - 1} de {total_lineas}...")
        
        lote_actual = {str(idx): datos_originales[idx] for idx in range(i, fin)}
        lote_traducido = traducir_lote(lote_actual)
        
        for idx in range(i, fin):
            datos_traducidos.append(lote_traducido[str(idx)])
            
        guardar_json(ARCHIVO_SALIDA, datos_traducidos)

    print("\n¡Traducción local completada con éxito! Archivo guardado en:", ARCHIVO_SALIDA)

if __name__ == "__main__":
    main()
