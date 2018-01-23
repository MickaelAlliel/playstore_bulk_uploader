import sys
import csv

import argparse
import httplib2
import json

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import AccessTokenRefreshError
from apiclient.discovery import build


def upload(package, service, apk, track):

	# Create an httplib2.Http object to handle our HTTP requests and authorize it
	# with the Credentials. Note that the first parameter, service_account_name,
	# is the Email address created for the Service account. It must be the email
	# address associated with the key that was created.
	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	  service, ['https://www.googleapis.com/auth/androidpublisher'])

	http_auth = credentials.authorize(http=httplib2.Http())
	service = build('androidpublisher', 'v2', http=http_auth)

	try:
		edit_request = service.edits().insert(body={}, packageName=package)
		result = edit_request.execute()
		edit_id = result['id']

		apk_response = service.edits().apks().upload(
			editId=edit_id,
			packageName=package,
			media_body=apk).execute()

		print('Version code %d has been uploaded for package %s' % (apk_response['versionCode'], package))


		track_response = service.edits().tracks().update(
			editId=edit_id,
			track=track,
			packageName=package,
			body={u'versionCodes': [apk_response['versionCode']]}).execute()

		print('Track %s is set for version code(s) %s'% (
			track_response['track'], str(track_response['versionCodes'])))

		commit_request = service.edits().commit(
			editId=edit_id, packageName=package).execute()

		print('Edit "%s" has been committed' % (commit_request['id']))
		

	except AccessTokenRefreshError:
		print ('The credentials have been revoked or expired, please re-run the '
			   'application to re-authorize')
	
	
	

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--csv', help='The path to the CSV file with all the other arguments', default='bulkupdate.csv')
	args = parser.parse_args()
	
	
	#CSV Format : 1 Row = 1 APK Upload -- PackageName >> ServiceAccountJsonPath >> ApkPath
	with open(args.csv, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		
		for row in csvreader:
			#You can change the 'track' parameter for these options : alpha, beta, rollout, production - as needed
			#row[0] = Package Name (ie: com.android.test)
			#row[1] = Path TO : ServiceAccount.json
			#row[2] = Path TO : New APK to upload
			
			upload(row[0], row[1], row[2], 'production')
  
  

if __name__ == '__main__':
	main()