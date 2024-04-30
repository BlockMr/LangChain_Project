#!/bin/bash

if [ "$CLEAR_DB" == "true" ]; then
    python db/db_delete.py
fi

python CharacterSheetBuilder.py
