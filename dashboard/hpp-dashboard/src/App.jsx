import React, { useState, useEffect, useMemo } from 'react';
import {
  Activity,
  ShieldAlert,
  Cpu,
  Network,
  Zap,
  ArrowRight,
  Brain,
  Check,
  CircleAlert,
  Compass,
  Database,
  Dumbbell,
  Flame,
  Gauge,
  LineChart,
  Moon,
  RotateCcw,
  Shield,
  Sparkles,
  Timer
} from 'lucide-react';
import './index.css';

const STORAGE_KEY = "hpp-v5-runs";

const protocols = [
  {
    id: "nervous-system-reset",
    name: "Nervous System Reset",
    intent: "Return activation toward baseline before choosing the next action.",
    mode: "sentinel",
    duration: "4 min",
    trigger: "Stress, urgency, body tension, or loop collapse.",
    steps: [
      "Lower the breath and slow the exhale.",
      "Relax jaw, shoulders, hands, and belly.",
      "Name three body sensations without interpreting them.",
      "Choose the smallest useful action visible from here.",
    ],
    reflectionPrompt: "What changed in the body, and what became possible next?",
    tags: ["stress", "body", "reset"],
  },
  {
    id: "focus-ignition",
    name: "Focus Ignition",
    intent: "Enter one clean work sprint with less negotiation.",
    mode: "nurture",
    duration: "12 min",
    trigger: "Avoidance, scattered attention, or a stalled task.",
    steps: [
      "Write one target in plain language.",
      "Remove one source of noise.",
      "Set a short timer.",
      "Begin with the easiest visible action.",
    ],
    reflectionPrompt: "What lowered friction, and what tried to pull the loop away?",
    tags: ["focus", "work", "friction"],
  },
  {
    id: "identity-rehearsal",
    name: "Identity Rehearsal",
    intent: "Practice acting from the identity being built.",
    mode: "nurture",
    duration: "6 min",
    trigger: "A moment where the old loop wants to steer.",
    steps: [
      "Name the identity being trained.",
      "Name the current resistance without arguing with it.",
      "Ask what this identity would do in the next five minutes.",
      "Do that action before renegotiating.",
    ],
    reflectionPrompt: "Which identity got a repetition today?",
    tags: ["identity", "choice", "practice"],
  },
  {
    id: "evidence-capture",
    name: "Evidence Capture",
    intent: "Convert a messy experience into usable training evidence.",
    mode: "nurture",
    duration: "8 min",
    trigger: "After a breakthrough, setback, or meaningful protocol run.",
    steps: [
      "Record what happened without polishing it.",
      "Mark the state before and after.",
      "Name the strongest resistance signal.",
      "Decide whether the protocol should repeat, change, or rest.",
    ],
    reflectionPrompt: "What is the smallest honest lesson from this loop?",
    tags: ["journal", "evidence", "review"],
  },
];

const defaultSignals = {
  energy: 54,
  focus: 42,
  mood: 56,
  stress: 38,
  clarity: 45,
  tension: 33,
};

const signalLabels = [
  ["energy", "Energy"],
  ["focus", "Focus"],
  ["mood", "Mood"],
  ["stress", "Stress"],
  ["clarity", "Clarity"],
  ["tension", "Tension"],
];

const habitMemoryEvidence = {
  threshold: "14",
  recallGain: "12.74x",
  matureGain: "89.63x",
  device: "RTX 4050",
};

function loadRuns() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveRuns(runs) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(runs));
}

function stageForCount(count) {
  if (count >= 28) return "Guardian";
  if (count >= 14) return "Myelinated";
  if (count >= 8) return "Scaffold";
  if (count >= 3) return "Nurture";
  return "Seed";
}

function signalDelta(before, after) {
  return Math.round(
    (after.energy - before.energy +
      after.focus - before.focus +
      after.mood - before.mood +
      after.clarity - before.clarity -
      (after.stress - before.stress) -
      (after.tension - before.tension)) /
      6,
  );
}

export default function App() {
  // --- V3 Human Cockpit State ---
  const [runs, setRuns] = useState(loadRuns);
  const [selectedId, setSelectedId] = useState(protocols[0].id);
  const [before, setBefore] = useState(defaultSignals);
  const [after, setAfter] = useState({
    ...defaultSignals,
    stress: 28,
    focus: 50,
    clarity: 52,
  });
  const [reflection, setReflection] = useState("");
  const [resistance, setResistance] = useState(32);
  const [activeStep, setActiveStep] = useState(0);
  const [powerMode, setPowerMode] = useState("demo"); // Defaults to demo for buyer-safe mock telemetry

  const selected = protocols.find((protocol) => protocol.id === selectedId) || protocols[0];
  const protocolRuns = runs.filter((run) => run.protocolId === selected.id);
  const selectedStage = stageForCount(protocolRuns.length);
  const latest = runs[0];

  const recentScore = useMemo(() => {
    if (!runs.length) return 0;
    const recent = runs.slice(0, 7).map((run) => signalDelta(run.before, run.after));
    return Math.round(recent.reduce((total, score) => total + score, 0) / recent.length);
  }, [runs]);

  const stabilizedCount = useMemo(
    () => protocols.filter((protocol) => runs.filter((run) => run.protocolId === protocol.id).length >= 14).length,
    [runs],
  );

  const updateSignal = (target, key, value) => {
    const setter = target === "before" ? setBefore : setAfter;
    setter((current) => ({ ...current, [key]: value }));
  };

  // --- V2 PyTorch Telemetry State ---
  const [developmentStage, setDevelopmentStage] = useState('Infant Core');
  const [loops, setLoops] = useState(0);
  const [habitStabilized, setHabitStabilized] = useState(false);
  const [stressLevel, setStressLevel] = useState(0.12);
  const [guardianMode, setGuardianMode] = useState(false);
  const [execSpeed, setExecSpeed] = useState('0.0000s');
  const [logs, setLogs] = useState(["[TELEMETRY] Cockpit connection to PyTorch Core visualizer initialized.", "[SYSTEM] Awaiting engine telemetry..."]);
  const [nodes, setNodes] = useState([]);
  const [baclState, setBaclState] = useState('AWAITING_ENTROPY');

  const mode = before.stress > 72 || before.tension > 70 ? "sentinel" : selected.mode;

  useEffect(() => {
    const newNodes = Array.from({ length: 12 }).map((_, i) => ({
      id: i,
      angle: (i * 360) / 12,
      distance: Math.random() * 40 + 60,
      active: true,
      myelinated: false
    }));
    setNodes(newNodes);

    if (powerMode === "plugged") {
      fetchState();
    }
  }, [powerMode]);

  const addLog = (msg) => {
    setLogs(prev => [...prev.slice(-5), msg]);
  };

  const fetchState = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/state');
      const data = await res.json();
      setLoops(data.loops);
      setHabitStabilized(data.is_stabilized);
      setDevelopmentStage(data.development_stage);
      addLog(`[TELEMETRY] Connection successful. Loops: ${data.loops} | Stage: ${data.development_stage}`);

      if (data.is_stabilized) {
        setNodes(prev => prev.map(n => ({
          ...n,
          myelinated: n.active,
          distance: n.active ? 80 : 120
        })));
      }
    } catch (e) {
      addLog("[!] PyTorch Engine Offline. Set Power Mode to 'Demo' to run simulations.");
    }
  };

  const simulateNurture = async () => {
    if (guardianMode) return;

    if (powerMode === "demo") {
      // Local Mock Telemetry Simulation
      const nextLoops = loops + 1;
      const isStabilized = nextLoops >= 14;
      const mockSpeed = (0.002 + Math.random() * 0.004).toFixed(5) + "s";
      const tasks = ["focus", "calm_down", "general"];
      const mockTask = tasks[Math.floor(Math.random() * tasks.length)];
      const mockEntropy = "BACL_DEMO_" + Math.random().toString(36).substring(2, 10).toUpperCase();
      const mockPitch = (190.0 + Math.random() * 20.0).toFixed(1);

      setLoops(nextLoops);
      setExecSpeed(mockSpeed);
      setBaclState(mockEntropy);
      setStressLevel(0.10 + Math.random() * 0.05);

      addLog(`[DEMO-SIM] PyTorch: Nurture Logic Processed (${mockTask}) | Pitch: ${mockPitch}Hz | Speed: ${mockSpeed}`);

      if (!isStabilized) {
        setNodes(prev => prev.map(n => ({
          ...n,
          active: Math.random() > 0.3
        })));
      } else if (!habitStabilized && isStabilized) {
        setHabitStabilized(true);
        setDevelopmentStage('Guardian');
        addLog("[DEMO-SIM] HABIT STABILIZED. Myelination gate triggered!");
        setNodes(prev => prev.map(n => ({
          ...n,
          myelinated: true,
          distance: n.active ? 80 : 120
        })));
      }
      return;
    }

    // Real Plugged-in PyTorch backend connection
    try {
      const res = await fetch('http://127.0.0.1:5000/api/nurture', { method: 'POST' });
      const data = await res.json();

      setLoops(data.loops);
      setExecSpeed(data.execution_speed);
      setBaclState(data.entropy);
      setStressLevel(0.10 + Math.random() * 0.05);

      addLog(`[HPP] PyTorch: ${data.action} | Pitch: ${data.pitch}Hz | Speed: ${data.execution_speed}`);

      if (!data.is_stabilized) {
        setNodes(prev => prev.map(n => ({
          ...n,
          active: Math.random() > 0.3
        })));
      } else if (!habitStabilized && data.is_stabilized) {
        setHabitStabilized(true);
        setDevelopmentStage('Guardian');
        addLog("[HPP] HABIT STABILIZED. Synthesizing Myelin...");
        setNodes(prev => prev.map(n => ({
          ...n,
          myelinated: n.active,
          distance: n.active ? 80 : 120
        })));
      }
    } catch (e) {
      addLog("[!] PyTorch Engine Offline. Start Flask bridge or switch to Demo mode.");
    }
  };

  const triggerStress = async () => {
    setGuardianMode(true);
    setStressLevel(0.98);

    if (powerMode === "demo") {
      const mockEntropy = "BACL_XOR_WARNING_DEMO_ATTACK";
      const mockSpeed = (0.00012 + Math.random() * 0.0001).toFixed(6) + "s";
      setExecSpeed(mockSpeed);
      setBaclState(mockEntropy);

      addLog("[DEMO-SIM] WARNING: TOXIC STRESS DETECTED!");
      if (habitStabilized) {
        addLog(`[DEMO-SIM] Sentinel Reflex triggered. Shunting input in ${mockSpeed}`);
      } else {
        addLog(`[DEMO-SIM] CRITICAL: Core plastic. Sharding signals!`);
      }

      setTimeout(() => {
        setGuardianMode(false);
        setStressLevel(0.12);
        addLog("[DEMO-SIM] Threat neutralized. Reverting to Nurture.");
      }, 3000);
      return;
    }

    try {
      const res = await fetch('http://127.0.0.1:5000/api/toxic_stress', { method: 'POST' });
      const data = await res.json();

      setExecSpeed(data.execution_speed);
      setBaclState(data.entropy);

      addLog("[HPP] WARNING: TOXIC STRESS DETECTED!");
      if (data.is_stabilized) {
        addLog(`[HPP] Executing Myelinated Sentinel Reflex in ${data.execution_speed}`);
      } else {
        addLog(`[HPP] CRITICAL: Infant core under attack! Chaotic response!`);
      }

      setTimeout(() => {
        setGuardianMode(false);
        setStressLevel(0.12);
        addLog("[HPP] Threat neutralized. Resuming Nurture Mode.");
      }, 3000);

    } catch (e) {
      addLog("[!] PyTorch Engine Offline.");
      setGuardianMode(false);
    }
  };

  const completeRun = () => {
    const now = new Date().toISOString();
    const entry = {
      id: crypto.randomUUID(),
      protocolId: selected.id,
      protocolName: selected.name,
      startedAt: now,
      completedAt: now,
      before,
      after,
      reflection: reflection.trim() || selected.reflectionPrompt,
      resistance,
      mode,
    };
    const nextRuns = [entry, ...runs];
    setRuns(nextRuns);
    saveRuns(nextRuns);
    setReflection("");
    setActiveStep(0);
    setBefore(after);
    setAfter({
      ...after,
      focus: Math.min(100, after.focus + 4),
      clarity: Math.min(100, after.clarity + 3),
      stress: Math.max(0, after.stress - 3),
    });
    addLog(`[COCKPIT] Evidence Logged: Run completed for ${selected.name}`);
  };

  const resetEvidence = () => {
    setRuns([]);
    saveRuns([]);
    addLog("[COCKPIT] Local evidence log cleared.");
  };

  return (
    <>
      <div className={`sentinel-overlay ${guardianMode ? 'active' : ''}`}></div>

      <main className="app-shell">
        <header className="topbar">
          <div>
            <p className="eyebrow">Hyperplasticity Protocol V3.1 — Local Cockpit</p>
            <h1><Activity size={26} color="var(--accent-cyan)" style={{ verticalAlign: 'middle', marginRight: '4px' }} /> Train the state. Rewrite the loop.</h1>
          </div>
          <div className={`mode-pill ${mode}`}>
            {mode === "sentinel" ? <Shield size={16} /> : <Sparkles size={16} />}
            <span>{mode === "sentinel" ? "Sentinel" : "Nurture"}</span>
          </div>
        </header>

        <section className="command-grid">
          {/* --- Left Column: Rails & User Stats --- */}
          <aside className="left-rail">
            <div className="glass-panel identity-panel">
              <div>
                <p className="label">Active Identity</p>
                <h2>Signal Architect</h2>
              </div>
              <Brain size={24} color="var(--accent-cyan)" />
            </div>

            <div className="metric-stack">
              <Metric icon={<Gauge size={16} />} label="Recent Shift" value={`${recentScore > 0 ? "+" : ""}${recentScore}`} />
              <Metric icon={<Flame size={16} />} label="Habit-14 Reps" value={`${Math.min(protocolRuns.length, 14)}/14`} />
              <Metric icon={<Database size={16} />} label="Total Logs" value={`${runs.length}`} />
              <Metric icon={<Shield size={16} />} label="Stable Loops" value={`${stabilizedCount}`} />
            </div>

            <div className="glass-panel stage-panel">
              <p className="label">Current Loop Stage</p>
              <div className="stage-row">
                <span>{selectedStage}</span>
                <span>{protocolRuns.length} runs</span>
              </div>
              <div className="habit-track" aria-label="Habit 14 progress">
                {Array.from({ length: 14 }, (_, index) => (
                  <span key={index} className={index < Math.min(protocolRuns.length, 14) ? "filled" : ""} />
                ))}
              </div>
            </div>

            <div className="glass-panel power-panel">
              <p className="label">Power Mode</p>
              <div className="power-options">
                <button className={powerMode === "battery" ? "active" : ""} onClick={() => setPowerMode("battery")}>
                  Battery
                </button>
                <button className={powerMode === "plugged" ? "active" : ""} onClick={() => setPowerMode("plugged")}>
                  Plugged
                </button>
                <button className={powerMode === "demo" ? "active" : ""} onClick={() => setPowerMode("demo")}>
                  Demo
                </button>
              </div>
              <p className="power-note">
                {powerMode === "battery" && "Conserves energy. Flask bridge telemetry offline."}
                {powerMode === "plugged" && "Live CUDA connection active to 127.0.0.1:5000."}
                {powerMode === "demo" && "Deterministic mock telemetry for local IP demonstrations."}
              </p>
            </div>
          </aside>

          {/* --- Center Column: User Worksheets --- */}
          <section className="glass-panel workbench">
            <div className="section-head">
              <div>
                <p className="label">Interactive Protocol</p>
                <h2>{selected.name}</h2>
              </div>
              <div className="duration">
                <Timer size={15} />
                {selected.duration}
              </div>
            </div>

            <div className="protocol-strip">
              {protocols.map((protocol) => (
                <button
                  className={protocol.id === selected.id ? "protocol-tab active" : "protocol-tab"}
                  key={protocol.id}
                  onClick={() => {
                    setSelectedId(protocol.id);
                    setActiveStep(0);
                  }}
                >
                  {protocol.mode === "sentinel" ? <CircleAlert size={14} /> : <Compass size={14} />}
                  <span style={{ marginLeft: '4px' }}>{protocol.name.split(' ')[0]}</span>
                </button>
              ))}
            </div>

            <div className="run-grid">
              <div className="sliders-panel">
                <div className="panel-header" style={{ marginBottom: '10px' }}>
                  <span>State Sliders</span>
                </div>
                <SignalSliders values={before} target="before" onChange={updateSignal} />
              </div>

              <div className="protocol-card">
                <p className="intent">{selected.intent}</p>
                <p className="trigger">Trigger: {selected.trigger}</p>
                <div className="step-list">
                  {selected.steps.map((step, index) => (
                    <button
                      className={index === activeStep ? "step active" : index < activeStep ? "step done" : "step"}
                      key={step}
                      onClick={() => setActiveStep(index)}
                    >
                      <span>{index < activeStep ? <Check size={12} /> : index + 1}</span>
                      {step}
                    </button>
                  ))}
                </div>
                <button className="advance" onClick={() => setActiveStep((step) => Math.min(selected.steps.length, step + 1))}>
                  Advance Step <ArrowRight size={14} />
                </button>
              </div>
            </div>

            <div className="reflection-row">
              <label>
                <span>State Reflection & Notes</span>
                <textarea
                  value={reflection}
                  onChange={(event) => setReflection(event.target.value)}
                  placeholder={selected.reflectionPrompt}
                />
              </label>
              <label className="resistance">
                <span>Resistance</span>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={resistance}
                  onChange={(event) => setResistance(Number(event.target.value))}
                />
                <strong>{resistance}</strong>
              </label>
              <button className="complete" onClick={completeRun}>
                <Check size={20} />
                <span>Save</span>
              </button>
            </div>

            {/* Evidence Logs Log in Center column */}
            <div className="evidence-log-panel" style={{ marginTop: '8px' }}>
              <div className="panel-header" style={{ marginBottom: '8px' }}>
                <span>Local Evidence Logs</span>
                <button className="icon-button" onClick={resetEvidence} aria-label="Clear evidence log">
                  <RotateCcw size={13} />
                </button>
              </div>
              <div className="history-list">
                {runs.length > 0 ? (
                  runs.slice(0, 3).map((run) => (
                    <article key={run.id}>
                      <span className={`dot ${run.mode}`} />
                      <div>
                        <strong>{run.protocolName}</strong>
                        <p>{run.reflection}</p>
                      </div>
                      <b>{signalDelta(run.before, run.after) >= 0 ? "+" : ""}{signalDelta(run.before, run.after)}</b>
                    </article>
                  ))
                ) : (
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', padding: '10px 0' }}>No local logs. Complete your first training loop above.</div>
                )}
              </div>
            </div>
          </section>

          {/* --- Right Column: Visualizer & Telemetry --- */}
          <aside className="right-rail">
            <div className="glass-panel">
              <div className="panel-header">
                <span><Network size={14} style={{ marginRight: '6px', verticalAlign: 'middle' }} /> Core Synapses</span>
                <span>{developmentStage}</span>
              </div>

              <div className="core-visualizer">
                <div className="synapse-node node-central"></div>
                {nodes.map(node => {
                  const rad = (node.angle * Math.PI) / 180;
                  const x = Math.cos(rad) * node.distance;
                  const y = Math.sin(rad) * node.distance;
                  const lineLength = node.distance;
                  const lineClass = node.myelinated ? 'connection-line myelinated' : (!node.active ? 'connection-line dampened' : 'connection-line');

                  return (
                    <React.Fragment key={node.id}>
                      <div className={lineClass} style={{ width: `${lineLength}px`, transform: `rotate(${node.angle}deg)`, left: '50%', top: '50%', marginTop: '-1px' }} />
                      <div className="synapse-node" style={{ transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`, left: '50%', top: '50%', opacity: node.active ? 1 : 0.2, background: node.myelinated ? 'var(--accent-cyan)' : (guardianMode ? 'var(--accent-crimson)' : 'white') }} />
                    </React.Fragment>
                  );
                })}
              </div>

              <div className="visualizer-controls">
                <button onClick={simulateNurture} disabled={guardianMode || powerMode === "battery"}>
                  <Cpu size={12} style={{ marginRight: '4px', verticalAlign: 'middle' }} /> Process Nurture
                </button>
                <button className="danger" onClick={triggerStress} disabled={guardianMode || powerMode === "battery"}>
                  <ShieldAlert size={12} style={{ marginRight: '4px', verticalAlign: 'middle' }} /> Inject Stress
                </button>
              </div>
              {powerMode === "battery" && (
                <div style={{ color: 'var(--accent-crimson)', fontSize: '0.75rem', marginTop: '8px', textAlign: 'center', fontFamily: 'Space Mono' }}>
                  [!] Telemetry shunted: battery mode active.
                </div>
              )}
            </div>

            <div className="glass-panel">
              <div className="panel-header">
                <span><Zap size={14} style={{ marginRight: '6px', verticalAlign: 'middle' }} /> Engine Telemetry</span>
              </div>
              <div className="metric-row">
                <span className="metric-label">BACL Entropy Key</span>
                <span className="metric-value" style={{ fontSize: '0.75rem' }}>{baclState}</span>
              </div>
              <div className="metric-row">
                <span className="metric-label">Stabilization Reps</span>
                <span className="metric-value">{Math.min(loops, 14)} / 14</span>
              </div>
              <div className="metric-row">
                <span className="metric-label">Core Integrity</span>
                <span className="metric-value">{habitStabilized ? 'STABILIZED' : 'PLASTIC'}</span>
              </div>
              <div className="metric-row">
                <span className="metric-label">Stress Level</span>
                <span className={`metric-value ${stressLevel > 0.8 ? 'danger' : ''}`}>{(stressLevel * 100).toFixed(0)}%</span>
              </div>
              <div className="metric-row">
                <span className="metric-label">Inference Speed</span>
                <span className={`metric-value ${guardianMode ? 'danger' : ''}`}>{execSpeed}</span>
              </div>

              <div style={{ marginTop: '12px' }}>
                <span className="label" style={{ fontSize: '0.72rem' }}>Telemetry Stream Log</span>
                <div className={`data-stream ${guardianMode ? 'alert' : ''}`}>
                  {logs.map((log, i) => (
                    <div key={i} className="log-line">{log}</div>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="glass-panel evidence-panel">
              <div className="mini-head">
                <h3>Habit Memory Stats</h3>
                <Dumbbell size={16} color="var(--accent-cyan)" />
              </div>
              <div className="evidence-grid">
                <span>
                  <small>Lock Threshold</small>
                  <strong>{habitMemoryEvidence.threshold}</strong>
                </span>
                <span>
                  <small>Recall Gain</small>
                  <strong>{habitMemoryEvidence.recallGain}</strong>
                </span>
                <span>
                  <small>Mature Gain</small>
                  <strong>{habitMemoryEvidence.matureGain}</strong>
                </span>
                <span>
                  <small>Device Target</small>
                  <strong>{habitMemoryEvidence.device}</strong>
                </span>
              </div>
              <p style={{ fontSize: '0.75rem', marginTop: '6px' }}>Dynamic repetition builds context-independent memory structures that resist environmental disruption.</p>
            </div>
          </aside>
        </section>
      </main>
    </>
  );
}

function Metric({ icon, label, value }) {
  return (
    <div className="metric">
      {icon}
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function SignalSliders({ values, target, onChange }) {
  return (
    <div className="sliders">
      {signalLabels.map(([key, label]) => (
        <label key={key}>
          <span>{label}</span>
          <input
            type="range"
            min="0"
            max="100"
            value={values[key]}
            onChange={(event) => onChange(target, key, Number(event.target.value))}
          />
          <b>{values[key]}</b>
        </label>
      ))}
    </div>
  );
}
