FROM python:3.10-slim

ARG USER=boto
RUN useradd -ms /bin/bash ${USER}
USER ${USER}
WORKDIR /home/${USER}
COPY . .
RUN mkdir /home/${USER}/.aws && \
    mv config /home/${USER}/.aws && \
    pip install -r requirements.txt

CMD ["python", "script.py"]
