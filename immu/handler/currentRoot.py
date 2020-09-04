from dataclasses import dataclass

from immu.schema import schema_pb2
from immu.service import schema_pb2_grpc
from immu.rootService import RootService

@dataclass
class CurrentRootResponse:
    index: int
    root: bytes

def call(service: schema_pb2_grpc.ImmuServiceStub, rs: RootService, request: None):
    root = rs.get()
    return CurrentRootResponse(index=root.index, root=root.root)
