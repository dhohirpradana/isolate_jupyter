#!/bin/bash

# Remove unused Docker volumes containing '_jupyter-'
sudo docker volume ls -qf "name=_jupyter-" | \
  while read -r vol; do \
    if ! docker ps -q -a -f volume="$vol" | grep -q . ; then \
      sudo docker volume rm "$vol"; \
    fi; \
  done
