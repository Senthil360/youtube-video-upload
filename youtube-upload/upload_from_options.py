
import json
import os
from .support import dotdict
from .upload_video import upload_video
from .get_credentials import get_credentials

from google.oauth2.credentials import Credentials


def upload_from_options(options):
    """
    config_path: |
        ...

    cresentials_path: |
        credentials

    videos:
        -
            title:  video title
            file:  path
            description: sdf
            category: 22
            privacy: private
            tags:
                - shit
                - holy
    """
    options = dotdict(**options)

    credentials = None
    config = None

    if 'credentials' in options:
        credentials = Credentials.from_authorized_user_info(options.credentials)

    elif 'credentials_path' in options:
        credentials = Credentials.from_authorized_user_file(options.credentials_path)

    elif 'config' in options:
        config = json.loads(options.config)

    elif 'config_path' in options:
        file = open(options.config_path, 'r')
        config = json.load(file.read())
        file.close()

    if not credentials and config:
        credentials = get_credentials(config)
    else:
        raise Exception('neither config or credentials')

    for video_options in options.videos:

        print(credentials)


        try:
            upload_video(
                credentials,
                **video_options
            )

        except Exception as e:
            print(e)

    save_credentials(credentials, options.credentials_path or "./credentials.json")

    return credentials



def save_credentials(creds, credentials_path):

    creds_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

    del creds_data['token']

    config_path = os.path.dirname(credentials_path)
    if not os.path.isdir(config_path):
        os.makedirs(config_path)

    with open(credentials_path, 'w') as outfile:
        json.dump(creds_data, outfile)
