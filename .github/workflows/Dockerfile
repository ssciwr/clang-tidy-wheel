ARG BASEOS=slim-bullseye
FROM python:3.11-${BASEOS}

ARG PLATFORM=manylinux

COPY test /src/test
COPY wheelhouse/clang*${PLATFORM}*.whl /tmp
RUN python -m pip install pytest /tmp/*whl \
    && pytest -vs /src/test
