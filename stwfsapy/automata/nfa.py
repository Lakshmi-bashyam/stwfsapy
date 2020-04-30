# Copyright 2020 Leibniz Information Centre for Economics
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


from typing import Dict, Set, List
from stwfsapy.automata.heap import BinaryMinHeap
from stwfsapy.automata.util import safe_set_add_in_dict


class State:

    def __init__(self):
        self.symbol_transitions: Dict[str, int] = dict()
        """Determines the states that can be reached
        by consuming a character."""
        self.non_word_char_transitions: Set[int] = set()
        """Is not None if there is a transition via a non word symbol."""
        self.empty_transitions: Set[int] = set()
        """What can be reached using the empty String/Symbol."""
        self.incoming_empty_transitions: Set[int] = set()
        """How this state can be reached using the empty String/Symbol."""
        self.accepts = []
        """What is accepted by this State."""


class Nfa:

    def __init__(self):
        self.states: List[State] = []
        self.starts: List[int] = []

    def add_state(self):
        idx = len(self.states)
        self.states.append(State())
        return idx

    def add_start(self, idx):
        self.starts.append(idx)

    def add_acceptance(self, idx, accept):
        self.states[idx].accepts.append(accept)

    def add_symbol_transition(self, start: int, end: int, symbol: str):
        transitions = self.states[start].symbol_transitions
        safe_set_add_in_dict(transitions, symbol, end)

    def add_empty_transition(self, start: int, end: int):
        self.states[start].empty_transitions.add(end)
        self.states[end].incoming_empty_transitions.add(start)

    def add_non_word_char_transition(self, start: int, end: int):
        self.states[start].non_word_char_transitions.add(end)

    def remove_empty_transitions(self):
        queue = BinaryMinHeap()
        for idx in range(len(self.states)):
            if len(self.states[idx].incoming_empty_transitions) > 0:
                queue.push(len(self.states[idx].empty_transitions), idx)
        while len(queue.heap) > 0:
            ptr_idx = queue.pop()
            ptr = self.states[ptr_idx]
            if len(ptr.empty_transitions) > 0:
                raise Exception(
                    "There is an empty transition loop in the NFA.")
            for incoming_idx in ptr.incoming_empty_transitions.copy():
                incoming = self.states[incoming_idx]
                self._remove_empty_transition(
                    incoming_idx,
                    incoming,
                    ptr_idx,
                    ptr)
                if len(incoming.incoming_empty_transitions) > 0:
                    queue.change_key(
                        incoming_idx,
                        len(incoming.empty_transitions))

    def _remove_empty_transition(self, start_idx, start, end_idx, end):
        for symbol, states in end.symbol_transitions.items():
            for state_idx in states:
                safe_set_add_in_dict(
                    start.symbol_transitions,
                    symbol,
                    state_idx)
        for state_idx in end.non_word_char_transitions:
            start.non_word_char_transitions.add(state_idx)
        start.empty_transitions.discard(end_idx)
        end.incoming_empty_transitions.discard(start_idx)
