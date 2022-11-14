"""Console script for repaper."""
import sys

import click

from .repaper import Repaper as repaper


@click.group()
def main(args=None):
    """Console script for repaper."""
    click.echo(
        "Check repaper <command> --help for more information on the commands")


@main.command('google-form', help='Create a google form from the image')
@click.option('--img_path', default=None, required=True, help='Path to image')
@click.option('--use_gpu', default=False, help='Bool parameter to use gpu')
@click.option('--oauth_json', default=None, required=True, help='Path to oauth client json \n check https://developers.google.com/forms/api/quickstart/python to generate oauth client json')
def google_form(img_path, use_gpu, oauth_json):
    """
    Console script for repaper.
    """
    re_paper = repaper(img_path, use_gpu)
    form_id = re_paper.make_google_from(oauth_json)
    click.echo(
        f'''https://docs.google.com/forms/d/{form_id['formId']}/viewform''')


@main.command('editable-pdf', help='Create an editable pdf from the image')
@click.option('--img_path', default=None, required=True, help='Path to image')
@click.option('--use_gpu', default=False, help='Bool parameter to use gpu')
def editable_pdf(img_path, use_gpu):
    """
    Console script for repaper.
    """
    click.echo(
        f"Will be implemented in the next release args : {img_path} {use_gpu}")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
