import click
import requests
import os

from StorageCLI.validator import *


@click.group()
def cli():
    pass


@cli.group()
@click.option('-o', '--organization', 'organization',
              type=str,
              envvar="STORAGECLI_ORGANIZATION",
              required=True,
              prompt=True,
              help="Name of organization at app.merklebot.com")
@click.option('-t', '--bucket-token', 'token',
              type=str,
              envvar="STORAGECLI_BUCKET_TOKEN",
              callback=token_validation,
              required=True,
              prompt=True,
              help="Token of bucket at app.merklebot.com")
@click.pass_context
def content(ctx, organization, token):
    ctx.ensure_object(dict)
    ctx.obj["ORGANIZATION"] = organization
    ctx.obj["TOKEN"] = token


@content.command()
@click.option('-p', '--page', 'page',
              type=int,
              required=False,
              default=1,
              help="")
@click.option('-s', '--size', 'size',
              type=int,
              required=False,
              default=10,
              help="")
@click.pass_context
def ls(ctx, page, size):
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    url = f"https://{organization}.storage.api2.merklebot.com/contents/"
    rqst = requests.get(url, headers={
        "Authorization": token,
    }, params={
        "page": page,
        "size": size
    })

    click.echo(rqst.json())


@content.command()
@click.argument('content_id',
                required=True)
@click.pass_context
def get(ctx, content_id):
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    url = f"https://{organization}.storage.api2.merklebot.com/contents/{content_id}"
    rqst = requests.get(url, headers={
        "Authorization": token,
    })

    click.echo(rqst.json())
    return rqst.json()


@content.command()
@click.argument('content_id',
                required=True)
@click.pass_context
def delete(ctx, content_id):
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    url = f"https://{organization}.storage.api2.merklebot.com/contents/{content_id}"
    rqst = requests.delete(url, headers={
        "Authorization": token,
    })

    click.echo(rqst.json())


@content.command()
@click.argument('filepath',
                required=True,
                type=click.Path())
@click.pass_context
def add(ctx, filepath):
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    files = {'file_in': open(filepath, 'rb')}

    url = f"https://{organization}.storage.api2.merklebot.com/contents/"
    rqst = requests.post(url, headers={
        "Authorization": token,
    }, files=files)

    click.echo(rqst.json())


@content.command()
@click.argument('content_id',
                required=True)
@click.pass_context
def get_link(ctx, content_id):
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    url = f"https://{organization}.storage.api2.merklebot.com/contents/{content_id}/download"
    rqst = requests.get(url, headers={
        "Authorization": token,
    })

    click.echo(rqst.json())


@content.command()
@click.argument('content_id',
                required=True)
@click.argument('dest_file',
                required=True,
                type=click.Path())
@click.pass_context
def download(ctx, content_id, dest_file):
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    url = f"https://{organization}.storage.api2.merklebot.com/contents/{content_id}/download"
    rqst = requests.get(url, headers={
        "Authorization": token,
    })

    download_url = rqst.json().get("url")
    with open(dest_file, "wb") as f:
        f.write(requests.get(download_url).content)


@content.command()
@click.option('-d', '--restore-days', 'restore_days',
              type=int,
              required=True)
@click.option('-w', '--web-hook', 'web_hook',
              type=str,
              callback=web_hook_validation,
              required=False
              )
@click.argument('content_id',
                required=True)
@click.pass_context
def restore(ctx, content_id, restore_days, web_hook):
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    json_data = {
        'restoreDays': restore_days,
    }

    if web_hook:
        json_data["webhookUrl"] = web_hook

    url = f"https://{organization}.storage.api2.merklebot.com/contents/{content_id}/restore"
    rqst = requests.post(url, headers={
        "Authorization": token,
    }, json=json_data)

    click.echo(rqst.json())
