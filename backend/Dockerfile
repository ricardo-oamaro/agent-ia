# Etapa 1: build da imagem Python
FROM python:3.11-slim AS backend

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8000 (FastAPI)
EXPOSE 8000

# Define o comando de execução
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]