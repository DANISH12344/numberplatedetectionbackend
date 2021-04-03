from PIL import Image
from io import BytesIO
import requests

def analyze_number(output):
    image_name=[]
    image_number=[]
    subscription_key = "f5eff5d029cb4b70881dfb6e8b13c1d6"
    assert subscription_key
    vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v3.0/"
    ocr_url = vision_base_url + "ocr"
    try:
        image_url = output
        image_data = open(image_url, "rb").read()
        headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
        params = {'language': 'unk', 'detectOrientation': 'true'}
        data = {'url': image_url}
        response = requests.post(ocr_url, headers=headers, params=params, data = image_data)
        response.raise_for_status()

        analysis = response.json()
        line_infos = [region["lines"] for region in analysis["regions"]]
        word_infos = []
        for line in line_infos:
             for word_metadata in line:
                    for word_info in word_metadata["words"]:
                              word_infos.append(word_info)
        label=[]
        for word in word_infos:
            label.append(word["text"])
        image_number.append(label)
        image_name.append(image_url)
    except Exception as ex:
        print(ex)

    return image_number