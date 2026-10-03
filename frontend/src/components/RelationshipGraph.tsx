import React, { useState, useMemo } from 'react';
import { GraphData, GraphNode, GraphEdge } from '../types';
import { Network, Filter, Info, X } from 'lucide-react';

interface RelationshipGraphProps {
  graph: GraphData;
}

export const RelationshipGraph: React.FC<RelationshipGraphProps> = ({ graph }) => {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [filterType, setFilterType] = useState<string>('all');

  const filteredNodes = useMemo(() => {
    if (filterType === 'all') return graph.nodes;
    return graph.nodes.filter((n) => n.type === filterType || n.type === 'session');
  }, [graph.nodes, filterType]);

  const activeNodeIds = useMemo(() => new Set(filteredNodes.map((n) => n.id)), [filteredNodes]);

  const filteredEdges = useMemo(() => {
    return graph.edges.filter((e) => activeNodeIds.has(e.source) && activeNodeIds.has(e.target));
  }, [graph.edges, activeNodeIds]);

  // Compute 2D node layout positions
  const nodePositions = useMemo(() => {
    const pos: Record<string, { x: number; y: number }> = {};
    const width = 800;
    const height = 460;
    const centerX = width / 2;
    const centerY = height / 2;

    const sessionNodes = filteredNodes.filter((n) => n.type === 'session');
    const procNodes = filteredNodes.filter((n) => n.type === 'process');
    const fileNodes = filteredNodes.filter((n) => n.type === 'file');
    const dirNodes = filteredNodes.filter((n) => n.type === 'directory');
    const eventNodes = filteredNodes.filter((n) => n.type === 'event');

    sessionNodes.forEach((n) => {
      pos[n.id] = { x: centerX, y: centerY - 140 };
    });

    dirNodes.forEach((n, i) => {
      const angle = (i / Math.max(1, dirNodes.length)) * Math.PI - Math.PI / 2;
      pos[n.id] = {
        x: centerX + Math.cos(angle) * 260,
        y: centerY - 40 + Math.sin(angle) * 80,
      };
    });

    fileNodes.forEach((n, i) => {
      const angle = (i / Math.max(1, fileNodes.length)) * 2 * Math.PI;
      pos[n.id] = {
        x: centerX + Math.cos(angle) * 160,
        y: centerY + Math.sin(angle) * 100,
      };
    });

    procNodes.forEach((n, i) => {
      pos[n.id] = {
        x: 100 + i * 160,
        y: 60,
      };
    });

    eventNodes.forEach((n, i) => {
      const angle = (i / Math.max(1, eventNodes.length)) * Math.PI;
      pos[n.id] = {
        x: 100 + (i * (width - 200)) / Math.max(1, eventNodes.length - 1),
        y: height - 60 - (i % 2) * 35,
      };
    });

    return pos;
  }, [filteredNodes]);

  const getNodeColor = (type: string) => {
    switch (type) {
      case 'session':
        return '#8B5CF6';
      case 'file':
        return '#10B981';
      case 'event':
        return '#06B6D4';
      case 'process':
        return '#F97316';
      case 'directory':
        return '#64748B';
      default:
        return '#38BDF8';
    }
  };

  return (
    <div className="card" style={{ marginTop: '1.5rem', position: 'relative' }}>
      {/* Header and Controls */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <Network size={18} color="#A855F7" />
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF' }}>
            Multi-Relational Knowledge Graph (NetworkX)
          </h3>
        </div>

        {/* Node Filters */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Filter size={14} color="var(--text-dim)" />
          <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>Filter Entities:</span>
          {['all', 'file', 'event', 'process', 'directory'].map((t) => (
            <button
              key={t}
              onClick={() => setFilterType(t)}
              style={{
                background: filterType === t ? 'rgba(168, 85, 247, 0.2)' : 'rgba(255, 255, 255, 0.04)',
                color: filterType === t ? '#C084FC' : 'var(--text-muted)',
                border: filterType === t ? '1px solid rgba(168, 85, 247, 0.5)' : '1px solid var(--border-subtle)',
                padding: '0.2rem 0.5rem',
                borderRadius: '4px',
                fontSize: '0.7rem',
                fontWeight: 600,
                cursor: 'pointer',
                textTransform: 'uppercase',
              }}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* SVG Canvas */}
      <div
        style={{
          width: '100%',
          height: '480px',
          background: 'rgba(8, 12, 20, 0.75)',
          borderRadius: '0.75rem',
          border: '1px solid var(--border-subtle)',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <svg width="100%" height="100%" viewBox="0 0 800 460" preserveAspectRatio="xMidYMid meet">
          <defs>
            <marker
              id="arrowhead"
              markerWidth="8"
              markerHeight="6"
              refX="14"
              refY="3"
              orient="auto"
            >
              <polygon points="0 0, 8 3, 0 6" fill="rgba(148, 163, 184, 0.6)" />
            </marker>
            <marker
              id="arrowhead-derived"
              markerWidth="10"
              markerHeight="7"
              refX="16"
              refY="3.5"
              orient="auto"
            >
              <polygon points="0 0, 10 3.5, 0 7" fill="#38BDF8" />
            </marker>
          </defs>

          {/* Edges */}
          {filteredEdges.map((edge, idx) => {
            const src = nodePositions[edge.source];
            const tgt = nodePositions[edge.target];
            if (!src || !tgt) return null;

            const isDerived = edge.relationship_type.includes('DERIVED') || edge.relationship_type.includes('RELATED');
            const strokeColor = isDerived ? '#38BDF8' : 'rgba(148, 163, 184, 0.3)';
            const strokeWidth = isDerived ? 2 : 1;
            const midX = (src.x + tgt.x) / 2;
            const midY = (src.y + tgt.y) / 2;

            return (
              <g key={`edge-${idx}`}>
                <line
                  x1={src.x}
                  y1={src.y}
                  x2={tgt.x}
                  y2={tgt.y}
                  stroke={strokeColor}
                  strokeWidth={strokeWidth}
                  strokeDasharray={edge.relationship_type === 'POSSIBLY_DERIVED_FROM' ? '4 3' : 'none'}
                  markerEnd={isDerived ? 'url(#arrowhead-derived)' : 'url(#arrowhead)'}
                />
                {isDerived && (
                  <text
                    x={midX}
                    y={midY - 4}
                    fill="#38BDF8"
                    fontSize="9"
                    fontWeight="700"
                    textAnchor="middle"
                    className="font-mono"
                    style={{ background: 'rgba(0,0,0,0.8)' }}
                  >
                    {edge.label} ({edge.score.toFixed(2)})
                  </text>
                )}
              </g>
            );
          })}

          {/* Nodes */}
          {filteredNodes.map((node) => {
            const p = nodePositions[node.id];
            if (!p) return null;
            const isSelected = selectedNode?.id === node.id;
            const color = getNodeColor(node.type);

            return (
              <g
                key={node.id}
                transform={`translate(${p.x}, ${p.y})`}
                onClick={() => setSelectedNode(node)}
                style={{ cursor: 'pointer' }}
              >
                <circle
                  r={isSelected ? 18 : 14}
                  fill="#0F172A"
                  stroke={color}
                  strokeWidth={isSelected ? 3 : 2}
                  filter={isSelected ? 'drop-shadow(0 0 8px ' + color + ')' : 'none'}
                />
                <circle r={isSelected ? 7 : 5} fill={color} />
                <text
                  y={isSelected ? 30 : 26}
                  fill="#F1F5F9"
                  fontSize="10"
                  fontWeight="600"
                  textAnchor="middle"
                  className="font-mono"
                >
                  {node.label.length > 20 ? node.label.substring(0, 18) + '...' : node.label}
                </text>
                <text
                  y={isSelected ? 40 : 36}
                  fill="var(--text-dim)"
                  fontSize="8"
                  textAnchor="middle"
                  style={{ textTransform: 'uppercase' }}
                >
                  {node.type}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Legend */}
        <div
          style={{
            position: 'absolute',
            bottom: '10px',
            left: '10px',
            display: 'flex',
            gap: '0.75rem',
            background: 'rgba(14, 22, 38, 0.9)',
            padding: '0.4rem 0.75rem',
            borderRadius: '6px',
            border: '1px solid var(--border-subtle)',
            fontSize: '0.7rem',
          }}
        >
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: '#8B5CF6' }}>● Session</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: '#10B981' }}>● File</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: '#06B6D4' }}>● Event</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: '#F97316' }}>● Process</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: '#64748B' }}>● Directory</span>
        </div>

        {/* Selected Node Details Drawer */}
        {selectedNode && (
          <div
            style={{
              position: 'absolute',
              top: '10px',
              right: '10px',
              width: '280px',
              background: 'rgba(19, 31, 51, 0.95)',
              border: '1px solid var(--inference-color)',
              borderRadius: '8px',
              padding: '1rem',
              boxShadow: '0 8px 30px rgba(0,0,0,0.6)',
              zIndex: 10,
              fontSize: '0.8rem',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Info size={14} color="#38BDF8" />
                <span style={{ fontWeight: 700, color: '#FFFFFF' }}>Entity Inspector</span>
              </div>
              <button
                onClick={() => setSelectedNode(null)}
                style={{ background: 'transparent', border: 'none', color: 'var(--text-dim)', cursor: 'pointer' }}
              >
                <X size={14} />
              </button>
            </div>

            <div style={{ marginBottom: '0.5rem' }}>
              <span className="badge" style={{ background: 'rgba(255,255,255,0.06)', color: getNodeColor(selectedNode.type), fontSize: '0.68rem' }}>
                {selectedNode.type.toUpperCase()}
              </span>
            </div>

            <div className="font-mono" style={{ color: '#FFFFFF', fontWeight: 600, wordBreak: 'break-all', marginBottom: '0.5rem' }}>
              {selectedNode.label}
            </div>

            {selectedNode.metadata && Object.keys(selectedNode.metadata).length > 0 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                {Object.entries(selectedNode.metadata).map(([k, v]) => (
                  <div key={k}>
                    <strong style={{ color: 'var(--text-dim)' }}>{k}:</strong> {String(v)}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
