import click
import requests

from StorageCLI.validator import *
from StorageCLI.CustomComponents.OptionalPrompt import OptionPromptNull
from StorageCLI.config import *
from StorageCLI.exceptions import check_response_for_error

from StorageCLI.sdk import list_content, get_content, delete_content, get_content_link, download_content, restore_content

@click.group()
def cli():
    pass


# Group of config related commands
@cli.group()
def config():
    pass


@config.command()
def info():
    """Shows config file location. Be aware, configs are stored in opened way."""
    click.echo(f'Config is stored at {config_file}')


@config.command()
@click.option('-o', '--organization', 'organization',
              type=str,
              prompt=True,
              help="Name of organization at app.merklebot.com")
@click.option('-t', '--bucket-token', 'token',
              type=str,
              prompt=True,
              hidden=True,
              help="Token of bucket at app.merklebot.com")
def init(organization, token):
    """Put organization name and bucket token for future use"""
    write_config(organization, token)
    click.echo("Config inited")


@config.command()
def clear():
    """Clear config files"""
    clear_config()
    click.echo("Config cleared")


# Group of storage related commands
@cli.group()
@click.option('-o', '--organization', 'organization',
              type=str,
              envvar="STORAGECLI_ORGANIZATION",
              prompt=True,
              cls=OptionPromptNull,
              default=lambda: read_organization_name(),
              help="Name of organization at app.merklebot.com")
@click.option('-t', '--bucket-token', 'token',
              type=str,
              envvar="STORAGECLI_BUCKET_TOKEN",
              prompt=True,
              hidden=True,
              cls=OptionPromptNull,
              default=lambda: read_token(),
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
              help="Number of page")
@click.option('-s', '--size', 'size',
              type=int,
              required=False,
              default=10,
              help="Number of files in page")
@click.pass_context
def ls(ctx, page, size):
    """Enlist files contained in bucket with pagination"""
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    rez = list_content(organization, token, page, size, cli_mode=True)

    click.echo(json.dumps(rez, indent=2))


@content.command()
@click.argument('content_id',
                required=True)
@click.pass_context
def get(ctx, content_id):
    """Get info about file with id"""
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    rez = get_content(organization, token, content_id, cli_mode=True)

    click.echo(json.dumps(rez, indent=2))



@content.command()
@click.argument('content_id',
                required=True)
@click.pass_context
def delete(ctx, content_id):
    """Delete file by id"""
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    rez = delete_content(organization, token, content_id, cli_mode=True)

    click.echo(json.dumps(rez, indent=2))


@content.command()
@click.argument('filepath',
                required=True,
                type=click.Path())
@click.pass_context
def add(ctx, filepath):
    """Add file with filepath"""
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    files = {'file_in': open(filepath, 'rb')}

    url = f"https://{organization}.storage.api2.merklebot.com/contents/"
    rqst = requests.post(url, headers={
        "Authorization": token,
    }, files=files)

    check_response_for_error(rqst)
    click.echo(json.dumps(rqst.json(), indent=2))


@content.command()
@click.argument('content_id',
                required=True)
@click.pass_context
def get_link(ctx, content_id):
    """Get direct link to download file by id"""
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    rez = get_content_link(organization, token, content_id, cli_mode=True)

    click.echo(json.dumps(rez, indent=2))


@content.command()
@click.argument('content_id',
                required=True)
@click.argument('dest_file',
                required=True,
                type=click.Path())
@click.pass_context
def download(ctx, content_id, dest_file):
    """Download file directly to local storage with destination filepath"""
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    download_content(organization, token, content_id, dest_file, cli_mode=True)


@content.command()
@click.option('-d', '--restore-days', 'restore_days',
              type=int,
              required=True,
              help="Number of days content will be kept in instant access state")
@click.option('-w', '--web-hook', 'web_hook',
              type=str,
              callback=web_hook_validation,
              required=False,
              help="URL. POST request will be send here as file change access status"
              )
@click.argument('content_id',
                required=True)
@click.pass_context
def restore(ctx, content_id, restore_days, web_hook):
    """Restore file from cold storage for instant access"""
    organization = ctx.obj["ORGANIZATION"]
    token = ctx.obj["TOKEN"]

    rez = restore_content(organization, token, content_id, restore_days, web_hook, cli_mode=True)

    click.echo(json.dumps(rez, indent=2))
