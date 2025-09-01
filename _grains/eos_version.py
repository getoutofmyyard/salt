import pyeapi

# This script executes on the Arista EOS node

def eos_version():

    grains = {}

    try:
        node = pyeapi.connect_to('localhost')
        output = node.enable('show version')
        version = output[0]['result']['version']
        grains['eos_version'] = version

    except Exception as e:
        grains['eos_version'] = str(e)

    return grains

def main():
    eos_version()

if __name__ == '__main__':
    main()
