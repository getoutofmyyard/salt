# /_grains/eos_vlans.py
import pyeapi

def eos_vlans(device_name='localhost'):
    """
    Return EOS VLAN information as Salt grains.

    eos_vlans:          [1, 10, 20, ...]                # list of VLAN IDs
    eos_vlans_detail:   [{'id': 1, 'name': 'default', ...}, ...]
    """
    grains = {}

    try:
        node = pyeapi.connect_to(device_name)
        # 'show vlan' is stable across EOS releases and returns a 'vlans' dict.
        output = node.enable('show vlan')
        result = output[0].get('result', {})
        vlans_dict = result.get('vlans', {}) or {}

        vlan_ids = sorted(int(v) for v in vlans_dict.keys())
        vlan_detail = []
        for vid_str, data in vlans_dict.items():
            try:
                vid = int(vid_str)
            except ValueError:
                # Skip any unexpected non-numeric keys
                continue
            vlan_detail.append({
                'id': vid,
                'name': data.get('name', ''),
                # Some versions use 'status', others 'state'—capture both safely.
                'status': data.get('status', data.get('state', '')),
                # Include trunk groups if present
                'trunk_groups': data.get('trunkGroups', []),
                # Include interface membership if present (keys vary by EOS)
                'interfaces': list((data.get('interfaces') or {}).keys())
                              if isinstance(data.get('interfaces'), dict)
                              else (data.get('interfaces') or []),
            })

        grains['eos_vlans'] = vlan_ids
        grains['eos_vlans_detail'] = sorted(vlan_detail, key=lambda x: x['id'])

    except Exception as e:
        # Mirror your pattern: surface the error string as the grain value
        grains['eos_vlans'] = []
        grains['eos_vlans_detail'] = []
        grains['eos_vlans_error'] = str(e)

    return grains


def main():
    # Simple local test runner (won't print in Salt context, but handy standalone)
    g = eos_vlans()
    print(g)


if __name__ == '__main__':
    main()

