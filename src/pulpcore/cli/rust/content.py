import click

from pulp_glue.common.i18n import get_translation
from pulp_glue.rust.context import PulpRustContentContext

from pulp_cli.generic import (
    PulpCLIContext,
    content_filter_options,
    href_option,
    list_command,
    pass_pulp_context,
    pulp_group,
    show_command,
)

translation = get_translation(__package__)
_ = translation.gettext


@pulp_group()
@click.option(
    "-t",
    "--type",
    "content_type",
    type=click.Choice(["rust"], case_sensitive=False),
    default="rust",
)
@pass_pulp_context
@click.pass_context
def content(ctx: click.Context, pulp_ctx: PulpCLIContext, /, content_type: str) -> None:
    if content_type == "rust":
        ctx.obj = PulpRustContentContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [
    href_option,
]

content.add_command(
    list_command(
        decorators=[
            click.option("--name"),
            click.option("--vers"),
            *content_filter_options,
        ]
    )
)
content.add_command(show_command(decorators=lookup_options))
