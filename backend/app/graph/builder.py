import networkx as nx
from typing import List, Dict, Any
from app.schemas.event import EventNormalized
from app.schemas.investigation import GraphData, GraphNode, GraphEdge
from app.engine.correlator import compute_pairwise_correlation

def build_investigation_graph(
    session_id: str,
    events: List[EventNormalized],
    min_relationship_score: float = 0.35
) -> GraphData:
    """
    Constructs a NetworkX multi-type directed graph connecting:
    Sessions, Directories, Files, Events, and Processes.
    Exports cleanly to GraphData schema for interactive frontend rendering.
    """
    G = nx.DiGraph()
    
    # 1. Add Session Root Node
    G.add_node(
        f"session:{session_id}",
        label=f"Session: {session_id}",
        type="session",
        metadata={"session_id": session_id}
    )

    # Track distinct files, directories, processes
    files_added = set()
    dirs_added = set()
    procs_added = set()

    sorted_events = sorted(events, key=lambda e: e.timestamp)

    # 2. Add Entities and Event Nodes
    for evt in sorted_events:
        # Directory node
        dir_id = f"dir:{evt.directory}"
        if dir_id not in dirs_added:
            dirs_added.add(dir_id)
            G.add_node(dir_id, label=evt.directory or "Root", type="directory", metadata={"path": evt.directory})

        # File node
        file_id = f"file:{evt.path}"
        if file_id not in files_added:
            files_added.add(file_id)
            G.add_node(
                file_id,
                label=evt.file_name,
                type="file",
                metadata={"file_name": evt.file_name, "extension": evt.extension, "path": evt.path}
            )
            # File located in Directory edge
            G.add_edge(file_id, dir_id, label="LOCATED_IN", relationship_type="LOCATED_IN", score=1.0, evidence_ids=[evt.event_id])

        # Process node
        if evt.process_name:
            proc_id = f"proc:{evt.process_name}"
            if proc_id not in procs_added:
                procs_added.add(proc_id)
                G.add_node(proc_id, label=evt.process_name, type="process", metadata={"process_name": evt.process_name})

        # Event node
        evt_node_id = f"evt:{evt.event_id}"
        G.add_node(
            evt_node_id,
            label=f"{evt.event_type}\n({evt.timestamp.strftime('%H:%M:%S')})",
            type="event",
            timestamp=evt.timestamp.isoformat(),
            size=evt.file_size,
            metadata={
                "event_id": evt.event_id,
                "event_type": evt.event_type,
                "file_name": evt.file_name,
                "file_size": evt.file_size,
                "path": evt.path
            }
        )

        # Event belongs to Session
        G.add_edge(evt_node_id, f"session:{session_id}", label="SAME_SESSION", relationship_type="SAME_SESSION", score=1.0, evidence_ids=[evt.event_id])

        # Event operates on File
        edge_rel = evt.event_type.replace("FILE_", "")
        G.add_edge(evt_node_id, file_id, label=edge_rel, relationship_type=edge_rel, score=1.0, evidence_ids=[evt.event_id])

        # Process triggered Event
        if evt.process_name:
            G.add_edge(f"proc:{evt.process_name}", evt_node_id, label="INITIATED", relationship_type="INITIATED", score=1.0, evidence_ids=[evt.event_id])

    # 3. Add Pairwise File Relationships (RELATED_TO, POSSIBLY_DERIVED_FROM)
    for i in range(len(sorted_events)):
        for j in range(i + 1, len(sorted_events)):
            e1 = sorted_events[i]
            e2 = sorted_events[j]
            if e1.file_name == e2.file_name:
                continue

            score, _ = compute_pairwise_correlation(e1, e2)
            if score >= min_relationship_score:
                f1_id = f"file:{e1.path}"
                f2_id = f"file:{e2.path}"
                
                # Check for derived relationship (e.g. docx -> pdf, image -> archive)
                if (e1.extension in ("docx", "doc", "txt") and e2.extension == "pdf") or (e1.extension in ("png", "jpg") and e2.extension == "zip"):
                    rel_label = "POSSIBLY_DERIVED_FROM"
                else:
                    rel_label = "RELATED_TO"

                if not G.has_edge(f1_id, f2_id) and not G.has_edge(f2_id, f1_id):
                    G.add_edge(
                        f1_id,
                        f2_id,
                        label=rel_label,
                        relationship_type=rel_label,
                        score=score,
                        evidence_ids=[e1.event_id, e2.event_id]
                    )

    # 4. Serialize to GraphData schema
    nodes: List[GraphNode] = []
    for node_id, attrs in G.nodes(data=True):
        nodes.append(GraphNode(
            id=node_id,
            label=attrs.get("label", node_id),
            type=attrs.get("type", "entity"),
            timestamp=attrs.get("timestamp"),
            size=attrs.get("size"),
            is_anomaly=attrs.get("is_anomaly", False),
            metadata=attrs.get("metadata", {})
        ))

    edges: List[GraphEdge] = []
    for u, v, attrs in G.edges(data=True):
        edges.append(GraphEdge(
            source=u,
            target=v,
            label=attrs.get("label", "CONNECTS"),
            relationship_type=attrs.get("relationship_type", "CONNECTS"),
            score=attrs.get("score", 1.0),
            evidence_ids=attrs.get("evidence_ids", [])
        ))

    return GraphData(nodes=nodes, edges=edges)
