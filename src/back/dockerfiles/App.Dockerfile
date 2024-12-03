FROM python:3.12-slim

WORKDIR /app

COPY src/back/__init__.py ./src/back/__init__.py
COPY src/front/main.py ./src/front/main.py
COPY src/front/pages ./src/front/pages
COPY src/back/plot_maker.py ./src/back/plot_maker.py
COPY src/back/create_pdf.py ./src/back/create_pdf.py
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app/src

CMD ["streamlit", "run", "./src/front/main.py", "--server.address=0.0.0.0", "--server.port=8501"]