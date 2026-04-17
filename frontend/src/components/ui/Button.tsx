import type { ButtonHTMLAttributes, ReactNode } from 'react'

type Variant = 'primary' | 'secondary' | 'ghost'

const variants: Record<Variant, string> = {
  primary:
    'bg-teal-600 text-white shadow-md hover:bg-teal-700 active:bg-teal-800 border border-teal-700/20',
  secondary:
    'bg-white/80 text-slate-800 border border-slate-200/80 shadow-sm hover:bg-white hover:border-slate-300',
  ghost: 'bg-transparent text-slate-700 hover:bg-slate-100/80 border border-transparent',
}

export function Button({
  children,
  variant = 'primary',
  className = '',
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant
  children: ReactNode
}) {
  return (
    <button
      type="button"
      className={`inline-flex cursor-pointer items-center justify-center gap-2 rounded-xl px-5 py-3 text-base font-semibold transition-all duration-200 ease-out disabled:pointer-events-none disabled:opacity-50 ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
