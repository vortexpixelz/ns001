FROM python:3.12.7-slim-bookworm

ARG VCS_REF=unknown
LABEL org.opencontainers.image.title="NS-001"
LABEL org.opencontainers.image.description="Reproducible JHTDB extreme-vorticity feasibility experiment"
LABEL org.opencontainers.image.revision=$VCS_REF

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NS001_SOURCE_COMMIT=$VCS_REF

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

COPY ns001_tau_check.py run_experiment.py ./
COPY protocols ./protocols

RUN mkdir -p /outputs
VOLUME ["/outputs"]

ENTRYPOINT ["python", "run_experiment.py"]
CMD ["protocols/sanity.json", "--output-dir", "/outputs"]
