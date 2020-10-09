FROM python:3.8

# Create user
RUN useradd -ms /bin/bash recipecatalog

WORKDIR /home/recipecatalog

# Install project dependencies
COPY requirements.txt requirements.txt
ENV VIRTUAL_ENV=/dock-venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN $VIRTUAL_ENV/bin/pip install -r requirements.txt
RUN $VIRTUAL_ENV/bin/pip install gunicorn

# copy project files and folders to working directory
COPY app app
COPY migrations migrations
COPY recipe_catalog.py config.py boot.sh ./
RUN chmod +x boot.sh

# Change ownership of working directory to the user we created, then switch to it
RUN chown -R recipecatalog:recipecatalog ./
USER recipecatalog

# Expose on port 5000 and set entry point to script, boot.sh
EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]