#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per l'invio automatico di PEC MAD alle scuole della provincia BAT.
- Template A (Formale): per il Dirigente Diviccaro (BTIS046002)
- Template B (Tecnico/Business): per tutte le altre scuole
- SMTP Aruba PEC: smtps.pec.aruba.it:465 (SSL)
- Delay di 120 secondi tra un invio e l'altro
"""

import os
import sys
import time
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# ──────────────────────────────────────────────
# CONFIGURAZIONE LOGGING
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("invio_mad.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# CONFIGURAZIONE SMTP ARUBA PEC
# ──────────────────────────────────────────────
SMTP_SERVER = "smtps.pec.aruba.it"
SMTP_PORT = 465
PEC_MITTENTE = "danzi.antonio@pec.it"
PEC_PASSWORD = os.environ.get("PEC_PASSWORD")

if not PEC_PASSWORD:
    logger.error("La variabile d'ambiente PEC_PASSWORD non e' impostata. Interruzione.")
    sys.exit(1)

# ──────────────────────────────────────────────
# SCUOLA SPECIALE (Template Formale)
# ──────────────────────────────────────────────
CODICE_DIVICCARO = "BTIS046002"

# ──────────────────────────────────────────────
# DELAY TRA UN INVIO E L'ALTRO (secondi)
# ──────────────────────────────────────────────
DELAY_SECONDI = 120

# ──────────────────────────────────────────────
# CARTELLA ALLEGATI
# ──────────────────────────────────────────────
CARTELLA_ALLEGATI = Path(__file__).parent / "allegati"

LISTA_ALLEGATI = [
    "Curriculum_Vitae_Danzi.pdf",
    "Attestato_Diploma.jpg",
    "Cisco_CCNA.pdf",
    "Cisco_Wireless.pdf",
    "Comptia_A_plus.jpg",
    "ECC_Evaluation.pdf",
    "ECDL_Update.pdf",
    "Ethical_Hacker_CEH.pdf",
    "EXIN_Privacy.pdf",
    "ICDL_Base.pdf",
    "ICDL_Essentials.pdf",
    "ICDL_Security.pdf",
    "ICDL_Standard.pdf",
    "microsoft.PDF",
    "OSINT_Analysis.pdf",
    "vmware.pdf",
]

# ──────────────────────────────────────────────
# TEMPLATE A – FORMALE (Dirigente Diviccaro)
# ──────────────────────────────────────────────
OGGETTO_FORMALE = (
    "Disponibilita' professionale per supplenze brevi e supporto transizione "
    "digitale - Ing. Antonio Danzi (Classe A041/B016)"
)

TESTO_FORMALE = """\
Gentile Dirigente Scolastico Prof. Antonio Francesco Diviccaro,

in qualita' di Ingegnere Informatico (Laurea Magistrale 2025) ed esperto in \
Cybersecurity, sottopongo alla Sua attenzione il mio profilo, avendo scelto \
il Vostro Istituto nelle Graduatorie Provinciali di Supplenza \
(Protocollo: m_pi.AOOPOLIS.REGISTRO UFFICIALE.I.17717763.15-03-2026).

Consapevole della complessita' gestionale di un istituto di prestigio come \
il De Nittis, confermo la mia immediata disponibilita' per supplenze brevi \
e per supportare l'Istituto in progetti di sicurezza informatica e \
resilienza delle reti.

In allegato il Curriculum Vitae e il portfolio certificazioni.

Cordiali saluti,
Ing. Antonio Danzi
danzi.antonio@pec.it
"""

# ──────────────────────────────────────────────
# TEMPLATE B – TECNICO/BUSINESS (Altre scuole)
# ──────────────────────────────────────────────
OGGETTO_TECNICO = (
    "MAD Assistente Tecnico/Docente | Ing. Informatico | "
    "Esperto Cybersecurity e Reti | Residente a Barletta"
)

TESTO_TECNICO = """\
Alla cortese attenzione del Dirigente Scolastico e del DSGA,

sono l'Ing. Antonio Danzi, titolare di AssistenzaBAT.it e specialista in \
Cybersecurity e VoIP. Oltre alla docenza per le classi A041/B016, offro la \
mia competenza per la gestione operativa dei laboratori e la messa in \
sicurezza delle infrastrutture di rete dell'Istituto.

Risiedo a Barletta e garantisco massima tempestivita' per coprire urgenze o \
progetti speciali di automazione AI.

Appartengo alle Categorie Protette (L. 68/99) e sono automunito.

In allegato la documentazione tecnica e il CV.

Cordiali saluti,
Ing. Antonio Danzi
danzi.antonio@pec.it
AssistenzaBAT.it
"""


def carica_lista_scuole(percorso: str = "lista_scuole.txt") -> list[str]:
    """Legge il file lista_scuole.txt e restituisce una lista di indirizzi PEC."""
    file_path = Path(__file__).parent / percorso
    if not file_path.exists():
        logger.error("File %s non trovato!", file_path)
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        scuole = [line.strip() for line in f if line.strip()]

    logger.info("Caricate %d scuole da %s", len(scuole), percorso)
    return scuole


def identifica_codice_meccanografico(email: str) -> str:
    """Estrae il codice meccanografico dall'indirizzo PEC della scuola."""
    return email.split("@")[0].upper()


def seleziona_template(email: str) -> tuple[str, str]:
    """Restituisce (oggetto, testo) in base alla scuola destinataria."""
    codice = identifica_codice_meccanografico(email)
    if codice == CODICE_DIVICCARO:
        logger.info("  -> Template FORMALE selezionato (Dirigente Diviccaro)")
        return OGGETTO_FORMALE, TESTO_FORMALE
    else:
        logger.info("  -> Template TECNICO/BUSINESS selezionato")
        return OGGETTO_TECNICO, TESTO_TECNICO


def allega_file(msg: MIMEMultipart) -> int:
    """Allega tutti i 16 file professionali al messaggio. Restituisce il conteggio."""
    allegati_ok = 0
    for nome_file in LISTA_ALLEGATI:
        percorso_file = CARTELLA_ALLEGATI / nome_file
        if not percorso_file.exists():
            logger.warning("  Allegato non trovato: %s (saltato)", nome_file)
            continue

        with open(percorso_file, "rb") as f:
            parte = MIMEBase("application", "octet-stream")
            parte.set_payload(f.read())
            encoders.encode_base64(parte)
            parte.add_header(
                "Content-Disposition",
                f'attachment; filename="{nome_file}"',
            )
            msg.attach(parte)
            allegati_ok += 1
            logger.info("  Allegato: %s", nome_file)

    return allegati_ok


def costruisci_email(destinatario: str) -> MIMEMultipart:
    """Costruisce il messaggio email completo con template e allegati."""
    oggetto, testo = seleziona_template(destinatario)

    msg = MIMEMultipart()
    msg["From"] = PEC_MITTENTE
    msg["To"] = destinatario
    msg["Subject"] = oggetto

    msg.attach(MIMEText(testo, "plain", "utf-8"))

    num_allegati = allega_file(msg)
    logger.info("  Allegati inclusi: %d/%d", num_allegati, len(LISTA_ALLEGATI))

    return msg


def invia_email(server: smtplib.SMTP_SSL, msg: MIMEMultipart, destinatario: str) -> bool:
    """Invia una singola email tramite il server SMTP. Restituisce True se OK."""
    try:
        server.sendmail(PEC_MITTENTE, destinatario, msg.as_string())
        logger.info("  Email inviata con successo a %s", destinatario)
        return True
    except smtplib.SMTPException as e:
        logger.error("  Errore invio a %s: %s", destinatario, str(e))
        return False


def main():
    """Funzione principale: carica le scuole, si connette a SMTP e invia le PEC."""
    logger.info("=" * 60)
    logger.info("AVVIO INVIO PEC MAD - Scuole BAT")
    logger.info("=" * 60)

    scuole = carica_lista_scuole()

    # Verifica allegati disponibili
    allegati_presenti = [f for f in LISTA_ALLEGATI if (CARTELLA_ALLEGATI / f).exists()]
    allegati_mancanti = [f for f in LISTA_ALLEGATI if not (CARTELLA_ALLEGATI / f).exists()]

    logger.info("Allegati trovati: %d/%d", len(allegati_presenti), len(LISTA_ALLEGATI))
    if allegati_mancanti:
        logger.warning("Allegati mancanti: %s", ", ".join(allegati_mancanti))

    # Connessione SMTP SSL
    logger.info("Connessione a %s:%d ...", SMTP_SERVER, SMTP_PORT)
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=60)
        server.login(PEC_MITTENTE, PEC_PASSWORD)
        logger.info("Login SMTP riuscito per %s", PEC_MITTENTE)
    except smtplib.SMTPAuthenticationError:
        logger.error("Autenticazione SMTP fallita. Verifica PEC_PASSWORD.")
        sys.exit(1)
    except Exception as e:
        logger.error("Errore connessione SMTP: %s", str(e))
        sys.exit(1)

    # Invio a ciascuna scuola
    inviate = 0
    fallite = 0

    for i, destinatario in enumerate(scuole, start=1):
        logger.info("-" * 50)
        logger.info("Invio %d/%d -> %s", i, len(scuole), destinatario)

        msg = costruisci_email(destinatario)
        successo = invia_email(server, msg, destinatario)

        if successo:
            inviate += 1
        else:
            fallite += 1

        # Delay anti-spam (tranne dopo l'ultimo invio)
        if i < len(scuole):
            logger.info("  Attesa %d secondi (anti-spam)...", DELAY_SECONDI)
            time.sleep(DELAY_SECONDI)

    # Chiusura connessione
    try:
        server.quit()
        logger.info("Connessione SMTP chiusa.")
    except Exception:
        pass

    # Riepilogo finale
    logger.info("=" * 60)
    logger.info("RIEPILOGO INVIO PEC MAD")
    logger.info("  Totale scuole:  %d", len(scuole))
    logger.info("  Inviate:        %d", inviate)
    logger.info("  Fallite:        %d", fallite)
    logger.info("=" * 60)

    if fallite > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
