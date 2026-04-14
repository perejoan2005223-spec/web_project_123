FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar uv
RUN pip install uv

# Copiar los archivos de dependencias
COPY pyproject.toml uv.lock ./

# Instalar las dependencias
RUN uv pip install --system -r pyproject.toml

# Copiar todo el código fuente al contenedor
COPY . .

ENV PORT=8000
EXPOSE $PORT

RUN python manage.py collectstatic --noinput --clear || true
RUN python manage.py migrate
RUN python manage.py scrape_professors

# Arrancamos Gunicorn con --reload para que detecte los cambios de código en vivo
CMD gunicorn --reload -b 0.0.0.0:$PORT web_project.wsgi:application