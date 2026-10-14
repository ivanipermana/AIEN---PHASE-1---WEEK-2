# Lengkapi placeholder TODO mengikuti README. Jangan mengubah kode API.
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# TODO 1: salin requirements.txt ke direktori kerja
COPY TODO_REQUIREMENTS ./
RUN pip install --no-cache-dir -r requirements.txt

# TODO 2: salin kedua file Python
COPY TODO_PYTHON_FILES ./

# TODO 3: salin folder model
COPY TODO_MODEL_DIRECTORY ./data/

RUN useradd --create-home --uid 10001 appuser
USER appuser
EXPOSE 8000
# TODO 4: isi host dan port; API harus menerima koneksi dari luar container
CMD ["uvicorn", "app:app", "--host", "TODO_HOST", "--port", "TODO_PORT"]
