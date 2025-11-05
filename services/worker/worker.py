import base64
from lxml import etree

def _strip_ns(tag: str) -> str:
    return tag.split('}', 1)[-1] if '}' in tag else tag

def classify_xml(xml_bytes: bytes) -> dict:
    root = etree.fromstring(xml_bytes)
    tag = _strip_ns(root.tag).lower()
    kind = "Desconhecido"

    if tag in ("nfeproc", "nfe"):
        # tentar identificar modelo 55 (NF-e) x 65 (NFC-e)
        mod = root.find(".//{*}ide/{*}mod")
        kind = "NFe" if (mod is None or mod.text == "55") else "NFCe"
    elif tag in ("cteproc", "cte"):
        kind = "CTe"
    elif tag in ("mdfeproc", "mdfe"):
        kind = "MDFe"
    elif tag.endswith("evento") or tag.endswith("procEventoNFe"):
        kind = "Evento"

    # aqui depois você persiste no banco (SQLAlchemy) e extrai metadados
    return {"kind": kind, "root": tag}

def process_xml(content_b64: str, filename: str) -> dict:
    xml_bytes = base64.b64decode(content_b64)
    cls = classify_xml(xml_bytes)
    # TODO: extrair chave, CNPJ, datas, valores e salvar
    print(f"[worker] {filename} → {cls}")
    return {"filename": filename, **cls}
