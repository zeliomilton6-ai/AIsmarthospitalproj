MEDI AI — SMART HOSPITAL (BEGINNER PROTOTYPE)

FILES
- app.py: Streamlit hospital appointment and waiting-time demo.
- requirements.txt: Python packages.
- run_windows.bat: Windows installer/launcher.

RUN ON WINDOWS
1. Install Python 3.10 or newer.
2. Extract this ZIP file.
3. Open the extracted MEDI_AI_SMART_HOSPITAL folder.
4. Double-click run_windows.bat.
   OR open Command Prompt in this folder and run:
   py -m pip install -r requirements.txt
   py -m streamlit run app.py
5. Open the local address shown, usually http://localhost:8501.

SAFETY
This is an educational prototype, not a production hospital system.
Use fictional/demo data only. The SQLite database is not encrypted or access-controlled.
The waiting-time model uses synthetic data and is not validated for real operations.
Never use its estimates for triage, clinical decisions, or delaying urgent care.
Real deployment needs professional clinical, privacy, security and technical review,
authentication, access controls, encryption, backups, audit logs and model validation.
