#!/bin/sh

alembic upgrade head
uvicorn src.main:app --reload --port=8000 --host=0.0.0.0