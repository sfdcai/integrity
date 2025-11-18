import { Activity, AlertTriangle, CheckCircle, Flame, ShieldCheck } from 'lucide-react'
import { Link } from 'react-router-dom'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'

const COLORS = ['#1CD9A1', '#FFB020', '#FF7043', '#FF5A63']

const wells = [
  { id: 1, name: 'DG-12', status: 'GREEN', field: 'Vega', utilisation: 62 },
  { id: 2, name: 'DG-07', status: 'AMBER', field: 'Vega', utilisation: 83 },
  { id: 3, name: 'DG-04', status: 'RED', field: 'Luna', utilisation: 109 }
]

const tasks = [
  { id: 1, title: 'Integrity review DG-07', due: '7d', priority: 'HIGH' },
  { id: 2, title: 'Bleed-down plan DG-04', due: 'today', priority: 'CRITICAL' }
]

export default function Dashboard() {
  const statusCounts = ['GREEN','AMBER','HIGH AMBER','RED'].map(status => ({
    status,
    value: wells.filter(w => w.status === status).length
  }))
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-white/50">Portfolio overview</p>
          <h2 className="text-3xl font-semibold">Well Integrity Dashboard</h2>
        </div>
        <button className="px-4 py-2 rounded-lg bg-gradient-to-r from-teal to-amber text-midnight font-semibold shadow-soft">Add well</button>
      </div>

      <div className="grid md:grid-cols-4 gap-4">
        <SummaryCard icon={<CheckCircle />} title="Healthy" value="12" tone="teal" />
        <SummaryCard icon={<AlertTriangle />} title="Watch" value="3" tone="amber" />
        <SummaryCard icon={<Flame />} title="Critical" value="1" tone="redish" />
        <SummaryCard icon={<Activity />} title="Tasks" value="8 open" tone="teal" />
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="glass rounded-2xl p-6 col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Fleet status</h3>
          </div>
          <div className="grid md:grid-cols-3 gap-4">
            {wells.map(well => (
              <Link key={well.id} to={`/wells/${well.id}`} className="glass rounded-xl p-4 border border-white/5 hover:border-teal transition">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-white/60">{well.field}</p>
                    <h4 className="text-xl font-semibold">{well.name}</h4>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs ${badgeTone(well.status)}`}>{well.status}</span>
                </div>
                <div className="mt-3 text-sm text-white/70">Utilisation {well.utilisation}%</div>
              </Link>
            ))}
          </div>
        </div>
        <div className="glass rounded-2xl p-6">
          <h3 className="text-lg font-semibold mb-4">Status distribution</h3>
          <div className="h-56">
            <ResponsiveContainer>
              <PieChart>
                <Pie data={statusCounts} innerRadius={50} outerRadius={80} dataKey="value">
                  {statusCounts.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="glass rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Overdue tasks</h3>
          <button className="text-sm text-teal">View all</button>
        </div>
        <div className="space-y-3">
          {tasks.map(task => (
            <div key={task.id} className="flex items-center justify-between p-3 rounded-lg bg-white/5 border border-white/5">
              <div>
                <p className="font-medium">{task.title}</p>
                <p className="text-xs text-white/60">Due {task.due}</p>
              </div>
              <span className="text-xs px-3 py-1 rounded-full bg-redish/20 text-redish border border-redish/30">{task.priority}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function SummaryCard({ icon, title, value, tone }) {
  return (
    <div className="glass rounded-xl p-4 border border-white/5">
      <div className="flex items-center gap-3">
        <div className={`p-2 rounded-lg bg-${tone}/20 text-${tone}`}>
          {icon}
        </div>
        <div>
          <p className="text-sm text-white/60">{title}</p>
          <p className="text-2xl font-semibold">{value}</p>
        </div>
      </div>
    </div>
  )
}

function badgeTone(status){
  switch(status){
    case 'GREEN': return 'bg-teal/20 text-teal border border-teal/30'
    case 'AMBER': return 'bg-amber/20 text-amber border border-amber/30'
    case 'HIGH AMBER': return 'bg-orange-500/20 text-orange-300 border border-orange-300/30'
    default: return 'bg-redish/20 text-redish border border-redish/30'
  }
}
