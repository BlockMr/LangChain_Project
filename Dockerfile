FROM python:3.11.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN ls -la
ENV ITER=2
ENV API_KEY_OPENAI=sk--beE7YCDsO-SwnG5gxTH-KDnHNju5Eco2GpwejQi0-T3BlbkFJnfH455O2_hgZsmURbJubMlk389fVdu9NjO_xhFl1EA
ENV TG_API=7026319380:AAErNkgGngWwQxFT7mBvcmrchUrfzmf5oGE
CMD ["python", "CharacterSheetBuilder.py"]
