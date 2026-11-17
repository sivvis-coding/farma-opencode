"""Export REDCap metadata or selected fields locally, without displaying the token."""
import argparse
import getpass
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "Redirect refused", headers, fp)


def prepare_request(url, token, content, fields):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme.lower() != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("La dirección debe ser HTTPS, sin usuario ni contraseña.")
    if parsed.query or parsed.fragment:
        raise ValueError("La dirección no debe incluir parámetros ni fragmentos.")
    if content == "record" and not fields:
        raise ValueError("Para registros hay que especificar al menos un campo.")
    params = [("token", token), ("content", content), ("format", "csv")]
    if content == "record":
        params.extend(("fields[]", field) for field in fields)
        params.append(("type", "flat"))
    body = urllib.parse.urlencode(params).encode("utf-8")
    return urllib.request.Request(url, data=body, method="POST")


def main():
    parser = argparse.ArgumentParser(description="Exportación local de REDCap: solo lectura.")
    parser.add_argument("--url", required=True, help="URL HTTPS de la API, sin token")
    parser.add_argument("--tipo", choices=("metadata", "record"), default="metadata")
    parser.add_argument("--campo", action="append", default=[], help="Campo a exportar; repetir por campo")
    parser.add_argument("--salida", required=True, help="Ruta de un archivo nuevo; no se sobrescribe")
    args = parser.parse_args()
    try:
        # Validate before asking for credentials or creating a file.
        prepare_request(args.url, "", args.tipo, args.campo)
        output = Path(args.salida)
        if output.exists():
            raise ValueError("La salida ya existe; elige otro nombre.")
        print("Esta operación contactará REDCap y guardará datos localmente.")
        print("Confirma que tienes autorización institucional; campos y metadatos pueden ser sensibles.")
        print("Registros: se exportan todos los registros accesibles para los campos indicados.")
        if input("Escribe SI para continuar: ") != "SI":
            print("Cancelado.")
            return 0
        token = getpass.getpass("Token REDCap (no se muestra): ")
        if not token:
            raise ValueError("Token vacío.")
        request = prepare_request(args.url, token, args.tipo, args.campo)
        opener = urllib.request.build_opener(NoRedirect, urllib.request.HTTPSHandler(context=ssl.create_default_context()))
        # Exclusive creation avoids overwriting existing work, including concurrent creation.
        with output.open("xb") as target:
            try:
                with opener.open(request, timeout=60) as response:
                    content_type = response.headers.get("Content-Type", "").lower()
                    if "json" in content_type or "html" in content_type:
                        raise ValueError("REDCap no devolvió CSV; revisa URL y permisos.")
                    while True:
                        chunk = response.read(65536)
                        if not chunk:
                            break
                        target.write(chunk)
            except Exception:
                target.close()
                output.unlink(missing_ok=True)
                raise
        print("Exportación completada. Protege el archivo y no lo subas al repositorio.")
        return 0
    except (ValueError, OSError, urllib.error.URLError) as exc:
        # Never print a server response or URL: either could contain sensitive content.
        print(f"No se pudo completar la exportación ({type(exc).__name__}). Revisa URL, permisos y conexión.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
