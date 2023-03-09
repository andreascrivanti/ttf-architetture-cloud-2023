FROM alpine:3.15.0

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
# Copy code
ADD code/hello_world.py .
# Execute code
CMD python3 hello_world.py $@