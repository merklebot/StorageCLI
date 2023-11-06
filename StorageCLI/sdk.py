import requests


from StorageCLI.exceptions import check_response_for_error
from StorageCLI.utils import download_with_progressbar


def list_content(organization, token, page, size, cli_mode=False):
    url = f"https://{organization}.storage.api2.merklebot.com/contents/"
    rqst = requests.get(url, headers={
        "Authorization": token,
    }, params={
        "page": page,
        "size": size
    })
    check_response_for_error(rqst, cli_mode=cli_mode)
    return rqst.json()


def get_content(organization, token, content_id, cli_mode=False):
    url = f"https://{organization}.storage.api2.merklebot.com/contents/{content_id}"
    rqst = requests.get(url, headers={
        "Authorization": token,
    })

    check_response_for_error(rqst, cli_mode=cli_mode)
    return rqst.json()


def delete_content(organization, token, content_id, cli_mode=False):
    url = f"https://{organization}.storage.api2.merklebot.com/contents/{content_id}"
    rqst = requests.delete(url, headers={
        "Authorization": token,
    })

    check_response_for_error(rqst, cli_mode=cli_mode)
    return rqst.json()


def get_content_link(organization, token, content_id, cli_mode=False):
    url = f"https://{organization}.storage.api2.merklebot.com/contents/{content_id}/download"
    rqst = requests.get(url, headers={
        "Authorization": token,
    })

    check_response_for_error(rqst, cli_mode=cli_mode)
    return rqst.json()


def download_content(organization, token, content_id, dest_file, cli_mode=False):
    url = f"https://{organization}.storage.api2.merklebot.com/contents/{content_id}/download"
    rqst = requests.get(url, headers={
        "Authorization": token,
    })

    check_response_for_error(rqst, cli_mode=cli_mode)
    download_url = rqst.json().get("url")
    download_with_progressbar(download_url, dest_file)
    return True


def restore_content(organization, token, content_id, restore_days, web_hook, cli_mode=False):
    json_data = {
        'restoreDays': restore_days,
    }

    if web_hook:
        json_data["webhookUrl"] = web_hook

    url = f"https://{organization}.storage.api2.merklebot.com/contents/{content_id}/restore"
    rqst = requests.post(url, headers={
        "Authorization": token,
    }, json=json_data)

    check_response_for_error(rqst, cli_mode=cli_mode)
    return rqst.json()
