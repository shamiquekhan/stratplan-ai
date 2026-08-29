'use client'

import { formatDate } from '@/lib/utils'
import { SectionCard } from '@/components/shared'
import { CheckCircle, AlertCircle, Target, TrendingUp, Flag } from 'lucide-react'

interface StrategyTabProps {
  planData: any
}

export function StrategyTab({ planData }: StrategyTabProps) {
  const strategy = planData.strategy
  const swot = strategy?.swot
  const pestle = strategy?.pestle
  const gtm = strategy?.gtm_strategy
  const okrs = strategy?.okrs || []
  const milestones = strategy?.milestones || []
  const risks = strategy?.risk_assessment || []

  if (!strategy || Object.keys(strategy).length === 0) {
    return <div className="py-12 text-center text-muted-foreground">No strategy data available</div>
  }

  return (
    <div className="space-y-6 pt-6">
      {swot && (
        <SectionCard title="SWOT Analysis">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <SWOTQuadrant title="Strengths" icon={CheckCircle} color="text-green-600" items={swot.strengths} />
            <SWOTQuadrant title="Weaknesses" icon={AlertCircle} color="text-red-600" items={swot.weaknesses} />
            <SWOTQuadrant title="Opportunities" icon={TrendingUp} color="text-blue-600" items={swot.opportunities} />
            <SWOTQuadrant title="Threats" icon={AlertCircle} color="text-orange-600" items={swot.threats} />
          </div>
        </SectionCard>
      )}

      {pestle && (
        <SectionCard title="PESTLE Analysis">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(pestle).map(([category, factors]) => (
              <div key={category} className="p-4 bg-muted/50 rounded-lg">
                <h4 className="font-medium capitalize mb-3">{category}</h4>
                <ul className="space-y-1 text-sm">
                  {(factors as string[]).map((factor, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <span className="h-1.5 w-1.5 rounded-full bg-primary" />
                      {factor}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </SectionCard>
      )}

      {gtm && (
        <div className="space-y-6">
          <SectionCard title="Go-to-Market Strategy">
            <div className="space-y-6">
              {gtm.value_proposition && (
                <div>
                  <h4 className="font-medium mb-2">Value Proposition</h4>
                  <p className="text-muted-foreground">{gtm.value_proposition}</p>
                </div>
              )}
              {gtm.target_customer && (
                <div>
                  <h4 className="font-medium mb-2">Target Customer</h4>
                  <p className="text-muted-foreground">{gtm.target_customer}</p>
                </div>
              )}
              {gtm.pricing_strategy && (
                <div>
                  <h4 className="font-medium mb-2">Pricing Strategy</h4>
                  <p className="text-muted-foreground">{gtm.pricing_strategy}</p>
                </div>
              )}
              {gtm.channels && gtm.channels.length > 0 && (
                <div>
                  <h4 className="font-medium mb-3">Channels</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b text-left text-muted-foreground">
                          <th className="pb-2">Channel</th>
                          <th className="pb-2">Priority</th>
                          <th className="pb-2">Budget %</th>
                          <th className="pb-2">Expected CAC</th>
                          <th className="pb-2">Timeline</th>
                        </tr>
                      </thead>
                      <tbody>
                        {gtm.channels.map((ch: any, i: number) => (
                          <tr key={i} className="border-b">
                            <td className="py-2 font-medium">{ch.channel}</td>
                            <td className="py-2">
                              <span className={`px-2 py-1 text-xs rounded-full ${
                                ch.priority === 'high' ? 'bg-red-100 text-red-800' :
                                ch.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-green-100 text-green-800'
                              }`}>
                                {ch.priority}
                              </span>
                            </td>
                            <td className="py-2">{ch.budget_allocation ? `${(ch.budget_allocation * 100).toFixed(0)}%` : 'N/A'}</td>
                            <td className="py-2">{ch.expected_cac ? `$${ch.expected_cac}` : 'N/A'}</td>
                            <td className="py-2">{ch.timeline}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
              {gtm.launch_sequence && gtm.launch_sequence.length > 0 && (
                <div>
                  <h4 className="font-medium mb-3">Launch Sequence</h4>
                  <div className="space-y-3">
                    {gtm.launch_sequence.map((phase: any, i: number) => (
                      <div key={i} className="p-4 bg-muted/50 rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                          <h5 className="font-medium">{phase.phase}</h5>
                          <span className="text-sm text-muted-foreground">{phase.timeline}</span>
                        </div>
                        <ul className="space-y-1 text-sm">
                          {phase.activities?.map((act: string, j: number) => (
                            <li key={j} className="flex items-center gap-2">
                              <span className="h-1.5 w-1.5 rounded-full bg-primary" />
                              {act}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {gtm.partnerships && gtm.partnerships.length > 0 && (
                <div>
                  <h4 className="font-medium mb-2">Key Partnerships</h4>
                  <ul className="space-y-1">
                    {gtm.partnerships.map((p: string, i: number) => (
                      <li key={i} className="flex items-center gap-2 text-sm">
                        <Flag className="h-4 w-4 text-primary" />
                        {p}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </SectionCard>
        </div>
      )}

      {okrs.length > 0 && (
        <SectionCard title="OKRs">
          <div className="space-y-4">
            {okrs.map((okr: any, i: number) => (
              <div key={i} className="p-4 bg-muted/50 rounded-lg">
                <div className="flex items-start justify-between mb-3">
                  <h4 className="font-medium flex-1">{okr.objective}</h4>
                  <div className="flex items-center gap-2 ml-4">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      okr.status === 'completed' ? 'bg-green-100 text-green-800' :
                      okr.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {okr.status}
                    </span>
                    {okr.timeline && <span className="text-sm text-muted-foreground">{okr.timeline}</span>}
                  </div>
                </div>
                {okr.owner && <p className="text-sm text-muted-foreground mb-3">Owner: {okr.owner}</p>}
                <div className="space-y-2">
                  {okr.key_results?.map((kr: any, j: number) => (
                    <div key={j} className="flex items-center justify-between p-3 bg-background rounded">
                      <div className="flex-1">
                        <p className="font-medium text-sm">{kr.metric}</p>
                        <p className="text-xs text-muted-foreground">Target: {kr.target} {kr.unit} • Current: {kr.current} {kr.unit}</p>
                      </div>
                      <div className="w-32">
                        <ProgressBar value={kr.current} max={kr.target} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </SectionCard>
      )}

      {milestones.length > 0 && (
        <SectionCard title="Milestones & Timeline">
          <div className="space-y-3">
            {milestones.map((ms: any, i: number) => (
              <div key={i} className="flex items-center gap-4 p-4 bg-muted/50 rounded-lg">
                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <Target className="h-6 w-6 text-primary" />
                </div>
                <div className="flex-1">
                  <p className="font-medium">{ms.milestone}</p>
                  <p className="text-sm text-muted-foreground">{formatDate(ms.target_date)}</p>
                  {ms.success_criteria && <p className="text-sm text-muted-foreground mt-1">Success: {ms.success_criteria}</p>}
                </div>
                <span className={`px-3 py-1 text-sm rounded-full ${
                  ms.status === 'completed' ? 'bg-green-100 text-green-800' :
                  ms.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {ms.status}
                </span>
              </div>
            ))}
          </div>
        </SectionCard>
      )}

      {risks.length > 0 && (
        <SectionCard title="Risk Assessment">
          <div className="space-y-3">
            {risks.map((risk: any, i: number) => (
              <div key={i} className="p-4 bg-muted/50 rounded-lg border-l-4 border-destructive">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="font-medium">{risk.risk}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <AlertCircle className="h-3.5 w-3.5" />
                        Likelihood: {risk.likelihood}
                      </span>
                      <span className="flex items-center gap-1">
                        <TrendingUp className="h-3.5 w-3.5" />
                        Impact: {risk.impact}
                      </span>
                    </div>
                  </div>
                </div>
                {risk.mitigation && (
                  <p className="mt-3 text-sm text-muted-foreground">
                    <strong>Mitigation:</strong> {risk.mitigation}
                  </p>
                )}
              </div>
            ))}
          </div>
        </SectionCard>
      )}
    </div>
  )
}

function SWOTQuadrant({ title, icon: Icon, color, items }: { title: string; icon: React.ComponentType<{ className?: string }>; color: string; items: string[] }) {
  return (
    <div className="p-4 bg-muted/50 rounded-lg">
      <div className="flex items-center gap-2 mb-3">
        <Icon className={`h-5 w-5 ${color}`} />
        <h4 className="font-medium">{title}</h4>
      </div>
      <ul className="space-y-2">
        {items?.map((item, i) => (
          <li key={i} className="text-sm flex items-center gap-2">
            <span className={`h-1.5 w-1.5 rounded-full ${color.replace('text-', 'bg-')}`} />
            {item}
          </li>
        ))}
      </ul>
    </div>
  )
}

function ProgressBar({ value, max }: { value: number; max: number }) {
  const percent = max > 0 ? Math.min(100, (value / max) * 100) : 0
  return (
    <div className="h-2 bg-muted rounded-full overflow-hidden">
      <div
        className="h-full bg-primary rounded-full transition-all"
        style={{ width: `${percent}%` }}
      />
    </div>
  )
}