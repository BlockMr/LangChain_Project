FROM python:3.11.0
WORKDIR /app
COPY /requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV ITER=2
ENV API_KEY_OPENAI=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
ENV USER=postgres
ENV DB_NAME=dnd
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=dnd
ENV PASS=qawsed
ENV TG_API=7026319380:AAErNkgGngWwQxFT7mBvcmrchUrfzmf5oGE
CMD ["python", "CharacterSheetBuilder.py"]
