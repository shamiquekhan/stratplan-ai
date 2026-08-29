'use client'

import { useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { Download, ArrowLeft, Loader2 } from 'lucide-react'
import { plansApi } from '@/lib/api'
import { useQuery, useMutation } from '@tanstack/react-query'
import { toast } from 'sonner'
import { formatCurrency, formatNumber, formatPercent, formatDate } from '@/lib/utils'
import { OverviewTab } from './OverviewTab'
import { FinancialsTab } from './financials/FinancialsTab'
import { CompetitorsTab } from './competitors/CompetitorsTab'
import { StrategyTab } from './strategy/StrategyTab'
import { ExportTab } from './export/ExportTab'
import { SectionCard } from '@/components/shared'
import { PlanData } from '@/lib/types'

export type { PlanData }

export default function PlanDetailPage() {
  const params = useParams()
  const planId = parseInt(params.id as string)
  const [activeTab, setActiveTab] = useState('overview')

  const { data, isLoading, error } = useQuery({
    queryKey: ['plan', planId],
    queryFn: () => plansApi.get(planId).then(res => res.data),
    enabled: !!planId,
  })

  const exportMutation = useMutation({
    mutationFn: (format: 'pdf' | 'docx' | 'xlsx') => plansApi.export(planId, format),
    onSuccess: (response, format) => {
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `plan-${planId}.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success(`Exported as ${format.toUpperCase()}`)
    },
    onError: (error: Error) => toast.error(error.message),
  })

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">Plan not found</h2>
          <Link href="/dashboard" className="text-primary hover:underline">Back to Dashboard</Link>
        </div>
      </div>
    )
  }

  const planData: PlanData = {
    plan: data,
    generated_plan: data.executive_summary?.content || '',
    financial_projections: data.financial_projections?.[0] || {},
    market_analysis: data.market_analysis || {},
    competitor_analysis: data.competitor_analysis || {},
    strategy: data.strategy || {},
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="p-2 hover:bg-muted rounded-lg">
              <ArrowLeft className="h-5 w-5" />
            </Link>
            <div>
              <h1 className="text-2xl font-bold">{data.name}</h1>
              <p className="text-sm text-muted-foreground">
                {data.frequency} • {data.industry} • {data.status}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" onClick={() => exportMutation.mutate('pdf')}>
              <Download className="h-4 w-4 mr-2" />
              PDF
            </Button>
            <Button variant="outline" onClick={() => exportMutation.mutate('docx')}>
              <Download className="h-4 w-4 mr-2" />
              DOCX
            </Button>
            <Button variant="outline" onClick={() => exportMutation.mutate('xlsx')}>
              <Download className="h-4 w-4 mr-2" />
              XLSX
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-6">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="financials">Financials</TabsTrigger>
            <TabsTrigger value="market">Market</TabsTrigger>
            <TabsTrigger value="competitors">Competitors</TabsTrigger>
            <TabsTrigger value="strategy">Strategy</TabsTrigger>
            <TabsTrigger value="export">Export</TabsTrigger>
          </TabsList>

          <TabsContent value="overview">
            <OverviewTab planData={planData} />
          </TabsContent>

          <TabsContent value="financials">
            <FinancialsTab planData={planData} />
          </TabsContent>

          <TabsContent value="market">
            <MarketTab planData={planData} />
          </TabsContent>

          <TabsContent value="competitors">
            <CompetitorsTab planData={planData} />
          </TabsContent>

          <TabsContent value="strategy">
            <StrategyTab planData={planData} />
          </TabsContent>

          <TabsContent value="export">
            <ExportTab planId={planId} />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

function MarketTab({ planData }: { planData: PlanData }) {
  const market = planData.market_analysis
  if (!market || Object.keys(market).length === 0) {
    return <div className="py-12 text-center text-muted-foreground">No market analysis data available</div>
  }

  return (
    <div className="space-y-6 pt-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MetricCard label="TAM" value={formatCurrency(market.tam || 0)} />
        <MetricCard label="SAM" value={formatCurrency(market.sam || 0)} />
        <MetricCard label="SOM" value={formatCurrency(market.som || 0)} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SectionCard title="Key Trends">
          <ul className="space-y-2">
            {market.key_trends?.map((trend: string, i: number) => (
              <li key={i} className="flex items-center gap-2 text-sm">
                <span className="h-2 w-2 rounded-full bg-primary" />
                {trend}
              </li>
            ))}
          </ul>
        </SectionCard>

        <SectionCard title="Market Drivers & Barriers">
          <div className="space-y-4">
            <div>
              <h5 className="font-medium mb-2">Drivers</h5>
              <ul className="space-y-1 text-sm">
                {market.market_drivers?.map((d: string, i: number) => (
                  <li key={i} className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-green-500" /> {d}</li>
                ))}
              </ul>
            </div>
            <div>
              <h5 className="font-medium mb-2">Barriers</h5>
              <ul className="space-y-1 text-sm">
                {market.market_barriers?.map((b: string, i: number) => (
                  <li key={i} className="flex items-center gap-2"><span className="h-1.5 w-1.5 rounded-full bg-red-500" /> {b}</li>
                ))}
              </ul>
            </div>
          </div>
        </SectionCard>
      </div>

      {market.target_segments && market.target_segments.length > 0 && (
        <SectionCard title="Target Segments">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-muted-foreground">
                  <th className="pb-2">Segment</th>
                  <th className="pb-2">Size</th>
                  <th className="pb-2">Growth</th>
                  <th className="pb-2">Characteristics</th>
                </tr>
              </thead>
              <tbody>
                {market.target_segments.map((seg: any, i: number) => (
                  <tr key={i} className="border-b">
                    <td className="py-2 font-medium">{seg.segment}</td>
                    <td className="py-2">{formatCurrency(seg.size || 0)}</td>
                    <td className="py-2">{formatPercent(seg.growth_rate || 0)}</td>
                    <td className="py-2">{seg.characteristics?.join(', ')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </SectionCard>
      )}

      {market.industry_benchmarks && (
        <SectionCard title="Industry Benchmarks">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(market.industry_benchmarks).map(([key, value]) => (
              <div key={key} className="p-4 bg-muted/50 rounded-lg">
                <p className="text-sm text-muted-foreground">{key.replace(/_/g, ' ')}</p>
                <p className="font-semibold">{typeof value === 'number' ? (value < 1 ? formatPercent(value) : formatNumber(value)) : String(value)}</p>
              </div>
            ))}
          </div>
        </SectionCard>
      )}

      {market.macro_indicators && (
        <SectionCard title="Macro Indicators">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {Object.entries(market.macro_indicators).map(([key, value]) => (
              <div key={key} className="p-4 bg-muted/50 rounded-lg">
                <p className="text-sm text-muted-foreground">{key.replace(/_/g, ' ')}</p>
                <p className="font-semibold">{typeof value === 'number' ? formatPercent(value) : String(value)}</p>
              </div>
            ))}
          </div>
        </SectionCard>
      )}
    </div>
  )
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-card border rounded-xl p-6">
      <p className="text-sm text-muted-foreground">{label}</p>
      <p className="text-3xl font-bold mt-1">{value}</p>
    </div>
  )
}