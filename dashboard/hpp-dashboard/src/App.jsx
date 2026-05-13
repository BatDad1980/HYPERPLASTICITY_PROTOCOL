import React, { useState, useEffect } from 'react';
import { Activity, ShieldAlert, Cpu, Network, Zap } from 'lucide-react';
import './index.css';

export default function App() {
  const [developmentStage, setDevelopmentStage] = useState('Infant Core');
  const [loops, setLoops] = useState(0);
  const [habitStabilized, setHabitStabilized] = useState(false);
  const [stressLevel, setStressLevel] = useState(0.12);
  const [guardianMode, setGuardianMode] = useState(false);
  const [execSpeed, setExecSpeed] = useState('0.0000s');
  const [logs, setLogs] = useState(["[TELEMETRY] Live connection to PyTorch Engine established.", "[SYSTEM] Microglial dampening active."]);
  const [nodes, setNodes] = useState([]);
  const [baclState, setBaclState] = useState('AWAITING_ENTROPY');

  useEffect(() => {
    const newNodes = Array.from({ length: 12 }).map((_, i) => ({
      id: i,
      angle: (i * 360) / 12,
      distance: Math.random() * 40 + 60,
      active: true,
      myelinated: false
    }));
    setNodes(newNodes);
    
    // Initial fetch to get state
    fetchState();
  }, []);

  const addLog = (msg) => {
    setLogs(prev => [...prev.slice(-6), msg]);
  };

  const fetchState = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/state');
      const data = await res.json();
      setLoops(data.loops);
      setHabitStabilized(data.is_stabilized);
      setDevelopmentStage(data.development_stage);
      
      if (data.is_stabilized) {
        setNodes(prev => prev.map(n => ({
          ...n,
          myelinated: n.active,
          distance: n.active ? 80 : 120
        })));
      }
    } catch (e) {
      console.error("Engine offline.");
    }
  };

  const simulateNurture = async () => {
    if (guardianMode) return;
    
    try {
      const res = await fetch('http://127.0.0.1:5000/api/nurture', { method: 'POST' });
      const data = await res.json();
      
      setLoops(data.loops);
      setExecSpeed(data.execution_speed);
      setBaclState(data.entropy);
      setStressLevel(0.10 + Math.random() * 0.05);
      
      addLog(`[HPP] PyTorch: ${data.action} | Pitch: ${data.pitch}Hz`);
      
      // Update nodes (microglia dampening simulation)
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
      addLog("[!] PyTorch Engine Offline. Start telemetry server.");
    }
  };

  const triggerStress = async () => {
    setGuardianMode(true);
    setStressLevel(0.98);
    
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

  return (
    <>
      <div className={`sentinel-overlay ${guardianMode ? 'active' : ''}`}></div>
      
      <div className="dashboard-container">
        <header>
          <h1><Activity size={32} color="var(--accent-cyan)" /> HPP CORE VISUALIZER</h1>
          <div className={`status-badge ${guardianMode ? 'guardian' : ''}`}>
            {guardianMode ? 'SENTINEL REFLEX ACTIVE' : 'NURTURE MODE'}
          </div>
        </header>

        <div className="grid-layout">
          <div className="glass-panel">
            <div className="panel-header">
              <span><Network size={16} style={{marginRight: '8px', verticalAlign: 'middle'}}/> Synesthetic Core</span>
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

            <div className="controls">
              <button onClick={simulateNurture} disabled={guardianMode}>
                <Cpu size={14} style={{marginRight: '6px'}} /> Process Nurture Logic (PyTorch)
              </button>
              <button className="danger" onClick={triggerStress} disabled={guardianMode}>
                <ShieldAlert size={14} style={{marginRight: '6px'}} /> Inject Toxic Stress
              </button>
            </div>
          </div>

          <div className="glass-panel">
            <div className="panel-header">
              <span><Zap size={16} style={{marginRight: '8px', verticalAlign: 'middle'}}/> System Metabolism</span>
            </div>
            <div className="metric-row">
              <span className="metric-label">BACL Entropy Key</span>
              <span className="metric-value" style={{fontSize: '0.8rem'}}>{baclState}</span>
            </div>
            <div className="metric-row">
              <span className="metric-label">Habit-14 Progress</span>
              <span className="metric-value">{Math.min(loops, 14)} / 14</span>
            </div>
            <div className="metric-row">
              <span className="metric-label">Core Integrity</span>
              <span className="metric-value">{habitStabilized ? 'STABILIZED' : 'PLASTIC'}</span>
            </div>
            <div className="metric-row">
              <span className="metric-label">Environmental Stress</span>
              <span className={`metric-value ${stressLevel > 0.8 ? 'danger' : ''}`}>{(stressLevel * 100).toFixed(1)}%</span>
            </div>
            <div className="metric-row">
              <span className="metric-label">Live Inference Speed</span>
              <span className={`metric-value ${guardianMode ? 'danger' : ''}`}>{execSpeed}</span>
            </div>

            <div style={{marginTop: '1.5rem'}}>
              <div className="panel-header" style={{marginBottom: '0.5rem'}}>Core Telemetry Feed</div>
              <div className={`data-stream ${guardianMode ? 'alert' : ''}`}>
                {logs.map((log, i) => (
                  <div key={i} className="log-line">{log}</div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
