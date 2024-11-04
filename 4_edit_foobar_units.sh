#!/bin/bash

units=$(systemctl list-units --type=service --all --no-legend | awk '{print $1}' | grep '^foobar-')

for unit in $units; do
  echo "working with unit: $unit"

  sudo systemctl stop "$unit"

  working_dir=$(systemctl show "$unit" -p WorkingDirectory | cut -d'=' -f2)
  exec_start=$(systemctl show "$unit" -p ExecStart )
  path=$(echo "$exec_start" | awk -F'path=| ; argv' '{print $2}')

  service_name=$(basename "$working_dir")

  sudo mkdir -p "/srv/data/$service_name"
  sudo mv "$working_dir"/* "/srv/data/$service_name"

  new_working_dir="/srv/data/$service_name"
  new_exec_start=$(echo "$path" | sed "s|$working_dir|$new_working_dir|")

  sudo sed -i "s|^WorkingDirectory=.*|WorkingDirectory=$new_working_dir|" "/etc/systemd/system/$unit"
  sudo sed -i "s|^ExecStart=.*|ExecStart=$new_exec_start|" "/etc/systemd/system/$unit"

  sudo systemctl daemon-reload

  sudo systemctl start "$unit"

  echo "unit $unit is running with correct WorkingDirectory and ExecStart..."
done

echo "all units has been completed!"