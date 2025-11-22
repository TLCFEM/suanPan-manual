FROM python:3.12-slim AS dependency

RUN apt-get update && apt-get install -y --no-install-recommends binutils doxygen graphviz pngquant && rm -rf /var/lib/apt/lists/*

COPY docs /manual/docs
COPY plugins /manual/plugins
COPY mkdocs.yml /manual/mkdocs.yml
COPY requirements.txt /manual/requirements.txt
COPY setup.py /manual/setup.py
WORKDIR /manual 

RUN pip install --no-cache-dir --no-compile --upgrade .

RUN find /usr/local/lib/python*/site-packages -name "*.so" -exec strip --strip-unneeded {} +

RUN sed -i '/^extra:/,+2d' mkdocs.yml

RUN ln -sf "$(find /manual/suanPan* -type f -name suanPan.sh | head -n1)" /usr/local/bin/suanpan

ENV PYTHONOPTIMIZE=1

EXPOSE 8000

CMD ["mkdocs","serve","-a","0.0.0.0:8000"]
