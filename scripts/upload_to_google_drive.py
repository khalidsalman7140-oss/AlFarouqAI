"""Owner-authorized Google Drive upload. Dry-run by default, never a billing bypass.
Requires gdrive extra and YOUR Desktop OAuth client credentials from Google Cloud.
The assistant cannot authorize your Google account and no token ships in the ZIP.
"""
from pathlib import Path
import argparse,json,os
SCOPES=['https://www.googleapis.com/auth/drive.file']

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--file',required=True);parser.add_argument('--credentials');parser.add_argument('--folder-id');parser.add_argument('--approve-upload',action='store_true');args=parser.parse_args()
    path=Path(args.file).expanduser().resolve()
    if not path.is_file():parser.error('File not found')
    print(json.dumps({'file':path.name,'bytes':path.stat().st_size,'scope':'drive.file','upload_requested':args.approve_upload,'needs_user_google_oauth':True},indent=2))
    if not args.approve_upload:return
    if not args.credentials or not Path(args.credentials).is_file():parser.error('Provide YOUR Google Desktop OAuth credentials file; do not commit or send it to the assistant')
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:raise SystemExit("Install the optional gdrive extra in your own environment: pip install '.[gdrive]'")
    token=Path.home()/'.config/alfarouqai/gdrive-token.json'
    creds=Credentials.from_authorized_user_file(str(token),SCOPES) if token.exists() else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:creds.refresh(Request())
        else:creds=InstalledAppFlow.from_client_secrets_file(args.credentials,SCOPES).run_local_server(port=0)
        token.parent.mkdir(parents=True,exist_ok=True);token.write_text(creds.to_json())
        if os.name=='posix':token.chmod(0o600)
    service=build('drive','v3',credentials=creds,cache_discovery=False)
    body={'name':path.name}
    if args.folder_id:body['parents']=[args.folder_id]
    result=service.files().create(body=body,media_body=MediaFileUpload(str(path),resumable=True),fields='id,webViewLink').execute()
    print(json.dumps({'uploaded':True,'id':result['id'],'private_view_url':result.get('webViewLink'),'sharing_changed':False},indent=2))
if __name__=='__main__':main()
