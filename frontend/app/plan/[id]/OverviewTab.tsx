'use client'

import { PlanData } from '@/lib/types'
import { formatCurrency, formatPercent, formatDate } from '@/lib/utils'
import { TrendingUp, Target, DollarSign, ArrowUpRight } from 'lucide-react'
import { SectionCard } from '@/components/shared'

interface OverviewTabProps {
  planData: PlanData
}

export function OverviewTab({ planData }: OverviewTabProps) {
  const { plan, generated_plan, financial_projections, market_analysis, strategy } = planData
  const assumptions = financial_projections.assumptions || {}
  const pnl = financial_projections.pnl || []
  const keyMetrics = financial_projections.key_metrics || {}

  const latestPnl = pnl[pnl.length - 1]
  const yearlyRevenue = pnl.filter((p: any) => p.period.includes('Month 12') || p.period.includes('Month 24') || p.period.includes('Month 36'))
  const totalRevenue = yearlyRevenue.reduce((sum: number, p: any) => sum + (p.revenue || 0), 0)

  return (
    <div className="space-y-6 pt-6">
      <div className="prose max-w-none">
        {generated_plan.split('\n\n').map((paragraph, i) => (
          <p key={i} className="mb-4 text-muted-foreground">{paragraph}</p>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          label="Projected Revenue (Year 1)"
          value={formatCurrency(yearlyRevenue[0]?.revenue || 0)}
          icon={DollarSign}
          trend={assumptions.revenue_growth_rate ? `+${formatPercent(assumptions.revenue_growth_rate)}/yr` : undefined}
        />
        <KPICard
          label="Gross Margin"
          value={formatPercent(assumptions.gross_margin || 0)}
          icon={TrendingUp}
        />
        <KPICard
          label="Runway"
          value={`${keyMetrics.runway_months || 0} months`}
          icon={Target}
        />
        <KPICard
          label="Break-even"
          value={`Month ${keyMetrics.break_even_month || 'N/A'}`}
          icon={ArrowUpRight}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SectionCard title="Financial Summary">
          <div className="space-y-3">
            <MetricRow label="Revenue Growth Rate" value={formatPercent(assumptions.revenue_growth_rate || 0)} />
            <MetricRow label="Gross Margin" value={formatPercent(assumptions.gross_margin || 0)} />
            <MetricRow label="Operating Expense Ratio" value={formatPercent(assumptions.operating_expense_ratio || 0)} />
            <MetricRow label="Tax Rate" value={formatPercent(assumptions.tax_rate || 0.21)} />
            <MetricRow label="LTV/CAC Ratio" value={`${keyMetrics.ltv_cac_ratio || 0}x`} />
            <MetricRow label="Payback Period" value={`${keyMetrics.payback_period_months || 0} months`} />
          </div>
        </SectionCard>

        <SectionCard title="Plan Details">
          <div className="space-y-3">
            <MetricRow label="Frequency" value={plan.frequency} />
            <MetricRow label="Industry" value={plan.industry || 'Not specified'} />
            <MetricRow label="Company Size" value={plan.company_size || 'Not specified'} />
            <MetricRow label="Revenue Range" value={plan.revenue_range || 'Not specified'} />
            <MetricRow label="Status" value={plan.status} />
            <MetricRow label="Created" value={formatDate(plan.created_at)} />
          </div>
        </SectionCard>
      </div>

      {strategy?.okrs && strategy.okrs.length > 0 && (
        <SectionCard title="Top Objectives">
          <div className="space-y-4">
            {strategy.okrs.slice(0, 3).map((okr: any, i: number) => (
              <div key={i} className="p-4 bg-muted/50 rounded-lg">
                <h4 className="font-medium mb-2">{okr.objective}</h4>
                <div className="space-y-1">
                  {okr.key_results?.slice(0, 2).map((kr: any, j: number) => (
                    <div key={j} className="text-sm flex items-center gap-2">
                      <span className="h-1.5 w-1.5 rounded-full bg-primary" />
                      {kr.metric}: {kr.target} {kr.unit}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </SectionCard>
      )}

      {strategy?.milestones && strategy.milestones.length > 0 && (
        <SectionCard title="Upcoming Milestones">
          <div className="space-y-3">
            {strategy.milestones.slice(0, 5).map((ms: any, i: number) => (
              <div key={i} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                <div>
                  <p className="font-medium">{ms.milestone}</p>
                  <p className="text-sm text-muted-foreground">{formatDate(ms.target_date)}</p>
                </div>
                <span className={`px-2 py-1 text-xs rounded-full ${
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
    </div>
  )
}

function KPICard({ label, value, icon: Icon, trend }: { label: string; value: string; icon: React.ComponentType<{ className?: string }>; trend?: string }) {
  return (
    <div className="bg-card border rounded-xl p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground">{label}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
          {trend && <p className="text-sm text-green-600 mt-1">{trend}</p>}
        </div>
        <Icon className="h-8 w-8 text-muted-foreground/50" />
      </div>
    </div>
  )
}

function MetricRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between py-2 border-b last:border-0">
      <span className="text-muted-foreground">{label}</span>
      <span className="font-medium">{value}</span>
    </div>
  )
}