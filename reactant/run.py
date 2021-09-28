import subprocess

import click


@click.command()
@click.argument("python_file", type=click.Path(exists=True))
def runner(python_file):
    click.secho(f"Running {python_file}", fg="cyan")
    subprocess.run(["python", f"{python_file}"])
