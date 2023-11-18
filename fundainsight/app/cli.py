import click


@click.group(invoke_without_command=True)
@click.option('--history', '--hist', is_flag=True, help='Display the history of filters used.')
@click.option('--debug', is_flag=True, help='Display details logging.')
@click.option('--set-filters', default="", help='Set filters to be used.')
@click.option('--scrape-link', default="", help='Set the scrape link to be used.')
@click.pass_context
def run_main(
    ctx: click.Context,
    history: bool = False,
    debug: bool = False,
    set_filters: str = "",
    scrape_link: str = ""
) -> None:
    
    from .main import get_opportunities
 

    if ctx.invoked_subcommand is None:
       get_opportunities(history=history,debug=debug,set_filters=set_filters,scrape_link=scrape_link)


if __name__ == '__main__':
    run_main()
