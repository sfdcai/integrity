import { useEffect, useState } from 'react'
import { fetchSchematic } from '../services/api'
import TrafficLight from '../components/TrafficLight'
import AnnulusCard from '../components/AnnulusCard'
import TaskList from '../components/TaskList'
import WellSchematic from '../d3/WellSchematic'
import { ArrowLeft } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export default function WellDetail({ wellId, onBack }) {
  const [schematic, setSchematic] = useState(null)

  useEffect(() => {
    fetchSchematic(wellId).then(setSchematic)
  }, [wellId])

  if (!schematic) return <div className="p-8">Loading...</div>
  const measurements = schematic.annuli_pressures.map(m => ({...m, recorded_at: new Date(m.recorded_at).toLocaleString()}))

  return (
    <div className="p-8 space-y-6">
      <button onClick={onBack} className="text-neon flex items-center gap-2"><ArrowLeft size={16}/>Back</button>
      <div className="glass-card p-6 flex justify-between items-center">
        <div>
          <p className="text-slate-400 text-sm">{schematic.well.field}</p>
          <h1 className="text-3xl font-bold">{schematic.well.name}</h1>
          <p className="text-slate-300">{schematic.recommendation}</p>
        </div>
        <TrafficLight status={schematic.status} />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 glass-card p-4">
          <h3 className="font-semibold mb-3">Annulus Pressures</h3>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={measurements}>
              <Line type="monotone" dataKey="pressure_bar" stroke="#7af0ff" strokeWidth={3} dot={false} />
              <XAxis dataKey="recorded_at" tick={{fill:'#cbd5e1'}} interval={0} angle={-30} height={60}/>
              <YAxis tick={{fill:'#cbd5e1'}} />
              <Tooltip contentStyle={{background:'#0b1021', border:'1px solid #1e293b', color:'#e2e8f0'}} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <TaskList tasks={schematic.well.tasks || []} />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <AnnulusCard name="A" pressure={schematic.annuli_pressures[0]?.pressure_bar || 0} maasp={schematic.maasp} status={schematic.status} />
      </div>
      <div className="glass-card p-4">
        <h3 className="font-semibold mb-4">Well Schematic</h3>
        <WellSchematic schematic={schematic} />
      </div>
      <div className="glass-card p-4">
        <h3 className="font-semibold mb-2">Barrier Elements</h3>
        <table className="w-full text-left text-sm">
          <thead className="text-slate-400">
            <tr>
              <th className="py-2">Type</th>
              <th>Name</th>
              <th>Depth</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {schematic.well.barrier_elements.map(b => (
              <tr key={b.id} className="border-t border-white/5">
                <td className="py-2">{b.barrier_type}</td>
                <td>{b.name}</td>
                <td>{b.depth || '—'}</td>
                <td>{b.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
