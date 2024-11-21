FROM python:3.11.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV ITER=2
ENV API_KEY_OPENAI=
ENV TG_API=7026319380:AAErNkgGngWwQxFT7mBvcmrchUrfzmf5oGE
CMD ["python", "CharacterSheetBuilder.py"]
