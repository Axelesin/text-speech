# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import logging
import subprocess

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common_templates = gcp.CommonTemplates()

versions = ['v1', 'v1beta1']

for version in versions:
    library = gapic.node_library('texttospeech', version)

    # skip index, protos, package.json, and README.md
    s.copy(
        library,
        excludes=['package.json', 'README.md', 'src/index.js'],
    )

templates = common_templates.node_library()
s.copy(templates)

# Fix dead link
s.replace('src/v1/doc/google/cloud/texttospeech/v1/doc_cloud_tts.js',
        "\(https:[\s\*]+(.*)\)",
        r"(https:\1)")

# Node.js specific cleanup
subprocess.run(['npm', 'install'])
subprocess.run(['npm', 'run', 'fix'])
subprocess.run(['npx', 'compileProtos', 'src'])
