# Istruzioni di Setup Completo – Invio PEC MAD Scuole BAT

## Stato attuale del repository

Il repository privato **applamosca/invio-mad-scuola-bat** è stato creato e contiene:

| File | Stato | Descrizione |
|---|---|---|
| `invio_mad.py` | Pushato | Script Python principale con i 2 template |
| `lista_scuole.txt` | Pushato | Lista delle 20 PEC delle scuole BAT |
| `allegati/.gitkeep` | Pushato | Cartella pronta per i 16 allegati |
| `README.md` | Pushato | Documentazione del progetto |
| `.github/workflows/invio-mad.yml` | Da aggiungere manualmente | Workflow GitHub Actions |

## Passaggio 1: Aggiungere il file Workflow (obbligatorio)

Il file `.github/workflows/invio-mad.yml` non può essere pushato da questa sandbox per limiti di permessi GitHub. Devi aggiungerlo manualmente.

### Opzione A – Tramite interfaccia web GitHub

1. Vai su https://github.com/applamosca/invio-mad-scuola-bat
2. Clicca **Add file** → **Create new file**
3. Nel campo del nome file scrivi: `.github/workflows/invio-mad.yml`
4. Incolla il contenuto seguente:

```yaml
name: Invio PEC MAD Scuole BAT

on:
  # Esecuzione automatica alle 06:45 UTC (07:45 ora italiana)
  schedule:
    - cron: '45 6 * * *'

  # Esecuzione manuale dal pannello GitHub Actions
  workflow_dispatch:

jobs:
  invio-mad:
    name: Invio PEC MAD
    runs-on: ubuntu-latest
    timeout-minutes: 60

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Verifica struttura file
        run: |
          echo "=== Verifica lista scuole ==="
          cat lista_scuole.txt
          echo ""
          echo "=== Verifica allegati ==="
          ls -la allegati/
          echo ""
          echo "=== Conteggio allegati ==="
          ls allegati/ | wc -l

      - name: Esegui script invio PEC MAD
        env:
          PEC_PASSWORD: ${{ secrets.PEC_PASSWORD }}
        run: python3 invio_mad.py

      - name: Carica log come artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: log-invio-mad-${{ github.run_number }}
          path: invio_mad.log
          retention-days: 30
```

5. Clicca **Commit changes**

### Opzione B – Tramite git dalla tua macchina locale

```bash
cd invio-mad-scuola-bat
mkdir -p .github/workflows
# Crea il file invio-mad.yml con il contenuto sopra
git add .github/workflows/invio-mad.yml
git commit -m "Aggiunta workflow GitHub Actions"
git push origin master
```

## Passaggio 2: Caricare i 16 allegati

Dalla tua cartella locale `C:\Users\Antonio\OneDrive\Desktop\script mad scuola`, carica i 16 file nella cartella `allegati/` del repository.

### Tramite interfaccia web GitHub

1. Vai su https://github.com/applamosca/invio-mad-scuola-bat
2. Clicca sulla cartella **allegati**
3. Clicca **Add file** → **Upload files**
4. Trascina tutti i 16 file:
   - `Curriculum_Vitae_Danzi.pdf`
   - `Attestato_Diploma.jpg`
   - `Cisco_CCNA.pdf`
   - `Cisco_Wireless.pdf`
   - `Comptia_A_plus.jpg`
   - `ECC_Evaluation.pdf`
   - `ECDL_Update.pdf`
   - `Ethical_Hacker_CEH.pdf`
   - `EXIN_Privacy.pdf`
   - `ICDL_Base.pdf`
   - `ICDL_Essentials.pdf`
   - `ICDL_Security.pdf`
   - `ICDL_Standard.pdf`
   - `microsoft.PDF`
   - `OSINT_Analysis.pdf`
   - `vmware.pdf`
5. Clicca **Commit changes**

## Passaggio 3: Impostare il Secret PEC_PASSWORD

1. Vai su https://github.com/applamosca/invio-mad-scuola-bat/settings/secrets/actions
2. Clicca **New repository secret**
3. Nome: `PEC_PASSWORD`
4. Valore: la tua password della PEC `danzi.antonio@pec.it`
5. Clicca **Add secret**

## Passaggio 4: Verifica e test

1. Vai su https://github.com/applamosca/invio-mad-scuola-bat/actions
2. Dovresti vedere il workflow **Invio PEC MAD Scuole BAT**
3. Clicca su **Run workflow** → **Run workflow** per un test manuale
4. Controlla i log per verificare che tutto funzioni

## Riepilogo funzionamento

| Parametro | Valore |
|---|---|
| PEC mittente | `danzi.antonio@pec.it` |
| Server SMTP | `smtps.pec.aruba.it:465` (SSL) |
| Scuole destinatarie | 20 PEC della provincia BAT |
| Template Formale | Solo per `BTIS046002` (Dir. Diviccaro) |
| Template Tecnico | Per le altre 19 scuole |
| Cron | Ogni giorno alle 06:45 UTC (07:45 italiane) |
| Delay anti-spam | 120 secondi tra ogni invio |
| Allegati | 16 file professionali |
| Tempo totale stimato | ~40 minuti (20 scuole x 120s) |
