from fastapi import FastAPI,HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import csv
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/report")
async def get_report():
    try:
        with open("summary2.0.json", "r") as file:
            data = json.load(file)

        return data
    except FileNotFoundError:
        return {"status": "error", "message": "File not found"}
    except json.JSONDecodeError:
        return {"status": "error", "message": "Failed to decode JSON"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/download-csv")
async def download_csv():
    try:
        # Legge il file JSON
        with open("summary2.0.json", "r") as file:
            data = json.load(file)

        # Creazione di un buffer in memoria per il CSV
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)

        # Determina le chiavi uniche (intestazioni) da tutti gli oggetti
        headers = set()
        for item in data["results"]:
            headers.update(item.keys())
        headers = sorted(headers)  # Ordine alfabetico o personalizzato, se necessario

        # Scrive l'intestazione
        csv_writer.writerow(headers)

        # Scrive i dati per ogni oggetto, garantendo l'allineamento con le intestazioni
        for item in data["results"]:
            row = [item.get(key, "") for key in headers]  # Usa `""` per i campi mancanti
            csv_writer.writerow(row)

        # Reimposta il puntatore all'inizio del buffer
        csv_buffer.seek(0)

        # Restituisce il CSV come risposta scaricabile
        response = StreamingResponse(
            csv_buffer,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=report.csv"},
        )
        return response

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Il file JSON non è stato trovato.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Errore nella decodifica del JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore generico: {str(e)}")