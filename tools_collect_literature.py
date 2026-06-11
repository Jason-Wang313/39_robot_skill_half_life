import csv
import hashlib
import json
import re
import time
from datetime import datetime
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

UA = {"User-Agent": "CodexLiteratureSweep/1.0 (mailto:codex@example.com)"}


QUERIES = [
    "robot skill aging",
    "robot policy drift",
    "robot continual learning manipulation",
    "robot adaptation drift",
    "robot skill retention",
    "robot lifelong learning manipulation",
    "robot self calibration manipulation",
    "robot fault recovery manipulation",
    "robot domain shift manipulation",
    "robot sim to real adaptation",
    "policy drift robotics",
    "continual robot learning",
    "robot concept drift",
    "robot maintenance learning",
    "robot skill decay",
    "robot adaptability physical drift",
    "robot online adaptation manipulation",
    "robot forgetting continual learning",
    "robot calibration drift",
    "robot robustness manipulation",
    "robotics drift detection",
    "embodied agent adaptation",
    "dexterous manipulation adaptation",
    "world model robot adaptation",
    "robot skill evaluation",
]


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()


def safe_year(item):
    for key in ("published-print", "published-online", "created", "issued"):
        parts = item.get(key, {}).get("date-parts")
        if parts and parts[0]:
            return parts[0][0]
    return ""


def fetch_crossref(query, rows=50, offset=0):
    url = "https://api.crossref.org/works"
    params = {"query": query, "rows": rows, "offset": offset}
    r = requests.get(url, params=params, headers=UA, timeout=30)
    r.raise_for_status()
    return r.json()["message"]["items"]


def fetch_arxiv(query, start=0, max_results=50):
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": query, "start": start, "max_results": max_results, "sortBy": "relevance"}
    r = requests.get(url, params=params, headers=UA, timeout=30)
    r.raise_for_status()
    return r.text


def parse_arxiv(xml_text):
    import xml.etree.ElementTree as ET

    root = ET.fromstring(xml_text)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for entry in root.findall("a:entry", ns):
        title = norm(entry.findtext("a:title", default="", namespaces=ns))
        authors = [a.findtext("a:name", default="", namespaces=ns) for a in entry.findall("a:author", ns)]
        published = entry.findtext("a:published", default="", namespaces=ns)
        doi = ""
        for link in entry.findall("a:link", ns):
            if link.attrib.get("title") == "doi":
                doi = link.attrib.get("href", "")
        out.append(
            {
                "title": title,
                "authors": "; ".join(authors),
                "year": published[:4] if published else "",
                "doi": doi,
                "venue": "arXiv",
                "source": "arxiv",
                "url": entry.findtext("a:id", default="", namespaces=ns),
            }
        )
    return out


def main():
    records = []
    seen = set()

    for qi, q in enumerate(QUERIES, 1):
        for offset in (0, 50):
            try:
                items = fetch_crossref(q, rows=50, offset=offset)
            except Exception as e:
                items = []
            for item in items:
                title = norm((item.get("title") or [""])[0])
                if not title:
                    continue
                key = title
                if key in seen:
                    continue
                seen.add(key)
                records.append(
                    {
                        "source": "crossref",
                        "query": q,
                        "title": title,
                        "authors": "; ".join(a.get("family", "") for a in item.get("author", [])[:6]),
                        "year": safe_year(item),
                        "doi": item.get("DOI", ""),
                        "venue": (item.get("container-title") or [""])[0],
                        "url": item.get("URL", ""),
                    }
                )
            time.sleep(0.2)

    arxiv_queries = [
        "all:robot AND all:adaptation",
        "all:continual AND all:robot",
        "all:manipulation AND all:drift",
        "all:policy AND all:drift AND all:robot",
        "all:skill AND all:robot AND all:learning",
    ]
    for q in arxiv_queries:
        try:
            xml = fetch_arxiv(q, start=0, max_results=100)
            items = parse_arxiv(xml)
        except Exception:
            items = []
        for item in items:
            if item["title"] in seen:
                continue
            seen.add(item["title"])
            records.append(item)

    # Rank by keyword overlap with the seed topic.
    keywords = [
        "robot",
        "skill",
        "policy",
        "drift",
        "adapt",
        "continual",
        "lifelong",
        "manipulation",
        "calibration",
        "maintenance",
        "forget",
        "self",
        "recovery",
        "sim",
        "real",
        "world model",
        "embodied",
    ]
    for r in records:
        txt = " ".join([r.get("title", ""), r.get("venue", ""), r.get("query", "")])
        score = sum(1 for k in keywords if k in txt)
        r["relevance_score"] = score
        r["notes"] = ""

    def sortable_year(record):
        try:
            return int(record.get("year") or 0)
        except (TypeError, ValueError):
            return 0

    records.sort(key=lambda r: (-r["relevance_score"], sortable_year(r), r.get("title", "")))

    out = DOCS / "related_work_matrix.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["source", "query", "title", "authors", "year", "doi", "venue", "url", "relevance_score", "notes"],
        )
        writer.writeheader()
        for r in records[:1200]:
            writer.writerow(r)

    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "count": min(len(records), 1200),
        "queries": len(QUERIES),
        "hash": hashlib.sha256(out.read_bytes()).hexdigest()[:12],
    }
    (DOCS / "sweep_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
