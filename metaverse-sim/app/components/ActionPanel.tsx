"use client";

interface ActionPanelProps {
  onWork: () => void;
  onMove: () => void;
  onStartCombat: () => void;
  onEndCombat: () => void;
  onSave: () => void;
  onLoad: () => void;
}

export default function ActionPanel({
  onWork,
  onMove,
  onStartCombat,
  onEndCombat,
  onSave,
  onLoad
}: ActionPanelProps) {
  return (
    <section className="action-panel">
      <button className="primary" onClick={onWork} type="button">
        打工
      </button>
      <button onClick={onMove} type="button">
        移動
      </button>
      <button onClick={onStartCombat} type="button">
        開始戰鬥(假)
      </button>
      <button onClick={onEndCombat} type="button">
        結束模式回 WORLD
      </button>
      <button onClick={onSave} type="button">
        存檔
      </button>
      <button onClick={onLoad} type="button">
        讀檔
      </button>
    </section>
  );
}
