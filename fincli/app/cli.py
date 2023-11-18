import click
import os

@click.group(invoke_without_command=True)
@click.option('--history','--hist',is_flag=True,help='Use filters of recent search.')
@click.option('--debug',is_flag=True,help='Display details logging.')
@click.pass_context
def run_main(ctx: click.Context,
             history: bool = False,
             debug: bool = False
             ) -> None:
    """
    Welcome to the Stock Screener CLI!
    """
    click.echo("Welcome to the Stock Screener CLI!")
    from .main import run_stock_screener
    
    if ctx.invoked_subcommand is None:
        run_stock_screener(history=history,debug=debug)

if __name__ == '__main__':
    run_main()
    
