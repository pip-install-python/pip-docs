FROM python:3.10-slim

RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

# Update pip
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY package.json package-lock.json ./
RUN npm install

COPY . .

EXPOSE 8550
CMD ["gunicorn", "app:run", "-b", "0.0.0.0:8550"]

