import requests
import os

from django.core.files import File


OCR_API_TOKEN_HEADER = os.environ.get("OCR_API_TOKEN_HEADER")
OCR_API_ENDPOINT = os.environ.get("OCR_API_ENDPOINT")


def extract_text_via_ocr_service(file_obj: File = None):
    data = {}
    if OCR_API_ENDPOINT is None:
        print("1")
        return data
    if OCR_API_TOKEN_HEADER is None:
        print("2")
        return data
    if file_obj is None:
        print("3")
        return data
    # get image
    # send image through HTTP POST
    # return dict {}

    payload = {'isOverlayRequired': False,
               'apikey': OCR_API_TOKEN_HEADER,
               'language': "eng",
               }
    print(payload)

    with file_obj.open('rb') as f:
        r = requests.post(OCR_API_ENDPOINT, files={
                          "filename": f}, data=payload)
        if r.status_code in range(200, 299):
            print(r.json())
            data = r.json() # after changing database to postgres database
            data = r.content.decode()
        else : 
            print("Error")

    return data

# import requests
# import os

# from django.core.files import File


# OCR_API_TOKEN_HEADER=os.environ.get("OCR_API_TOKEN_HEADER")
# OCR_API_ENDPOINT=os.environ.get("OCR_API_ENDPOINT")

# def extract_text_via_ocr_service(file_obj: File=None):
#     data = {}
#     if OCR_API_ENDPOINT is None:
#         return data
#     if OCR_API_TOKEN_HEADER is None:
#         return data
#     if file_obj is None:
#         return data
#     # get image
#     # send image through HTTP POST
#     # return dict {}
#     headers={
#         "Authorization": f"Bearer {OCR_API_TOKEN_HEADER}"
#     }
#     with file_obj.open('rb') as f:
#         r = requests.post(OCR_API_ENDPOINT, files={"file": f}, headers=headers)
#         if r.status_code in range(200, 299):
#             # if r.headers.get("content-type") == 'application/json':
#                 # data = r.json()
#             data = r.content.decode()
#     return data