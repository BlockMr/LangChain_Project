FROM python:3.11.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV ITER=2
ENV API_KEY_OPENAI=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
ENV TG_API=7026319380:AAErNkgGngWwQxFT7mBvcmrchUrfzmf5oGE
CMD ["python", "CharacterSheetBuilder.py"]
