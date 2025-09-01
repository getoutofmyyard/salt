import pyeapi

def eos_serial():

    grains = {}

    try:

        node = pyeapi.connect_to('localhost')
        output = node.enable('show version')
        serial = output[0]['result']['serialNumber']
        grains['eos_serial'] = serial

    except Exception as e:
        grains['eos_serial'] = str(e)

    return grains

def main():
    eos_serial()

if __name__ == '__main__':
    main()
