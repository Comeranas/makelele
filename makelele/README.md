# ⚽ Makelele

> **The tireless web content recovery engine.**  
> Recupera, limpia y estructura el contenido textual de cualquier sitio web para rediseños, migraciones o preparación de datasets para LLMs y sistemas RAG.

Al igual que Claude Makélélé en el campo de fútbol, este script hace el trabajo sucio e invisible: recorre los enlaces de un dominio, filtra menús, barras laterales, avisos legales repetitivos y código basura, y te entrega el contenido limpio y organizado.

---

## 🚀 Características

- 🔍 **Detección automática de enlaces internos:** Mapea el dominio evitando enlaces externos, anclas y archivos multimedia pesados (.pdf, .png, .zip, etc.).
- 🧹 **Extracción limpia con Trafilatura:** Conserva títulos, párrafos y tablas sin ruido publicitario ni código HTML.
- 📁 **Organización inteligente:**
  - Guarda un archivo `.txt` por cada página encontrada.
  - Genera automáticamente un `_resumen_completo.txt` con todo el contenido del sitio unificado.
- ⚙️ **CLI flexible:** Soporta parámetros por terminal o modo interactivo.

---

## 📦 Instalación

```bash
git clone https://github.com/Comeranas/makelele.git
cd makelele

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🛠️ Uso

### 1. Modo directo
```bash
python makelele.py https://ejemplo.com
```

### 2. Especificando carpeta de destino y profundidad
```bash
python makelele.py https://ejemplo.com -o ./mi_contenido -d 2
```

### 3. Modo interactivo
Si lo ejecutas sin argumentos, te solicitará la URL:
```bash
python makelele.py
```

---

## 📄 Licencia

MIT License.
