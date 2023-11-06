import click
import requests


def check_response_for_error(response: requests.Response, cli_mode=False):
    if response.status_code in [200, 201]:
        pass
    elif response.status_code in [403, 404, 422, 410, 503, 500]:
        try:
            detail = (response.json().get("detail")
                      .replace("Tenant", "Organization").replace("tenant", "organization"))
        except:
            detail = response.content
            if cli_mode:
                raise click.ClickException(f"{response.status_code}\n"
                                           f"{detail}")
            else:
                raise Exception(f"{response.status_code}\n"
                                f"{detail}")
    else:
        pass
