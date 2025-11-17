const colorMap = {
  GREEN: 'bg-green-400',
  AMBER: 'bg-amber-300',
  'HIGH-AMBER': 'bg-orange-400',
  RED: 'bg-red-500'
}

export default function TrafficLight({ status }) {
  return (
    <div className="flex gap-1 items-center">
      <span className={`h-3 w-3 rounded-full ${colorMap[status] || 'bg-slate-500'}`}></span>
      <span className="text-xs text-slate-300">{status}</span>
    </div>
  )
}
