# VN-JSON-Local-Translator
Una herramienta ligera en Python diseñada específicamente para traducir archivos JSON masivos de novelas visuales (como scripts de 40,000+ líneas) 100% offline, de forma gratuita y sin límites de API, utilizando modelos locales ejecutados a través de Ollama.
Resuelve el mayor problema de las traducciones automáticas en novelas visuales: mantiene la estructura exacta de los índices del JSON y respeta los saltos de línea (\n), evitando que el juego sufra desajustes o cuelgues en los diálogos.

Características Principales
100% Local y Privado: Todo corre en tu propia máquina mediante Ollama. Tus datos y archivos nunca salen de tu PC.

Gratis para Siempre: Sin costos por tokens, sin tarjetas de crédito y sin límites de velocidad de nube.

Sistema de Checkpoints (Guardado Continuo): Guarda el progreso automáticamente bloque por bloque. Si pausas el script, apagas la PC o te vas a dormir, al volver a ejecutarlo retomará exactamente desde la última línea traducida.

Protección de Estructura e Índices: Envía bloques controlados y valida mediante código que el JSON devuelto mantenga exactamente las mismas claves numéricas, evitando desfases fatales en el motor del juego.

Tono Literario: Al usar modelos de lenguaje locales (como Llama 3 o Mistral), comprende el contexto narrativo, la poesía visual y los monólogos internos mucho mejor que un traductor tradicional línea por línea.

Requisitos Previos
Python 3.x instalado en tu sistema.

Tener instalado Ollama en tu equipo.

Guía de Instalación y Uso
1. Clonar el repositorio
Bash
git clone https://github.com/soyvalal/vn-json-local-translator.git
cd vn-json-local-translator
2. Instalar las dependencias de Python
Bash
pip install ollama
3. Descargar el modelo local
Abre tu terminal y descarga el modelo recomendado (por ejemplo, Llama 3 de 8B):

Bash
ollama run llama3:8b
(Una vez descargado y listo para chatear, puedes salir escribiendo /exit o cerrando la terminal).

4. Configurar y Ejecutar
Coloca tu archivo JSON original en la misma carpeta del script y cámbiale el nombre (o edita la variable ARCHIVO_ENTRADA en el código) para que coincida.

Ejecuta el script:

Bash
python traductor_ollama.py
⚙️ Configuración Personalizada
Puedes abrir el archivo traductor_ollama.py con cualquier editor de texto y modificar las variables globales según tus necesidades:

Python
ARCHIVO_ENTRADA = "original.json"      # Tu archivo JSON de origen
ARCHIVO_SALIDA = "traducido.json"      # El archivo resultante
TAMANO_LOTE = 20                       # Líneas por lote (bájalo si tu PC va justa de RAM)
MODELO_OLLAMA = "llama3:8b"            # Puedes cambiarlo por 'gemma2', 'mistral', etc.

Contribuir
¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la gestión de etiquetas, añadir soporte para otros formatos o refinar el prompt literario, siéntete libre de abrir un Pull Request o un Issue.

📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
