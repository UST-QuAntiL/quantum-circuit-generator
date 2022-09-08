![Tests passed](https://github.com/UST-QuAntiL/quantum-circuit-generator/actions/workflows/main.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/UST-QuAntiL/quantum-circuit-generator/branch/main/graph/badge.svg?token=0GO5H9V7QC)](https://codecov.io/gh/UST-QuAntiL/quantum-circuit-generator)
# Quantum Circuit Generator
The quantum circuit generator enables service-based generation of quantum circuit fragments via a REST API.

It implements a selection of commonly used encodings, algorithms and algorithm fragments.
* Encodings are used to encode classical data for a quantum computer. Currently, basis encoding, amplitude encoding, angle encoding and schmidt decomposition are supported by the quantum circuit generator (more info [here](https://quantumcomputingpatterns.org/#/)
* Quantum algorithms can solve difficult problems efficiently on a quantum computer. The quantum circuit generator currently supports QAOA for the Maximum Cut (MaxCut) and Traveling Sales Person (TSP) problem. Moreover the HHL algorithm is supported to solve systems of linear equations.

## Running the Application
The easiest way to get start is using a pre-built Docker image:

``docker run -p 5073:5073 planqk/quantum-circuit-generator``

Alternatively, the application can be built manually:
1. Clone the repository using ``git clone https://github.com/UST-QuAntiL/quantum-circuit-generator.git``
2. Navigate to the repository  ``cd quantum-circuit-generator``
3. Build the Docker container: ``docker build -t quantum-circuit-generator .``
4. Run the Docker container: ``docker run -p 5073:5073 quantum-circuit-generator``

Then the application can be accessed via: [http://127.0.0.1:5073](http://127.0.0.1:5073).

## API Documentation

The quantum circuit generator service provides a Swagger UI, specifying the request schemas and showcasing exemplary requests for all API endpoints.
 * Swagger UI: [http://127.0.0.1:5073/app/swagger-ui](http://127.0.0.1:5073/app/swagger-ui).



## Developer Guide

### Setup (exemplary for ubuntu 18.04): 
* ``git clone https://github.com/UST-QuAntiL/objective-function-service.git`` 
* ``cd objective-function-service``
* ``sudo -H pip install virtualenv`` (if you don't have virtualenv installed)
* ``virtualenv venv`` (create virtualenv named 'venv')
* ``source venv/bin/activate`` (enter virtualenv; in Windows systems activate might be in ``venv/Scripts``)
* ``pip install -r requirements.txt`` (install application requirements)

### Execution:
* Run the application with: ``flask run --port=5072``
* Test with: ``python -m unittest discover``
* Coverage with: ``coverage run --branch --include 'app/*' -m unittest discover; coverage report``

### Codestyle: 
``black .`` OR ``black FILE|DIRECTORY``

### Disclaimer of Warranty
Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.

### Haftungsausschluss
Dies ist ein Forschungsprototyp. Die Haftung für entgangenen Gewinn, Produktionsausfall, Betriebsunterbrechung, entgangene Nutzungen, Verlust von Daten und Informationen, Finanzierungsaufwendungen sowie sonstige Vermögens- und Folgeschäden ist, außer in Fällen von grober Fahrlässigkeit, Vorsatz und Personenschäden, ausgeschlossen.
