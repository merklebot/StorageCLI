import click


@click.group()
def cli():
    pass


@cli.group()
def auth():
    pass


# Group of commands to work with content
@cli.group()
def content():
    pass


@content.command()
def enlist():
    click.echo("ENLIST")
    pass


@content.command()
def get():
    pass


@content.command()
def add():
    click.echo("content add")
    pass


@content.command()
def download():
    pass


@content.command()
def restore():
    pass


# Group of commands to work with tenant

@cli.group()
def organization():
    pass


@organization.command()
def add():
    pass


# Group of commands to work with bucket
@cli.group()
def bucket():
    pass


@bucket.command()
def add():
    click.echo("bucket add")
    pass


@bucket.command()
def generate_token():
    pass


@bucket.command()
def enlist_tokens():
    pass
