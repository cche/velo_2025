FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Copy only what's needed to run stage 4 scripts
COPY 4_cluster_slurm /app/4_cluster_slurm

ENTRYPOINT ["python"]
CMD ["--version"]
