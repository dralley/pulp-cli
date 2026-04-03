import click

from pulp_glue.common.i18n import get_translation
from pulp_glue.rust.context import (
    PulpRustDistributionContext,
    PulpRustRemoteContext,
    PulpRustRepositoryContext,
)

from pulp_cli.generic import (
    PulpCLIContext,
    common_distribution_create_options,
    content_guard_option,
    create_command,
    destroy_command,
    distribution_filter_options,
    distribution_lookup_option,
    href_option,
    label_command,
    list_command,
    name_option,
    pass_pulp_context,
    pulp_group,
    pulp_labels_option,
    pulp_option,
    resource_option,
    show_command,
    update_command,
)

translation = get_translation(__package__)
_ = translation.gettext


repository_option = resource_option(
    "--repository",
    default_plugin="rust",
    default_type="rust",
    context_table={"rust:rust": PulpRustRepositoryContext},
    href_pattern=PulpRustRepositoryContext.HREF_PATTERN,
    help=_(
        "Repository to be used for auto-distributing."
        " Specified as '[[<plugin>:]<type>:]<name>' or as href."
    ),
)


@pulp_group()
@click.option(
    "-t",
    "--type",
    "distribution_type",
    type=click.Choice(["rust"], case_sensitive=False),
    default="rust",
)
@pass_pulp_context
@click.pass_context
def distribution(ctx: click.Context, pulp_ctx: PulpCLIContext, /, distribution_type: str) -> None:
    if distribution_type == "rust":
        ctx.obj = PulpRustDistributionContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option, name_option, distribution_lookup_option]
nested_lookup_options = [distribution_lookup_option]
update_options = [
    repository_option,
    pulp_option(
        "--version",
        type=int,
        help=_(
            "The repository version number to distribute."
            " When unset, the latest version of the repository will be auto-distributed."
        ),
    ),
    resource_option(
        "--remote",
        default_plugin="rust",
        default_type="rust",
        context_table={"rust:rust": PulpRustRemoteContext},
        href_pattern=PulpRustRemoteContext.HREF_PATTERN,
        help=_(
            "Remote to use for pull-through caching."
            " Specified as '[[<plugin>:]<type>:]<name>' or as href."
        ),
    ),
    content_guard_option,
    pulp_labels_option,
]
create_options = common_distribution_create_options + update_options

distribution.add_command(list_command(decorators=distribution_filter_options))
distribution.add_command(show_command(decorators=lookup_options))
distribution.add_command(create_command(decorators=create_options))
distribution.add_command(
    update_command(decorators=lookup_options + update_options + [click.option("--base-path")])
)
distribution.add_command(destroy_command(decorators=lookup_options))
distribution.add_command(label_command(decorators=nested_lookup_options))
