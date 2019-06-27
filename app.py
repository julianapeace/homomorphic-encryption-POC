import csv
import click
import gspread
from oauth2client.service_account import ServiceAccountCredentials

@click.command()
@click.argument('filename')

def cli(filename):
    """Perform calculations on Google sheets with a layer of fully homomorphic encryption."""

    click.echo('Hello %s!' % filename)

    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('homomorphic-encryption-poc-gcreds.json', scope)

    gc = gspread.authorize(credentials)

    worksheet = gc.open("Homomorphic-encryption-poc-test-sheet").sheet1

    # read in CSV file
    content = open(filename, 'r').read()
    gc.import_csv('12oISEPmhZ4_tcPEzrCXsaa2qfQaUqPJFHrWteVBd3Yo', content)

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in.')
                line_count += 1
        print(f'Processed {line_count} lines.')

if __name__ == '__main__':
    cli()