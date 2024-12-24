FROM python:3.13

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /booking/docker/app.sh

CMD ["sh", "/booking/docker/app.sh"]

