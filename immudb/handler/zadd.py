# Copyright 2021 CodeNotary, Inc. All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass

from immudb.grpc import schema_pb2
from immudb.grpc import schema_pb2_grpc
from immudb.rootService import RootService
from immudb.exceptions import VerificationException
from immudb import datatypes


def call(service: schema_pb2_grpc.ImmuServiceStub, rs: RootService, zset: bytes, score: float, key: bytes, atTx: int = 0):
    request = schema_pb2.ZAddRequest(
        set=zset,
        score=score,
        key=key,
        atTx=atTx,
        boundRef=atTx > 0,
    )
    msg = service.ZAdd(request)
    if msg.nentries != 1:
        raise VerificationException
    return datatypes.SetResponse(
        id=msg.id,
        verified=False,
    )
