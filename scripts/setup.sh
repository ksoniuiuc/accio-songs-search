#!usr/bin/bash

## Creating a Virtual Environment
python3 -m venv env

## Activating the Virtual Environment 
source ../env/bin/activate

## Install the Dependencies from requirement.txt
pip install -r requirements.txt