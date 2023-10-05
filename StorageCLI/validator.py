import click


# TODO validation
def token_validation(_ctx, _param, token):
    try:
        return token
    except ValueError:
        raise click.BadParameter("...")


def web_hook_validation(_ctx, _param, webhook):
    return webhook