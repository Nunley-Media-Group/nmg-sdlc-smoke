# Marker verification repair

**Issue**: #87

Retain the exact-byte marker scenario. Remove Git-history assertions and recursive suite execution from marker steps. CI already runs pytest and Ruff externally. Release metadata and squash history are not product behavior.
