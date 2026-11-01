#!/usr/bin/env python3
"""Static checks for PBJ-2 model, DMN, and form files. Does not replace Camunda runtime tests."""
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BPMN_NS = {"bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL", "zeebe": "http://camunda.org/schema/zeebe/1.0"}
errors = []
for path in sorted(ROOT.glob("Lab*/*.bpmn")):
    try:
        root = ET.parse(path).getroot()
        processes = root.findall("bpmn:process", BPMN_NS)
        if len(processes) != 1:
            errors.append(f"{path}: expected exactly one process")
            continue
        proc = processes[0]
        nodes = {node.get("id"): node for node in proc if node.tag.rsplit("}", 1)[-1] != "sequenceFlow"}
        flows = proc.findall("bpmn:sequenceFlow", BPMN_NS)
        flow_ids = {f.get("id") for f in flows}
        for flow in flows:
            fid, source_id, target_id = flow.get("id"), flow.get("sourceRef"), flow.get("targetRef")
            if source_id not in nodes or target_id not in nodes:
                errors.append(f"{path}: {fid} has missing source/target")
                continue
            outgoing = [x.text for x in nodes[source_id].findall("bpmn:outgoing", BPMN_NS)]
            incoming = [x.text for x in nodes[target_id].findall("bpmn:incoming", BPMN_NS)]
            if fid not in outgoing or fid not in incoming:
                errors.append(f"{path}: {fid} is not linked on both source and target")
        for node in nodes.values():
            for reference in node.findall("bpmn:incoming", BPMN_NS) + node.findall("bpmn:outgoing", BPMN_NS):
                if reference.text not in flow_ids:
                    errors.append(f"{path}: {node.get('id')} references missing flow {reference.text}")
        # Every sequence flow should have a visual BPMN-DI edge.
        di_ns = {"bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI"}
        edge_ids = {edge.get("bpmnElement") for edge in root.findall(".//bpmndi:BPMNEdge", di_ns)}
        for fid in flow_ids - edge_ids:
            errors.append(f"{path}: {fid} has no BPMN-DI edge")
        # Every referenced deployment-bound form must exist and its JSON id must match.
        form_ids = {item.get("formId") for item in proc.findall(".//zeebe:formDefinition", BPMN_NS)}
        available_form_ids = set()
        for form_path in path.parent.glob("*.form"):
            try:
                available_form_ids.add(json.loads(form_path.read_text(encoding="utf-8")).get("id"))
            except Exception as exc:
                errors.append(f"{form_path}: {exc}")
        for form_id in form_ids - available_form_ids:
            errors.append(f"{path}: referenced form id '{form_id}' is missing")
        # Every called DMN decision must exist next to the BPMN model.
        dmn_ids = set()
        for dmn_path in path.parent.glob("*.dmn"):
            try:
                dmn_root = ET.parse(dmn_path).getroot()
                dmn_ids.update(d.get("id") for d in dmn_root.iter() if d.tag.rsplit("}", 1)[-1] == "decision")
            except Exception as exc:
                errors.append(f"{dmn_path}: {exc}")
        called_ids = {d.get("decisionId") for d in proc.findall(".//zeebe:calledDecision", BPMN_NS)}
        for decision_id in called_ids - dmn_ids:
            errors.append(f"{path}: called DMN decision '{decision_id}' is missing")
        if not proc.get("isExecutable") == "true":
            errors.append(f"{path}: process is not executable")
        print(f"BPMN OK: {path.relative_to(ROOT)} — {len(nodes)} nodes, {len(flows)} sequence flows")
    except Exception as exc:
        errors.append(f"{path}: {exc}")
for path in sorted(ROOT.glob("Lab*/*.dmn")):
    try:
        ET.parse(path)
        print(f"DMN XML OK: {path.relative_to(ROOT)}")
    except Exception as exc:
        errors.append(f"{path}: {exc}")
for path in sorted(ROOT.glob("Lab*/*.form")):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data.get("components"), list):
            errors.append(f"{path}: form has no components list")
        print(f"FORM JSON OK: {path.relative_to(ROOT)}")
    except Exception as exc:
        errors.append(f"{path}: {exc}")
if errors:
    print("\nVALIDATION ERRORS:")
    for error in errors: print(" -", error)
    sys.exit(1)
print("\nStatic package validation passed. Deploy and execute in Camunda to complete runtime validation.")
