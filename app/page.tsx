"use client";

import { useMemo, useState } from "react";
import { GameEngine, type GameState } from "../server/engine/GameEngine";
import MapView from "./components/MapView";
import StatusPanel from "./components/StatusPanel";
import EventLog from "./components/EventLog";
import ActionPanel from "./components/ActionPanel";

export default function HomePage() {
  const engine = useMemo(() => new GameEngine(), []);
  const [state, setState] = useState<GameState>(engine.getState());
  const [zoom, setZoom] = useState(0);

  const handleZoomIn = () => setZoom((value) => Math.min(2, value + 1));
  const handleZoomOut = () => setZoom((value) => Math.max(0, value - 1));

  return (
    <main>
      <MapView zoom={zoom} state={state} onZoomIn={handleZoomIn} onZoomOut={handleZoomOut} />
      <StatusPanel state={state} />
      <EventLog state={state} />
      <ActionPanel
        onWork={() => setState(engine.work())}
        onMove={() => setState(engine.move())}
        onStartCombat={() => setState(engine.startCombat())}
        onEndCombat={() => setState(engine.endCombat())}
        onSave={() => {
          engine.save();
          setState(engine.getState());
        }}
        onLoad={() => setState(engine.load())}
      />
    </main>
  );
}
