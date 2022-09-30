# Quantum Circuit Generator
﻿![Tests passed](https://github.com/UST-QuAntiL/quantum-circuit-generator/actions/workflows/test.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/UST-QuAntiL/quantum-circuit-generator/branch/main/graph/badge.svg?token=0GO5H9V7QC)](https://codecov.io/gh/UST-QuAntiL/quantum-circuit-generator)

The quantum circuit generator enables service-based generation of quantum circuit fragments via a REST API.

It implements a selection of commonly used encodings, algorithms, and algorithm fragments:
* Encodings are used to encode classical data for a quantum computer. The following encodings are currently supported by the quantum circuit generator:
    * [Basis encoding](https://quantumcomputingpatterns.org/#/patterns/0)
    * [Amplitude encoding](https://quantumcomputingpatterns.org/#/patterns/2)
    * [Angle encoding](https://quantumcomputingpatterns.org/#/patterns/3)
    * [Schmidt decomposition](https://quantumcomputingpatterns.org/#/patterns/12)
* Quantum algorithms can solve difficult problems efficiently on a quantum computer. Currently, the following algorithms are supported:
    * [QAOA](https://quantumcomputingpatterns.org/#/patterns/9) for the Maximum Cut (MaxCut) and Traveling Sales Person (TSP) problems
    * [HHL algorithm](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.103.150502) to solve systems of linear equations
    * [VQE](https://quantumcomputingpatterns.org/#/patterns/7) for approximating the lowest eigenvalue of a matrix

## Running the Service
The easiest way to get start is using a pre-built Docker image:

``docker run -p 5073:5073 planqk/quantum-circuit-generator``

Alternatively, the service can be built manually:
1. Clone the repository using ``git clone https://github.com/UST-QuAntiL/quantum-circuit-generator.git``
2. Navigate to the repository  ``cd quantum-circuit-generator``
3. Build the Docker container: ``docker build -t quantum-circuit-generator .``
4. Run the Docker container: ``docker run -p 5073:5073 quantum-circuit-generator``

Then the service can be accessed via: [http://127.0.0.1:5073](http://127.0.0.1:5073).

## API Documentation

The quantum circuit generator service provides a Swagger UI, specifying the request schemas and showcasing exemplary requests for all API endpoints.
 * Swagger UI: [http://127.0.0.1:5073/api/swagger-ui](http://127.0.0.1:5073/api/swagger-ui).

## Developer Guide

### Setup (exemplary for ubuntu 18.04): 
```shell
git clone https://github.com/UST-QuAntiL/quantum-circuit-generator.git
cd quantum-circuit-generator

# if virtualenv is not installed
sudo -H pip install virtualenv

# create new virtualenv called 'venv'
virtualenv venv

# activate virtualenv; in Windows systems activate might be in 'venv/Scripts'
source venv/bin/activate

#install application requirements.
pip install -r requirements.txt
```

### Execution:
* Run the application with: ``flask run --port=5073``
* Test with: ``python -m unittest discover``
* Coverage with: ``coverage run --branch --include 'app/*' -m unittest discover; coverage report``

### Codestyle: 
``black .`` OR ``black FILE|DIRECTORY``

## Disclaimer of Warranty
Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.

## Haftungsausschluss
Dies ist ein Forschungsprototyp. Die Haftung für entgangenen Gewinn, Produktionsausfall, Betriebsunterbrechung, entgangene Nutzungen, Verlust von Daten und Informationen, Finanzierungsaufwendungen sowie sonstige Vermögens- und Folgeschäden ist, außer in Fällen von grober Fahrlässigkeit, Vorsatz und Personenschäden, ausgeschlossen.

## Acknowledgements
The initial code contribution has been supported by the project [SEQUOIA](https://www.iaas.uni-stuttgart.de/forschung/projekte/sequoia/) funded by the [Baden-Wuerttemberg Ministry of the Economy, Labour and Housing](https://wm.baden-wuerttemberg.de/).
