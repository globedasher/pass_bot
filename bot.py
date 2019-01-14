import sys, os, logging, json
import urllib.request
import key

def config():
    formatter = '%(asctime)s: %(levelname)s: %(message)s'
    logging.basicConfig(format=formatter,
            filename='debug.log',
            filemode='w',
            level=logging.DEBUG)
    logging.info("Logging initialized.")

def all_passes():
    #Get all passes
    all_passes_url = "https://wsdot.com/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionsAsJson?AccessCode={%s}" % (key.access_code)
    logging.info("All passes request")
    logging.info(all_passes_url)
    print(all_passes_url)

    response = urllib.request.urlopen(all_passes_url)
    data = json.loads(response.read().decode("utf-8"))
    print(data[0])
    logging.info(data[0])
    print(str(data[0]["TemperatureInFahrenheit"]) + " degrees")
    logging.info(str(data[0]["TemperatureInFahrenheit"]) + " degrees")
    #print(type(data))

    #for item in data:
        #print(item)
        #print(type(item))
        #logging.info(item)

    #print(data)
    #print(dir(data))
    #logging.info(str(data))
    logging.info("ouch")

def one_pass():
    #Get one pass with pass ID
    one_pass = "https://wsdot.com/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionAsJon?AccessCode={%s}&PassConditionID={%s}" % (key.access_code, 3)
    logging.info("One pass request")
    print(one_pass)
    logging.info(one_pass)
    response = urllib.request.urlopen(one_pass)
    data = json.loads(response.read().decode("utf-8"))
    print(data)
    #logging.info(str(data))
    logging.info("ouch")

def main():
    config()
    #print(key.access_code)
    all_passes()
    #one_pass()

if __name__ == "__main__":
    try:
        main()
    except:
        logging.warning(str(sys.exc_info()))
        print(str(sys.exc_info()))
        logging.warning(str(sys._getframe()))
        print(str(sys._getframe()))
        sys.exit(2)
