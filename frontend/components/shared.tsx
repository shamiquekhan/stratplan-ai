export function SectionCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-card border rounded-xl p-6">
      <h3 className="font-semibold mb-4">{title}</h3>
      {children}
    </div>
  )
}
