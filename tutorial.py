import os
import webbrowser
import msal
from dotenv import load_dotenv 

TUTORIAL_BASE_URL = 'https://graph.microsoft.com/v1.0'

def get_access_token(application_id, client_secret, scopes):
    client = msal.ConfidentialClientApplication(
        client_id=application_id,
        client_credential=client_secret,
        # authority= 'https://graph.microsoftonline.com/consumers/' 
        authority= 'https://login.microsoftonline.com/common/'
    )
    
    refresh_token = None
    if os.path.exists('refresh_token.txt'):
        with open('refresh_token.txt', 'r') as file:
            refresh_token = file.read().strip()
            
    if refresh_token:
        token_response = client.acquire_token_by_refresh_token(refresh_token, scopes=scopes)
    else:
        # Si no existe el refresh_token, pedir autorización
        auth_request_url = client.get_authorization_request_url(scopes)
        webbrowser.open(auth_request_url)
        authorization_code = input('Enter the authorization code: ')

        # Verificar si authorization_code está vacío
        if not authorization_code:
            raise ValueError('Authorization code is empty')
        
        # Usar el código de autorización para obtener el token
        token_response = client.acquire_token_by_authorization_code(
            code=authorization_code,
            scopes=scopes
        )
    
    # Verificar si el acceso fue exitoso
    if 'access_token' in token_response:
        # Guardar el refresh_token si está presente
        if 'refresh_token' in token_response:
            with open('refresh_token.txt', 'w') as file:
                file.write(token_response['refresh_token'])
            
        return token_response['access_token']
    else:
        raise Exception('Failed to acquire access token: ' + str(token_response))
    
def main():
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES = ['User.Read', 'Mail.ReadWrite', 'Mail.Send']
    
    try:
        access_token = get_access_token(application_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        print(headers)
    except Exception as e:
        print(f'Error: {e}')
        
main()
