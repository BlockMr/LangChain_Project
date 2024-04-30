FROM python:3.11.0
ENV MY_ENV=development
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG CLEAR_DB
ENV CLEAR_DB=${CLEAR_DB}
COPY run_bot.sh /app/run_bot.sh
RUN chmod +x /app/run_bot.sh
CMD ["/app/run_bot.sh"]