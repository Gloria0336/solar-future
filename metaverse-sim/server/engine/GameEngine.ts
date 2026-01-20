export type GameMode = "WORLD" | "COMBAT";

export interface PlayerState {
  location: string;
  credits: number;
  energy: number;
  mode: GameMode;
}

export interface WorldState {
  tick: number;
  nodes: string[];
}

export interface CombatState {
  inCombat: boolean;
}

export interface GameState {
  player: PlayerState;
  world: WorldState;
  log: string[];
  combat: CombatState;
}

const MAX_LOG_LINES = 30;
const SAVE_KEY = "metaverse_save_1";

export class GameEngine {
  private state: GameState;

  constructor() {
    this.state = this.createInitialState();
  }

  getState(): GameState {
    return structuredClone(this.state);
  }

  work(): GameState {
    this.state.player.energy = Math.max(0, this.state.player.energy - 10);
    this.state.player.credits += 30;
    this.state.world.tick += 1;
    this.appendLog("打工完成：energy -10，credits +30。");
    return this.getState();
  }

  move(): GameState {
    const currentIndex = this.state.world.nodes.indexOf(this.state.player.location);
    const nextIndex = (currentIndex + 1) % this.state.world.nodes.length;
    this.state.player.location = this.state.world.nodes[nextIndex];
    this.state.world.tick += 1;
    this.appendLog(`移動至 ${this.state.player.location}。`);
    return this.getState();
  }

  startCombat(): GameState {
    this.state.player.mode = "COMBAT";
    this.state.combat.inCombat = true;
    this.appendLog("進入戰鬥模式（假）。");
    return this.getState();
  }

  endCombat(): GameState {
    this.state.player.mode = "WORLD";
    this.state.combat.inCombat = false;
    this.appendLog("結束戰鬥模式，回到 WORLD。");
    return this.getState();
  }

  save(): void {
    if (typeof window === "undefined") {
      return;
    }
    localStorage.setItem(SAVE_KEY, JSON.stringify(this.state));
    this.appendLog("已存檔。", false);
  }

  load(): GameState {
    if (typeof window === "undefined") {
      return this.getState();
    }
    const payload = localStorage.getItem(SAVE_KEY);
    if (!payload) {
      this.appendLog("無存檔可讀取。", false);
      return this.getState();
    }
    this.state = JSON.parse(payload) as GameState;
    this.appendLog("已讀檔。", false);
    return this.getState();
  }

  private createInitialState(): GameState {
    return {
      player: {
        location: "EARTH",
        credits: 120,
        energy: 100,
        mode: "WORLD"
      },
      world: {
        tick: 0,
        nodes: ["EARTH", "MARS", "LUNA"]
      },
      log: ["系統啟動：開始測試。"],
      combat: {
        inCombat: false
      }
    };
  }

  private appendLog(message: string, includeTick = true): void {
    const prefix = includeTick ? `[${this.state.world.tick}] ` : "";
    this.state.log.unshift(`${prefix}${message}`);
    this.state.log = this.state.log.slice(0, MAX_LOG_LINES);
  }
}
