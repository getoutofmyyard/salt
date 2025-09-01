{% set hostname  = grains.get('id') %}

{%- if "msw" in hostname or "evpn" in hostname  %}
Distribute Pillar Data to Switch:
  file.managed:
    - name: /tmp/{{ hostname }}.yaml
    - source: salt://pillar/{{ hostname }}.yaml

Sync Grains:
  module.run:
    - name: saltutil.sync_grains

Refresh Grains:
  module.run:
    - name: saltutil.refresh_grains
    - require:
      - module: Sync Grains
  

Render and Apply Configuration:
  module.run:
    - pyeapi.config:
      - config_file: salt://templates/tor_default.j2
    - require:
      - module: Refresh Grains

Save Configuration:
  module.run:
    - pyeapi.run_commands:
      - 'write memory'

#Send Config Backups to Master:
#  module.run:
#    - eos_backup.backup:
{%- endif %}
