FROM tlcfem/suanpan:latest AS dependency

RUN dnf install -y python3-pip doxygen graphviz wget bzip2 && dnf clean all
RUN wget -qO- https://pngquant.org/pngquant-linux.tar.bz2 | tar -xj -C /usr/local/bin --strip-components=1

COPY docs /manual/docs
COPY plugins /manual/plugins
COPY mkdocs.yml /manual/mkdocs.yml
COPY requirements.txt /manual/requirements.txt
COPY setup.py /manual/setup.py
WORKDIR /manual

RUN pip install --no-cache-dir --no-compile --upgrade .

RUN sed -i '/^extra:/,+2d' mkdocs.yml

RUN mkdocs build --site-dir site

FROM python:3.12-slim AS runtime

COPY --from=dependency /manual/site /manual/site

CMD ["python3", "-m", "http.server", "8000", "--directory", "/manual/site"]

EXPOSE 8000
