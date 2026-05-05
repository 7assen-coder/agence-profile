from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import mysql.connector
import qrcode
import os
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io

app = Flask(__name__)
app.secret_key = 'agence_secret_key_2024'

# ─────────────────────────────────────────────
# CONFIG BASE DE DONNÉES
# ─────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',          # ← Mets ton mot de passe ici si tu en as un
    'database': 'voyage_mr'  # ← Mets le nom exact de ta base ici
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# ─────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────
@app.route('/')
def home():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM reservations")
    stats_res = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) as total FROM clients")
    stats_clients = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) as total FROM trajets")
    stats_trajets = cursor.fetchone()
    cursor.execute("""
        SELECT t.id_trajet, v1.nom_ville as depart, v2.nom_ville as arrivee,
               t.date_depart, t.heure_depart, t.prix
        FROM trajets t
        JOIN villes v1 ON t.id_ville_depart = v1.id_ville
        JOIN villes v2 ON t.id_ville_arrivee = v2.id_ville
        ORDER BY t.date_depart ASC LIMIT 6
    """)
    trajets = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('home.html',
                           stats_res=stats_res['total'],
                           stats_clients=stats_clients['total'],
                           stats_trajets=stats_trajets['total'],
                           trajets=trajets)


# ─────────────────────────────────────────────
# RÉSERVATION
# ─────────────────────────────────────────────
@app.route('/reserver', methods=['GET', 'POST'])
def reserver():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        id_client  = request.form['id_client']
        id_trajet  = request.form['id_trajet']
        id_place   = request.form['id_place']

        # Vérifier si la place est disponible
        cursor.execute("SELECT statut FROM places WHERE id_place = %s", (id_place,))
        place = cursor.fetchone()
        if not place or place['statut'] != 'disponible':
            flash('Cette place n\'est plus disponible.', 'error')
            return redirect(url_for('reserver'))

        # Créer la réservation
        cursor.execute("""
            INSERT INTO reservations (id_client, id_place, id_trajet, statut)
            VALUES (%s, %s, %s, 'en_attente')
        """, (id_client, id_place, id_trajet))
        db.commit()
        id_reservation = cursor.lastrowid

        # Marquer la place comme réservée
        cursor.execute("UPDATE places SET statut = 'reserve' WHERE id_place = %s", (id_place,))
        db.commit()
        cursor.close()
        db.close()

        flash('Réservation créée avec succès !', 'success')
        return redirect(url_for('paiement', id_reservation=id_reservation))

    # GET — charger les données pour le formulaire
    cursor.execute("SELECT id_client, nom, prenom FROM clients ORDER BY nom")
    clients = cursor.fetchall()

    cursor.execute("""
        SELECT t.id_trajet, v1.nom_ville as depart, v2.nom_ville as arrivee,
               t.date_depart, t.heure_depart, t.prix
        FROM trajets t
        JOIN villes v1 ON t.id_ville_depart = v1.id_ville
        JOIN villes v2 ON t.id_ville_arrivee = v2.id_ville
        ORDER BY t.date_depart ASC
    """)
    trajets = cursor.fetchall()

    cursor.execute("SELECT id_place, numero_place FROM places WHERE statut = 'disponible' ORDER BY numero_place")
    places = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template('book.html', clients=clients, trajets=trajets, places=places)


# ─────────────────────────────────────────────
# PAIEMENT
# ─────────────────────────────────────────────
@app.route('/paiement/<int:id_reservation>', methods=['GET', 'POST'])
def paiement(id_reservation):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Charger les infos de la réservation
    cursor.execute("""
        SELECT r.id_reservation, r.statut,
               c.nom, c.prenom, c.email,
               p.numero_place,
               v1.nom_ville as depart, v2.nom_ville as arrivee,
               t.date_depart, t.heure_depart, t.prix,
               a.nom_agence
        FROM reservations r
        JOIN clients c ON r.id_client = c.id_client
        JOIN places p ON r.id_place = p.id_place
        JOIN trajets t ON r.id_trajet = t.id_trajet
        JOIN villes v1 ON t.id_ville_depart = v1.id_ville
        JOIN villes v2 ON t.id_ville_arrivee = v2.id_ville
        JOIN agences a ON t.id_agence = a.id_agence
        WHERE r.id_reservation = %s
    """, (id_reservation,))
    reservation = cursor.fetchone()

    if not reservation:
        flash('Réservation introuvable.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        mode_paiement = request.form['mode_paiement']
        montant = reservation['prix']

        # Créer le paiement
        cursor.execute("""
            INSERT INTO paiements (id_client, montant, mode_paiement, statut)
            SELECT id_client, %s, %s, 'confirme' FROM reservations WHERE id_reservation = %s
        """, (montant, mode_paiement, id_reservation))
        db.commit()
        id_paiement = cursor.lastrowid

        # Mettre à jour la réservation
        cursor.execute("""
            UPDATE reservations SET statut = 'confirmee', id_paiement = %s
            WHERE id_reservation = %s
        """, (id_paiement, id_reservation))
        db.commit()

        # ── Générer le ticket ──
        code_ticket = 'TKT-' + str(uuid.uuid4()).upper()[:12]

        # Générer le QR code
        qr_data = f"code_ticket:{code_ticket}|id_reservation:{id_reservation}"
        qr_img = qrcode.make(qr_data)
        qr_folder = os.path.join('static', 'qrcodes')
        os.makedirs(qr_folder, exist_ok=True)
        qr_path = os.path.join(qr_folder, f'{code_ticket}.png')
        qr_img.save(qr_path)

        # Insérer le ticket en DB
        cursor.execute("""
            INSERT INTO tickets (reservation_id, code_ticket, qr_code_path, statut)
            VALUES (%s, %s, %s, 'valide')
        """, (id_reservation, code_ticket, qr_path))
        db.commit()
        id_ticket = cursor.lastrowid

        cursor.close()
        db.close()

        flash('Paiement confirmé ! Votre ticket a été généré.', 'success')
        return redirect(url_for('ticket', id_res=id_reservation))

    cursor.close()
    db.close()
    return render_template('payment.html', reservation=reservation)


# ─────────────────────────────────────────────
# TICKET (page HTML)
# ─────────────────────────────────────────────
@app.route('/ticket/<int:id_res>')
def ticket(id_res):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT tk.id, tk.code_ticket, tk.qr_code_path, tk.statut, tk.date_generation,
               c.nom, c.prenom,
               p.numero_place,
               v1.nom_ville as depart, v2.nom_ville as arrivee,
               t.date_depart, t.heure_depart,
               a.nom_agence,
               r.id_reservation
        FROM tickets tk
        JOIN reservations r ON tk.reservation_id = r.id_reservation
        JOIN clients c ON r.id_client = c.id_client
        JOIN places p ON r.id_place = p.id_place
        JOIN trajets t ON r.id_trajet = t.id_trajet
        JOIN villes v1 ON t.id_ville_depart = v1.id_ville
        JOIN villes v2 ON t.id_ville_arrivee = v2.id_ville
        JOIN agences a ON t.id_agence = a.id_agence
        WHERE r.id_reservation = %s
        ORDER BY tk.id DESC LIMIT 1
    """, (id_res,))
    ticket_data = cursor.fetchone()
    cursor.close()
    db.close()

    if not ticket_data:
        flash('Ticket introuvable.', 'error')
        return redirect(url_for('home'))

    return render_template('ticket.html', ticket=ticket_data)


# ─────────────────────────────────────────────
# TÉLÉCHARGER LE TICKET EN PDF
# ─────────────────────────────────────────────
@app.route('/ticket/<int:id_res>/pdf')
def ticket_pdf(id_res):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT tk.code_ticket, tk.qr_code_path, tk.statut, tk.date_generation,
               c.nom, c.prenom,
               p.numero_place,
               v1.nom_ville as depart, v2.nom_ville as arrivee,
               t.date_depart, t.heure_depart, t.prix,
               a.nom_agence,
               r.id_reservation
        FROM tickets tk
        JOIN reservations r ON tk.reservation_id = r.id_reservation
        JOIN clients c ON r.id_client = c.id_client
        JOIN places p ON r.id_place = p.id_place
        JOIN trajets t ON r.id_trajet = t.id_trajet
        JOIN villes v1 ON t.id_ville_depart = v1.id_ville
        JOIN villes v2 ON t.id_ville_arrivee = v2.id_ville
        JOIN agences a ON t.id_agence = a.id_agence
        WHERE r.id_reservation = %s
        ORDER BY tk.id DESC LIMIT 1
    """, (id_res,))
    d = cursor.fetchone()
    cursor.close()
    db.close()

    if not d:
        flash('Ticket introuvable.', 'error')
        return redirect(url_for('home'))

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  fontSize=22, textColor=colors.HexColor('#1a3c6e'),
                                  spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold')
    sub_style  = ParagraphStyle('Sub', parent=styles['Normal'],
                                 fontSize=11, textColor=colors.HexColor('#555555'),
                                 alignment=TA_CENTER, spaceAfter=20)
    label_style = ParagraphStyle('Label', parent=styles['Normal'],
                                  fontSize=10, textColor=colors.HexColor('#888888'),
                                  fontName='Helvetica')
    value_style = ParagraphStyle('Value', parent=styles['Normal'],
                                  fontSize=12, textColor=colors.HexColor('#1a1a1a'),
                                  fontName='Helvetica-Bold')

    elements = []

    # En-tête
    elements.append(Paragraph(d['nom_agence'].upper(), title_style))
    elements.append(Paragraph('TICKET DE VOYAGE', sub_style))
    elements.append(Spacer(1, 0.3*cm))

    # Ligne de séparation visuelle via tableau coloré
    header_table = Table([['']], colWidths=[17*cm], rowHeights=[0.3*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1a3c6e')),
        ('LINEABOVE', (0,0), (-1,-1), 2, colors.HexColor('#1a3c6e')),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.5*cm))

    # Trajet
    trajet_text = f"{d['depart'].upper()}  →  {d['arrivee'].upper()}"
    trajet_style = ParagraphStyle('Trajet', parent=styles['Normal'],
                                   fontSize=20, textColor=colors.HexColor('#1a3c6e'),
                                   fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)
    elements.append(Paragraph(trajet_text, trajet_style))
    elements.append(Spacer(1, 0.4*cm))

    # Informations du ticket dans un tableau
    date_str = d['date_depart'].strftime('%d/%m/%Y') if hasattr(d['date_depart'], 'strftime') else str(d['date_depart'])
    heure_str = str(d['heure_depart'])[:5]

    data = [
        [Paragraph('PASSAGER', label_style),   Paragraph(f"{d['prenom']} {d['nom']}", value_style),
         Paragraph('N° PLACE', label_style),    Paragraph(str(d['numero_place']), value_style)],
        [Paragraph('DATE', label_style),        Paragraph(date_str, value_style),
         Paragraph('HEURE', label_style),       Paragraph(heure_str, value_style)],
        [Paragraph('RÉSERVATION N°', label_style), Paragraph(str(d['id_reservation']), value_style),
         Paragraph('PRIX', label_style),        Paragraph(f"{d['prix']} MRU", value_style)],
        [Paragraph('CODE TICKET', label_style), Paragraph(d['code_ticket'], value_style),
         Paragraph('STATUT', label_style),      Paragraph(d['statut'].upper(), value_style)],
    ]

    info_table = Table(data, colWidths=[4*cm, 5*cm, 3.5*cm, 4.5*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9ff')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#f8f9ff'), colors.white]),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dddddd')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.8*cm))

    # QR Code
    if d['qr_code_path'] and os.path.exists(d['qr_code_path']):
        qr_section = []
        qr_img = RLImage(d['qr_code_path'], width=4*cm, height=4*cm)
        qr_label = Paragraph('Scannez pour vérifier', ParagraphStyle('QRLabel',
                              parent=styles['Normal'], fontSize=9,
                              textColor=colors.HexColor('#888888'), alignment=TA_CENTER))
        qr_table = Table([[qr_img], [qr_label]], colWidths=[5*cm])
        qr_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))

        full_row = Table([[info_table if False else '', qr_table]], colWidths=[12*cm, 5*cm])
        elements.append(Spacer(1, -8.5*cm))
        # Place QR à droite séparément
        elements.append(Spacer(1, 8.5*cm))
        elements.append(qr_table)

    # Pied de page
    elements.append(Spacer(1, 0.8*cm))
    footer_table = Table([['']], colWidths=[17*cm], rowHeights=[0.3*cm])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1a3c6e')),
    ]))
    elements.append(footer_table)
    elements.append(Spacer(1, 0.3*cm))

    generated = d['date_generation'].strftime('%d/%m/%Y à %H:%M') if hasattr(d['date_generation'], 'strftime') else str(d['date_generation'])
    footer_text = f"Ticket généré le {generated} — Merci de voyager avec {d['nom_agence']}"
    elements.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'],
                               fontSize=8, textColor=colors.HexColor('#aaaaaa'), alignment=TA_CENTER)))

    doc.build(elements)
    buffer.seek(0)
    filename = f"ticket_{d['code_ticket']}.pdf"
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')


# ─────────────────────────────────────────────
# DASHBOARD ADMIN
# ─────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM reservations")
    total_reservations = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM reservations WHERE statut = 'confirmee'")
    total_confirmees = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM tickets")
    total_tickets = cursor.fetchone()['total']

    cursor.execute("SELECT SUM(montant) as total FROM paiements WHERE statut = 'confirme'")
    total_revenus = cursor.fetchone()['total'] or 0

    cursor.execute("""
        SELECT r.id_reservation, c.nom, c.prenom,
               v1.nom_ville as depart, v2.nom_ville as arrivee,
               t.date_depart, r.statut, r.date_reservation,
               tk.code_ticket
        FROM reservations r
        JOIN clients c ON r.id_client = c.id_client
        JOIN trajets t ON r.id_trajet = t.id_trajet
        JOIN villes v1 ON t.id_ville_depart = v1.id_ville
        JOIN villes v2 ON t.id_ville_arrivee = v2.id_ville
        LEFT JOIN tickets tk ON tk.reservation_id = r.id_reservation
        ORDER BY r.date_reservation DESC
        LIMIT 20
    """)
    reservations = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('dashboard.html',
                           total_reservations=total_reservations,
                           total_confirmees=total_confirmees,
                           total_tickets=total_tickets,
                           total_revenus=total_revenus,
                           reservations=reservations)


# ─────────────────────────────────────────────
# DONNÉES DE TEST (route pour initialiser la DB)
# ─────────────────────────────────────────────
@app.route('/init-db')
def init_db():
    db = get_db()
    cursor = db.cursor()
    try:
        # Villes
        cursor.execute("INSERT IGNORE INTO villes (id_ville, nom_ville) VALUES (1,'Nouakchott'),(2,'Nouadhibou'),(3,'Rosso'),(4,'Kaédi')")
        # Agences
        cursor.execute("INSERT IGNORE INTO agences (id_agence, nom_agence) VALUES (1,'Agence Sahara Express')")
        # Bus
        cursor.execute("INSERT IGNORE INTO bus (id_bus, numero_bus, capacite) VALUES (1,'BUS-001',30)")
        # Trajets
        cursor.execute("""INSERT IGNORE INTO trajets (id_trajet, id_ville_depart, id_ville_arrivee, date_depart, heure_depart, prix, id_agence, id_bus)
                          VALUES (1,1,2,'2025-06-10','08:00:00',1500,1,1),
                                 (2,1,3,'2025-06-11','09:30:00',800,1,1),
                                 (3,2,4,'2025-06-12','07:00:00',1200,1,1)""")
        # Places
        for i in range(1, 13):
            cursor.execute(f"INSERT IGNORE INTO places (id_place, numero_place, statut) VALUES ({i},{i},'disponible')")
        # Clients
        cursor.execute("""INSERT IGNORE INTO clients (id_client, nom, prenom, email, telephone)
                          VALUES (1,'Diallo','Aminata','aminata@mail.mr','22212345678'),
                                 (2,'Ba','Moussa','moussa@mail.mr','22287654321'),
                                 (3,'Ould Ahmed','Fatima','fatima@mail.mr','22211223344')""")
        db.commit()
        cursor.close()
        db.close()
        return '<h2 style="font-family:sans-serif;color:green">✅ Base de données initialisée avec succès ! <a href="/">← Retour accueil</a></h2>'
    except Exception as e:
        db.rollback()
        return f'<h2 style="color:red">Erreur: {str(e)}</h2>'


if __name__ == '__main__':
    app.run(debug=True)
