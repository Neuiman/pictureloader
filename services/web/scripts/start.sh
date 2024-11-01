#!/bin/bash

alembic revision --autogenerate -m "make revision"

alembic upgrade head

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000