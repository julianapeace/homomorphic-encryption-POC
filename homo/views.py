from django.shortcuts import render

def hello_world(request):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('homomorphic-encryption-poc-gcreds.json', scope)

    gc = gspread.authorize(credentials)

    wks = gc.open("Homomorphic-encryption-poc-test-sheet").sheet1
    wks.update_acell('B2', "it's down there somewhere, let me take another look.")

    # Fetch a cell range
    cell_list = wks.range('A1:B7')

    return render(request, 'hello_world.html', {})
