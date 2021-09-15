import subprocess
import click


@click.command()
@click.argument("python_file", type=click.Path(exists=True))
def runner(python_file):
    try:
        click.secho(f"Running {python_file}", fg="cyan")
        subprocess.run(["python", f"{python_file}"])
    except Exception:
        click.secho(f"Sorry. Something went wrong.", fg="red")
        raise
    else:
        click.secho(f'Success! Please check "reactant_products" directory.', fg="cyan")
