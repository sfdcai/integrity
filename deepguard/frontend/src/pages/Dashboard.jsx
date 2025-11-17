import { useMemo } from 'react'
import { Activity, AlertTriangle, CheckCircle, Flame } from 'lucide-react'
import TrafficLight from '../components/TrafficLight'

export default function Dashboard({ wells, onSelectWell }) {
  const counts = useMemo(() => {
    const base = { GREEN:0, AMBER:0, 'HIGH-AMBER':0, RED:0 }
    wells.forEach(w => base[w.status] = (base[w.status] || 0)+1)
    return base
  }, [wells])

  return (
    <div className="p-8 space-y-8">
      <header className="flex justify-between items-center">
        <div>
          <p className="text-slate-400">DeepGuard Dashboard</p>
          <h1 className="text-3xl font-bold">Well Integrity Overview</h1>
        </div>
        <div className="flex gap-3">
          {Object.entries(counts).map(([k,v]) => (
            <div key={k} className="glass-card px-4 py-3 text-center">
              <p className="text-xs text-slate-400">{k}</p>
              <p className="text-2xl font-semibold">{v}</p>
            </div>
          ))}
        </div>
      </header>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {wells.map(well => (
          <div key={well.id} className="glass-card p-5 hover:border-neon/40 cursor-pointer transition" onClick={()=>onSelectWell(well.id)}>
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm text-slate-400">{well.field}</p>
                <h3 className="text-xl font-semibold">{well.name}</h3>
              </div>
              <TrafficLight status={well.status} />
            </div>
            <p className="text-sm text-slate-300 mt-2">Type: {well.well_type || 'N/A'}</p>
            <div className="mt-4 flex gap-3">
              <div className="flex items-center gap-2 text-sm text-amber-300"><AlertTriangle size={16}/> Tasks {well.tasks?.length || 0}</div>
              <div className="flex items-center gap-2 text-sm text-neon"><Activity size={16}/> Annuli {well.annuli?.length || 0}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
