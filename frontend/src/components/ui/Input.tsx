import type { InputHTMLAttributes } from 'react'

export function Input({
  label,
  id,
  className = '',
  ...props
}: InputHTMLAttributes<HTMLInputElement> & { label: string; id: string }) {
  return (
    <div className="flex flex-col gap-1.5 text-left">
      <label htmlFor={id} className="text-sm font-medium text-slate-700">
        {label}
      </label>
      <input
        id={id}
        className={`rounded-xl border border-slate-200/90 bg-white/90 px-3.5 py-2.5 text-slate-900 shadow-inner transition duration-200 placeholder:text-slate-400 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/25 ${className}`}
        {...props}
      />
    </div>
  )
}

export function TextArea({
  label,
  id,
  className = '',
  ...props
}: React.TextareaHTMLAttributes<HTMLTextAreaElement> & {
  label: string
  id: string
}) {
  return (
    <div className="flex flex-col gap-1.5 text-left">
      <label htmlFor={id} className="text-sm font-medium text-slate-700">
        {label}
      </label>
      <textarea
        id={id}
        rows={4}
        className={`resize-y rounded-xl border border-slate-200/90 bg-white/90 px-3.5 py-2.5 text-slate-900 shadow-inner transition duration-200 placeholder:text-slate-400 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/25 ${className}`}
        {...props}
      />
    </div>
  )
}
