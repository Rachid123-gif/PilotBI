#!/usr/bin/env python3
"""Generate PilotBI Strategy PDF for Chaimae"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, Frame
from reportlab.lib.utils import simpleSplit
import os

# ── Colors ──
BLUE_900 = HexColor("#0f1b4d")
BLUE_700 = HexColor("#1e3a8a")
BLUE_600 = HexColor("#2563eb")
BLUE_500 = HexColor("#3b82f6")
BLUE_100 = HexColor("#dbeafe")
BLUE_50 = HexColor("#eff6ff")
GOLD = HexColor("#f59e0b")
GOLD_LIGHT = HexColor("#fef3c7")
GREEN = HexColor("#059669")
GREEN_LIGHT = HexColor("#d1fae5")
RED = HexColor("#dc2626")
GRAY_50 = HexColor("#f8fafc")
GRAY_100 = HexColor("#f1f5f9")
GRAY_200 = HexColor("#e2e8f0")
GRAY_400 = HexColor("#94a3b8")
GRAY_500 = HexColor("#64748b")
GRAY_600 = HexColor("#475569")
GRAY_700 = HexColor("#334155")
GRAY_800 = HexColor("#1e293b")
GRAY_900 = HexColor("#0f172a")
WHITE = white

# ── Page dimensions ──
PAGE_W, PAGE_H = A4
MARGIN_L = 20 * mm
MARGIN_R = 20 * mm
MARGIN_T = 25 * mm
MARGIN_B = 20 * mm

# ── Styles ──
def get_styles():
    return {
        'cover_title': ParagraphStyle(
            'cover_title', fontSize=32, leading=38, textColor=WHITE,
            fontName='Helvetica-Bold', alignment=TA_LEFT,
            spaceAfter=8
        ),
        'cover_subtitle': ParagraphStyle(
            'cover_subtitle', fontSize=14, leading=20, textColor=HexColor("#93c5fd"),
            fontName='Helvetica', alignment=TA_LEFT,
            spaceAfter=4
        ),
        'section_title': ParagraphStyle(
            'section_title', fontSize=22, leading=28, textColor=BLUE_700,
            fontName='Helvetica-Bold', alignment=TA_LEFT,
            spaceBefore=20, spaceAfter=12
        ),
        'subsection': ParagraphStyle(
            'subsection', fontSize=15, leading=20, textColor=BLUE_600,
            fontName='Helvetica-Bold', alignment=TA_LEFT,
            spaceBefore=16, spaceAfter=8
        ),
        'h3': ParagraphStyle(
            'h3', fontSize=12, leading=16, textColor=GRAY_800,
            fontName='Helvetica-Bold', alignment=TA_LEFT,
            spaceBefore=10, spaceAfter=6
        ),
        'body': ParagraphStyle(
            'body', fontSize=10, leading=15, textColor=GRAY_700,
            fontName='Helvetica', alignment=TA_LEFT,
            spaceAfter=6
        ),
        'body_bold': ParagraphStyle(
            'body_bold', fontSize=10, leading=15, textColor=GRAY_800,
            fontName='Helvetica-Bold', alignment=TA_LEFT,
            spaceAfter=6
        ),
        'bullet': ParagraphStyle(
            'bullet', fontSize=10, leading=15, textColor=GRAY_700,
            fontName='Helvetica', alignment=TA_LEFT,
            leftIndent=15, spaceAfter=3,
            bulletIndent=5, bulletFontSize=10
        ),
        'quote': ParagraphStyle(
            'quote', fontSize=11, leading=17, textColor=BLUE_700,
            fontName='Helvetica-BoldOblique', alignment=TA_LEFT,
            leftIndent=20, rightIndent=20, spaceBefore=10, spaceAfter=10,
            borderPadding=10
        ),
        'small': ParagraphStyle(
            'small', fontSize=8, leading=10, textColor=GRAY_500,
            fontName='Helvetica', alignment=TA_CENTER
        ),
        'table_header': ParagraphStyle(
            'table_header', fontSize=9, leading=12, textColor=WHITE,
            fontName='Helvetica-Bold', alignment=TA_LEFT
        ),
        'table_cell': ParagraphStyle(
            'table_cell', fontSize=9, leading=13, textColor=GRAY_700,
            fontName='Helvetica', alignment=TA_LEFT
        ),
        'table_cell_bold': ParagraphStyle(
            'table_cell_bold', fontSize=9, leading=13, textColor=GRAY_800,
            fontName='Helvetica-Bold', alignment=TA_LEFT
        ),
        'footer': ParagraphStyle(
            'footer', fontSize=8, leading=10, textColor=GRAY_400,
            fontName='Helvetica', alignment=TA_CENTER
        ),
        'page_num': ParagraphStyle(
            'page_num', fontSize=8, leading=10, textColor=GRAY_500,
            fontName='Helvetica', alignment=TA_RIGHT
        ),
    }

S = get_styles()


def header_footer(canvas, doc):
    """Draw header line and footer on each page."""
    canvas.saveState()
    # Top blue line
    canvas.setStrokeColor(BLUE_600)
    canvas.setLineWidth(2)
    canvas.line(MARGIN_L, PAGE_H - 18 * mm, PAGE_W - MARGIN_R, PAGE_H - 18 * mm)
    # Header text
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(BLUE_600)
    canvas.drawString(MARGIN_L, PAGE_H - 16 * mm, "PilotBI")
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(GRAY_400)
    canvas.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 16 * mm, "Strategie Commerciale & Marketing")
    # Footer
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(GRAY_400)
    canvas.drawString(MARGIN_L, 12 * mm, "PilotBI - Document confidentiel")
    canvas.drawRightString(PAGE_W - MARGIN_R, 12 * mm, f"Page {doc.page}")
    # Bottom line
    canvas.setStrokeColor(GRAY_200)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, 16 * mm, PAGE_W - MARGIN_R, 16 * mm)
    canvas.restoreState()


def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    w = PAGE_W - MARGIN_L - MARGIN_R
    if col_widths is None:
        col_widths = [w / len(headers)] * len(headers)

    header_cells = [Paragraph(h, S['table_header']) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([Paragraph(str(c), S['table_cell']) for c in row])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), BLUE_700),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GRAY_50]),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def make_highlight_box(text, bg=BLUE_50, border=BLUE_500):
    """Create a highlighted box."""
    data = [[Paragraph(text, S['quote'])]]
    t = Table(data, colWidths=[PAGE_W - MARGIN_L - MARGIN_R - 10])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LINEBEFOREDECORATION', (0, 0), (0, -1), 3, border),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    return t


def build_cover(canvas, doc):
    """Draw cover page."""
    canvas.saveState()
    # Background gradient (solid blue)
    canvas.setFillColor(BLUE_900)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Decorative circle
    canvas.setFillColor(HexColor("#1e3a8a"))
    canvas.circle(PAGE_W - 60 * mm, PAGE_H - 80 * mm, 120 * mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#1e40af"))
    canvas.circle(PAGE_W - 40 * mm, PAGE_H - 60 * mm, 80 * mm, fill=1, stroke=0)
    # Gold accent bar
    canvas.setFillColor(GOLD)
    canvas.rect(MARGIN_L, PAGE_H - 200 * mm, 40 * mm, 3, fill=1, stroke=0)
    canvas.restoreState()


def generate_pdf():
    output_path = "/Users/mac/Documents/Projet IA/PilotBI/PilotBI_Strategie_Chaimae.pdf"

    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
        title="PilotBI - Strategie Commerciale & Marketing",
        author="PilotBI",
    )

    # Cover frame
    cover_frame = Frame(
        MARGIN_L, MARGIN_B,
        PAGE_W - MARGIN_L - MARGIN_R,
        PAGE_H - MARGIN_T - MARGIN_B,
        id='cover'
    )
    cover_template = PageTemplate(id='cover', frames=[cover_frame], onPage=build_cover)

    # Content frame
    content_frame = Frame(
        MARGIN_L, MARGIN_B + 5 * mm,
        PAGE_W - MARGIN_L - MARGIN_R,
        PAGE_H - MARGIN_T - MARGIN_B - 10 * mm,
        id='content'
    )
    content_template = PageTemplate(id='content', frames=[content_frame], onPage=header_footer)

    doc.addPageTemplates([cover_template, content_template])

    story = []
    W = PAGE_W - MARGIN_L - MARGIN_R

    # ═══════════════════════════════════
    # COVER PAGE
    # ═══════════════════════════════════
    story.append(Spacer(1, 60 * mm))
    story.append(Paragraph("PilotBI", ParagraphStyle(
        'logo', fontSize=16, leading=20, textColor=HexColor("#93c5fd"),
        fontName='Helvetica-Bold', spaceAfter=8
    )))
    story.append(Paragraph(
        "Strategie Commerciale<br/>& Marketing",
        S['cover_title']
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "Guide complet des cibles, du positionnement<br/>et du plan d'action pour le marche marocain",
        S['cover_subtitle']
    ))
    story.append(Spacer(1, 15 * mm))
    story.append(Paragraph(
        "Prepare pour <b>Chaimae</b> - Data Analyst & Sales",
        ParagraphStyle('for', fontSize=12, textColor=GOLD, fontName='Helvetica', spaceAfter=4)
    ))
    story.append(Paragraph(
        "Avril 2026 | Confidentiel",
        ParagraphStyle('date', fontSize=10, textColor=HexColor("#64748b"), fontName='Helvetica')
    ))

    # Switch to content template
    story.append(PageBreak())
    from reportlab.platypus.doctemplate import NextPageTemplate
    story.insert(-1, NextPageTemplate('content'))

    # ═══════════════════════════════════
    # TABLE DES MATIERES
    # ═══════════════════════════════════
    story.append(Paragraph("Sommaire", S['section_title']))
    story.append(Spacer(1, 5 * mm))
    toc_items = [
        ("1.", "Cibles prioritaires (Tier 1)", "PMEs a fort besoin immediat"),
        ("2.", "Cibles secondaires (Tier 2)", "Marche a eduquer, fort potentiel"),
        ("3.", "Niches et opportunites (Tier 3)", "Segments specifiques"),
        ("4.", "Prescripteurs et canaux indirects", "Fiduciaires, integrateurs, institutions"),
        ("5.", "Secteur public et institutionnel", "Communes, etablissements, programmes"),
        ("6.", "L'avantage Chaimae", "Positionnement Data Analyst"),
        ("7.", "Cibles ou Chaimae est imbattable", "Fiduciaires, DAF, distributeurs..."),
        ("8.", "L'offre Audit Data Gratuit", "Arme secrete de conversion"),
        ("9.", "Reponses aux objections", "Scripts de vente"),
        ("10.", "Plan de prospection hebdomadaire", "Organisation semaine type"),
        ("11.", "Objectifs et projections", "MRR Mois 1 a 12"),
    ]
    for num, title, desc in toc_items:
        story.append(Paragraph(
            f'<b><font color="{BLUE_600.hexval()}">{num}</font></b>  '
            f'<b>{title}</b>  '
            f'<font color="{GRAY_500.hexval()}">{desc}</font>',
            ParagraphStyle('toc', fontSize=10, leading=18, textColor=GRAY_800,
                           fontName='Helvetica', leftIndent=5, spaceAfter=2)
        ))
    story.append(Spacer(1, 5 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY_200))

    # ═══════════════════════════════════
    # 1. CIBLES TIER 1
    # ═══════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("1. Cibles prioritaires (Tier 1)", S['section_title']))
    story.append(Paragraph(
        "Ces secteurs ont un <b>besoin immediat</b>, un <b>budget present</b> et une <b>douleur forte</b>. "
        "C'est le premier marche a attaquer.",
        S['body']
    ))
    story.append(Spacer(1, 3 * mm))

    tier1 = [
        ["Distribution &\nCommerce de gros",
         "Grossistes Derb Omar,\ndistributeurs FMCG,\nimportateurs",
         "10-200 emp.",
         "Marges invisibles,\nExcel ingerable,\nzero visibilite"],
        ["Retail\nmulti-points",
         "Chaines pret-a-porter,\nelectromenager,\ncosmetiques",
         "3-30 magasins",
         "Pas de vue consolidee\nmulti-magasins"],
        ["Industrie PME",
         "Textile, agro,\nplasturgie, BTP",
         "30-300 emp.",
         "Pas de dashboard,\nrapports manuels,\n3 jours d'attente"],
        ["Transport &\nLogistique",
         "Flottes camions,\ntransitaires,\nmessagerie",
         "10-100 emp.",
         "Cout par trajet\ninconnu, rentabilite\nfloue"],
        ["Pharmacies\nen chaine",
         "Groupements\n3-20 pharmacies",
         "3-20 pts\nde vente",
         "Stock eclate, pas\nde comparatif entre\npoints de vente"],
    ]
    story.append(make_table(
        ["Secteur", "Exemples", "Taille", "Douleur principale"],
        tier1,
        [W * 0.22, W * 0.28, W * 0.15, W * 0.35]
    ))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("KPIs critiques par secteur :", S['subsection']))

    kpis = [
        ["Distribution", "Marge par reference, rotation stock, CA par commercial, creances clients"],
        ["Retail", "CA par magasin, panier moyen, top/flop produits, stock par point de vente"],
        ["Industrie", "Cout de production, rendement, taux de rebut, commandes en retard"],
        ["Transport", "Cout par km, taux de remplissage, CA par vehicule, delai moyen"],
        ["Pharmacies", "CA par officine, stock critique, marge par categorie"],
    ]
    story.append(make_table(
        ["Secteur", "KPIs a proposer dans le dashboard"],
        kpis,
        [W * 0.2, W * 0.8]
    ))

    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("Villes prioritaires :", S['h3']))
    story.append(Paragraph(
        "<b>Casablanca</b> (Derb Omar, Ain Sebaa, zones industrielles) | "
        "<b>Tanger</b> (TFZ) | <b>Agadir</b> | <b>Marrakech</b> | "
        "<b>Kenitra</b> | <b>Fes</b>",
        S['body']
    ))

    # ═══════════════════════════════════
    # 2. CIBLES TIER 2
    # ═══════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("2. Cibles secondaires (Tier 2)", S['section_title']))
    story.append(Paragraph(
        "Besoin latent mais reel. Il faut <b>eduquer</b> ces prospects sur la valeur d'un dashboard BI.",
        S['body']
    ))
    story.append(Spacer(1, 3 * mm))

    tier2 = [
        ["Restaurants & F&B", "Chaines fast-food, dark kitchens, traiteurs", "2-15 unites", "Food cost non maitrise"],
        ["E-commerce", "Vendeurs Instagram, Shopify, Jumia", "CA 500K-10M MAD", "Donnees eclatees partout"],
        ["Cliniques privees", "Multi-specialites, labos, dentaires", "10-80 emp.", "Gestion financiere sur papier"],
        ["Immobilier", "Promoteurs regionaux, agences", "5-50 emp.", "Suivi projets/ventes sur Excel"],
        ["Agriculture moderne", "Fermes export, cooperatives structurees", "20-200 emp.", "Rendement, couts, tracabilite"],
        ["Hotels & Riads", "Chaines 3-15 etablissements", "20-150 emp.", "RevPAR, taux occupation"],
        ["Auto-ecoles", "Chaines multi-villes", "3-10 centres", "CA par centre, taux reussite"],
        ["Stations-service", "Independants ou mini-reseaux", "2-10 stations", "Volume, marge, comparatif"],
    ]
    story.append(make_table(
        ["Secteur", "Exemples", "Taille", "Douleur"],
        tier2,
        [W * 0.2, W * 0.3, W * 0.18, W * 0.32]
    ))

    # ═══════════════════════════════════
    # 3. NICHES TIER 3
    # ═══════════════════════════════════
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("3. Niches a fort potentiel (Tier 3)", S['section_title']))

    tier3 = [
        ["Franchises (toutes)", "Multi-unites = besoin natif de consolidation et comparaison"],
        ["Cooperatives (ONCA, lait, argan)", "Subventions Etat pour la digitalisation, budget disponible"],
        ["Startups en croissance", "Besoin de KPIs structures pour lever des fonds"],
        ["Gardiennage / Nettoyage", "Gros effectifs, marges serrees, besoin de controle strict"],
    ]
    story.append(make_table(
        ["Niche", "Pourquoi c'est une opportunite"],
        tier3,
        [W * 0.35, W * 0.65]
    ))

    # ═══════════════════════════════════
    # 4. PRESCRIPTEURS
    # ═══════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("4. Prescripteurs & canaux indirects", S['section_title']))
    story.append(make_highlight_box(
        "Un seul cabinet comptable peut vous apporter 20 a 50 clients PME. "
        "C'est le canal le plus puissant et le moins cher."
    ))
    story.append(Spacer(1, 3 * mm))

    prescripteurs = [
        ["Fiduciaires & cabinets comptables", "1 cabinet = 20-50 clients PME", "~8 000 au Maroc"],
        ["Integrateurs Sage / Odoo", "Ont les clients, pas l'offre BI", "~200 au Maroc"],
        ["Consultants independants", "Finance, strategie, accompagnement", "~2 000"],
        ["Banques (conseillers PME)", "BCP, AWB, BMCE - programmes", "Milliers de PMEs"],
        ["CRI", "Centres Regionaux d'Investissement", "12 regions"],
        ["CGEM & Federations", "Acces direct aux dirigeants", "Par secteur"],
    ]
    story.append(make_table(
        ["Prescripteur", "Pourquoi c'est strategique", "Volume"],
        prescripteurs,
        [W * 0.35, W * 0.40, W * 0.25]
    ))

    # ═══════════════════════════════════
    # 5. SECTEUR PUBLIC
    # ═══════════════════════════════════
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("5. Secteur public & institutionnel", S['section_title']))

    public = [
        ["Communes & Collectivites", "Budget digitalisation, besoin tableaux de bord budgetaires"],
        ["Etablissements publics (ONEE, ONCF...)", "Reporting interne, suivi performance"],
        ["Universites & Ecoles privees", "Suivi inscriptions, budget, performance pedagogique"],
        ["ONG & Associations", "Reporting bailleurs de fonds, transparence"],
        ["Programmes Etat (Forsa, Intelaka)", "Partenariats, subventions, accompagnement"],
    ]
    story.append(make_table(
        ["Cible", "Opportunite"],
        public,
        [W * 0.40, W * 0.60]
    ))

    # ═══════════════════════════════════
    # 6. L'AVANTAGE CHAIMAE
    # ═══════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("6. L'avantage Chaimae : le profil Data Analyst", S['section_title']))
    story.append(Paragraph(
        "Le profil Data Analyst de Chaimae est un <b>avantage competitif enorme</b>. "
        "C'est exactement ce qu'un vendeur classique ne peut PAS faire.",
        S['body']
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(make_highlight_box(
        '"Je ne vous vends pas un logiciel. Je lis vos donnees, je comprends votre business, '
        'et je vous livre un dashboard qui parle votre langue."',
        bg=GOLD_LIGHT, border=GOLD
    ))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Ce que Chaimae peut faire et qu'un commercial ne peut pas :", S['subsection']))

    avantages = [
        "Analyser un extrait Excel/Sage en 10 minutes et montrer la valeur immediate",
        "Parler le langage des DAF et comptables (KPIs, marges, ratios)",
        "Faire une demo live avec les VRAIES donnees du prospect",
        "Identifier les insights cles que le prospect ne voit pas dans ses propres fichiers",
        "Structurer les KPIs pour les investisseurs (startups)",
        "Connecter et consolider des sources multiples (Shopify, GA, Excel)",
    ]
    for a in avantages:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {a}", S['bullet']))

    # ═══════════════════════════════════
    # 7. CIBLES IMBATTABLES
    # ═══════════════════════════════════
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("7. Cibles ou Chaimae est imbattable", S['section_title']))

    cibles_ch = [
        ["Fiduciaires",
         "Parle leur langage\n(donnees, Excel, KPIs)",
         '"Je transforme les fichiers\nde vos clients en dashboards\nautomatiques"'],
        ["DG / DAF\nde PMEs",
         "Peut analyser un extrait\nSage en 10 min",
         "Demo live avec leurs\nvraies donnees"],
        ["Distributeurs",
         "Comprend les marges,\nrotations, creances",
         '"Envoyez votre Excel,\nje vous montre votre\ndashboard en 24h"'],
        ["Startups",
         "Structure les KPIs\npour investisseurs",
         '"Je prepare le reporting\nque les VCs attendent"'],
        ["Cabinets\nde conseil",
         "Elle est leur pair\ntechnique",
         "Partenariat win-win"],
        ["E-commerce",
         "Sait connecter\nShopify / GA / Excel",
         '"Je consolide toutes vos\nsources en un seul\ndashboard"'],
    ]
    story.append(make_table(
        ["Cible", "Pourquoi Chaimae", "Approche / Pitch"],
        cibles_ch,
        [W * 0.18, W * 0.35, W * 0.47]
    ))

    # ═══════════════════════════════════
    # 8. OFFRE AUDIT GRATUIT
    # ═══════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("8. L'offre \"Audit Data Gratuit\"", S['section_title']))
    story.append(Paragraph(
        "C'est l'<b>arme secrete</b> de conversion. Voici le processus :",
        S['body']
    ))
    story.append(Spacer(1, 3 * mm))

    steps = [
        ["1", "Le prospect envoie un fichier Excel de ses ventes\n(par email ou WhatsApp)"],
        ["2", "Chaimae l'analyse en 30 minutes"],
        ["3", "Elle renvoie 3 insights cles + un screenshot\ndu dashboard PilotBI avec SES donnees"],
        ["4", "Le prospect est impressionne --> il signe"],
    ]
    step_data = [[
        Paragraph(f'<font color="{BLUE_600.hexval()}" size="16"><b>{s[0]}</b></font>', S['table_cell']),
        Paragraph(s[1], S['table_cell'])
    ] for s in steps]

    t = Table(step_data, colWidths=[W * 0.1, W * 0.9])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), BLUE_50),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY_200),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, GRAY_50]),
    ]))
    story.append(t)

    story.append(Spacer(1, 3 * mm))
    story.append(make_highlight_box(
        "Taux de conversion attendu : <b>40-60%</b> des prospects qui envoient leur fichier. "
        "C'est 10x mieux qu'une demo generique.",
        bg=GREEN_LIGHT, border=GREEN
    ))

    # ═══════════════════════════════════
    # 9. OBJECTIONS
    # ═══════════════════════════════════
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("9. Reponses aux objections", S['section_title']))

    objections = [
        ['"C\'est quoi PilotBI ?"',
         "C'est votre comptable qui vous fait un rapport visuel chaque mois,\nsauf que c'est automatique et instantane."],
        ['"J\'ai deja Excel"',
         "Exactement ! C'est votre Excel que je transforme.\nVous gardez vos habitudes, vous gagnez la visibilite."],
        ['"C\'est cher"',
         "990 MAD c'est moins qu'un stagiaire.\nEt ca ne prend pas de vacances."],
        ['"Je n\'ai pas le temps"',
         "Envoyez-moi votre fichier par WhatsApp.\nDans 48h votre dashboard est pret."],
        ['"Mon comptable fait ca"',
         "Votre comptable regarde le passe.\nPilotBI vous montre ou vous allez."],
        ['"Je ne suis pas technique"',
         "Justement, zero competence technique requise.\nSi vous savez lire un SMS, vous savez lire PilotBI."],
    ]
    story.append(make_table(
        ["Objection", "Reponse de Chaimae"],
        objections,
        [W * 0.30, W * 0.70]
    ))

    # ═══════════════════════════════════
    # 10. PLAN HEBDOMADAIRE
    # ═══════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("10. Plan de prospection hebdomadaire", S['section_title']))
    story.append(Paragraph(
        "Organisation type d'une semaine de prospection pour Chaimae :",
        S['body']
    ))
    story.append(Spacer(1, 3 * mm))

    semaine = [
        ["Lundi", "Messages LinkedIn\npersonnalises", "DG / DAF PMEs\nindustrielles Casa", "20 messages"],
        ["Mardi", "Visites terrain\nDerb Omar / Ain Sebaa", "Grossistes &\ndistributeurs", "5-8 visites"],
        ["Mercredi", "Appels telephoniques\nfiduciaires", "Cabinets comptables\nCasa / Rabat", "15 appels"],
        ["Jeudi", "Demos live\n(Zoom / Meet)", "Prospects chauds\nde la semaine", "3-5 demos"],
        ["Vendredi", "Contenu LinkedIn +\nsuivi relances", "Audience organique", "1 post +\n10 relances"],
    ]
    story.append(make_table(
        ["Jour", "Action", "Cible", "Volume"],
        semaine,
        [W * 0.15, W * 0.28, W * 0.30, W * 0.27]
    ))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Metriques de suivi hebdomadaire :", S['subsection']))

    metriques = [
        "Nombre de prospects contactes : objectif 50/semaine",
        "Nombre de fichiers Excel recus (Audit Gratuit) : objectif 5-10/semaine",
        "Nombre de demos realisees : objectif 3-5/semaine",
        "Nombre de clients signes : objectif 2-3/semaine",
        "Taux de conversion Audit --> Client : objectif > 40%",
    ]
    for m in metriques:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {m}", S['bullet']))

    # ═══════════════════════════════════
    # 11. OBJECTIFS & PROJECTIONS
    # ═══════════════════════════════════
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("11. Objectifs et projections financieres", S['section_title']))

    projections = [
        ["Mois 1-2", "5-10 clients", "5 000 - 15 000 MAD", "Reseau personnel, terrain, amis d'amis"],
        ["Mois 3-4", "15-25 clients", "20 000 - 40 000 MAD", "Bouche a oreille + premiers fiduciaires"],
        ["Mois 6", "40-60 clients", "50 000 - 80 000 MAD", "Canaux indirects actifs"],
        ["Mois 12", "100-150 clients", "150 000 - 250 000 MAD", "Machine commerciale rodee"],
    ]
    story.append(make_table(
        ["Periode", "Clients", "MRR", "Source principale"],
        projections,
        [W * 0.15, W * 0.18, W * 0.30, W * 0.37]
    ))

    story.append(Spacer(1, 5 * mm))
    story.append(make_highlight_box(
        "Objectif Annee 1 : <b>150 clients</b> | <b>250 000 MAD MRR</b> | <b>3M MAD ARR</b>",
        bg=GOLD_LIGHT, border=GOLD
    ))

    # ═══════════════════════════════════
    # CLOSING PAGE
    # ═══════════════════════════════════
    story.append(PageBreak())
    story.append(Spacer(1, 40 * mm))
    story.append(Paragraph(
        "Le profil Data Analyst de Chaimae est son<br/><b>meilleur argument de vente</b>.",
        ParagraphStyle('closing1', fontSize=18, leading=24, textColor=BLUE_700,
                       fontName='Helvetica', alignment=TA_CENTER, spaceAfter=15)
    ))
    story.append(Paragraph(
        "Elle ne vend pas un SaaS.<br/>Elle vend <b>son expertise + un outil</b>.",
        ParagraphStyle('closing2', fontSize=16, leading=22, textColor=GRAY_700,
                       fontName='Helvetica', alignment=TA_CENTER, spaceAfter=20)
    ))
    story.append(Paragraph(
        "C'est 10x plus convaincant<br/>qu'un commercial classique.",
        ParagraphStyle('closing3', fontSize=14, leading=20, textColor=BLUE_600,
                       fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=30)
    ))
    story.append(HRFlowable(width="40%", thickness=1, color=GOLD, spaceAfter=20))
    story.append(Paragraph(
        "PilotBI | pilotbi.ma | 2026",
        ParagraphStyle('closing_footer', fontSize=10, textColor=GRAY_400,
                       fontName='Helvetica', alignment=TA_CENTER)
    ))

    # Build
    doc.build(story)
    print(f"PDF genere : {output_path}")
    return output_path


if __name__ == "__main__":
    generate_pdf()
