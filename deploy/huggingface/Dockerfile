FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir . 'gradio>=5,<7'
RUN useradd -m -u 1000 appuser
USER appuser
EXPOSE 7860
CMD ["python", "deploy/huggingface/app.py"]
