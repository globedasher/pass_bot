import sys, os, logging, json
import urllib.request
from twitter import *

# This is your key file to keep your API id and such.
import key

def config():
    formatter = '%(asctime)s: %(levelname)s: %(message)s'
    logging.basicConfig(format=formatter,
            filename='debug.log',
            filemode='w',
            level=logging.DEBUG)
    logging.info("Logging initialized.")

def all_passes():
    #Get information all passes
    all_passes_url = "https://wsdot.com/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionsAsJson?AccessCode={%s}" % (key.wa_access_code)
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

def one_from_all_passes(pass_id):
    #Get information all passes
    all_passes_url = "https://wsdot.com/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionsAsJson?AccessCode={%s}" % (key.wa_access_code)
    logging.info("One from all passes request")
    logging.info(all_passes_url)
    #print(all_passes_url)

    response = urllib.request.urlopen(all_passes_url)
    data = json.loads(response.read().decode("utf-8"))
    logging.info(data[pass_id])
    post_string = str(data[pass_id]["MountainPassName"]) + "\n"
    post_string += "Road Condition: "
    post_string += str(data[pass_id]["RoadCondition"]) + "\n"
    post_string += "Current temperature: "
    post_string += str(data[pass_id]["TemperatureInFahrenheit"]) + " Degrees Fahrenheit\n"
    post_string += str(data[pass_id]["RestrictionOne"]["TravelDirection"]) + ": "
    post_string += str(data[pass_id]["RestrictionOne"]["RestrictionText"]) + "\n"
    post_string += str(data[pass_id]["RestrictionTwo"]["TravelDirection"]) + ": "
    post_string += str(data[pass_id]["RestrictionTwo"]["RestrictionText"]) + "\n"
    return post_string


def get_camera(camera_id):
    # Get a camera image.
    #save_file = open("image.jpg", "w")
    print(key.wa_access_code, camera_id)
    #camera_url = "https://wsdot.wa.gov/Traffic/api/HighwayCameras/HighwayCamerasREST.svc/GetCameraAsJson?AccessCode={%s}&CameraID={%s}" % (key.wa_access_code, camera_id)

    camera_url = "http://wsdot.wa.gov/Traffic/api/HighwayCameras/HighwayCamerasREST.svc/GetCamerasAsJson?AccessCode={%s}" % (key.wa_access_code)
    log_message = "Getting image from camera #%s" % (camera_id)
    logging.info(log_message)
    logging.info(camera_url)

    response = urllib.request.urlopen(camera_url)
    data = json.loads(response.read().decode("utf-8"))
    #print(data)
    #print(type(data))
    print("78")
    print(camera_id)
    camera_dict = {}
    for message in data:
        #print("81")
        #print(message)
        #print(type(message))
        #print("84")
        #for item in message:
            #print(item, message[item])
        #print(message["CameraID"])
        #print("88")
        if message["CameraID"] == camera_id:
            #print("91")
            #print(message["CameraID"])
            #print(dir(message))
            #print(type(message))
            #print(message["ImageURL"])
            image_url = message["ImageURL"]
        #camera_dict[message["CameraId"]] = message

    print(image_url)
    logging.info(image_url)


def one_pass():
    #Get one pass with pass ID
    one_pass = "https://wsdot.com/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionAsJon?AccessCode={%s}&PassConditionID={%s}" % (key.wa_access_code, 3)
    logging.info("One pass request")
    print(one_pass)
    logging.info(one_pass)
    response = urllib.request.urlopen(one_pass)
    data = json.loads(response.read().decode("utf-8"))
    print(data)
    #logging.info(str(data))
    logging.info("ouch")

def post_test(post_data):
    logging.info("Twitter post attempt.")
    auth = OAuth(
            key.token,
            key.token_secret,
            key.consumer_key,
            key.consumer_secret,
            )
    twitter = Twitter(auth=auth)
    logging.info(str(post_data))
    twitter.statuses.update(status=str(post_data))


def main():
    config()
    #print(key.wa_access_code)
    #all_passes()
    get_camera(1138)
    pass_report = one_from_all_passes(0)
    post_test(pass_report)
    #one_pass()

if __name__ == "__main__":
    try:
        main()
    except:
        logging.warning(str(sys.exc_info()))
        logging.warning(str(sys._getframe()))
        sys.exit(2)
