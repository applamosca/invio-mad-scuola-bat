# Invio PEC MAD – Scuole della Provincia BAT

Script automatizzato per l'invio di **Messa a Disposizione (MAD)** via PEC alle scuole della provincia BAT, con due template differenziati e 16 allegati professionali.

## Struttura del Repository

```
invio-mad-scuola-bat/
├── .github/workflows/
│   └── invio-mad.yml          # Workflow GitHub Actions (cron 06:45 UTC)
├── allegati/                   # Cartella per i 16 file professionali
│   ├── Curriculum_Vitae_Danzi.pdf
│   ├── Attestato_Diploma.jpg
│   ├── Cisco_CCNA.pdf
│   ├── Cisco_Wireless.pdf
│   ├── Comptia_A_plus.jpg
│   ├── ECC_Evaluation.pdf
│   ├── ECDL_Update.pdf
│   ├── Ethical_Hacker_CEH.pdf
│   ├── EXIN_Privacy.pdf
│   ├── ICDL_Base.pdf
│   ├── ICDL_Essentials.pdf
│   ├── ICDL_Security.pdf
│   ├── ICDL_Standard.pdf
│   ├── microsoft.PDF
│   ├── OSINT_Analysis.pdf
│   └── vmware.pdf
├── lista_scuole.txt            # Lista delle 20 PEC destinatarie
├── invio_mad.py                # Script Python principale
└── README.md
```

## Configurazione

### 1. Caricare gli allegati

Copiare i 16 file professionali nella cartella `allegati/` del repository.

### 2. Impostare il Secret della password PEC

1. Vai su **Settings** → **Secrets and variables** → **Actions**
2. Clicca **New repository secret**
3. Nome: `PEC_PASSWORD`
4. Valore: la password della PEC `danzi.antonio@pec.it`

### 3. Attivare il workflow

Il workflow si attiva automaticamente ogni giorno alle **06:45 UTC** (07:45 ora italiana).

Per un'esecuzione manuale: vai su **Actions** → **Invio PEC MAD Scuole BAT** → **Run workflow**.

## Template Email

| Destinatario | Template | Oggetto |
|---|---|---|
| BTIS046002 (I.I.S.S. De Nittis – Dir. Diviccaro) | Formale | Disponibilità professionale per supplenze brevi e supporto transizione digitale |
| Tutte le altre 19 scuole | Tecnico/Business | MAD Assistente Tecnico/Docente - Ing. Informatico - Esperto Cybersecurity e Reti |

## Sicurezza

- La password PEC è gestita tramite **GitHub Secrets** e non è mai presente nel codice
- Il server SMTP utilizza connessione **SSL** (porta 465)
- Delay di **120 secondi** tra ogni invio per evitare blocchi anti-spam di Aruba
