#!/bin/bash

if [ "$CLEAR_DB" == "true" ]; then
    python db/db_delete.py
    python db/db_start.py
fi

python CharacterSheetBuilder.py
