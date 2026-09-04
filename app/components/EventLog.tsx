"use client";

import type { GameState } from "../../server/engine/GameEngine";

interface EventLogProps {
  state: GameState;
}

export default function EventLog({ state }: EventLogProps) {
  return (
    <section className="event-log">
      <h3>Event Log</h3>
      <ul>
        {state.log.map((entry, index) => (
          <li key={`${entry}-${index}`}>{entry}</li>
        ))}
      </ul>
    </section>
  );
}
