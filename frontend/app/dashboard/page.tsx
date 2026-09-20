'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Plus, FileText, Download, Trash2, TrendingUp, Users, Target } from 'lucide-react'
import { plansApi } from '@/lib/api'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { formatDate } from '@/lib/utils'

interface Plan {
  id: number
  name: string
  description: string | null
  frequency: string
  industry: string | null
  company_size: string | null
  revenue_range: string | null
  status: string
  created_at: string
  updated_at: string | null
}

export default function DashboardPage() {
  const queryClient = useQueryClient()
  const [search, setSearch] = useState('')

  const { data: plans = [], isLoading } = useQuery({
    queryKey: ['plans'],
    queryFn: () => plansApi.list().then(res => res.data),
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => plansApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plans'] })
      toast.success('Plan deleted')
    },
    onError: (error: Error) => toast.error(error.message),
  })

  const filteredPlans = plans.filter((p: any) =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.industry?.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <p className="text-sm text-muted-foreground">{plans.length} plan{plans.length !== 1 ? 's' : ''} total</p>
          </div>
          <Link href="/" className="bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:bg-primary/90 flex items-center gap-2">
            <Plus className="h-4 w-4" />
            New Plan
          </Link>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <input
            type="text"
            placeholder="Search plans..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full max-w-md px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
          />
        </div>

        {isLoading ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="bg-card border rounded-xl p-6 animate-pulse">
                <div className="h-6 bg-muted rounded w-3/4 mb-4"></div>
                <div className="h-4 bg-muted rounded w-1/2 mb-2"></div>
                <div className="h-4 bg-muted rounded w-1/3"></div>
              </div>
            ))}
          </div>
        ) : filteredPlans.length === 0 ? (
          <div className="text-center py-16">
            <FileText className="h-16 w-16 mx-auto text-muted-foreground/50 mb-4" />
            <h3 className="text-lg font-medium mb-2">No plans yet</h3>
            <p className="text-muted-foreground mb-6">Create your first business plan</p>
            <Link href="/" className="bg-primary text-primary-foreground px-6 py-2 rounded-lg hover:bg-primary/90 inline-flex items-center gap-2">
              <Plus className="h-4 w-4" />
              Create Plan
            </Link>
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {filteredPlans.map((plan: any) => (
              <Link
                key={plan.id}
                href={`/plan/${plan.id}`}
                className="bg-card border rounded-xl p-6 hover:border-primary/50 transition-colors group"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="font-semibold text-lg group-hover:text-primary transition-colors">{plan.name}</h3>
                    <p className="text-sm text-muted-foreground mt-1">{plan.description || 'No description'}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    plan.status === 'active' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
                    plan.status === 'draft' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' :
                    'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400'
                  }`}>
                    {plan.status}
                  </span>
                </div>

                <div className="flex items-center gap-4 text-sm text-muted-foreground mb-4">
                  <span className="flex items-center gap-1"><TrendingUp className="h-3.5 w-3.5" /> {plan.frequency}</span>
                  {plan.industry && <span className="flex items-center gap-1"><Users className="h-3.5 w-3.5" /> {plan.industry}</span>}
                  {plan.company_size && <span className="flex items-center gap-1"><Target className="h-3.5 w-3.5" /> {plan.company_size}</span>}
                </div>

                <div className="flex items-center justify-between pt-4 border-t">
                  <span className="text-xs text-muted-foreground">
                    Updated {formatDate(plan.updated_at || plan.created_at)}
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={(e) => {
                        e.preventDefault()
                        e.stopPropagation()
                        plansApi.export(plan.id, 'pdf').then(res => {
                          const url = window.URL.createObjectURL(new Blob([res.data]))
                          const link = document.createElement('a')
                          link.href = url
                          link.setAttribute('download', `${plan.name}.pdf`)
                          document.body.appendChild(link)
                          link.click()
                          link.remove()
                        }).catch(() => toast.error('Export failed'))
                      }}
                      className="p-2 hover:bg-muted rounded-lg transition-colors"
                      title="Export PDF"
                    >
                      <Download className="h-4 w-4" />
                    </button>
                    <button
                      onClick={(e) => {
                        e.preventDefault()
                        e.stopPropagation()
                        if (confirm('Delete this plan?')) deleteMutation.mutate(plan.id)
                      }}
                      className="p-2 hover:bg-muted rounded-lg transition-colors text-destructive"
                      title="Delete"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}