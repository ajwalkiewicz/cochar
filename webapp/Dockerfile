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

FROM ubuntu:20.04

# set the working directory
WORKDIR /webapp

RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install python3.8 python3-pip --yes

# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# clean .build-deps
# RUN apk del --no-network .build-deps

# copy the scripts to the folder
COPY . /webapp

# start the server
CMD ["uwsgi", "--http", "0.0.0.0:80", "--master", "-p", "4", "-w", "wsgi", "--py-autoreload", "3"]
