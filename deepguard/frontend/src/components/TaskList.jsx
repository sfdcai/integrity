export default function TaskList({ tasks }) {
  return (
    <div className="glass-card p-4">
      <div className="flex justify-between mb-3">
        <h3 className="font-semibold">Tasks & Reminders</h3>
      </div>
      <div className="space-y-3">
        {tasks.map(task => (
          <div key={task.id} className="flex justify-between items-center bg-white/5 px-3 py-2 rounded-lg">
            <div>
              <p className="font-medium">{task.title}</p>
              <p className="text-xs text-slate-400">Priority: {task.priority}</p>
            </div>
            <span className="text-xs text-slate-400">Due: {task.due_date ? new Date(task.due_date).toLocaleDateString() : 'TBD'}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
