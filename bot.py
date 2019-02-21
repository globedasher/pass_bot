import sys, os, logging, json, requests
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
    logging.info("One from all passes request")
    all_passes_url = "https://wsdot.com/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionsAsJson?AccessCode={%s}" % (key.wa_access_code)
    logging.info(all_passes_url)
    #print(all_passes_url)

    other_response = requests.get(all_passes_url)
    response = json.loads(other_response.content.decode("utf-8"))
    data = response

    logging.info(dir(response))
    #data = json.loads(response.read().decode("utf-8"))
    logging.info(data[pass_id])
    post_string = ""
    post_string += str(data[pass_id]["TemperatureInFahrenheit"]) + "°F\n"
    post_string += str(data[pass_id]["RoadCondition"]) + "\n"


    rest_one = str(data[pass_id]["RestrictionOne"]["RestrictionText"])
    rest_two = str(data[pass_id]["RestrictionTwo"]["RestrictionText"])

    # if the string doesn't have no restrictions, add it to the post
    if "No restrictions" not in rest_one:
        post_string += "E: "
        post_string += rest_one + "\n"
    if "No restrictions" not in rest_two:
        post_string += "W: "
        post_string += rest_two
    if rest_one == rest_two:
        post_string += rest_one + " either direction"
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
    camera_dict = {}
    for message in data:
        print(message)
        if message["CameraID"] == camera_id:
            image_url = message["ImageURL"]

    logging.info(image_url)
    return image_url


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


def twitter_post(post_data, image_url=0):
    logging.info("Twitter post attempt.")
    if image_url:
        auth = OAuth(
                key.token,
                key.token_secret,
                key.consumer_key,
                key.consumer_secret,
                )

        t_upload = Twitter(
                domain="upload.twitter.com",
                auth=auth)

        logging.info(image_url)
        response = requests.get(image_url)
        imagedata = response.content

        image_url_1 = "https://images.wsdot.wa.gov/sc/090VC05347.jpg"
        response1 = requests.get(image_url_1)
        imagedata1 = response1.content

        #id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
        id_img2 = t_upload.media.upload(media=imagedata1)["media_id_string"]

    #print(id_img1, id_img2)


    auth = OAuth(
            key.token,
            key.token_secret,
            key.consumer_key,
            key.consumer_secret,
            )
    twitter = Twitter(auth=auth)
    logging.info(str(post_data))
    #twitter.statuses.update(status=str(post_data))
    twitter.statuses.update(status=str(post_data), media_ids=",".join([id_img2]))

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
    #all_passes()
    camera_image = get_camera(9715)
    print(camera_image)
    pass_report = one_from_all_passes(11)
    print(pass_report)
    twitter_post(pass_report, camera_image)

if __name__ == "__main__":
    try:
        main()
    except:
        logging.exception(str(sys.exc_info()))
        logging.exception(str(sys._getframe()))
        sys.exit(2)
