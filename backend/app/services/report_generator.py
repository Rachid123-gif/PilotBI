"""
AI-powered report generation using Anthropic Claude.

Generates structured monthly business reports in French for Moroccan SMEs.
"""

from __future__ import annotations

import json
import logging
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

import anthropic
from supabase import Client

from app.config import get_settings
from app.models.enums import KpiType, PeriodType
from app.services.kpi_calculator import calculate_all_kpis

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """Tu es un analyste business intelligence expert pour les PME marocaines.
Tu produis des rapports mensuels professionnels, clairs et actionnables.

Consignes :
- Rédige en français professionnel, adapté au contexte business marocain.
- Utilise le dirham marocain (MAD) comme unité monétaire.
- Structure le rapport en sections claires avec des titres.
- Fournis des analyses chiffrées et des recommandations concrètes.
- Identifie les tendances, anomalies et opportunités.
- Reste factuel et base tes analyses uniquement sur les données fournies.
- Format de sortie : JSON avec un tableau "sections", chaque section ayant "title" et "content".

Exemple de structure de sections :
1. Résumé Exécutif
2. Performance Commerciale
3. Analyse des Clients
4. Analyse des Produits/Services
5. Tendances et Anomalies
6. Recommandations
"""


def _build_user_prompt(org_name: str, period: str, kpis: list, row_sample: list) -> str:
    """Build the user prompt with context data."""
    kpi_text = ""
    for kpi in kpis:
        trend = ""
        if kpi.change_pct is not None:
            direction = "hausse" if kpi.change_pct > 0 else "baisse"
            trend = f" ({direction} de {abs(kpi.change_pct)}% vs période précédente)"
        kpi_text += f"- {kpi.label}: {kpi.value:,.2f} {kpi.unit}{trend}\n"

    sample_text = ""
    if row_sample:
        sample_text = "Échantillon de données (5 premières lignes) :\n"
        for i, row in enumerate(row_sample[:5], 1):
            sample_text += f"  Ligne {i}: {json.dumps(row, ensure_ascii=False, default=str)}\n"

    return f"""Génère un rapport mensuel pour l'entreprise "{org_name}" pour la période {period}.

KPIs du mois :
{kpi_text}

{sample_text}

Produis un rapport structuré en JSON avec le format :
{{
  "sections": [
    {{"title": "Titre de la section", "content": "Contenu détaillé de la section"}}
  ]
}}
"""


async def generate_monthly_report(
    db: Client,
    org_id: str,
    period: str,
    language: str = "fr",
) -> Dict[str, Any]:
    """
    Generate a monthly business report using Claude.

    Parameters
    ----------
    db : Client
        Supabase client.
    org_id : str
        Organization ID.
    period : str
        Period string (e.g. "2025-03").
    language : str
        Report language (default: "fr").

    Returns
    -------
    dict
        The created report record.
    """
    settings = get_settings()

    # Fetch organization info
    org_result = db.table("organizations").select("name").eq("id", org_id).single().execute()
    org_name = org_result.data.get("name", "Entreprise")

    # Calculate KPIs for the period
    # Parse period into date range
    try:
        year, month = period.split("-")
        start_date = f"{year}-{month}-01"
        if int(month) == 12:
            end_date = f"{int(year) + 1}-01-01"
        else:
            end_date = f"{year}-{int(month) + 1:02d}-01"
    except (ValueError, IndexError):
        start_date = None
        end_date = None

    kpis = calculate_all_kpis(db, org_id, PeriodType.MONTHLY, start_date, end_date)

    # Fetch a sample of rows for context
    rows_result = (
        db.table("data_rows")
        .select("row_data")
        .eq("organization_id", org_id)
        .limit(5)
        .execute()
    )
    row_sample = [r.get("row_data", {}) for r in (rows_result.data or [])]

    # Build prompts
    user_prompt = _build_user_prompt(org_name, period, kpis, row_sample)

    # Call Claude API
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
    )

    # Parse response
    response_text = message.content[0].text
    sections = _parse_report_response(response_text)

    # Store report
    report_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    report_data = {
        "id": report_id,
        "organization_id": org_id,
        "title": f"Rapport Mensuel - {period}",
        "period": period,
        "sections": sections,
        "generated_at": now,
        "created_at": now,
        "language": language,
        "model_used": "claude-sonnet-4-20250514",
        "token_usage": {
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
        },
    }

    db.table("reports").insert(report_data).execute()
    logger.info("Report %s generated for org %s, period %s", report_id, org_id, period)

    return report_data


def _parse_report_response(text: str) -> List[Dict[str, Any]]:
    """
    Parse the Claude response into structured sections.

    Tries JSON parsing first, then falls back to regex extraction.
    """
    # Try to extract JSON from the response
    json_match = re.search(r"\{[\s\S]*\"sections\"[\s\S]*\}", text)
    if json_match:
        try:
            parsed = json.loads(json_match.group())
            raw_sections = parsed.get("sections", [])
            return [
                {
                    "title": s.get("title", f"Section {i + 1}"),
                    "content": s.get("content", ""),
                    "order": i,
                }
                for i, s in enumerate(raw_sections)
            ]
        except json.JSONDecodeError:
            pass

    # Fallback: split by markdown-style headers
    sections: List[Dict[str, Any]] = []
    current_title = "Rapport"
    current_content: list[str] = []
    order = 0

    for line in text.split("\n"):
        header_match = re.match(r"^#{1,3}\s+(.+)$", line.strip())
        if header_match:
            if current_content:
                sections.append({
                    "title": current_title,
                    "content": "\n".join(current_content).strip(),
                    "order": order,
                })
                order += 1
            current_title = header_match.group(1).strip()
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        sections.append({
            "title": current_title,
            "content": "\n".join(current_content).strip(),
            "order": order,
        })

    return sections if sections else [{"title": "Rapport", "content": text, "order": 0}]
