export function ProgressBar({ value }) {
  return (
    <div className="w-full h-3 rounded-full bg-white/10">
      <div className="h-3 rounded-full bg-gradient-to-r from-teal to-amber" style={{ width: `${Math.min(value, 120)}%` }}></div>
    </div>
  )
}
