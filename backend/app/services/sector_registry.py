"""
Sector registry — central configuration for all 12 industry verticals.

Each sector defines: KPI types, chart layout, default alerts,
AI report prompt, and Moroccan market benchmarks.
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Sector definitions
# ---------------------------------------------------------------------------

SECTORS: dict[str, dict[str, Any]] = {
    # ══════════════════════════════════════
    # 1. DISTRIBUTION & COMMERCE DE GROS
    # ══════════════════════════════════════
    "distribution": {
        "label": "Distribution & Commerce de Gros",
        "icon": "truck",
        "description": "Grossistes, distributeurs FMCG, importateurs",
        "kpis": [
            "revenue", "margin", "client_count", "stock_level",
            "receivables", "revenue_per_rep", "stock_rotation", "return_rate",
        ],
        "primary_kpis": ["revenue", "margin", "receivables", "stock_level", "revenue_per_rep", "return_rate"],
        "charts": [
            {"kpi": "revenue", "type": "bar", "title": "Evolution du CA"},
            {"kpi": "revenue_per_rep", "type": "pie", "title": "CA par commercial"},
            {"kpi": "margin", "type": "line", "title": "Evolution de la marge"},
        ],
        "rankings": [
            {"field": "product_name", "metric": "margin", "title": "Top produits par marge", "order": "desc"},
            {"field": "client_name", "metric": "revenue", "title": "Top clients par CA", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Stock critique", "kpi_type": "stock_level", "condition": "below", "threshold": 10},
            {"name": "Creances elevees", "kpi_type": "receivables", "condition": "above", "threshold": 100000},
            {"name": "Baisse CA mensuel", "kpi_type": "revenue", "condition": "change_pct", "threshold": -15},
        ],
        "ai_prompt": (
            "Tu es un expert en distribution et commerce de gros au Maroc. "
            "Analyse les donnees de ce distributeur marocain. "
            "Focus : marges par reference, rotation stock, concentration clients, "
            "performance des commerciaux, creances et delais de paiement. "
            "Benchmarks secteur Maroc : marge brute 15-25%, rotation stock saine 8-12x/an, "
            "concentration client top 3 < 30% du CA. "
            "Recommandations : negociation fournisseurs, politique de recouvrement, "
            "optimisation tournees commerciales, gestion des references a faible rotation."
        ),
        "benchmarks": {
            "margin_pct": {"low": 10, "avg": 18, "high": 25, "unit": "%", "label": "Marge brute"},
            "stock_rotation": {"low": 4, "avg": 8, "high": 12, "unit": "x/an", "label": "Rotation stock"},
            "client_concentration_top3": {"healthy": 30, "warning": 50, "unit": "%", "label": "Concentration top 3"},
        },
    },

    # ══════════════════════════════════════
    # 2. RETAIL MULTI-POINTS
    # ══════════════════════════════════════
    "retail": {
        "label": "Retail & Chaines de Magasins",
        "icon": "store",
        "description": "Chaines de magasins, franchises, points de vente multiples",
        "kpis": [
            "revenue", "revenue_per_store", "avg_order_value", "client_count",
            "stock_level", "order_count", "conversion_rate",
        ],
        "primary_kpis": ["revenue", "revenue_per_store", "avg_order_value", "stock_level", "order_count", "conversion_rate"],
        "charts": [
            {"kpi": "revenue_per_store", "type": "comparison", "title": "CA par magasin"},
            {"kpi": "avg_order_value", "type": "line", "title": "Evolution du panier moyen"},
            {"kpi": "revenue", "type": "heatmap", "title": "Performance par magasin/semaine"},
        ],
        "rankings": [
            {"field": "store_id", "metric": "revenue", "title": "Classement magasins par CA", "order": "desc"},
            {"field": "product_name", "metric": "quantity", "title": "Top produits vendus", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "CA magasin en baisse", "kpi_type": "revenue_per_store", "condition": "change_pct", "threshold": -15},
            {"name": "Stock bas", "kpi_type": "stock_level", "condition": "below", "threshold": 5},
        ],
        "ai_prompt": (
            "Tu es un expert en retail et commerce de detail au Maroc. "
            "Analyse les donnees de cette chaine de magasins marocaine. "
            "Focus : performance comparee des points de vente, panier moyen, "
            "produits best-sellers vs flops, saisonnalite, gestion du stock multi-sites. "
            "Benchmarks Maroc : panier moyen pret-a-porter 250-500 MAD, "
            "taux de conversion magasin 15-25%, CA/m2 cible 800-1500 MAD. "
            "Recommandations : merchandising, politique promotionnelle, "
            "reequilibrage stock entre magasins, fermeture/ouverture de points de vente."
        ),
        "benchmarks": {
            "avg_basket": {"low": 150, "avg": 350, "high": 600, "unit": "MAD", "label": "Panier moyen"},
            "conversion_rate": {"low": 10, "avg": 20, "high": 30, "unit": "%", "label": "Taux conversion"},
        },
    },

    # ══════════════════════════════════════
    # 3. INDUSTRIE PME
    # ══════════════════════════════════════
    "industrie": {
        "label": "Industrie & Fabrication",
        "icon": "factory",
        "description": "Usines textile, agroalimentaire, plasturgie, BTP",
        "kpis": [
            "revenue", "margin", "production_cost", "yield_rate",
            "defect_rate", "on_time_delivery", "order_count", "stock_level",
        ],
        "primary_kpis": ["revenue", "margin", "production_cost", "defect_rate", "yield_rate", "on_time_delivery"],
        "charts": [
            {"kpi": "revenue", "type": "bar", "title": "CA mensuel"},
            {"kpi": "production_cost", "type": "line", "title": "Evolution cout de production"},
            {"kpi": "defect_rate", "type": "gauge", "title": "Taux de rebut"},
        ],
        "rankings": [
            {"field": "product_name", "metric": "margin", "title": "Produits par marge", "order": "desc"},
            {"field": "product_name", "metric": "defect_rate", "title": "Produits par taux de rebut", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Taux de rebut anormal", "kpi_type": "defect_rate", "condition": "above", "threshold": 5},
            {"name": "Retard commandes", "kpi_type": "on_time_delivery", "condition": "below", "threshold": 85},
        ],
        "ai_prompt": (
            "Tu es un expert en industrie manufacturiere au Maroc. "
            "Analyse les donnees de cette usine/PME industrielle marocaine. "
            "Focus : cout de production unitaire, rendement, taux de rebut, "
            "delai de livraison, marge par produit. "
            "Benchmarks Maroc : taux de rebut cible < 3%, "
            "OTD (On-Time Delivery) > 90%, marge industrielle 20-35%. "
            "Recommandations : optimisation chaine production, reduction gaspillage, "
            "maintenance preventive, negociation matieres premieres."
        ),
        "benchmarks": {
            "defect_rate": {"low": 1, "avg": 3, "high": 5, "unit": "%", "label": "Taux de rebut"},
            "on_time_delivery": {"low": 80, "avg": 90, "high": 97, "unit": "%", "label": "Livraison a temps"},
            "margin_pct": {"low": 15, "avg": 25, "high": 35, "unit": "%", "label": "Marge industrielle"},
        },
    },

    # ══════════════════════════════════════
    # 4. TRANSPORT & LOGISTIQUE
    # ══════════════════════════════════════
    "transport": {
        "label": "Transport & Logistique",
        "icon": "truck",
        "description": "Flottes de camions, transitaires, messagerie express",
        "kpis": [
            "revenue", "cost_per_km", "fill_rate", "fuel_consumption",
            "deliveries_count", "margin", "order_count",
        ],
        "primary_kpis": ["revenue", "cost_per_km", "fill_rate", "fuel_consumption", "deliveries_count", "margin"],
        "charts": [
            {"kpi": "revenue", "type": "bar", "title": "CA mensuel"},
            {"kpi": "cost_per_km", "type": "line", "title": "Cout au km"},
            {"kpi": "fill_rate", "type": "gauge", "title": "Taux de remplissage"},
        ],
        "rankings": [
            {"field": "vehicle_id", "metric": "revenue", "title": "CA par vehicule", "order": "desc"},
            {"field": "driver", "metric": "deliveries_count", "title": "Livraisons par chauffeur", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Cout/km eleve", "kpi_type": "cost_per_km", "condition": "above", "threshold": 8},
            {"name": "Remplissage faible", "kpi_type": "fill_rate", "condition": "below", "threshold": 60},
        ],
        "ai_prompt": (
            "Tu es un expert en transport et logistique au Maroc. "
            "Analyse les donnees de cette entreprise de transport marocaine. "
            "Focus : cout par km, taux de remplissage, consommation carburant, "
            "rentabilite par vehicule/chauffeur, delais de livraison. "
            "Benchmarks Maroc : cout/km poids lourd 5-7 MAD, "
            "taux remplissage cible > 75%, consommation gasoil 30-35L/100km. "
            "Recommandations : optimisation tournees, maintenance preventive, "
            "negociation carburant, formation eco-conduite."
        ),
        "benchmarks": {
            "cost_per_km": {"low": 4, "avg": 6, "high": 8, "unit": "MAD", "label": "Cout par km"},
            "fill_rate": {"low": 55, "avg": 70, "high": 85, "unit": "%", "label": "Taux remplissage"},
        },
    },

    # ══════════════════════════════════════
    # 5. RESTAURANTS & F&B
    # ══════════════════════════════════════
    "restaurant": {
        "label": "Restaurants & F&B",
        "icon": "utensils",
        "description": "Restaurants, chaines fast-food, dark kitchens, traiteurs",
        "kpis": [
            "revenue", "food_cost_pct", "avg_order_value", "order_count",
            "dishes_sold", "waste_rate", "margin",
        ],
        "primary_kpis": ["revenue", "food_cost_pct", "avg_order_value", "order_count", "dishes_sold", "waste_rate"],
        "charts": [
            {"kpi": "revenue", "type": "heatmap", "title": "CA par jour de semaine"},
            {"kpi": "food_cost_pct", "type": "gauge", "title": "Food Cost"},
            {"kpi": "dishes_sold", "type": "bar", "title": "Top plats vendus"},
        ],
        "rankings": [
            {"field": "product_name", "metric": "margin", "title": "Plats par rentabilite", "order": "desc"},
            {"field": "product_name", "metric": "quantity", "title": "Plats les plus vendus", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Food cost trop eleve", "kpi_type": "food_cost_pct", "condition": "above", "threshold": 35},
            {"name": "Baisse ticket moyen", "kpi_type": "avg_order_value", "condition": "change_pct", "threshold": -10},
        ],
        "ai_prompt": (
            "Tu es un expert en restauration et F&B au Maroc. "
            "Analyse les donnees de cette chaine de restaurants marocaine. "
            "Focus : food cost par plat, ticket moyen par service, "
            "performance par jour de semaine, saisonnalite, gaspillage. "
            "Benchmarks Maroc : food cost ideal 28-32%, "
            "ticket moyen fast-casual 80-120 MAD, ratio personnel/CA < 30%. "
            "Recommandations : ingenierie du menu (retirer plats non rentables), "
            "optimisation des horaires, reduction gaspillage, promotions ciblees."
        ),
        "benchmarks": {
            "food_cost_pct": {"low": 25, "avg": 30, "high": 35, "unit": "%", "label": "Food cost"},
            "avg_ticket": {"low": 60, "avg": 100, "high": 180, "unit": "MAD", "label": "Ticket moyen"},
        },
    },

    # ══════════════════════════════════════
    # 6. E-COMMERCE
    # ══════════════════════════════════════
    "ecommerce": {
        "label": "E-commerce",
        "icon": "shopping-cart",
        "description": "Vente en ligne, Instagram, Shopify, Jumia",
        "kpis": [
            "revenue", "order_count", "avg_order_value", "client_count",
            "conversion_rate", "cac", "return_rate_ecom", "revenue_per_channel",
        ],
        "primary_kpis": ["revenue", "order_count", "avg_order_value", "conversion_rate", "cac", "return_rate_ecom"],
        "charts": [
            {"kpi": "revenue", "type": "line", "title": "Evolution du CA"},
            {"kpi": "revenue_per_channel", "type": "pie", "title": "CA par canal"},
            {"kpi": "order_count", "type": "bar", "title": "Commandes par mois"},
        ],
        "rankings": [
            {"field": "product_name", "metric": "revenue", "title": "Top produits par CA", "order": "desc"},
            {"field": "channel", "metric": "revenue", "title": "Performance par canal", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Taux retour eleve", "kpi_type": "return_rate_ecom", "condition": "above", "threshold": 10},
            {"name": "Baisse conversions", "kpi_type": "conversion_rate", "condition": "change_pct", "threshold": -20},
        ],
        "ai_prompt": (
            "Tu es un expert en e-commerce au Maroc. "
            "Analyse les donnees de ce vendeur en ligne marocain. "
            "Focus : taux de conversion, cout d'acquisition client, "
            "panier moyen, taux de retour, performance par canal. "
            "Benchmarks Maroc : taux conversion e-commerce 1-3%, "
            "panier moyen 150-300 MAD, taux de retour < 8%. "
            "Recommandations : optimisation fiches produits, strategie de prix, "
            "retargeting, amelioration logistique livraison."
        ),
        "benchmarks": {
            "conversion_rate": {"low": 1, "avg": 2.5, "high": 5, "unit": "%", "label": "Taux conversion"},
            "return_rate": {"low": 3, "avg": 6, "high": 10, "unit": "%", "label": "Taux retour"},
        },
    },

    # ══════════════════════════════════════
    # 7. CLINIQUES PRIVEES
    # ══════════════════════════════════════
    "clinique": {
        "label": "Cliniques & Sante",
        "icon": "heart-pulse",
        "description": "Cliniques, laboratoires, cabinets dentaires",
        "kpis": [
            "revenue", "revenue_per_doctor", "patient_count", "occupancy_rate",
            "receivables", "margin", "order_count",
        ],
        "primary_kpis": ["revenue", "revenue_per_doctor", "patient_count", "occupancy_rate", "receivables", "margin"],
        "charts": [
            {"kpi": "revenue", "type": "bar", "title": "CA mensuel"},
            {"kpi": "revenue_per_doctor", "type": "comparison", "title": "CA par medecin"},
            {"kpi": "occupancy_rate", "type": "gauge", "title": "Taux d'occupation"},
        ],
        "rankings": [
            {"field": "doctor_name", "metric": "revenue", "title": "CA par medecin", "order": "desc"},
            {"field": "specialty", "metric": "patient_count", "title": "Patients par specialite", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Creances patients elevees", "kpi_type": "receivables", "condition": "above", "threshold": 50000},
            {"name": "Occupation faible", "kpi_type": "occupancy_rate", "condition": "below", "threshold": 60},
        ],
        "ai_prompt": (
            "Tu es un expert en gestion de cliniques privees au Maroc. "
            "Analyse les donnees de cet etablissement de sante marocain. "
            "Focus : CA par medecin/specialite, taux d'occupation des lits/salles, "
            "nombre de patients, creances patients, rentabilite par acte. "
            "Benchmarks Maroc : taux occupation clinique 60-80%, "
            "delai recouvrement < 45 jours, ratio personnel/lit optimal. "
            "Recommandations : optimisation planning medecins, "
            "politique de recouvrement, developpement specialites rentables."
        ),
        "benchmarks": {
            "occupancy_rate": {"low": 50, "avg": 65, "high": 80, "unit": "%", "label": "Taux occupation"},
        },
    },

    # ══════════════════════════════════════
    # 8. PHARMACIES EN CHAINE
    # ══════════════════════════════════════
    "pharmacie": {
        "label": "Pharmacies & Parapharmacies",
        "icon": "pill",
        "description": "Groupements de pharmacies, parapharmacies",
        "kpis": [
            "revenue", "revenue_per_store", "margin", "stock_level",
            "prescriptions_per_day", "critical_stock", "order_count",
        ],
        "primary_kpis": ["revenue", "revenue_per_store", "margin", "critical_stock", "prescriptions_per_day", "stock_level"],
        "charts": [
            {"kpi": "revenue_per_store", "type": "comparison", "title": "CA par officine"},
            {"kpi": "margin", "type": "pie", "title": "Marge par categorie"},
            {"kpi": "revenue", "type": "line", "title": "Evolution du CA"},
        ],
        "rankings": [
            {"field": "store_id", "metric": "revenue", "title": "Officines par CA", "order": "desc"},
            {"field": "category", "metric": "margin", "title": "Categories par marge", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Stock critique medicament", "kpi_type": "critical_stock", "condition": "above", "threshold": 5},
            {"name": "Baisse CA officine", "kpi_type": "revenue_per_store", "condition": "change_pct", "threshold": -10},
        ],
        "ai_prompt": (
            "Tu es un expert en gestion de pharmacies au Maroc. "
            "Analyse les donnees de ce groupement de pharmacies marocain. "
            "Focus : CA par officine, marge par categorie (medicaments, parapharmacie, "
            "cosmetique), gestion des stocks critiques, ordonnances/jour. "
            "Benchmarks Maroc : marge pharmacie 20-30%, "
            "parapharmacie 35-50%, rotation stock medicaments 15-20x/an. "
            "Recommandations : equilibrage stock entre officines, "
            "developpement parapharmacie, gestion perimes."
        ),
        "benchmarks": {
            "margin_pct": {"low": 18, "avg": 25, "high": 35, "unit": "%", "label": "Marge globale"},
        },
    },

    # ══════════════════════════════════════
    # 9. IMMOBILIER
    # ══════════════════════════════════════
    "immobilier": {
        "label": "Immobilier & Promotion",
        "icon": "building",
        "description": "Promoteurs immobiliers, agences, lotisseurs",
        "kpis": [
            "revenue", "sales_count", "commercialization_rate", "price_per_sqm",
            "avg_sale_delay", "margin", "client_count",
        ],
        "primary_kpis": ["revenue", "sales_count", "commercialization_rate", "price_per_sqm", "avg_sale_delay", "margin"],
        "charts": [
            {"kpi": "revenue", "type": "bar", "title": "CA par projet"},
            {"kpi": "commercialization_rate", "type": "gauge", "title": "Taux de commercialisation"},
            {"kpi": "price_per_sqm", "type": "line", "title": "Prix au m2"},
        ],
        "rankings": [
            {"field": "project_name", "metric": "revenue", "title": "Projets par CA", "order": "desc"},
            {"field": "sales_rep", "metric": "sales_count", "title": "Commerciaux par ventes", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Commercialisation lente", "kpi_type": "commercialization_rate", "condition": "below", "threshold": 50},
        ],
        "ai_prompt": (
            "Tu es un expert en immobilier et promotion au Maroc. "
            "Analyse les donnees de ce promoteur/agence immobilier marocain. "
            "Focus : ventes par projet, taux de commercialisation, prix au m2, "
            "delai moyen de vente, performance des commerciaux. "
            "Benchmarks Maroc : prix m2 economique 8000-12000 MAD, "
            "moyen standing 14000-20000 MAD, haut standing 20000-35000 MAD. "
            "Recommandations : politique de prix, ciblage clientele, "
            "acceleration commercialisation lots restants."
        ),
        "benchmarks": {
            "commercialization_rate": {"low": 40, "avg": 65, "high": 85, "unit": "%", "label": "Taux commercialisation"},
        },
    },

    # ══════════════════════════════════════
    # 10. HOTELS & RIADS
    # ══════════════════════════════════════
    "hotel": {
        "label": "Hotels & Riads",
        "icon": "bed",
        "description": "Hotels, riads, maisons d'hotes, resorts",
        "kpis": [
            "revenue", "revpar", "occupancy_rate_hotel", "adr",
            "fb_revenue", "order_count", "client_count",
        ],
        "primary_kpis": ["revenue", "revpar", "occupancy_rate_hotel", "adr", "fb_revenue", "client_count"],
        "charts": [
            {"kpi": "occupancy_rate_hotel", "type": "line", "title": "Taux d'occupation mensuel"},
            {"kpi": "revenue", "type": "pie", "title": "CA Hebergement vs F&B"},
            {"kpi": "revpar", "type": "bar", "title": "RevPAR mensuel"},
        ],
        "rankings": [
            {"field": "room_type", "metric": "revenue", "title": "CA par type de chambre", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Occupation faible", "kpi_type": "occupancy_rate_hotel", "condition": "below", "threshold": 50},
            {"name": "RevPAR en baisse", "kpi_type": "revpar", "condition": "change_pct", "threshold": -15},
        ],
        "ai_prompt": (
            "Tu es un expert en hotellerie au Maroc. "
            "Analyse les donnees de cet hotel/riad marocain. "
            "Focus : RevPAR, taux d'occupation, ADR, revenue F&B, "
            "saisonnalite, performance par type de chambre. "
            "Benchmarks Maroc : taux occupation 55-65%, "
            "RevPAR 3 etoiles 300-500 MAD, ratio F&B/hebergement 25-35%. "
            "Recommandations : yield management, packages weekends, "
            "upselling chambres superieures, optimisation OTA vs direct."
        ),
        "benchmarks": {
            "occupancy_rate": {"low": 45, "avg": 60, "high": 75, "unit": "%", "label": "Taux occupation"},
            "revpar": {"low": 200, "avg": 400, "high": 700, "unit": "MAD", "label": "RevPAR"},
        },
    },

    # ══════════════════════════════════════
    # 11. SERVICES B2B
    # ══════════════════════════════════════
    "services": {
        "label": "Services & Prestations B2B",
        "icon": "briefcase",
        "description": "Cabinets conseil, agences, maintenance, nettoyage",
        "kpis": [
            "revenue", "margin", "client_count", "billable_hours",
            "collection_rate", "active_contracts", "margin_per_project",
        ],
        "primary_kpis": ["revenue", "margin", "collection_rate", "billable_hours", "active_contracts", "client_count"],
        "charts": [
            {"kpi": "revenue", "type": "line", "title": "Evolution du CA"},
            {"kpi": "margin_per_project", "type": "bar", "title": "Marge par projet/client"},
            {"kpi": "collection_rate", "type": "gauge", "title": "Taux de recouvrement"},
        ],
        "rankings": [
            {"field": "client_name", "metric": "revenue", "title": "Clients par CA", "order": "desc"},
            {"field": "project_name", "metric": "margin", "title": "Projets par marge", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Recouvrement faible", "kpi_type": "collection_rate", "condition": "below", "threshold": 80},
            {"name": "Baisse CA", "kpi_type": "revenue", "condition": "change_pct", "threshold": -15},
        ],
        "ai_prompt": (
            "Tu es un expert en gestion de societes de services B2B au Maroc. "
            "Analyse les donnees de cette entreprise de services marocaine. "
            "Focus : CA par client, taux de recouvrement, heures facturees, "
            "marge par projet, contrats actifs. "
            "Benchmarks Maroc : taux recouvrement sain > 85%, "
            "marge services 30-50%, concentration client top 3 < 40%. "
            "Recommandations : diversification clientele, amelioration recouvrement, "
            "optimisation des heures non facturees, upselling services."
        ),
        "benchmarks": {
            "collection_rate": {"low": 70, "avg": 85, "high": 95, "unit": "%", "label": "Taux recouvrement"},
            "margin_pct": {"low": 25, "avg": 35, "high": 50, "unit": "%", "label": "Marge services"},
        },
    },

    # ══════════════════════════════════════
    # 12. AGRICULTURE
    # ══════════════════════════════════════
    "agriculture": {
        "label": "Agriculture & Cooperatives",
        "icon": "sprout",
        "description": "Fermes modernes, cooperatives, export agricole",
        "kpis": [
            "revenue", "yield_per_ha", "cost_per_ton", "harvest_stock",
            "margin", "client_count", "order_count",
        ],
        "primary_kpis": ["revenue", "yield_per_ha", "cost_per_ton", "harvest_stock", "margin", "client_count"],
        "charts": [
            {"kpi": "revenue", "type": "bar", "title": "CA par culture"},
            {"kpi": "yield_per_ha", "type": "comparison", "title": "Rendement par parcelle"},
            {"kpi": "cost_per_ton", "type": "line", "title": "Cout par tonne"},
        ],
        "rankings": [
            {"field": "crop_name", "metric": "revenue", "title": "Cultures par CA", "order": "desc"},
            {"field": "plot_id", "metric": "yield_per_ha", "title": "Parcelles par rendement", "order": "desc"},
        ],
        "default_alerts": [
            {"name": "Rendement faible", "kpi_type": "yield_per_ha", "condition": "change_pct", "threshold": -20},
            {"name": "Cout production eleve", "kpi_type": "cost_per_ton", "condition": "above", "threshold": 5000},
        ],
        "ai_prompt": (
            "Tu es un expert en agriculture moderne au Maroc. "
            "Analyse les donnees de cette exploitation/cooperative agricole marocaine. "
            "Focus : rendement par hectare et par culture, cout de production par tonne, "
            "stock de recolte, performance par parcelle. "
            "Benchmarks Maroc : rendement tomates 80-120 T/ha, "
            "agrumes 20-30 T/ha, cereales 2-5 T/ha (irrigue). "
            "Recommandations : optimisation irrigation, choix varietaux, "
            "calendrier cultural, negociation avec les intermediaires."
        ),
        "benchmarks": {
            "yield_tomato": {"low": 60, "avg": 90, "high": 120, "unit": "T/ha", "label": "Rendement tomates"},
        },
    },
}


def get_sector(slug: str) -> dict[str, Any] | None:
    """Get sector config by slug."""
    return SECTORS.get(slug)


def get_all_sectors() -> dict[str, dict[str, Any]]:
    """Get all sector configs."""
    return SECTORS


def get_sector_kpis(slug: str) -> list[str]:
    """Get the list of KPI types for a sector."""
    sector = SECTORS.get(slug)
    if not sector:
        return ["revenue", "margin", "client_count", "order_count", "avg_order_value", "stock_level"]
    return sector["kpis"]


def get_sector_primary_kpis(slug: str) -> list[str]:
    """Get primary (dashboard-visible) KPIs for a sector."""
    sector = SECTORS.get(slug)
    if not sector:
        return ["revenue", "margin", "client_count", "stock_level"]
    return sector["primary_kpis"]


def get_sector_ai_prompt(slug: str) -> str:
    """Get the AI system prompt addition for a sector."""
    sector = SECTORS.get(slug)
    if not sector:
        return ""
    return sector.get("ai_prompt", "")


def get_sector_benchmarks(slug: str) -> dict[str, Any]:
    """Get benchmarks for a sector."""
    sector = SECTORS.get(slug)
    if not sector:
        return {}
    return sector.get("benchmarks", {})


def get_sector_default_alerts(slug: str) -> list[dict]:
    """Get default alerts config for a sector."""
    sector = SECTORS.get(slug)
    if not sector:
        return []
    return sector.get("default_alerts", [])


def get_sector_choices() -> list[dict[str, str]]:
    """Get sector list for onboarding UI."""
    return [
        {"slug": slug, "label": s["label"], "icon": s["icon"], "description": s["description"]}
        for slug, s in SECTORS.items()
    ]
