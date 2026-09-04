"use client";

import type { GameState } from "../../server/engine/GameEngine";

interface MapViewProps {
  zoom: number;
  state: GameState;
  onZoomIn: () => void;
  onZoomOut: () => void;
}

const nodeDetails: Record<string, { security: number; opportunity: number }> = {
  EARTH: { security: 78, opportunity: 64 },
  MARS: { security: 42, opportunity: 88 },
  LUNA: { security: 55, opportunity: 53 }
};

export default function MapView({ zoom, state, onZoomIn, onZoomOut }: MapViewProps) {
  const currentLocation = state.player.location;

  return (
    <section className="map-view">
      <div className="map-header">
        <h2>MapView</h2>
        <div className="zoom-controls">
          <button onClick={onZoomOut} disabled={zoom === 0}>
            -
          </button>
          <button onClick={onZoomIn} disabled={zoom === 2}>
            +
          </button>
        </div>
        <span className="badge">Zoom {zoom}</span>
      </div>

      {zoom === 0 && (
        <div className="map-card">
          <h3>Solar System</h3>
          <p>縮放後可以查看行星與節點資訊。</p>
        </div>
      )}

      {zoom === 1 && (
        <div className="map-card">
          <h3>行星節點</h3>
          <div className="map-list">
            {state.world.nodes.map((node) => (
              <button
                key={node}
                className={`map-button ${node === currentLocation ? "active" : ""}`}
                type="button"
              >
                {node}
              </button>
            ))}
          </div>
        </div>
      )}

      {zoom === 2 && (
        <div className="map-card">
          <h3>{currentLocation} 資訊卡</h3>
          <p>Security: {nodeDetails[currentLocation].security}</p>
          <p>Opportunity: {nodeDetails[currentLocation].opportunity}</p>
        </div>
      )}
    </section>
  );
}
