#!/usr/bin/env python3
"""PilotBI — Document Strategique Complet : Approche 100% Digitale"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, Frame, NextPageTemplate

# Colors
BLUE_900 = HexColor("#0f1b4d")
BLUE_700 = HexColor("#1e3a8a")
BLUE_600 = HexColor("#2563eb")
BLUE_50 = HexColor("#eff6ff")
GOLD = HexColor("#f59e0b")
GOLD_LIGHT = HexColor("#fef3c7")
GREEN = HexColor("#059669")
GREEN_LIGHT = HexColor("#d1fae5")
RED_LIGHT = HexColor("#fee2e2")
RED = HexColor("#dc2626")
GRAY_50 = HexColor("#f8fafc")
GRAY_200 = HexColor("#e2e8f0")
GRAY_400 = HexColor("#94a3b8")
GRAY_500 = HexColor("#64748b")
GRAY_700 = HexColor("#334155")
GRAY_800 = HexColor("#1e293b")
WHITE = white

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 20*mm, 20*mm, 25*mm, 20*mm
W = PAGE_W - ML - MR

# Styles
S = {
    'cover_title': ParagraphStyle('ct', fontSize=30, leading=36, textColor=WHITE, fontName='Helvetica-Bold', spaceAfter=8),
    'cover_sub': ParagraphStyle('cs', fontSize=13, leading=18, textColor=HexColor("#93c5fd"), fontName='Helvetica', spaceAfter=4),
    'section': ParagraphStyle('sec', fontSize=20, leading=26, textColor=BLUE_700, fontName='Helvetica-Bold', spaceBefore=16, spaceAfter=10),
    'subsection': ParagraphStyle('sub', fontSize=14, leading=19, textColor=BLUE_600, fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6),
    'h3': ParagraphStyle('h3', fontSize=11, leading=15, textColor=GRAY_800, fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=4),
    'body': ParagraphStyle('body', fontSize=10, leading=15, textColor=GRAY_700, fontName='Helvetica', spaceAfter=5),
    'bold': ParagraphStyle('bold', fontSize=10, leading=15, textColor=GRAY_800, fontName='Helvetica-Bold', spaceAfter=5),
    'bullet': ParagraphStyle('bul', fontSize=10, leading=15, textColor=GRAY_700, fontName='Helvetica', leftIndent=15, spaceAfter=3, bulletIndent=5),
    'quote': ParagraphStyle('q', fontSize=11, leading=16, textColor=BLUE_700, fontName='Helvetica-BoldOblique', leftIndent=15, rightIndent=15, spaceBefore=8, spaceAfter=8),
    'th': ParagraphStyle('th', fontSize=9, leading=12, textColor=WHITE, fontName='Helvetica-Bold'),
    'td': ParagraphStyle('td', fontSize=9, leading=13, textColor=GRAY_700, fontName='Helvetica'),
    'td_b': ParagraphStyle('tdb', fontSize=9, leading=13, textColor=GRAY_800, fontName='Helvetica-Bold'),
    'small': ParagraphStyle('sm', fontSize=8, leading=10, textColor=GRAY_400, fontName='Helvetica', alignment=TA_CENTER),
    'num_big': ParagraphStyle('nb', fontSize=22, leading=26, textColor=BLUE_600, fontName='Helvetica-Bold', alignment=TA_CENTER),
    'num_label': ParagraphStyle('nl', fontSize=9, leading=12, textColor=GRAY_500, fontName='Helvetica', alignment=TA_CENTER),
}

def hf(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BLUE_600); canvas.setLineWidth(2)
    canvas.line(ML, PAGE_H-18*mm, PAGE_W-MR, PAGE_H-18*mm)
    canvas.setFont('Helvetica-Bold', 8); canvas.setFillColor(BLUE_600)
    canvas.drawString(ML, PAGE_H-16*mm, "PilotBI")
    canvas.setFont('Helvetica', 8); canvas.setFillColor(GRAY_400)
    canvas.drawRightString(PAGE_W-MR, PAGE_H-16*mm, "Strategie Go-To-Market — Confidentiel")
    canvas.setFont('Helvetica', 7); canvas.setFillColor(GRAY_400)
    canvas.drawString(ML, 12*mm, "PilotBI — Document confidentiel")
    canvas.drawRightString(PAGE_W-MR, 12*mm, f"Page {doc.page}")
    canvas.setStrokeColor(GRAY_200); canvas.setLineWidth(0.5)
    canvas.line(ML, 16*mm, PAGE_W-MR, 16*mm)
    canvas.restoreState()

def cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BLUE_900); canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#1e3a8a")); canvas.circle(PAGE_W-50*mm, PAGE_H-70*mm, 110*mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#1e40af")); canvas.circle(PAGE_W-30*mm, PAGE_H-50*mm, 70*mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD); canvas.rect(ML, PAGE_H-195*mm, 35*mm, 3, fill=1, stroke=0)
    canvas.restoreState()

def tbl(headers, rows, cw=None):
    if not cw: cw = [W/len(headers)]*len(headers)
    data = [[Paragraph(h, S['th']) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), S['td']) for c in r])
    t = Table(data, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE_700), ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 8), ('TOPPADDING', (0,0), (-1,0), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 7), ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,1), (-1,-1), 5), ('BOTTOMPADDING', (0,1), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, GRAY_200), ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, GRAY_50]),
    ]))
    return t

def box(text, bg=BLUE_50, border=BLUE_600):
    data = [[Paragraph(text, S['quote'])]]
    t = Table(data, colWidths=[W-10])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBEFOREDECORATION', (0,0), (0,-1), 3, border),
    ]))
    return t

def stat_row(items):
    """items = list of (number, label)"""
    cells = []
    for num, label in items:
        cells.append([Paragraph(num, S['num_big']), Paragraph(label, S['num_label'])])
    data = [cells]
    t = Table(data, colWidths=[W/len(items)]*len(items))
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,0), (-1,-1), GRAY_50),
    ]))
    return t

def build():
    path = "/Users/mac/Documents/Projet IA/PilotBI/PilotBI_Strategie_GoToMarket.pdf"
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
                          title="PilotBI — Strategie Go-To-Market", author="PilotBI")
    cf = Frame(ML, MB, W, PAGE_H-MT-MB, id='cover')
    ct = PageTemplate(id='cover', frames=[cf], onPage=cover)
    nf = Frame(ML, MB+5*mm, W, PAGE_H-MT-MB-10*mm, id='content')
    nt = PageTemplate(id='content', frames=[nf], onPage=hf)
    doc.addPageTemplates([ct, nt])

    st = []
    # ══════════ COVER ══════════
    st.append(Spacer(1, 55*mm))
    st.append(Paragraph("PilotBI", ParagraphStyle('l', fontSize=15, textColor=HexColor("#93c5fd"), fontName='Helvetica-Bold', spaceAfter=6)))
    st.append(Paragraph("Strategie Go-To-Market<br/>100% Digitale", S['cover_title']))
    st.append(Spacer(1, 3*mm))
    st.append(Paragraph("Plan d'acquisition, pricing, canaux de croissance<br/>et projections financieres — marche marocain", S['cover_sub']))
    st.append(Spacer(1, 12*mm))
    st.append(Paragraph("Approche <b>Product-Led Growth</b> sans prospection terrain", ParagraphStyle('f', fontSize=12, textColor=GOLD, fontName='Helvetica', spaceAfter=4)))
    st.append(Paragraph("Avril 2026 | Confidentiel", ParagraphStyle('d', fontSize=10, textColor=GRAY_500, fontName='Helvetica')))

    st.append(NextPageTemplate('content'))
    st.append(PageBreak())

    # ══════════ SOMMAIRE ══════════
    st.append(Paragraph("Sommaire", S['section']))
    toc = [
        ("1.", "Analyse du marche marocain", "Realites, contraintes, opportunites"),
        ("2.", "Analyse des couts infrastructure", "Combien coute chaque utilisateur"),
        ("3.", "Modele Freemium agressif", "Grille tarifaire optimisee"),
        ("4.", "Modele hybride de revenus", "SaaS + Fiduciaires + Affiliation"),
        ("5.", "5 moteurs de croissance digitaux", "Sans prospection terrain"),
        ("6.", "Projections financieres mois 1-12", "Scenarios realistes"),
        ("7.", "Plan d'execution semaine par semaine", "Actions concretes"),
        ("8.", "Offre de lancement Early Bird", "Accelerateur de revenus"),
        ("9.", "Architecture scalable", "Protections et couts maitrises"),
        ("10.", "Fonctionnalites a implementer", "Code necessaire pour la viralite"),
    ]
    for n, title, desc in toc:
        st.append(Paragraph(f'<b><font color="{BLUE_600.hexval()}">{n}</font></b>  <b>{title}</b>  <font color="{GRAY_500.hexval()}">{desc}</font>',
                             ParagraphStyle('toc', fontSize=10, leading=17, textColor=GRAY_800, fontName='Helvetica', leftIndent=5, spaceAfter=2)))
    st.append(HRFlowable(width="100%", thickness=0.5, color=GRAY_200, spaceAfter=5))

    # ══════════ 1. MARCHE ══════════
    st.append(PageBreak())
    st.append(Paragraph("1. Analyse du marche marocain", S['section']))
    st.append(Paragraph("Le marche marocain a des specificites uniques qu'il faut respecter pour reussir.", S['body']))
    st.append(Spacer(1, 3*mm))
    st.append(tbl(
        ["Realite", "Implication pour PilotBI"],
        [
            ["Salaire moyen gerant PME : 8 000-15 000 MAD", "Le prix doit etre < 100 MAD/mois pour le plan de base"],
            ["Budget digital PME : quasi ZERO", "Il faut un plan GRATUIT genereux pour hooker"],
            ["ChatGPT a 200 MAD = 'trop cher' pour 80%", "L'IA doit etre incluse, pas un extra payant"],
            ["Un repas d'affaires = 500 MAD sans hesitation", "La valeur percue doit etre immediate et concrete"],
            ["Les dirigeants sont sur Facebook, pas LinkedIn", "Canaux : Facebook groupes + WhatsApp + Instagram"],
            ["Bouche a oreille = canal #1 au Maroc", "Le produit doit etre partageable et impressionnant"],
            ["Fiduciaires = prescripteurs naturels", "Programme partenaire/affiliation obligatoire"],
        ],
        [W*0.45, W*0.55]
    ))

    st.append(Spacer(1, 5*mm))
    st.append(box("Le produit doit vendre le produit. Pas de terrain. Pas de commerciaux.<br/>"
                   "L'utilisateur arrive, upload son Excel, voit le resultat en 30 secondes, et ne peut plus s'en passer."))

    # ══════════ 2. COUTS ══════════
    st.append(Spacer(1, 8*mm))
    st.append(Paragraph("2. Analyse des couts infrastructure", S['section']))
    st.append(tbl(
        ["Composant", "Cout", "Limite gratuite"],
        [
            ["Supabase (DB + Auth)", "0 MAD", "500MB DB, 50K users, 1GB storage"],
            ["Supabase Pro (si depassement)", "250 MAD/mois", "8GB DB, 100K users"],
            ["Vercel (frontend)", "0 MAD", "100GB bandwidth/mois"],
            ["Railway (backend)", "~50 MAD/mois", "$5 credit gratuit"],
            ["Claude API (par rapport IA)", "0.5-2 MAD par appel", "Pay-per-use"],
            ["Resend (emails)", "0 MAD", "3 000 emails/mois"],
            ["Twilio (WhatsApp)", "~0.5 MAD/message", "Pay-per-use"],
        ],
        [W*0.30, W*0.25, W*0.45]
    ))
    st.append(Spacer(1, 3*mm))
    st.append(Paragraph("Cout par palier d'utilisateurs :", S['h3']))
    st.append(tbl(
        ["Palier", "Cout infra/mois", "Cout par user"],
        [
            ["0-1 000 users", "50-300 MAD", "~0.3 MAD/user"],
            ["1 000-10 000 users", "500-2 000 MAD", "~0.2 MAD/user"],
            ["10 000+ users", "2 000-5 000 MAD", "~0.3 MAD/user"],
        ],
        [W*0.33, W*0.33, W*0.34]
    ))
    st.append(Spacer(1, 3*mm))
    st.append(box("Un utilisateur GRATUIT coute ~0 MAD. Le dashboard = requetes SQL sur Supabase gratuit.<br/>"
                   "Pas d'appel IA. Pas de service externe. 10 000 gratuits = ~500 MAD/mois.",
                   bg=GREEN_LIGHT, border=GREEN))

    # ══════════ 3. PRICING ══════════
    st.append(PageBreak())
    st.append(Paragraph("3. Modele Freemium agressif", S['section']))
    st.append(tbl(
        ["", "Gratuit", "Pro (99 MAD/mois)", "Business (249 MAD/mois)"],
        [
            ["Dashboard sectoriel", "Oui", "Oui", "Oui"],
            ["Sources de donnees", "1 fichier", "3 sources", "Illimite + Odoo/Sage"],
            ["Lignes de donnees", "1 000", "20 000", "Illimite"],
            ["KPIs temps reel", "Oui", "Oui", "Oui"],
            ["Charts interactifs", "Oui", "Oui", "Oui"],
            ["Rapports IA", "1 offert", "5/mois", "Illimite"],
            ["Insights IA dashboard", "Non", "Oui", "Oui"],
            ["Alertes", "1", "5", "Illimite"],
            ["Utilisateurs", "1", "3", "20"],
            ["Export PDF", "Non", "Oui", "Oui"],
            ["WhatsApp alerts", "Non", "Oui", "Oui"],
            ["Support", "Communaute", "WhatsApp", "Telephone"],
            ["Prix annuel", "0", "990 MAD/an (-17%)", "2 490 MAD/an (-17%)"],
        ],
        [W*0.22, W*0.22, W*0.28, W*0.28]
    ))
    st.append(Spacer(1, 3*mm))
    st.append(Paragraph("Pourquoi ces prix :", S['h3']))
    for b in [
        "<b>99 MAD/mois</b> = 3.3 MAD/jour = moins qu'un cafe. Decision impulsive, pas reflechie.",
        "<b>249 MAD/mois</b> = moins qu'un stagiaire pour 1 journee. Multi-utilisateurs = le patron + comptable + commercial.",
        "<b>Gratuit genereux</b> = le dashboard complet sans IA. L'utilisateur est accro AVANT de payer.",
        "<b>L'IA est le declencheur de paiement</b> : le 1er rapport gratuit doit etre tellement bon qu'il veut les suivants.",
    ]:
        st.append(Paragraph(f"<bullet>&bull;</bullet> {b}", S['bullet']))

    # ══════════ 4. MODELE HYBRIDE ══════════
    st.append(Spacer(1, 8*mm))
    st.append(Paragraph("4. Modele hybride de revenus", S['section']))
    st.append(tbl(
        ["Source", "Prix", "Cible", "Marge"],
        [
            ["SaaS Gratuit", "0 MAD", "Masse / adoption", "0 (cout ~0)"],
            ["SaaS Pro", "99 MAD/mois", "PMEs autonomes", "~95%"],
            ["SaaS Business", "249 MAD/mois", "PMEs structurees", "~95%"],
            ["Offre Fiduciaire (20 clients)", "1 500 MAD/mois", "Cabinets comptables", "~95%"],
            ["Offre Fiduciaire+ (50 clients)", "3 000 MAD/mois", "Gros cabinets", "~95%"],
            ["Affiliation fiduciaires", "30% commission", "Partenaires en ligne", "70%"],
            ["Annuel Early Bird", "690 MAD/an", "100 premiers", "~95%"],
        ],
        [W*0.28, W*0.18, W*0.30, W*0.24]
    ))

    # ══════════ 5. MOTEURS ══════════
    st.append(PageBreak())
    st.append(Paragraph("5. Les 5 moteurs de croissance (100% digitaux)", S['section']))

    st.append(Paragraph("MOTEUR 1 — L'outil gratuit viral : Analyse Excel instantanee", S['subsection']))
    st.append(box(
        "Page publique pilotbi.ma/analyse-gratuite :<br/>"
        "1. Upload Excel → 2. Entre email → 3. En 60 sec : PDF par email avec 5 KPIs + 3 insights IA + screenshot dashboard<br/>"
        "4. Bouton 'Voir le dashboard complet' → inscription gratuite<br/>"
        "5. Relance J+3 : 'Vos donnees ont change ? Mettez a jour votre dashboard'"
    ))
    st.append(Paragraph("Cout par lead : 1-2 MAD. Le dirigeant partage le PDF avec son comptable = viralite naturelle.", S['body']))

    st.append(Spacer(1, 3*mm))
    st.append(Paragraph("MOTEUR 2 — LinkedIn content (15 min/jour)", S['subsection']))
    st.append(tbl(
        ["Type de post", "Exemple", "Frequence"],
        [
            ["Screenshot reel", "'Dashboard d'un distributeur Casa.\nSon food cost = 42% sans le savoir.'", "2x/semaine"],
            ["Chiffre choc", "'73% des PMEs ne connaissent pas\nleur marge nette. Et vous ?'", "2x/semaine"],
            ["Temoignage", "'Ahmed, distributeur Derb Omar :\n3 produits me faisaient perdre de l'argent'", "1x/semaine"],
            ["Video Loom 1 min", "Screen recording : Excel → Dashboard\nen 30 secondes", "1x/semaine"],
            ["Carrousel educatif", "'5 KPIs que tout restaurateur\nmarocain doit suivre'", "1x/semaine"],
        ],
        [W*0.22, W*0.48, W*0.30]
    ))

    st.append(Spacer(1, 3*mm))
    st.append(Paragraph("MOTEUR 3 — Groupes Facebook & WhatsApp", S['subsection']))
    st.append(Paragraph("C'est LA ou sont les dirigeants PME marocains. Pas sur LinkedIn.", S['body']))
    for g in [
        "'Entrepreneurs Marocains' (50K+ membres)",
        "'PME Maroc' (30K+), 'Commercants Casablanca'",
        "'Restaurateurs Maroc', 'Auto-entrepreneurs Maroc'",
        "Groupes regionaux : 'Business Tanger', 'Entrepreneurs Marrakech'",
    ]:
        st.append(Paragraph(f"<bullet>&bull;</bullet> {g}", S['bullet']))
    st.append(Paragraph("<b>Approche :</b> Poster du contenu utile, repondre aux questions avec des screenshots du dashboard. "
                         "Creer le groupe 'Pilotage PME Maroc'. <b>20 min/jour. Cout : 0 MAD.</b>", S['body']))

    st.append(Spacer(1, 3*mm))
    st.append(Paragraph("MOTEUR 4 — Facebook/Instagram Ads (500-1000 MAD/mois)", S['subsection']))
    st.append(tbl(
        ["Metrique", "Valeur Maroc"],
        [
            ["CPC moyen", "0.5-2 MAD"],
            ["Budget 1000 MAD =", "500-2000 clics"],
            ["Taux inscription", "~20% = 100-400 inscriptions"],
            ["Taux conversion Pro", "~5% = 5-20 clients Pro"],
            ["Revenu genere", "495-1 980 MAD MRR pour 1000 MAD de pub"],
        ],
        [W*0.40, W*0.60]
    ))

    st.append(Spacer(1, 3*mm))
    st.append(Paragraph("MOTEUR 5 — Partenariats fiduciaires en ligne", S['subsection']))
    st.append(box(
        "Email de prospection (20/semaine, automatisable) :<br/><br/>"
        "'Vos clients s'inscrivent via votre lien partenaire. Pour chaque client Pro (99 MAD/mois),<br/>"
        "vous recevez 30% = 30 MAD/mois recurent. Un cabinet avec 30 clients = 900 MAD/mois passifs.<br/>"
        "Vous recevez un acces Fiduciaire gratuit pour gerer tous vos clients.'<br/><br/>"
        "80 emails/mois = 5-10 partenaires en 2 mois.",
        bg=GOLD_LIGHT, border=GOLD
    ))

    # ══════════ 6. PROJECTIONS ══════════
    st.append(PageBreak())
    st.append(Paragraph("6. Projections financieres", S['section']))

    st.append(Paragraph("Scenario conservateur (100% digital, pas de terrain) :", S['h3']))
    st.append(tbl(
        ["Mois", "Inscrits gratuits", "Clients Pro", "Clients Business", "Fiduciaires", "MRR"],
        [
            ["Mois 1", "200-400", "10-20", "2-5", "1-2", "3 000 - 6 500 MAD"],
            ["Mois 2", "600-1 200", "40-80", "8-15", "3-6", "10 000 - 20 000 MAD"],
            ["Mois 3", "1 500-3 000", "80-150", "15-30", "5-10", "20 000 - 40 000 MAD"],
            ["Mois 6", "5 000-8 000", "250-400", "40-70", "10-20", "50 000 - 90 000 MAD"],
            ["Mois 12", "15 000-25 000", "700-1 200", "100-200", "20-40", "140 000 - 260 000 MAD"],
        ],
        [W*0.12, W*0.18, W*0.16, W*0.18, W*0.16, W*0.20]
    ))

    st.append(Spacer(1, 5*mm))
    st.append(Paragraph("Pour atteindre ~50 000 MAD au mois 2 :", S['h3']))
    st.append(tbl(
        ["Source", "Volume", "Unitaire", "Total"],
        [
            ["Early Bird annuel (690 MAD)", "30-50 clients", "690 MAD one-shot", "20 700 - 34 500 MAD"],
            ["SaaS Pro mensuel", "50-80 clients", "99 MAD", "4 950 - 7 920 MAD"],
            ["SaaS Business", "10-15 clients", "249 MAD", "2 490 - 3 735 MAD"],
            ["Fiduciaires", "4-6 partenaires", "2 000 MAD moy.", "8 000 - 12 000 MAD"],
            ["", "", "TOTAL", "36 000 - 58 000 MAD"],
        ],
        [W*0.30, W*0.20, W*0.25, W*0.25]
    ))

    st.append(Spacer(1, 3*mm))
    st.append(box(
        "L'offre Early Bird est l'accelerateur critique : les 100 premiers clients payent l'annuel a -30%.<br/>"
        "690 MAD = 57 MAD/mois. C'est une decision impulsive. 50 clients x 690 = 34 500 MAD en one-shot.",
        bg=GREEN_LIGHT, border=GREEN
    ))

    # ══════════ 7. PLAN EXECUTION ══════════
    st.append(PageBreak())
    st.append(Paragraph("7. Plan d'execution (sans terrain)", S['section']))

    st.append(Paragraph("Pre-lancement (1 semaine) :", S['subsection']))
    st.append(tbl(
        ["Tache", "Qui", "Temps"],
        [
            ["Preparer 12 fichiers Excel demo (1/secteur)", "Chaimae", "3h"],
            ["Filmer 3 videos Loom demo (1 min chacune)", "Chaimae", "1h"],
            ["Creer page LinkedIn PilotBI + optimiser profil", "Chaimae", "1h"],
            ["Rediger 10 posts LinkedIn a programmer", "Vous", "2h"],
            ["Lister 100 fiduciaires sur LinkedIn", "Vous", "2h"],
            ["Preparer pub Facebook (video + carrousel)", "Vous", "2h"],
            ["Rejoindre 10 groupes Facebook PME", "Vous", "30min"],
        ],
        [W*0.55, W*0.20, W*0.25]
    ))

    st.append(Spacer(1, 5*mm))
    st.append(Paragraph("Routine quotidienne apres lancement (35 min/jour) :", S['subsection']))
    st.append(tbl(
        ["Horaire", "Action", "Duree"],
        [
            ["8h (cafe)", "Publier le post LinkedIn du jour", "5 min"],
            ["12h (pause)", "Commentaires LinkedIn + 1 post Facebook groupe", "15 min"],
            ["18h (fin journee)", "5 emails fiduciaires + check inscriptions", "15 min"],
            ["Week-end", "Programmer posts semaine + 1 video Loom", "1h"],
        ],
        [W*0.20, W*0.55, W*0.25]
    ))

    st.append(Spacer(1, 3*mm))
    st.append(box("Total : 35 minutes par jour en semaine + 1 heure le week-end.<br/>"
                   "Compatible avec un emploi a temps plein."))

    # ══════════ 8. EARLY BIRD ══════════
    st.append(Spacer(1, 8*mm))
    st.append(Paragraph("8. Offre Early Bird — Accelerateur de revenus", S['section']))
    st.append(Paragraph(
        "Les <b>100 premiers clients</b> beneficient du plan Pro annuel a <b>690 MAD</b> au lieu de 990 MAD (-30%).",
        S['bold']))
    st.append(Spacer(1, 2*mm))
    for b in [
        "690 MAD/an = 57.5 MAD/mois. C'est le prix d'un sandwich.",
        "Compteur degressif visible sur la landing page ('Plus que 37 places Early Bird').",
        "Urgence + rarete = decision rapide, pas de reflexion.",
        "50 clients Early Bird = 34 500 MAD en cash immediat.",
        "Ces clients deviennent les ambassadeurs (temoignages, referrals).",
    ]:
        st.append(Paragraph(f"<bullet>&bull;</bullet> {b}", S['bullet']))

    # ══════════ 9. SCALABILITE ══════════
    st.append(PageBreak())
    st.append(Paragraph("9. Architecture scalable et securisee", S['section']))

    st.append(Paragraph("Principe : le gratuit ne coute JAMAIS cher", S['h3']))
    st.append(tbl(
        ["Risque", "Protection"],
        [
            ["Trop de requetes DB", "Rate limiting 60 req/min, cache 5 min"],
            ["Abus rapport IA gratuit", "1 seul rapport, lie au compte, non regenerable"],
            ["Fichiers trop gros", "5MB gratuit, 50MB payant"],
            ["Trop de lignes", "Hard limit 1000 gratuit, tronquer au-dela"],
            ["DDoS", "Vercel + Cloudflare en front (gratuit)"],
            ["Pic de charge", "Vercel auto-scale, Railway auto-scale"],
            ["Cout Claude explose", "Budget max/org, file d'attente si surcharge"],
            ["Multi-comptes abus", "Verification email + 1 compte par email"],
        ],
        [W*0.35, W*0.65]
    ))

    st.append(Spacer(1, 5*mm))
    st.append(Paragraph("Stack optimisee pour le cout :", S['h3']))
    st.append(tbl(
        ["Service", "Plan", "Cout"],
        [
            ["Frontend", "Vercel Free", "0 MAD"],
            ["Backend", "Railway Starter", "~50 MAD/mois"],
            ["DB + Auth", "Supabase Free puis Pro", "0 → 250 MAD/mois"],
            ["Cache", "Supabase Edge Functions", "0 MAD"],
            ["IA", "Claude API pay-per-use", "Variable (~1 MAD/rapport)"],
            ["Email", "Resend Free", "0 MAD"],
            ["Monitoring", "Vercel Analytics", "0 MAD"],
        ],
        [W*0.30, W*0.40, W*0.30]
    ))

    # ══════════ 10. FEATURES A IMPLEMENTER ══════════
    st.append(Spacer(1, 8*mm))
    st.append(Paragraph("10. Fonctionnalites pour la viralite", S['section']))
    st.append(tbl(
        ["Fonctionnalite", "Impact", "Priorite"],
        [
            ["Page /analyse-gratuite (upload sans compte)", "Acquisition virale, capture email", "P0"],
            ["Dashboard en temps reel (30 sec)", "Effet WOW immediat", "P0"],
            ["1 rapport IA gratuit offert", "Hook pour convertir en Pro", "P0"],
            ["Offre Early Bird avec compteur", "Urgence, cash immediat", "P0"],
            ["Sequence emails auto (3 emails)", "Nurturing, conversion", "P1"],
            ["Programme affiliation fiduciaires", "Canal multiplicateur", "P1"],
            ["Bouton partage WhatsApp du rapport", "Viralite organique", "P1"],
            ["Feature gating avec upsell contextuel", "Conversion naturelle", "P1"],
            ["Multi-tenant fiduciaire", "Revenue fiduciaire", "P2"],
            ["Dashboard comparatif multi-clients", "Valeur fiduciaire", "P2"],
        ],
        [W*0.40, W*0.35, W*0.25]
    ))

    # ══════════ CLOSING ══════════
    st.append(PageBreak())
    st.append(Spacer(1, 35*mm))
    st.append(Paragraph("Le produit vend le produit.", ParagraphStyle('c1', fontSize=20, leading=26, textColor=BLUE_700, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=12)))
    st.append(Paragraph("Pas de terrain. Pas de commerciaux.<br/>Juste un outil tellement bon que les gens<br/>le partagent d'eux-memes.", ParagraphStyle('c2', fontSize=14, leading=20, textColor=GRAY_700, fontName='Helvetica', alignment=TA_CENTER, spaceAfter=20)))
    st.append(HRFlowable(width="30%", thickness=1, color=GOLD, spaceAfter=15))
    st.append(Paragraph("35 minutes par jour.<br/>0 deplacement.<br/>50 000 MAD en mois 2.", ParagraphStyle('c3', fontSize=16, leading=22, textColor=BLUE_600, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=25)))
    st.append(HRFlowable(width="30%", thickness=1, color=GRAY_200, spaceAfter=15))
    st.append(Paragraph("PilotBI | pilotbi.ma | 2026", ParagraphStyle('cf', fontSize=10, textColor=GRAY_400, fontName='Helvetica', alignment=TA_CENTER)))

    doc.build(st)
    print(f"PDF genere : {path}")

if __name__ == "__main__":
    build()
