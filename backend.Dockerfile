FROM python:3.11-slim

WORKDIR /app

COPY ./kenvas /app/kenvas

COPY ./requirements.txt /kenvas/requirements.txt

ARG ZSCALER_ROOT_CERTIFICATE
RUN echo $ZSCALER_ROOT_CERTIFICATE > /usr/local/share/ca-certificates/ZScalerRootCertificate.crt
RUN chmod 644 /usr/local/share/ca-certificates/ZScalerRootCertificate.crt
RUN update-ca-certificates
ENV CERT_PATH=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=${CERT_PATH}

RUN pip install --no-cache-dir --upgrade -r /kenvas/requirements.txt



ENV PYTHONPATH=/app

CMD uvicorn kenvas.app:app --host 0.0.0.0 --port 8000