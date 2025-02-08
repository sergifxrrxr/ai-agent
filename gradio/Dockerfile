FROM python:3.11-slim AS base

WORKDIR /src

COPY gradio/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["python", "gradio_ui.py"]