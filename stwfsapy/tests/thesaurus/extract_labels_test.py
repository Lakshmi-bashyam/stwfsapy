# Copyright 2020-2023 Leibniz Information Centre for Economics
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


import stwfsapy.thesaurus as t
import stwfsapy.tests.thesaurus.common as c


def test_extract_labels(label_graph):
    extracted = list(t.extract_labels(label_graph))
    assert (c.concept_ref_printed, c.concept_prefLabel_printed_en) in extracted
    assert (c.concept_ref_printed, c.concept_altLabel_printed_en) in extracted
