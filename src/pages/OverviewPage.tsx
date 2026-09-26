import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Shield,
  Crosshair,
  Activity,
  Play,
  FileText,
  Zap,
  BarChart2,
  Compass,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Layers,
  Cpu,
  ArrowRight,
} from 'lucide-react'
import { useWargameStore, ScenarioPreset } from '../store/wargameStore'

const API_BASE = 'http://localhost:8000'

export default function OverviewPage() {
  const navigate = useNavigate()
  const { activeSessionId, currentTurnResult, turnHistory, presets, setPresets, setSelectedPreset } = useWargameStore()
  const [loadingPresets, setLoadingPresets] = useState(false)

  useEffect(() => {
    if (presets.length === 0) {
      setLoadingPresets(true)
      fetch(`${API_BASE}/wargame/presets`)
        .then((res) => res.json())
        .then((data) => {
          setPresets(data)
          setLoadingPresets(false)
        })
        .catch((err) => {
          console.error('Failed to fetch presets:', err)
          setLoadingPresets(false)
        })
    }
  }, [presets, setPresets])

  const currentTurn = currentTurnResult ? currentTurnResult.turn_number : turnHistory.length
  const blueLoss = currentTurnResult?.metrics.blue_losses_percentage ?? 0
  const redLoss = currentTurnResult?.metrics.red_losses_percentage ?? 0
  const blueStrength = Math.max(0, 100 - blueLoss)
  const redStrength = Math.max(0, 100 - redLoss)

  const handleLaunchPreset = (preset: ScenarioPreset) => {
    setSelectedPreset(preset)
    navigate('/wargaming')
  }

  return (
    <div className="max-w-[1500px] mx-auto px-6 py-6 space-y-8">
      {/* Strategic Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-slate-800/80 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono tracking-widest text-[#42C7FF] uppercase">
            <Activity className="w-4 h-4" />
            <span>STRATEGIC COMMAND DASHBOARD</span>
          </div>
          <h1 className="text-3xl font-display font-bold text-white tracking-wide mt-1">
            NIRNAY // OPERATIONAL OVERVIEW
          </h1>
          <p className="text-sm text-slate-400 mt-1 max-w-2xl">
            Real-time multi-agent campaign state, deterministic battle simulation adjudication, dynamic threat evaluations, and strategic intelligence synthesis.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/wargaming')}
            className="px-5 py-2.5 rounded bg-[#42C7FF] text-space-navy font-display font-bold text-xs tracking-wider uppercase hover:bg-[#63E6FF] transition-all flex items-center gap-2 shadow-[0_0_20px_rgba(66,199,255,0.4)]"
          >
            <Play className="w-4 h-4 fill-current" />
            <span>GO TO WARGAMING CONSOLE</span>
          </button>
        </div>
      </div>

      {/* Active Campaign Status Cards / Launch Prompt */}
      {activeSessionId ? (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {/* Active Campaign Card */}
          <div className="bg-[rgba(4,15,26,0.8)] border border-[rgba(100,190,255,0.2)] rounded-xl p-5 backdrop-blur-md relative overflow-hidden">
            <div className="absolute top-0 right-0 w-24 h-24 bg-[#42C7FF]/5 rounded-bl-full pointer-events-none" />
            <div className="text-xs font-mono text-slate-400 uppercase tracking-widest">CAMPAIGN IDENTIFIER</div>
            <div className="text-xl font-mono font-bold text-white mt-1">{activeSessionId}</div>
            <div className="mt-4 flex items-center justify-between font-mono text-xs">
              <span className="text-slate-400">TURN PROGRESS</span>
              <span className="text-[#42C7FF] font-bold">TURN {currentTurn} / 5</span>
            </div>
            <div className="w-full h-1.5 bg-slate-800 rounded-full mt-2 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-[#42C7FF] to-cyan-400 rounded-full"
                style={{ width: `${(currentTurn / 5) * 100}%` }}
              />
            </div>
          </div>

          {/* Blue Force Status */}
          <div className="bg-[rgba(4,15,26,0.8)] border border-blue-500/30 rounded-xl p-5 backdrop-blur-md">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono text-blue-400 uppercase tracking-widest flex items-center gap-1.5">
                <Shield className="w-4 h-4" /> BLUE FORCE INTEGRITY
              </span>
              <span className="font-mono text-xs font-bold text-blue-400">{blueStrength.toFixed(1)}%</span>
            </div>
            <div className="text-2xl font-mono font-bold text-white mt-2">{blueStrength.toFixed(1)}%</div>
            <div className="text-xs font-mono text-slate-400 mt-1">Loss Attrition: {blueLoss.toFixed(1)}%</div>
            <div className="w-full h-1.5 bg-slate-800 rounded-full mt-3 overflow-hidden">
              <div className="h-full bg-blue-500 rounded-full" style={{ width: `${blueStrength}%` }} />
            </div>
          </div>

          {/* Red Force Status */}
          <div className="bg-[rgba(4,15,26,0.8)] border border-red-500/30 rounded-xl p-5 backdrop-blur-md">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono text-red-400 uppercase tracking-widest flex items-center gap-1.5">
                <Crosshair className="w-4 h-4" /> RED FORCE INTEGRITY
              </span>
              <span className="font-mono text-xs font-bold text-red-400">{redStrength.toFixed(1)}%</span>
            </div>
            <div className="text-2xl font-mono font-bold text-white mt-2">{redStrength.toFixed(1)}%</div>
            <div className="text-xs font-mono text-slate-400 mt-1">Loss Attrition: {redLoss.toFixed(1)}%</div>
            <div className="w-full h-1.5 bg-slate-800 rounded-full mt-3 overflow-hidden">
              <div className="h-full bg-red-500 rounded-full" style={{ width: `${redStrength}%` }} />
            </div>
          </div>

          {/* Objectives Status */}
          <div className="bg-[rgba(4,15,26,0.8)] border border-[rgba(100,190,255,0.2)] rounded-xl p-5 backdrop-blur-md">
            <div className="text-xs font-mono text-slate-400 uppercase tracking-widest flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" /> ACTIVE OBJECTIVES
            </div>
            <div className="text-2xl font-mono font-bold text-white mt-2">
              {currentTurnResult?.metrics.objectives?.length || 3} STRATEGIC POINTS
            </div>
            <div className="text-xs font-mono text-emerald-400 mt-1">
              Condition: {currentTurnResult?.metrics.termination_condition || 'IN_PROGRESS'}
            </div>
            <div className="mt-3 text-xs text-slate-400 line-clamp-1">
              {currentTurnResult?.decisions?.blue_coa_name || 'Defend key operational corridors'}
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-[rgba(4,15,26,0.8)] border border-amber-500/30 rounded-xl p-6 backdrop-blur-md flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-amber-400 text-xs font-mono font-bold uppercase">
              <AlertTriangle className="w-4 h-4" /> NO ACTIVE CAMPAIGN IN MEMORY
            </div>
            <h3 className="text-lg font-display font-bold text-white">Initialize a Strategic Wargame Scenario</h3>
            <p className="text-xs text-slate-400">
              Select one of the pre-configured operational threat scenarios below or head to the Wargaming Console to customize your initial parameters.
            </p>
          </div>
          <button
            onClick={() => navigate('/scenarios')}
            className="px-5 py-2.5 rounded bg-amber-500/20 border border-amber-500/40 text-amber-300 font-mono text-xs font-bold hover:bg-amber-500/30 transition-all flex items-center gap-2 shrink-0"
          >
            <Compass className="w-4 h-4" />
            <span>BROWSE SCENARIO LIBRARY</span>
          </button>
        </div>
      )}

      {/* Main Grid: Latest Intelligence & Quick Scenario Presets */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Latest Turn Evaluation & Activity */}
        <div className="lg:col-span-2 space-y-6">
          {/* Latest Strategic Evaluation */}
          <div className="bg-[rgba(4,15,26,0.8)] border border-[rgba(100,190,255,0.2)] rounded-xl p-6 backdrop-blur-md space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2 font-mono text-xs text-[#42C7FF] uppercase font-bold">
                <FileText className="w-4 h-4" />
                <span>LATEST STRATEGIC ADJUDICATION (TURN {currentTurnResult?.scenario_id || currentTurn})</span>
              </div>
              <button
                onClick={() => navigate('/reports')}
                className="text-xs font-mono text-slate-400 hover:text-white flex items-center gap-1"
              >
                <span>Full Reports</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>

            {currentTurnResult ? (
              <div className="space-y-4 text-sm">
                <div>
                  <h4 className="text-xs font-mono text-slate-400 uppercase">Strategic Conclusion</h4>
                  <p className="text-slate-200 mt-1 leading-relaxed bg-[#02070D]/60 border border-slate-800 p-3.5 rounded text-xs font-mono">
                    {currentTurnResult.evaluation.strategic_conclusion}
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                  <div className="bg-red-950/20 border border-red-500/20 p-3 rounded">
                    <span className="text-red-400 font-bold uppercase block mb-1">Identified Operational Risks</span>
                    <ul className="list-disc list-inside space-y-1 text-slate-300">
                      {currentTurnResult.evaluation.risks.slice(0, 3).map((r, i) => (
                        <li key={i}>{r}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="bg-cyan-950/20 border border-cyan-500/20 p-3 rounded">
                    <span className="text-cyan-400 font-bold uppercase block mb-1">Strategic Trade-offs</span>
                    <ul className="list-disc list-inside space-y-1 text-slate-300">
                      {currentTurnResult.evaluation.tradeoffs.slice(0, 3).map((t, i) => (
                        <li key={i}>{t}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-12 text-center text-slate-500 font-mono text-xs space-y-2">
                <Clock className="w-8 h-8 mx-auto text-slate-600 animate-pulse" />
                <p>No turn evaluation recorded yet. Execute Turn 1 from the Wargaming interface.</p>
              </div>
            )}
          </div>

          {/* Cross-Page Shortcut Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div
              onClick={() => navigate('/simulation')}
              className="bg-[rgba(4,15,26,0.8)] border border-[rgba(100,190,255,0.15)] hover:border-[#42C7FF] rounded-xl p-4 transition-all cursor-pointer group"
            >
              <Zap className="w-5 h-5 text-amber-400 group-hover:scale-110 transition-transform" />
              <h3 className="font-display font-bold text-white text-sm mt-3">Simulation Adjudication</h3>
              <p className="text-xs text-slate-400 mt-1">Inspect Lanchester combat math, action validity, and turn results.</p>
            </div>

            <div
              onClick={() => navigate('/analytics')}
              className="bg-[rgba(4,15,26,0.8)] border border-[rgba(100,190,255,0.15)] hover:border-[#42C7FF] rounded-xl p-4 transition-all cursor-pointer group"
            >
              <BarChart2 className="w-5 h-5 text-cyan-400 group-hover:scale-110 transition-transform" />
              <h3 className="font-display font-bold text-white text-sm mt-3">Campaign Analytics</h3>
              <p className="text-xs text-slate-400 mt-1">Analyze attrition trajectories, objective trends, and agent metrics.</p>
            </div>

            <div
              onClick={() => navigate('/reports')}
              className="bg-[rgba(4,15,26,0.8)] border border-[rgba(100,190,255,0.15)] hover:border-[#42C7FF] rounded-xl p-4 transition-all cursor-pointer group"
            >
              <FileText className="w-5 h-5 text-emerald-400 group-hover:scale-110 transition-transform" />
              <h3 className="font-display font-bold text-white text-sm mt-3">Strategic Reports</h3>
              <p className="text-xs text-slate-400 mt-1">Review comprehensive LLM decision dossiers and memory archives.</p>
            </div>
          </div>
        </div>

        {/* Right Col: Operational Presets Quick Launch */}
        <div className="space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="font-mono text-xs text-[#42C7FF] font-bold uppercase flex items-center gap-1.5">
              <Compass className="w-4 h-4" /> OPERATIONAL PRESETS
            </span>
            <button
              onClick={() => navigate('/scenarios')}
              className="text-xs font-mono text-slate-400 hover:text-white"
            >
              View All ({presets.length})
            </button>
          </div>

          <div className="space-y-4">
            {presets.map((preset) => (
              <div
                key={preset.preset_id}
                className="bg-[rgba(4,15,26,0.8)] border border-[rgba(100,190,255,0.15)] hover:border-[#42C7FF]/50 rounded-xl p-4 transition-all space-y-3"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-[10px] font-mono text-[#42C7FF] uppercase tracking-wider">{preset.theater}</span>
                    <h3 className="font-display font-bold text-white text-sm">{preset.name}</h3>
                  </div>
                  <span className="px-2 py-0.5 text-[9px] font-mono bg-slate-800 text-slate-300 rounded border border-slate-700">
                    {preset.preset_id}
                  </span>
                </div>

                <p className="text-xs text-slate-400 line-clamp-2">{preset.description}</p>

                <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 font-mono text-[11px]">
                  <span className="text-slate-400">Weather: {preset.initial_weather}</span>
                  <button
                    onClick={() => handleLaunchPreset(preset)}
                    className="px-3 py-1 rounded bg-[#42C7FF]/15 text-[#42C7FF] hover:bg-[#42C7FF] hover:text-space-navy font-bold transition-all flex items-center gap-1"
                  >
                    <span>LAUNCH</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
