'use client'

import { useState } from 'react'
import Link from 'next/link'
import { ArrowRight, Sparkles, BarChart3, Users, Target, Shield, CheckCircle } from 'lucide-react'
import { plansApi } from '@/lib/api'
import { useMutation } from '@tanstack/react-query'
import { toast } from 'sonner'

const steps = [
  { id: 'basics', title: 'Basics', icon: Sparkles },
  { id: 'business', title: 'Business', icon: BarChart3 },
  { id: 'market', title: 'Market', icon: Users },
  { id: 'strategy', title: 'Strategy', icon: Target },
  { id: 'review', title: 'Review', icon: Shield },
]

const industries = [
  'SaaS', 'FinTech', 'HealthTech', 'E-commerce', 'Marketplace',
  'EdTech', 'PropTech', 'Logistics', 'Manufacturing', 'Professional Services',
  'Consumer App', 'B2B Services', 'Other'
]

const companySizes = ['Pre-revenue', '$0-100k', '$100k-1M', '$1M-10M', '$10M+']
const frequencies = ['Monthly', 'Quarterly', 'Yearly']
const stages = ['Idea', 'MVP', 'Early Traction', 'Growth', 'Scale']

export default function HomePage() {
  const [currentStep, setCurrentStep] = useState(0)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    industry: '',
    company_size: '',
    revenue_range: '',
    frequency: 'Quarterly',
    stage: '',
    target_customer: '',
    business_model: '',
    differentiation: '',
    competitors: '',
    funding_status: 'bootstrapped',
    gtm_preference: '',
  })
  const [isGenerating, setIsGenerating] = useState(false)

  const createPlanMutation = useMutation({
    mutationFn: (data: any) => plansApi.create(data),
    onSuccess: (response) => {
      const planId = response.data.id
      generatePlan(planId)
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to create plan')
      setIsGenerating(false)
    },
  })

  const generatePlan = async (planId: number) => {
    try {
      await plansApi.generate(planId, formData)
      toast.success('Plan generated successfully!')
      window.location.href = `/plan/${planId}`
    } catch (error: any) {
      toast.error(error.message || 'Generation failed')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (currentStep === steps.length - 1) {
      setIsGenerating(true)
      createPlanMutation.mutate({
        name: formData.name,
        description: formData.description,
        industry: formData.industry,
        company_size: formData.company_size,
        revenue_range: formData.revenue_range,
        frequency: formData.frequency.toLowerCase(),
      })
    } else {
      setCurrentStep(currentStep + 1)
    }
  }

  const handleBack = () => {
    if (currentStep > 0) setCurrentStep(currentStep - 1)
  }

  const updateField = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const renderStepContent = () => {
    switch (steps[currentStep].id) {
      case 'basics':
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Plan Name</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => updateField('name', e.target.value)}
                className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
                placeholder="e.g., Q3 2024 Growth Plan"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => updateField('description', e.target.value)}
                className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
                rows={4}
                placeholder="Brief description of what this plan covers..."
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Planning Frequency</label>
                <select
                  value={formData.frequency}
                  onChange={(e) => updateField('frequency', e.target.value)}
                  className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
                >
                  {frequencies.map(f => <option key={f} value={f}>{f}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Industry</label>
                <select
                  value={formData.industry}
                  onChange={(e) => updateField('industry', e.target.value)}
                  className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
                >
                  <option value="">Select industry</option>
                  {industries.map(i => <option key={i} value={i}>{i}</option>)}
                </select>
              </div>
            </div>
          </div>
        )
      case 'business':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Company Stage</label>
                <select
                  value={formData.stage}
                  onChange={(e) => updateField('stage', e.target.value)}
                  className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
                >
                  <option value="">Select stage</option>
                  {stages.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Company Size / Revenue</label>
                <select
                  value={formData.company_size}
                  onChange={(e) => updateField('company_size', e.target.value)}
                  className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
                >
                  <option value="">Select size</option>
                  {companySizes.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Target Customer</label>
              <input
                type="text"
                value={formData.target_customer}
                onChange={(e) => updateField('target_customer', e.target.value)}
                className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
                placeholder="e.g., B2B SaaS companies with 50-500 employees"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Business Model</label>
              <select
                value={formData.business_model}
                onChange={(e) => updateField('business_model', e.target.value)}
                className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
              >
                <option value="">Select model</option>
                <option value="subscription">Subscription (SaaS)</option>
                <option value="marketplace">Marketplace</option>
                <option value="ecommerce">E-commerce</option>
                <option value="freemium">Freemium</option>
                <option value="license">Perpetual License</option>
                <option value="services">Professional Services</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Key Differentiation</label>
              <textarea
                value={formData.differentiation}
                onChange={(e) => updateField('differentiation', e.target.value)}
                className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
                rows={3}
                placeholder="What makes you unique? (tech, pricing, service, niche...)"
              />
            </div>
          </div>
        )
      case 'market':
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Known Competitors (comma-separated URLs)</label>
              <input
                type="text"
                value={formData.competitors}
                onChange={(e) => updateField('competitors', e.target.value)}
                className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
                placeholder="https://competitor1.com, https://competitor2.com"
              />
              <p className="text-sm text-muted-foreground mt-1">We'll scrape their pricing, features, and tech stack</p>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">GTM Preference</label>
              <select
                value={formData.gtm_preference}
                onChange={(e) => updateField('gtm_preference', e.target.value)}
                className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
              >
                <option value="">No preference</option>
                <option value="content_seo">Content & SEO</option>
                <option value="paid_ads">Paid Acquisition</option>
                <option value="outbound">Outbound Sales</option>
                <option value="partnerships">Partnerships/Channel</option>
                <option value="product_led">Product-Led Growth</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Funding Status</label>
              <select
                value={formData.funding_status}
                onChange={(e) => updateField('funding_status', e.target.value)}
                className="w-full px-4 py-2 border rounded-lg bg-background focus:ring-2 focus:ring-primary"
              >
                <option value="bootstrapped">Bootstrapped</option>
                <option value="pre_seed">Pre-Seed</option>
                <option value="seed">Seed</option>
                <option value="series_a">Series A</option>
                <option value="series_b_plus">Series B+</option>
              </select>
            </div>
          </div>
        )
      case 'strategy':
        return (
          <div className="space-y-6">
            <div className="bg-muted/50 p-4 rounded-lg">
              <h4 className="font-medium mb-3">What happens next?</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-center gap-2"><CheckCircle className="h-4 w-4 text-primary" /> AI agents research your market & competitors</li>
                <li className="flex items-center gap-2"><CheckCircle className="h-4 w-4 text-primary" /> Financial agent builds 3-statement model</li>
                <li className="flex items-center gap-2"><CheckCircle className="h-4 w-4 text-primary" /> Strategy agent creates GTM, OKRs & milestones</li>
                <li className="flex items-center gap-2"><CheckCircle className="h-4 w-4 text-primary" /> Execution tracker sets up variance alerts</li>
                <li className="flex items-center gap-2"><CheckCircle className="h-4 w-4 text-primary" /> Export to PDF, DOCX, or Excel</li>
              </ul>
            </div>
            <div className="bg-primary/10 border border-primary/20 p-4 rounded-lg">
              <p className="text-sm">This typically takes 2-3 minutes. You'll be redirected to the complete plan when ready.</p>
            </div>
          </div>
        )
      case 'review':
        return (
          <div className="space-y-6">
            <dl className="space-y-4 text-sm">
              <div className="grid grid-cols-2 gap-4">
                <dt className="text-muted-foreground">Plan Name</dt>
                <dd className="font-medium">{formData.name}</dd>
                <dt className="text-muted-foreground">Frequency</dt>
                <dd>{formData.frequency}</dd>
                <dt className="text-muted-foreground">Industry</dt>
                <dd>{formData.industry}</dd>
                <dt className="text-muted-foreground">Stage</dt>
                <dd>{formData.stage}</dd>
                <dt className="text-muted-foreground">Size</dt>
                <dd>{formData.company_size}</dd>
                <dt className="text-muted-foreground">Model</dt>
                <dd>{formData.business_model}</dd>
              </div>
            </dl>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold">StratPlan AI</h1>
          <Link href="/dashboard" className="text-sm text-muted-foreground hover:text-foreground">
            View Dashboard →
          </Link>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12 max-w-3xl">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">Create Your Business Plan in Minutes</h2>
          <p className="text-lg text-muted-foreground">
            AI agents research, model, and write — you get an investor-ready plan with financials, market data, and execution tracking.
          </p>
        </div>

        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium transition-all ${
                    index < currentStep
                      ? 'bg-primary text-primary-foreground'
                      : index === currentStep
                      ? 'bg-primary/20 text-primary border-2 border-primary'
                      : 'bg-muted text-muted-foreground'
                  }`}
                >
                  {index < currentStep ? <CheckCircle className="h-5 w-5" /> : index + 1}
                </div>
                {index < steps.length - 1 && (
                  <div
                    className={`w-16 h-0.5 mx-2 ${
                      index < currentStep ? 'bg-primary' : 'bg-muted'
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-center gap-2">
            {steps.map((step, index) => (
              <span
                key={step.id}
                className={`text-xs font-medium px-2 py-1 rounded ${
                  index === currentStep ? 'bg-primary/20 text-primary' : 'text-muted-foreground'
                }`}
              >
                {step.title}
              </span>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="bg-card border rounded-xl p-8">
          {renderStepContent()}
          
          <div className="flex justify-between mt-8 pt-6 border-t">
            <button
              type="button"
              onClick={handleBack}
              disabled={currentStep === 0}
              className="px-6 py-2 border rounded-lg hover:bg-muted disabled:opacity-50"
            >
              Back
            </button>
            <button
              type="submit"
              disabled={isGenerating}
              className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 flex items-center gap-2"
            >
              {isGenerating ? (
                <>
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/></svg>
                  Generating...
                </>
              ) : currentStep === steps.length - 1 ? (
                <>
                  Create Plan
                  <ArrowRight className="h-4 w-4" />
                </>
              ) : (
                <>
                  Next
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </div>
        </form>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div className="p-6 bg-card border rounded-xl">
            <Sparkles className="h-10 w-10 mx-auto text-primary mb-3" />
            <h3 className="font-semibold mb-2">AI-Generated Narrative</h3>
            <p className="text-sm text-muted-foreground">Executive summary, market analysis, strategy sections written by specialized agents</p>
          </div>
          <div className="p-6 bg-card border rounded-xl">
            <BarChart3 className="h-10 w-10 mx-auto text-primary mb-3" />
            <h3 className="font-semibold mb-2">Real Financial Models</h3>
            <p className="text-sm text-muted-foreground">3-statement projections grounded in industry benchmarks & macro data</p>
          </div>
          <div className="p-6 bg-card border rounded-xl">
            <Users className="h-10 w-10 mx-auto text-primary mb-3" />
            <h3 className="font-semibold mb-2">Live Competitor Intel</h3>
            <p className="text-sm text-muted-foreground">Pricing, features, tech stack scraped from competitor websites</p>
          </div>
        </div>
      </main>
    </div>
  )
}