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

# apline 3.17 and python 3.8
# copied from https://github.com/docker-library/python/blob/f5b7b5a332bd4d2c1518325ab9647b09bf07412f/3.8/alpine3.17/Dockerfile

FROM ubuntu:20.04

# set the working directory
WORKDIR /cochar

RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install python3.8 python3-pip --yes

# install dependencies
COPY ./dev_requirements.txt .

RUN pip install --no-cache-dir --upgrade -r dev_requirements.txt

# copy the scripts to the folder
COPY . /cochar

RUN pip install -e .
