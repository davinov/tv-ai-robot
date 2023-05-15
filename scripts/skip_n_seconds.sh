#!/bin/bash
FILEPATH=$1

# Récupère le chemin d'accès au fichier
DIRPATH=$(dirname "$FILEPATH")
echo "Chemin du répertoire : $DIRPATH"

# Récupère le nom de fichier avec l'extension
FILENAME=$(basename "$FILEPATH")
echo "Nom du fichier avec extension : $FILENAME"

# Récupère l'extension du fichier
EXTENSION="${FILENAME##*.}"

# Récupère le nom du fichier sans l'extension
BASENAME=$(basename -s ."$EXTENSION" "$FILEPATH")
echo "Nom du fichier sans extension : $BASENAME"


ffmpeg -i "$FILEPATH" -ss 00:00:30 -c copy "$DIRPATH/$BASENAME-cut.$EXTENSION"
