# ⚽ Makelele

> **The tireless web crawler & clean text extractor.**  
> Extract, clean, and structure text content from any website for redesigns, migrations, or LLM / RAG dataset preparation.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*Read this in [English](#english) | [Español](#español)*

---

<a name="english"></a>
## 🇬🇧 English

Like the legendary football player Claude Makélélé, this engine does the tireless, essential "dirty work": it traverses internal links across a domain, filters out noise (headers, navbars, sidebars, cookie banners, legal footers, and HTML bloat), and outputs structured, clean text.

### ✨ Features
- 🔍 **Internal Link Discovery:** Crawls internal pages while skipping external links, anchors, query noise, and heavy media files (`.pdf`, `.png`, `.zip`, etc.).
- 🧹 **Noise-Free Content Extraction:** Powered by [Trafilatura](https://github.com/adbar/trafilatura) to retain headings, structured text, and tables without site clutter.
- 📁 **Organized Output:**
  - Saves an individual `.txt` file per discovered page.
  - Generates a consolidated `_resumen_completo.txt` containing all text across the entire site.
- ⚙️ **CLI & Interactive Mode:** Accepts terminal arguments or prompts for input if run with no parameters.

### 📦 Installation
```bash
git clone https://github.com/Comeranas/makelele.git
cd makelele

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🛠️ Usage

**1. Basic run:**
```bash
python makelele.py https://example.com
```

**2. Custom output directory and crawl depth:**
```bash
python makelele.py https://example.com -o ./extracted_data -d 2
```

**3. Interactive run:**
```bash
python makelele.py
```

---

<a name="español"></a>
## 🇪🇸 Español

Al igual que Claude Makélélé en el campo de fútbol, este script hace el trabajo sucio e invisible: recorre los enlaces internos de un dominio, filtra menús, barras de navegación, avisos de cookies y código innecesario, entregando contenido limpio y listo para usar.

### ✨ Características
- 🔍 **Detección automática de enlaces internos:** Mapea el dominio evitando enlaces externos, anclas y archivos multimedia pesados (`.pdf`, `.png`, `.zip`, etc.).
- 🧹 **Extracción limpia con Trafilatura:** Conserva títulos, párrafos y tablas sin ruido publicitario ni código HTML.
- 📁 **Organización inteligente:**
  - Guarda un archivo `.txt` por cada página encontrada.
  - Genera automáticamente un `_resumen_completo.txt` con todo el contenido del sitio unificado.
- ⚙️ **CLI y Modo Interactivo:** Admite argumentos por terminal o solicita la URL si se ejecuta sin parámetros.

### 📦 Instalación
```bash
git clone https://github.com/Comeranas/makelele.git
cd makelele

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🛠️ Uso

**1. Uso básico:**
```bash
python makelele.py https://ejemplo.com
```

**2. Carpeta de salida personalizada y profundidad:**
```bash
python makelele.py https://ejemplo.com -o ./mi_contenido -d 2
```

**3. Modo interactivo:**
```bash
python makelele.py
```

---

## 📄 License / Licencia
MIT License.
