FROM python:3.10-slim

RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

# Update pip
RUN pip install --upgrade pip

COPY requirements.txt dash_leaflet-1.0.18.tar.gz model_viewer-0.0.1.tar.gz ./
RUN pip install -r requirements.txt

# Output the version of dash-mantine-components
RUN pip show dash-mantine-components

COPY package.json package-lock.json ./
RUN npm install

COPY . .

EXPOSE 8550
CMD ["gunicorn", "run:server", "-b", "0.0.0.0:8550"]
