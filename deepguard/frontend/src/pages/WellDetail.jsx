import { useMemo } from 'react'
import { useParams } from 'react-router-dom'
import { ProgressBar } from '../components/widgets'
import WellSchematic from '../components/WellSchematic'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

const mockData = {
  name: 'DG-07',
  field: 'Vega',
  status: 'AMBER',
  annuli: [
    { name: 'A', pressure: 190, maasp: 220, measurements: [180, 185, 190] },
    { name: 'B', pressure: 90, maasp: 200, measurements: [80, 85, 90] },
  ],
  schematic: {
    casing_strings: [
      { name: 'Conductor', top: 0, bottom: 100 },
      { name: 'Surface', top: 0, bottom: 500 },
      { name: 'Intermediate', top: 0, bottom: 1200 },
      { name: 'Production', top: 0, bottom: 2500 },
    ],
    tubing: [{ name: 'Production Tubing', top: 0, bottom: 2400 }],
    barrier_elements: [
      { name: 'SSSV', type: 'SSSV', depth: 120, status: 'OK' },
      { name: 'Packer', type: 'Packer', depth: 1100, status: 'OK' },
      { name: 'Production Casing', type: 'Casing', depth: 2500, status: 'OK' },
    ],
  },
  barriers: [
    { id: 1, type: 'SSSV', name: 'Hydraulic', depth: 120, last: '2024-02-11', status: 'OK' },
    { id: 2, type: 'Packer', name: 'Permanent', depth: 1100, last: '2024-03-18', status: 'OK' },
    { id: 3, type: 'Cement', name: 'Tail slurry', depth: 2500, last: '2023-12-01', status: 'MONITOR' },
  ],
  tasks: [
    { id: 1, title: 'Integrity review at 90% MAASP', due: 'in 7 days', priority: 'HIGH' },
    { id: 2, title: 'Review SAP trend B-annulus', due: 'tomorrow', priority: 'MEDIUM' }
  ]
}

export default function WellDetail() {
  const { id } = useParams()
  const data = useMemo(() => mockData, [id])
  return (
    <div className="space-y-8">
      <header className="flex items-center justify-between">
        <div>
          <p className="text-white/50">Field {data.field}</p>
          <h2 className="text-3xl font-semibold flex items-center gap-3">{data.name} <span className="px-3 py-1 rounded-full bg-amber/20 text-amber border border-amber/30 text-sm">{data.status}</span></h2>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 rounded-lg bg-white/10 border border-white/10">Export</button>
          <button className="px-4 py-2 rounded-lg bg-gradient-to-r from-teal to-amber text-midnight font-semibold shadow-soft">Add measurement</button>
        </div>
      </header>

      <div className="grid md:grid-cols-3 gap-6">
        {data.annuli.map(ann => (
          <div key={ann.name} className="glass rounded-2xl p-5 border border-white/5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/60 text-sm">{ann.name}-Annulus</p>
                <h4 className="text-2xl font-semibold">{ann.pressure} bar</h4>
              </div>
              <span className="text-xs px-3 py-1 rounded-full bg-amber/20 text-amber border border-amber/30">Util {Math.round((ann.pressure/ann.maasp)*100)}%</span>
            </div>
            <div className="mt-4">
              <ProgressBar value={(ann.pressure/ann.maasp)*100} />
            </div>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-6 items-start">
        <div className="glass rounded-2xl p-5 border border-white/5">
          <h3 className="text-lg font-semibold mb-4">Well schematic</h3>
          <WellSchematic data={data.schematic} />
        </div>
        <div className="glass rounded-2xl p-5 border border-white/5 w-full">
          <h3 className="text-lg font-semibold mb-4">Annulus pressure trend</h3>
          <div className="h-[400px]">
            <ResponsiveContainer>
              <LineChart data={buildChartData(data.annuli)}>
                <XAxis dataKey="index" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip />
                {data.annuli.map((ann, idx) => (
                  <Line key={ann.name} dataKey={ann.name} stroke={["#1CD9A1", "#FFB020", "#FF5A63"][idx]} dot={false} strokeWidth={3} />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="glass rounded-2xl p-5 border border-white/5">
          <h3 className="text-lg font-semibold mb-4">Barrier elements</h3>
          <table className="w-full text-sm">
            <thead className="text-white/60">
              <tr>
                <th className="text-left pb-2">Type</th>
                <th className="text-left pb-2">Name</th>
                <th className="text-left pb-2">Depth</th>
                <th className="text-left pb-2">Last test</th>
                <th className="text-left pb-2">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {data.barriers.map(b => (
                <tr key={b.id} className="hover:bg-white/5">
                  <td className="py-2">{b.type}</td>
                  <td>{b.name}</td>
                  <td>{b.depth} m</td>
                  <td>{b.last}</td>
                  <td><span className="px-2 py-1 rounded-full bg-teal/20 text-teal text-xs">{b.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="glass rounded-2xl p-5 border border-white/5">
          <h3 className="text-lg font-semibold mb-4">Tasks & reminders</h3>
          <div className="space-y-3">
            {data.tasks.map(t => (
              <div key={t.id} className="p-3 rounded-xl bg-white/5 border border-white/5 flex items-center justify-between">
                <div>
                  <p className="font-medium">{t.title}</p>
                  <p className="text-xs text-white/60">{t.due}</p>
                </div>
                <span className="text-xs px-3 py-1 rounded-full bg-amber/20 text-amber border border-amber/30">{t.priority}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

function buildChartData(annuli){
  const maxPoints = Math.max(...annuli.map(a => a.measurements.length))
  return Array.from({ length: maxPoints }).map((_, idx) => {
    const row = { index: idx }
    annuli.forEach(ann => row[ann.name] = ann.measurements[idx] || null)
    return row
  })
}
