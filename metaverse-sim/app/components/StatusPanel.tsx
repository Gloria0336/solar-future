"use client";

import type { GameState } from "../../server/engine/GameEngine";

interface StatusPanelProps {
  state: GameState;
}

export default function StatusPanel({ state }: StatusPanelProps) {
  return (
    <aside className="status-panel">
      <div className="status-card">
        <h3 className="status-title">狀態</h3>
        <div>Tick: {state.world.tick}</div>
        <div>位置: {state.player.location}</div>
        <div>Credits: {state.player.credits}</div>
        <div>Energy: {state.player.energy}</div>
        <div>Mode: {state.player.mode}</div>
      </div>

      <div className="status-card">
        <h3 className="status-title">戰鬥狀態</h3>
        <div>{state.combat.inCombat ? "戰鬥中" : "待機"}</div>
      </div>
    </aside>
  );
}
