import TrafficLight from './TrafficLight'

export default function AnnulusCard({ name, pressure, maasp, status }) {
  const utilisation = maasp ? Math.round((pressure/maasp)*100) : 0
  return (
    <div className="glass-card p-4 space-y-2">
      <div className="flex justify-between items-center">
        <div>
          <p className="text-xs text-slate-400">{name}-Annulus</p>
          <h4 className="text-lg font-semibold">{pressure} bar</h4>
        </div>
        <TrafficLight status={status} />
      </div>
      <p className="text-sm text-slate-300">MAASP {maasp} bar</p>
      <div className="w-full bg-white/5 rounded-full h-2">
        <div className={`h-2 rounded-full ${status==='RED'?'bg-red-500':status==='HIGH-AMBER'?'bg-orange-400':status==='AMBER'?'bg-amber-300':'bg-green-400'}`} style={{width:`${Math.min(utilisation,100)}%`}}></div>
      </div>
      <p className="text-xs text-slate-400">Utilisation {utilisation}%</p>
    </div>
  )
}
