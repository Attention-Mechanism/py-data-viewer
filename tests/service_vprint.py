from py_data_viewer import vprint
from service import generate_mock_response

response = generate_mock_response()
vprint(response, var_name="response", output="out/response.txt")
