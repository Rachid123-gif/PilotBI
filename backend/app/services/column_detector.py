"""
Heuristic column detection for French business data.

Maps original column names to standardized KPI field names using
fuzzy matching against a dictionary of French business terms.
"""

from __future__ import annotations

import logging
import re
import unicodedata
from typing import Dict

import pandas as pd

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# French business term -> standardized field name
# ---------------------------------------------------------------------------
COLUMN_DICTIONARY: Dict[str, str] = {
    # Revenue
    "ca": "revenue",
    "chiffre d'affaires": "revenue",
    "chiffre d affaires": "revenue",
    "chiffre_affaires": "revenue",
    "montant ht": "revenue",
    "montant_ht": "revenue",
    "montant hors taxe": "revenue",
    "total ht": "revenue",
    "total_ht": "revenue",
    "ventes": "revenue",
    "vente": "revenue",
    "revenue": "revenue",
    "revenu": "revenue",
    "recette": "revenue",
    "recettes": "revenue",
    # Montant TTC
    "montant ttc": "amount_ttc",
    "montant_ttc": "amount_ttc",
    "total ttc": "amount_ttc",
    "total_ttc": "amount_ttc",
    # Prix unitaire
    "prix": "unit_price",
    "prix unitaire": "unit_price",
    "prix_unitaire": "unit_price",
    "pu": "unit_price",
    "tarif": "unit_price",
    # Quantite
    "quantite": "quantity",
    "quantit\u00e9": "quantity",
    "qte": "quantity",
    "qt\u00e9": "quantity",
    "nombre": "quantity",
    "nb": "quantity",
    "volume": "quantity",
    # Client
    "client": "client_name",
    "nom client": "client_name",
    "nom_client": "client_name",
    "raison sociale": "client_name",
    "societe": "client_name",
    "soci\u00e9t\u00e9": "client_name",
    "entreprise": "client_name",
    # Produit
    "produit": "product_name",
    "nom produit": "product_name",
    "nom_produit": "product_name",
    "article": "product_name",
    "designation": "product_name",
    "d\u00e9signation": "product_name",
    "libelle": "product_name",
    "libell\u00e9": "product_name",
    # Categorie
    "categorie": "category",
    "cat\u00e9gorie": "category",
    "famille": "category",
    "type": "category",
    "gamme": "category",
    # Region
    "region": "region",
    "r\u00e9gion": "region",
    "ville": "region",
    "zone": "region",
    "secteur": "region",
    # Commercial
    "commercial": "sales_rep",
    "vendeur": "sales_rep",
    "representant": "sales_rep",
    "repr\u00e9sentant": "sales_rep",
    "agent": "sales_rep",
    # Cout
    "cout": "cost",
    "co\u00fbt": "cost",
    "cout achat": "cost",
    "prix achat": "cost",
    "prix_achat": "cost",
    "charge": "cost",
    "charges": "cost",
    "depense": "cost",
    "d\u00e9pense": "cost",
    "depenses": "cost",
    # Marge
    "marge": "margin",
    "marge brute": "margin",
    "marge_brute": "margin",
    "benefice": "margin",
    "b\u00e9n\u00e9fice": "margin",
    "profit": "margin",
    # Stock
    "stock": "stock_level",
    "stock actuel": "stock_level",
    "quantite stock": "stock_level",
    "inventaire": "stock_level",
    # Date
    "date": "date",
    "date facture": "date",
    "date_facture": "date",
    "date commande": "date",
    "date_commande": "date",
    "date vente": "date",
    "date_vente": "date",
    "jour": "date",
    "mois": "date",
    "periode": "date",
    "p\u00e9riode": "date",
    # Facture
    "facture": "invoice_id",
    "numero facture": "invoice_id",
    "num facture": "invoice_id",
    "n facture": "invoice_id",
    "num\u00e9ro facture": "invoice_id",
    "reference": "invoice_id",
    "r\u00e9f\u00e9rence": "invoice_id",
    "ref": "invoice_id",
}


def _normalize(text: str) -> str:
    """Normalize text: lowercase, strip accents, remove special chars."""
    text = text.lower().strip()
    # Remove accents
    nfkd = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in nfkd if not unicodedata.combining(c))
    # Replace underscores and hyphens with spaces
    text = re.sub(r"[_\-]+", " ", text)
    # Remove non-alphanumeric (keep spaces)
    text = re.sub(r"[^a-z0-9 ]", "", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def detect_columns(df: pd.DataFrame) -> Dict[str, str]:
    """
    Detect and map DataFrame columns to standardized KPI field names.

    Uses a multi-pass strategy:
    1. Exact match (normalized)
    2. Contains match (column name contains a dictionary key)
    3. Reverse contains (dictionary key contains column name)

    Returns a dict mapping original column names to standardized field names.
    Only columns with a confident match are included.
    """
    result: Dict[str, str] = {}
    used_targets: set[str] = set()

    # Pre-normalize the dictionary
    normalized_dict: Dict[str, str] = {}
    for key, value in COLUMN_DICTIONARY.items():
        nk = _normalize(key)
        if nk:
            normalized_dict[nk] = value

    for col in df.columns:
        col_norm = _normalize(str(col))
        if not col_norm:
            continue

        matched_target: str | None = None

        # Pass 1: Exact match
        if col_norm in normalized_dict:
            matched_target = normalized_dict[col_norm]

        # Pass 2: Column name contains a dictionary key (prefer longer keys)
        if not matched_target:
            best_key = ""
            for dk, dv in normalized_dict.items():
                if dk in col_norm and len(dk) > len(best_key):
                    best_key = dk
                    matched_target = dv

        # Pass 3: Dictionary key contains column name (only for short column names >= 2 chars)
        if not matched_target and len(col_norm) >= 2:
            for dk, dv in normalized_dict.items():
                if col_norm in dk:
                    matched_target = dv
                    break

        if matched_target and matched_target not in used_targets:
            result[col] = matched_target
            used_targets.add(matched_target)
            logger.debug("Mapped column '%s' -> '%s'", col, matched_target)

    logger.info("Detected %d/%d columns: %s", len(result), len(df.columns), result)
    return result
