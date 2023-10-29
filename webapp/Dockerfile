# Cochar - create a random character for Call of Cthulhu RPG 7th ed. 
# Copyright (C) 2023  Adam Walkiewicz

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

FROM python:3.11-bullseye AS build

# Add non root user
RUN useradd -u 1001 nonroot

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN <<EOT
apt-get update
apt-get install -y --no-install-recommends gcc
EOT

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Copy the scripts to the folder
COPY . .

FROM python:3.11-slim-bullseye

WORKDIR /app

RUN <<EOT
apt-get update
apt-get install python3-libxml2 -y
EOT

# Copy the passwd file
COPY --from=build /etc/passwd /etc/passwd

COPY --link --from=build /app/wheels /wheels
COPY --link --from=build /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY --link --from=build /app .

# Use nonroot user
USER nonroot

EXPOSE 80

# Start the server
CMD ["uwsgi", "--http", "0.0.0.0:80", "--master", "-p", "4", "-w", "wsgi", "--py-autoreload", "3"]
