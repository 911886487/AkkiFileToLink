FROM python:3.10-slim

# Timezone fix
ENV TZ=Asia/Kolkata
RUN apt-get update && \
    apt-get install -y tzdata ntpdate && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

WORKDIR /Akki-stream-bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "Adarsh"]
