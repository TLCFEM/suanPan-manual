FROM python:3.12-slim AS dependency

RUN apt-get update && apt-get install -y --no-install-recommends doxygen graphviz pngquant && rm -rf /var/lib/apt/lists/*

COPY docs /manual/docs
COPY plugins /manual/plugins
COPY mkdocs.yml /manual/mkdocs.yml
COPY requirements.txt /manual/requirements.txt
COPY setup.py /manual/setup.py
WORKDIR /manual 

RUN pip install --no-cache-dir --no-compile --upgrade .

RUN sed -i '/^extra:/,+2d' mkdocs.yml

RUN ln -s "$(find /manual/suanPan* -type f -name suanPan.sh | head -n1)" /usr/local/bin/suanpan

RUN mkdocs build --site-dir site

FROM python:3.12-slim AS runtime

RUN pip install --no-cache-dir --no-compile --upgrade aiohttp

COPY --from=dependency /manual/site /manual/site
COPY plugins/misc/runner.py /manual/runner.py

WORKDIR /manual

CMD ["python3", "runner.py"]

EXPOSE 8000
