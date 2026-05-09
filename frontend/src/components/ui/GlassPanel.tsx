import type { HTMLAttributes, ReactNode } from 'react'

export function GlassPanel({
  children,
  className = '',
  ...props
}: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
  return (
    <div
      className={`rounded-2xl border border-white/60 bg-white/70 p-6 shadow-[0_8px_30px_rgb(0,0,0,0.06)] backdrop-blur-xl backdrop-saturate-150 ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}
