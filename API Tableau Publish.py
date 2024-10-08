import requests
import uuid
import os

base_url = "[YOUR_URL_TABLEAU]"
api_version = "api/[VERSION]"
auth_token = "[YOUR_TOKEN]"
site_id = "[YOUR_SITE_ID]"

### In general, this code must work for Flows, Datasources and Workbooks.
### You only need to change the xml_paylod atribute and the form-data: tableau_flow, tableau_workbook, etc.

def upload_flow(flow_name, project_id, flow_file_path):
    url = f"{base_url}/{api_version}/sites/{site_id}/flows"
    
    xml_payload = f"""
    <tsRequest>
        <flow name="{flow_name}">
            <project id="{project_id}" />
        </flow>
    </tsRequest>"""
    
    boundary = f"boundary-{uuid.uuid4()}"
    with open(flow_file_path, 'rb') as f:
        flow_file_content = f.read()

    #  boundary body
    body = (
        f"--{boundary}\r\n"
        "Content-Disposition: form-data; name=\"request_payload\"\r\n"
        "Content-Type: text/xml\r\n\r\n"
        f"{xml_payload}\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"tableau_flow\"; filename=\"{os.path.basename(flow_file_path)}\"\r\n"
        "Content-Type: application/octet-stream\r\n\r\n"
    ).encode('utf-8') + flow_file_content + f"\r\n--{boundary}--\r\n".encode('utf-8')


    content_length = str(len(body))

    # Configurar los headers
    headers = {
        "X-Tableau-Auth": auth_token,
        "Content-Type": f"multipart/mixed; boundary={boundary}",
        "Content-Length": content_length
    }

    # Enviar la solicitud multipart/mixed
    response = requests.post(url, data=body, headers=headers)

    if response.status_code == 201:
        print("Works")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

upload_flow("[FILE_NAME(WHITOUT THE EXTENSION)]", "[PROJECT_ID]", "[PATH OF THE FILE]")
## Example:
#upload_flow("Demo", "13df426a-34a7-4979-84d9-4c4fc9593f80", "Demo.tflx")
