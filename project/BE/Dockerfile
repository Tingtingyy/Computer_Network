FROM python:3.8

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Set up a working folder and install the pre-reqs
WORKDIR /BE

USER root

COPY --chown=root:root . .

RUN chmod 777 /BE

CMD [ "python", "./BE.py" ]
