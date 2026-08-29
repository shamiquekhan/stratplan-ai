'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Download, FileText, FileSpreadsheet, FileType, CheckCircle, Loader2 } from 'lucide-react'
import { plansApi } from '@/lib/api'
import { useMutation } from '@tanstack/react-query'
import { toast } from 'sonner'

interface ExportTabProps {
  planId: number
}

export function ExportTab({ planId }: ExportTabProps) {
  const [exporting, setExporting] = useState<string | null>(null)

  const exportMutation = useMutation({
    mutationFn: (format: 'pdf' | 'docx' | 'xlsx') => plansApi.export(planId, format),
    onSuccess: (response, format) => {
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      const ext = format === 'docx' ? 'docx' : format
      link.setAttribute('download', `plan-${planId}.${ext}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success(`Exported as ${format.toUpperCase()}`)
      setExporting(null)
    },
    onError: (error: Error) => {
      toast.error(error.message)
      setExporting(null)
    },
  })

  const handleExport = (format: 'pdf' | 'docx' | 'xlsx') => {
    setExporting(format)
    exportMutation.mutate(format)
  }

  const formats = [
    {
      key: 'pdf' as const,
      label: 'PDF Document',
      description: 'Professional formatted document for investors and stakeholders',
      icon: FileText,
      color: 'text-red-500',
      bg: 'bg-red-500/10',
    },
    {
      key: 'docx' as const,
      label: 'Word Document',
      description: 'Editable document for further customization and collaboration',
      icon: FileType,
      color: 'text-blue-500',
      bg: 'bg-blue-500/10',
    },
    {
      key: 'xlsx' as const,
      label: 'Excel Workbook',
      description: 'Financial models, tables, and data for analysis',
      icon: FileSpreadsheet,
      color: 'text-green-500',
      bg: 'bg-green-500/10',
    },
  ]

  return (
    <div className="space-y-6 pt-6 max-w-2xl">
      <div>
        <h3 className="text-lg font-semibold mb-2">Export Your Plan</h3>
        <p className="text-muted-foreground">
          Choose a format to download your complete business plan with all sections,
          financial projections, competitor analysis, and strategy.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {formats.map((fmt) => (
          <ExportFormatCard
            key={fmt.key}
            format={fmt}
            isExporting={exporting === fmt.key}
            onExport={() => handleExport(fmt.key)}
          />
        ))}
      </div>

      <div className="bg-muted/50 border rounded-xl p-6">
        <h4 className="font-medium mb-4">What's Included in Exports</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="space-y-2">
            <ExportItem label="Executive Summary" />
            <ExportItem label="Market Analysis (TAM/SAM/SOM)" />
            <ExportItem label="Competitive Analysis" />
            <ExportItem label="SWOT & PESTLE" />
          </div>
          <div className="space-y-2">
            <ExportItem label="3-Statement Financial Model" />
            <ExportItem label="OKRs & Milestones" />
            <ExportItem label="GTM Strategy" />
            <ExportItem label="Risk Assessment" />
          </div>
        </div>
      </div>

      <div className="bg-primary/10 border border-primary/20 rounded-xl p-6">
        <h4 className="font-medium mb-2">Pro Tips</h4>
        <ul className="space-y-1 text-sm text-muted-foreground">
          <li>• PDF is best for investor pitches and board presentations</li>
          <li>• DOCX allows you to customize branding and formatting</li>
          <li>• XLSX lets you stress-test financial assumptions</li>
          <li>• All exports include the generation timestamp and plan version</li>
        </ul>
      </div>
    </div>
  )
}

function ExportFormatCard({ format, isExporting, onExport }: { format: any; isExporting: boolean; onExport: () => void }) {
  const Icon = format.icon
  return (
    <Button
      onClick={onExport}
      disabled={isExporting}
      className={`relative h-40 w-full flex flex-col items-start justify-between p-6 border-2 transition-all ${
        isExporting ? 'border-primary bg-primary/5' : 'hover:border-primary/50'
      }`}
    >
      <div className="flex items-center gap-3">
        <div className={`p-3 rounded-xl ${format.bg}`}>
          <Icon className={`h-6 w-6 ${format.color}`} />
        </div>
        <div>
          <h4 className="font-semibold">{format.label}</h4>
          <p className="text-sm text-muted-foreground">{format.description}</p>
        </div>
      </div>
      <div className="flex items-center justify-between w-full">
        {isExporting ? (
          <div className="flex items-center gap-2 text-primary">
            <Loader2 className="h-4 w-4 animate-spin" />
            <span className="text-sm font-medium">Exporting...</span>
          </div>
        ) : (
          <Download className="h-5 w-5 text-muted-foreground" />
        )}
      </div>
    </Button>
  )
}

function ExportItem({ label }: { label: string }) {
  return (
    <div className="flex items-center gap-2">
      <CheckCircle className="h-4 w-4 text-green-500" />
      <span>{label}</span>
    </div>
  )
}