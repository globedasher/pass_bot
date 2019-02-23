import sys, os, logging, json, requests, argparse
import urllib.request
import twitter

# This is your key file to keep your API id and such.
import key

def config(log_level):
    # Get the log level and set the parameter for logging messages
    if log_level == "debug":
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Configure the format for the log messages
    formatter = '%(asctime)s: %(levelname)s: %(message)s'

    # Configure logging
    logging.basicConfig(format=formatter,
            filename='debug.log',
            filemode='w',
            level=log_level)

    # Log that
    logging.info("Logging initialized.")

def all_passes():
    #Get information all passes
    all_passes_url = "https://wsdot.com/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionsAsJson?AccessCode={%s}" % (key.wa_access_code)
    logging.info("All passes request")
    logging.debug(all_passes_url)
    print(all_passes_url)

    response = urllib.request.urlopen(all_passes_url)
    data = json.loads(response.read().decode("utf-8"))
    print(data[0])
    logging.debug(data[0])
    print(str(data[0]["TemperatureInFahrenheit"]) + " degrees")
    logging.debug(str(data[0]["TemperatureInFahrenheit"]) + " degrees")
    #print(type(data))

    #for item in data:
        #print(item)
        #print(type(item))
        #logging.debug(item)

    #print(data)
    #print(dir(data))
    #logging.debug(str(data))
    logging.debug("ouch")

def one_from_all_passes(pass_id):
    #Get information all passes and return the pass_report string
    logging.info("One from all passes request")
    all_passes_url = "https://wsdot.com/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionsAsJson?AccessCode={%s}" % (key.wa_access_code)
    logging.debug(all_passes_url)
    #print(all_passes_url)

    other_response = requests.get(all_passes_url)
    response = json.loads(other_response.content.decode("utf-8"))
    data = response

    logging.debug(dir(response))
    #data = json.loads(response.read().decode("utf-8"))
    logging.info(data[pass_id])
    post_string = ""

    travel_advisory = str(data[pass_id]["TravelAdvisoryActive"])

    if not travel_advisory:
        post_string += "No travel advisory at this time. Drive safe.\n"
    else:
        post_string += str(data[pass_id]["TemperatureInFahrenheit"]) + "°F\n"
        post_string += str(data[pass_id]["RoadCondition"]) + "\n"

        rest_one = str(data[pass_id]["RestrictionOne"]["RestrictionText"])
        rest_two = str(data[pass_id]["RestrictionTwo"]["RestrictionText"])

        # if the string doesn't have no restrictions, add it to the post

        if rest_one == rest_two and "No restrictions" in rest_one:
            post_string += rest_one

        else:
            post_string += "E: "
            post_string += rest_one + "\n"
            post_string += "W: "
            post_string += rest_two

    return post_string


def get_camera(camera_id):
    # Get a camera image.
    #save_file = open("image.jpg", "w")
    print(key.wa_access_code, camera_id)
    #camera_url = "https://wsdot.wa.gov/Traffic/api/HighwayCameras/HighwayCamerasREST.svc/GetCameraAsJson?AccessCode={%s}&CameraID={%s}" % (key.wa_access_code, camera_id)

    camera_url = "http://wsdot.wa.gov/Traffic/api/HighwayCameras/HighwayCamerasREST.svc/GetCamerasAsJson?AccessCode={%s}" % (key.wa_access_code)
    log_message = "Getting image from camera #%s" % (camera_id)
    logging.debug(log_message)
    logging.debug(camera_url)

    response = urllib.request.urlopen(camera_url)
    data = json.loads(response.read().decode("utf-8"))
    camera_dict = {}
    for message in data:
        print(message)
        if message["CameraID"] == camera_id:
            image_url = message["ImageURL"]

    logging.debug(image_url)
    return image_url


def one_pass():
    #Get one pass with pass ID
    one_pass = "https://wsdot.com/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionAsJon?AccessCode={%s}&PassConditionID={%s}" % (key.wa_access_code, 3)
    logging.info("One pass request")
    print(one_pass)
    logging.debug(one_pass)
    response = urllib.request.urlopen(one_pass)
    data = json.loads(response.read().decode("utf-8"))
    print(data)
    #logging.debug(str(data))
    logging.debug("ouch")


def twitter_post(post_data, image_url=0):
    logging.info("Twitter post attempt.")

    api = twitter.Api(
            key.consumer_key,
            key.consumer_secret,
            key.token,
            key.token_secret,
            )

    logging.debug(post_data)
    logging.debug(image_url)

    media="https://images.wsdot.wa.gov/sc/090VC05347.jpg"
    logging.debug(media)

    api.PostUpdate(post_data, media)


def get_args():
    """
    Get argument data passed from the command line and return a dictionary of
    the arguments.
    """
    parser = argparse.ArgumentParser()

    help_text = """The control selector can be set to either 'process' or 'post'. 'process' will run the main loop of the process. 'post' will post once and quit."""
    parser.add_argument("-s"
                        , "--selector"
                        , dest="selector"
                        , default=""
                        , help=help_text
                        )

    help_text = """Set the log level to debug or not."""
    parser.add_argument("-l"
                        , "--loglevel"
                        , dest="log_level"
                        , default=""
                        , help=help_text
                        )

    return parser.parse_args()


def main():

    args = get_args()
    #print(args)

    if not args.selector:
        print("No selectors?")
        sys.exit(2)

    # Configure the logging for this appliction.
    config(args.log_level)

    #all_passes()
    if args.selector == "post":
        pass_report = one_from_all_passes(11)
        twitter_post(pass_report)
    elif args.selector == "test":
        pass_report = one_from_all_passes(11)
        logging.info(pass_report)

if __name__ == "__main__":
    try:
        main()
    except:
        logging.exception(str(sys.exc_info()))
        logging.exception(str(sys._getframe()))
        sys.exit(2)
