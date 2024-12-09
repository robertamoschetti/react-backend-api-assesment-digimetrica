# Usa un'immagine Python leggera
FROM python:3.10-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file di configurazione
COPY requirements.txt requirements.txt

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice del backend
COPY . .

# Espone la porta usata da FastAPI
EXPOSE 8000

# Comando per avviare l'app FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
