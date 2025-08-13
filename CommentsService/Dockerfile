FROM python:3.10-slim

ENV ACCEPT_EULA=Y
# Install build dependencies
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev

# Install Microsoft ODBC drivers (Debian 12 / bookworm)
RUN mkdir -p /etc/apt/keyrings \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/keyrings/microsoft-prod.gpg \
    && curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && sed -i 's|signed-by=/usr/share/keyrings/microsoft-prod.gpg|signed-by=/etc/apt/keyrings/microsoft-prod.gpg|' /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 mssql-tools \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

COPY . .

RUN pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apt-get clean

EXPOSE 8000

CMD ["python", "app.py"]