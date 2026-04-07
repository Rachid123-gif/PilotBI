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
    "montant achat": "revenue",
    "montant_achat": "revenue",
    "montant achats": "revenue",
    "montant": "revenue",
    "total achat": "revenue",
    "total achats": "revenue",
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
    "nom client": "client_name",
    "nom_client": "client_name",
    "client": "client_name",
    "id client": "client_id",
    "id_client": "client_id",
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
    "nombre commandes": "order_count_raw",
    "nombre_commandes": "order_count_raw",
    "nb commandes": "order_count_raw",
    "commandes": "order_count_raw",
    "facture": "invoice_id",
    "numero facture": "invoice_id",
    "num facture": "invoice_id",
    "n facture": "invoice_id",
    "num\u00e9ro facture": "invoice_id",
    "reference": "invoice_id",
    "r\u00e9f\u00e9rence": "invoice_id",
    "ref": "invoice_id",

    # ── Transport & Logistique ──
    "km": "distance",
    "kilometrage": "distance",
    "kilom\u00e9trage": "distance",
    "distance": "distance",
    "carburant": "fuel",
    "gasoil": "fuel",
    "essence": "fuel",
    "consommation": "fuel",
    "litres": "fuel",
    "vehicule": "vehicle_id",
    "v\u00e9hicule": "vehicle_id",
    "camion": "vehicle_id",
    "immatriculation": "vehicle_id",
    "chauffeur": "driver",
    "conducteur": "driver",
    "livraison": "delivery_id",
    "bon livraison": "delivery_id",
    "bl": "delivery_id",

    # ── Restaurant & F&B ──
    "plat": "dish_name",
    "menu": "dish_name",
    "recette": "dish_name",
    "couvert": "covers",
    "couverts": "covers",
    "nb couverts": "covers",
    "table": "table_id",
    "service": "service_type",
    "midi": "service_type",
    "soir": "service_type",

    # ── Hotel & Riads ──
    "chambre": "room_id",
    "num chambre": "room_id",
    "type chambre": "room_type",
    "nuitee": "nights",
    "nuit\u00e9e": "nights",
    "nuits": "nights",
    "tarif chambre": "room_rate",
    "prix chambre": "room_rate",
    "reservation": "booking_id",
    "r\u00e9servation": "booking_id",
    "check in": "checkin_date",
    "check-in": "checkin_date",
    "arrivee": "checkin_date",
    "arriv\u00e9e": "checkin_date",
    "check out": "checkout_date",
    "depart": "checkout_date",
    "d\u00e9part": "checkout_date",

    # ── Clinique & Sante ──
    "patient": "patient_name",
    "nom patient": "patient_name",
    "medecin": "doctor_name",
    "m\u00e9decin": "doctor_name",
    "docteur": "doctor_name",
    "dr": "doctor_name",
    "acte": "procedure_name",
    "prestation": "procedure_name",
    "soin": "procedure_name",
    "specialite": "specialty",
    "sp\u00e9cialit\u00e9": "specialty",
    "diagnostic": "diagnosis",

    # ── Pharmacie ──
    "ordonnance": "prescription_id",
    "num ordonnance": "prescription_id",
    "medicament": "product_name",
    "m\u00e9dicament": "product_name",
    "dci": "molecule",
    "molecule": "molecule",
    "mol\u00e9cule": "molecule",
    "officine": "store_id",
    "pharmacie": "store_id",

    # ── Immobilier ──
    "lot": "unit_id",
    "appartement": "unit_id",
    "bien": "unit_id",
    "superficie": "area_sqm",
    "surface": "area_sqm",
    "m2": "area_sqm",
    "projet": "project_name",
    "programme": "project_name",
    "acquereur": "buyer_name",
    "acqu\u00e9reur": "buyer_name",
    "acheteur": "buyer_name",
    "etage": "floor",
    "\u00e9tage": "floor",

    # ── Agriculture ──
    "parcelle": "plot_id",
    "champ": "plot_id",
    "culture": "crop_name",
    "produit agricole": "crop_name",
    "recolte": "harvest",
    "r\u00e9colte": "harvest",
    "rendement": "harvest",
    "hectare": "area_ha",
    "ha": "area_ha",
    "superficie ha": "area_ha",
    "irrigation": "irrigation_type",

    # ── E-commerce ──
    "canal": "channel",
    "source": "channel",
    "plateforme": "channel",
    "panier": "cart_id",
    "commande en ligne": "order_id",
    "code promo": "promo_code",
    "coupon": "promo_code",
    "avis": "review_score",
    "note client": "review_score",

    # ── Multi-secteur (points de vente) ──
    "succursale": "store_id",
    "filiale": "store_id",
    "agence": "store_id",
    "point de vente": "store_id",
    "pdv": "store_id",
    "magasin": "store_id",
    "boutique": "store_id",
    "site": "store_id",

    # ── Services B2B ──
    "heures": "hours",
    "heures facturees": "billable_hours",
    "heures factur\u00e9es": "billable_hours",
    "temps passe": "hours",
    "temps pass\u00e9": "hours",
    "contrat": "contract_id",
    "mission": "project_name",
    "dossier": "project_name",
    "montant encaisse": "amount_collected",
    "montant encaiss\u00e9": "amount_collected",
    "encaissement": "amount_collected",
    "montant facture": "amount_invoiced",
    "montant factur\u00e9": "amount_invoiced",
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
