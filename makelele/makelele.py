#!/usr/bin/env python3
"""
Makelele - The tireless web content recovery engine.
Recupera, limpia y estructura el contenido textual de cualquier sitio web.
Ideal para rediseños web, migraciones y preparación de datasets para LLMs/RAG.
"""

import os
import re
import sys
import argparse
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import trafilatura

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

EXCLUDED_EXTENSIONS = (
    ".pdf", ".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg",
    ".zip", ".tar", ".gz", ".rar", ".7z", ".mp4", ".mp3", ".avi",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"
)

def clean_filename(url_path: str) -> str:
    """Genera un nombre de archivo seguro y ordenado basado en el path de la URL."""
    path = url_path.strip("/")
    if not path:
        return "00_home.txt"
    safe_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", path)
    return f"{safe_name}.txt"

def get_internal_links(base_url: str, max_depth: int = 1, timeout: int = 15) -> list:
    """
    Rastrea y recopila los enlaces internos que pertenecen al mismo dominio,
    ignorando anclas, scripts, correos y archivos binarios/multimedia.
    """
    domain = urlparse(base_url).netloc
    visited = set()
    to_visit = [(base_url, 0)]
    internal_links = set([base_url])

    while to_visit:
        current_url, depth = to_visit.pop(0)
        if current_url in visited or depth > max_depth:
            continue
        visited.add(current_url)

        try:
            r = requests.get(current_url, headers=DEFAULT_HEADERS, timeout=timeout)
            if r.status_code != 200:
                continue
        except Exception:
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue

            full_url = urljoin(current_url, href)
            parsed = urlparse(full_url)

            # Validar mismo dominio
            if parsed.netloc == domain:
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                clean_url = clean_url.rstrip("/") if parsed.path != "/" else clean_url

                if not clean_url.lower().endswith(EXCLUDED_EXTENSIONS):
                    if clean_url not in internal_links:
                        internal_links.add(clean_url)
                        if depth + 1 <= max_depth:
                            to_visit.append((clean_url, depth + 1))

    return sorted(list(internal_links))

def extract_content(url: str, timeout: int = 15) -> str:
    """
    Extrae el contenido textual principal usando Trafilatura,
    filtrando cabeceras, menús, footers y anuncios repetitivos.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            r = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
            if r.status_code == 200:
                downloaded = r.text

        if downloaded:
            text = trafilatura.extract(
                downloaded,
                include_links=True,
                include_images=False,
                output_format="txt"
            )
            return text
    except Exception as e:
        print(f"  [!] Error al extraer {url}: {e}")
    return None

def run_extraction(target_url: str, output_dir: str = None, max_depth: int = 1):
    parsed = urlparse(target_url)
    if not parsed.scheme:
        target_url = "https://" + target_url
        parsed = urlparse(target_url)

    domain_folder = parsed.netloc.replace("www.", "")
    if not output_dir:
        output_dir = os.path.join(os.getcwd(), "output", domain_folder)

    os.makedirs(output_dir, exist_ok=True)

    print("=" * 65)
    print("⚽ MAKELELE - The Tireless Web Content Recovery Engine")
    print(f"🌐 Objetivo: {target_url}")
    print(f"📁 Destino:  {output_dir}")
    print("=" * 65)

    print("\n[1/2] 🔍 Explorando enlaces internos del sitio...")
    links = get_internal_links(target_url, max_depth=max_depth)
    print(f"-> Localizadas {len(links)} páginas internas.")

    resumen_path = os.path.join(output_dir, "_resumen_completo.txt")
    with open(resumen_path, "w", encoding="utf-8") as resumen_f:
        resumen_f.write("RECOPILACIÓN DE CONTENIDO REALIZADA POR MAKELELE\n")
        resumen_f.write(f"URL Objetivo: {target_url}\n")
        resumen_f.write(f"Total páginas procesadas: {len(links)}\n")
        resumen_f.write("=" * 65 + "\n\n")

        print("\n[2/2] ⚡ Extrayendo y limpiando contenidos...")
        for idx, link in enumerate(links, 1):
            parsed_link = urlparse(link)
            fname = clean_filename(parsed_link.path)
            individual_file = os.path.join(output_dir, fname)

            print(f" [{idx}/{len(links)}] {link} -> {fname}")
            texto = extract_content(link)

            if texto and texto.strip():
                with open(individual_file, "w", encoding="utf-8") as f:
                    f.write(f"URL: {link}\n")
                    f.write("=" * 65 + "\n\n")
                    f.write(texto)

                resumen_f.write(f"\n\n{'#' * 65}\n")
                resumen_f.write(f"PÁGINA: {link}\n")
                resumen_f.write(f"{'#' * 65}\n\n")
                resumen_f.write(texto)
                resumen_f.write("\n")
            else:
                print("      (Sin texto principal identificable)")

    print("\n" + "=" * 65)
    print("✅ ¡Extracción completada con éxito!")
    print(f"📄 Resumen global unificado: {resumen_path}")
    print(f"📁 Páginas individuales:     {output_dir}")
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(
        description="Makelele: El recuperador incansable de contenidos web para migraciones y LLMs."
    )
    parser.add_argument("url", nargs="?", help="URL del sitio web a rastrear (ej. https://ejemplo.com)")
    parser.add_argument("-o", "--output", help="Carpeta de destino personalizada")
    parser.add_argument("-d", "--depth", type=int, default=1, help="Profundidad de rastreo interno (default: 1)")

    args = parser.parse_args()

    if not args.url:
        target = input("Introduce la URL a extraer: ").strip()
        if not target:
            print("Error: Se requiere una URL válida.")
            sys.exit(1)
        args.url = target

    run_extraction(args.url, args.output, max_depth=args.depth)

if __name__ == "__main__":
    main()
