import csv
import pdb
import click
import pickle
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from encryption_funcs.paillier import generate_keypair, encrypt, e_add, decrypt, e_mul_const, e_add_const
from encryption_funcs.checkdir import *
import pandas as pd

priv_path = "keys/priv.pkl"
pub_path = "keys/pub.pkl"

@click.command()
@click.argument('filename')

def cli(filename):
    """Perform calculations on Google sheets with a layer of fully homomorphic encryption."""

    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('homomorphic-encryption-poc-gcreds.json', scope)

    gc = gspread.authorize(credentials)

    worksheet = gc.open("Homomorphic-encryption-poc-test-sheet").sheet1
  
    if checkFileExistByPathlib(priv_path) & checkFileExistByPathlib(pub_path):
        with open("keys/priv.pkl", "rb") as f:
            priv = pickle.load(f)
        with open("keys/pub.pkl", "rb") as f:
            pub = pickle.load(f)
    else:
        print(f'Generating fresh private and public keypairs...')
        priv, pub = generate_keypair(7)  # we have to use n_bits<=7 for gsheets to handle the "computation" of multiplying big numbers

        with open(priv_path, "wb") as f:
            pickle.dump(priv, f)
        with open(pub_path, "wb") as f:
            pickle.dump(pub, f)

        print(f'Created new keypairs in {priv_path} and {pub_path}.')

    # content = open(filename, 'r').read()  
    # TODO: count how many rows. save as row_in_sheet

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        num = line_count + 1
        
        representation_dict = {
            "Input1": [],
            "Input2": [],
            "(Input1 + Input2)": [],
            "Enc(Input1)": [],
            "Enc(Input2)": [],
            "HE Sum(Pailler)": []
        }
        
        for row in csv_reader:
            if line_count == 0:
                worksheet.update_acell(f'A{num}', row[0])
                worksheet.update_acell(f'B{num}', row[1])
                # print(f'Input1 + \tInput2 = \t(Input1 + Input2) | Enc(Input1) Enc(Input2) | HE Sum (Pailler)')
                line_count += 1
                num +=1
            else:
                cx = encrypt(pub, int(row[0]))
                cy = encrypt(pub, int(row[1]))
                worksheet.update_acell(f'A{num}', cx)
                worksheet.update_acell(f'B{num}', cy)
                worksheet.update_acell(f'C{num}', f'=(A{num}*B{num})')
                
                """ Unencrypting response """
                cz = int(worksheet.acell(f'C{num}').value) % pub.n_sq
                z = decrypt(priv, pub, cz)
                
                representation_dict['Input1'].append(row[0])
                representation_dict['Input2'].append(row[1])
                representation_dict['(Input1 + Input2)'].append(int(row[0]) + int(row[1]))
                representation_dict['Enc(Input1)'].append(cx)
                representation_dict['Enc(Input2)'].append(cy)
                representation_dict['HE Sum(Pailler)'].append(cz)
                # print(f'{row[0]} + {row[1]} = {int(row[0]) + int(row[1])}  |  {cx} * {cy} % {pub.n_sq} = {cz}')
                worksheet.update_acell(f'D{num}', z)

                line_count += 1
                num += 1
        print()
        df = pd.DataFrame.from_dict(representation_dict,
                                    # columns=[
                                    #     "Input1",
                                    #     "Input2",
                                    #     "(Input1 + Input2)",
                                    #     "Enc(Input1)",
                                    #     "Enc(Input2)",
                                    #     "HE Sum (Pailler)"]
                                    )
        print(repr(df))
        print(f'Processed {line_count} lines.')
    return
    # pdb.set_trace() // debugger

if __name__ == '__main__':
    cli()