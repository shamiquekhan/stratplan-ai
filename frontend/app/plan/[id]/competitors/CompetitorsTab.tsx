'use client'

import { formatCurrency } from '@/lib/utils'
import { SectionCard } from '@/components/shared'
import { ExternalLink, Check, X } from 'lucide-react'

interface CompetitorsTabProps {
  planData: any
}

export function CompetitorsTab({ planData }: CompetitorsTabProps) {
  const competitors = planData.competitor_analysis?.competitors || []
  const matrix = planData.competitor_analysis?.competitive_matrix
  const positioning = planData.competitor_analysis?.positioning_map

  if (competitors.length === 0) {
    return <div className="py-12 text-center text-muted-foreground">No competitor analysis available</div>
  }

  return (
    <div className="space-y-6 pt-6">
      <SectionCard title="Competitor Profiles">
        <div className="space-y-6">
          {competitors.map((comp: any, i: number) => (
            <CompetitorCard key={i} competitor={comp} />
          ))}
        </div>
      </SectionCard>

      {matrix && matrix.criteria && matrix.scores && (
        <SectionCard title="Competitive Matrix">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-muted-foreground">
                  <th className="pb-2">Criteria</th>
                  {Object.keys(matrix.scores).map((name) => (
                    <th key={name} className="pb-2 text-center font-medium">{name}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {matrix.criteria.map((criterion: string, i: number) => (
                  <tr key={i} className="border-b">
                    <td className="py-2 font-medium">{criterion}</td>
                    {Object.values(matrix.scores).map((scores: any, j: number) => (
                      <td key={j} className="py-2 text-center">
                        <ScoreBadge score={scores[i] || 0} />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </SectionCard>
      )}

      {positioning && positioning.positions && (
        <SectionCard title="Positioning Map">
          <PositioningMap positions={positioning.positions} xAxis={positioning.x_axis} yAxis={positioning.y_axis} />
        </SectionCard>
      )}

      {(planData.competitor_analysis?.competitive_advantages || planData.competitor_analysis?.threats) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {planData.competitor_analysis?.competitive_advantages && (
            <SectionCard title="Competitive Advantages">
              <ul className="space-y-2">
                {planData.competitor_analysis.competitive_advantages.map((adv: string, i: number) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <Check className="h-4 w-4 text-green-500" />
                    {adv}
                  </li>
                ))}
              </ul>
            </SectionCard>
          )}

          {planData.competitor_analysis?.threats && (
            <SectionCard title="Threats">
              <ul className="space-y-2">
                {planData.competitor_analysis.threats.map((threat: string, i: number) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <X className="h-4 w-4 text-red-500" />
                    {threat}
                  </li>
                ))}
              </ul>
            </SectionCard>
          )}
        </div>
      )}
    </div>
  )
}

function CompetitorCard({ competitor }: { competitor: any }) {
  return (
    <div className="border rounded-xl p-6 bg-card">
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className="flex items-center gap-3">
            <h3 className="text-lg font-semibold">{competitor.name}</h3>
            {competitor.website && (
              <a href={competitor.website} target="_blank" rel="noopener noreferrer" className="text-sm text-primary hover:underline flex items-center gap-1">
                <ExternalLink className="h-3.5 w-3.5" />
                Website
              </a>
            )}
          </div>
          <p className="text-muted-foreground mt-1">{competitor.description || competitor.positioning}</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          {competitor.funding_stage && <span className="px-2 py-1 bg-muted rounded">{competitor.funding_stage}</span>}
          {competitor.employee_count && <span>{competitor.employee_count} employees</span>}
          {competitor.estimated_revenue && <span>{formatCurrency(competitor.estimated_revenue)} est. revenue</span>}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <h4 className="font-medium mb-2">Pricing</h4>
          <p className="text-sm text-muted-foreground mb-2">{competitor.pricing_model}</p>
          {competitor.pricing_tiers && competitor.pricing_tiers.length > 0 && (
            <ul className="space-y-1 text-sm">
              {competitor.pricing_tiers.slice(0, 3).map((tier: any, i: number) => (
                <li key={i} className="flex justify-between">
                  <span>{tier.name}</span>
                  <span className="font-medium">{tier.price ? `$${tier.price}/${tier.name.toLowerCase().includes('year') ? 'yr' : 'mo'}` : 'Custom'}</span>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div>
          <h4 className="font-medium mb-2">Key Features</h4>
          <ul className="space-y-1 text-sm">
            {competitor.key_features?.slice(0, 5).map((feat: string, i: number) => (
              <li key={i} className="flex items-center gap-2">
                <Check className="h-3.5 w-3.5 text-green-500" />
                {feat}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="font-medium mb-2">Tech Stack</h4>
          <div className="flex flex-wrap gap-1">
            {competitor.tech_stack?.map((tech: string, i: number) => (
              <span key={i} className="px-2 py-1 text-xs bg-muted rounded">{tech}</span>
            ))}
          </div>
        </div>
      </div>

      {(competitor.strengths || competitor.weaknesses) && (
        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t">
          {competitor.strengths && (
            <div>
              <h4 className="font-medium mb-2 text-green-600">Strengths</h4>
              <ul className="space-y-1 text-sm">
                {competitor.strengths.map((s: string, i: number) => (
                  <li key={i} className="flex items-center gap-2">
                    <Check className="h-3.5 w-3.5 text-green-500" />
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {competitor.weaknesses && (
            <div>
              <h4 className="font-medium mb-2 text-red-600">Weaknesses</h4>
              <ul className="space-y-1 text-sm">
                {competitor.weaknesses.map((w: string, i: number) => (
                  <li key={i} className="flex items-center gap-2">
                    <X className="h-3.5 w-3.5 text-red-500" />
                    {w}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function ScoreBadge({ score }: { score: number }) {
  const color = score >= 4 ? 'bg-green-100 text-green-800' : score >= 3 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'
  return <span className={`px-2 py-1 rounded text-sm font-medium ${color}`}>{score}/5</span>
}

function PositioningMap({ positions, xAxis, yAxis }: { positions: Record<string, number[]>; xAxis: string; yAxis: string }) {
  const entries = Object.entries(positions)
  const maxX = Math.max(...entries.map(([, [x]]) => x))
  const maxY = Math.max(...entries.map(([, [, y]]) => y))

  return (
    <div className="relative h-80 bg-muted/30 rounded-lg p-4">
      <svg viewBox="0 0 400 300" className="w-full h-full" preserveAspectRatio="none">
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="currentColor" />
          </marker>
        </defs>
        
        <line x1="40" y1="260" x2="360" y2="260" stroke="currentColor" strokeWidth="1" markerEnd="url(#arrowhead)" opacity="0.3" />
        <line x1="40" y1="260" x2="40" y2="40" stroke="currentColor" strokeWidth="1" markerEnd="url(#arrowhead)" opacity="0.3" />
        
        <text x="200" y="290" textAnchor="middle" fontSize="12" fill="currentColor" opacity="0.6">{xAxis}</text>
        <text x="15" y="150" textAnchor="middle" fontSize="12" fill="currentColor" opacity="0.6" transform="rotate(-90, 15, 150)">{yAxis}</text>

        {entries.map(([name, [x, y]]) => (
          <g key={name}>
            <circle
              cx={40 + (x / maxX) * 300}
              cy={260 - (y / maxY) * 220}
              r="8"
              fill="currentColor"
              opacity="0.8"
            />
            <text
              x={40 + (x / maxX) * 300}
              y={260 - (y / maxY) * 220 - 12}
              textAnchor="middle"
              fontSize="11"
              fontWeight="500"
              fill="currentColor"
            >
              {name}
            </text>
          </g>
        ))}
      </svg>
    </div>
  )
}