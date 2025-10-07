#!/bin/bash

cd src

uvicorn py_experimenter_dash.main:app --reload
