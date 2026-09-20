'use client'

import { useMemo } from 'react'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { formatCurrency, formatNumber, formatPercent } from '@/lib/utils'
import { SectionCard } from '@/components/shared'

interface FinancialsTabProps {
  planData: any
}

export function FinancialsTab({ planData }: FinancialsTabProps) {
  const financial = planData.financial_projections
  const pnl = financial.pnl || []
  const cashflow = financial.cash_flow || []
  const balance = financial.balance_sheet || []

  const chartData = useMemo(() => {
    return pnl.map((row: any) => ({
      period: row.period,
      revenue: row.revenue || 0,
      grossProfit: row.gross_profit || 0,
      ebitda: row.ebitda || 0,
      netIncome: row.net_income || 0,
      operatingExpenses: row.operating_expenses || 0,
    }))
  }, [pnl])

  const cashflowData = useMemo(() => {
    return cashflow.map((row: any) => ({
      period: row.period,
      operating: row.operating || 0,
      investing: row.investing || 0,
      financing: row.financing || 0,
      netCashFlow: row.net_cash_flow || 0,
      cashBalance: row.cash_balance || 0,
    }))
  }, [cashflow])

  const balanceData = useMemo(() => {
    return balance.map((row: any) => ({
      period: row.period,
      assets: row.total_assets || 0,
      liabilities: row.total_liabilities || 0,
      equity: row.equity || 0,
    }))
  }, [balance])

  if (chartData.length === 0) {
    return <div className="py-12 text-center text-muted-foreground">No financial projections available</div>
  }

  return (
    <div className="space-y-6 pt-6">
      <SectionCard title="P&L Projection">
        <ResponsiveContainer width="100%" height={350}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorProfit" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="period" tick={{ fontSize: 12 }} />
            <YAxis tickFormatter={formatCurrency} tick={{ fontSize: 12 }} />
            <Tooltip formatter={(value: number) => [formatCurrency(value), '']} labelFormatter={(label) => `Period: ${label}`} />
            <Legend />
            <Area type="monotone" dataKey="revenue" stroke="#3b82f6" fillOpacity={1} fill="url(#colorRevenue)" name="Revenue" />
            <Area type="monotone" dataKey="grossProfit" stroke="#22c55e" fillOpacity={1} fill="url(#colorProfit)" name="Gross Profit" />
            <Line type="monotone" dataKey="ebitda" stroke="#f59e0b" strokeWidth={2} dot={false} name="EBITDA" />
            <Line type="monotone" dataKey="netIncome" stroke="#ef4444" strokeWidth={2} dot={false} name="Net Income" />
          </AreaChart>
        </ResponsiveContainer>
      </SectionCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SectionCard title="Cash Flow">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={cashflowData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="period" tick={{ fontSize: 12 }} />
              <YAxis tickFormatter={formatCurrency} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(value: number) => [formatCurrency(value), '']} />
              <Legend />
              <Bar dataKey="operating" fill="#3b82f6" name="Operating" radius={[4, 4, 0, 0]} />
              <Bar dataKey="investing" fill="#f59e0b" name="Investing" radius={[4, 4, 0, 0]} />
              <Bar dataKey="financing" fill="#22c55e" name="Financing" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </SectionCard>

        <SectionCard title="Cash Balance">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={cashflowData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="period" tick={{ fontSize: 12 }} />
              <YAxis tickFormatter={formatCurrency} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(value: number) => [formatCurrency(value), 'Cash Balance']} />
              <Line type="monotone" dataKey="cashBalance" stroke="#8b5cf6" strokeWidth={3} dot={false} name="Cash Balance" />
            </LineChart>
          </ResponsiveContainer>
        </SectionCard>
      </div>

      <SectionCard title="Balance Sheet">
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={balanceData}>
            <defs>
              <linearGradient id="colorAssets" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorLiabilities" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="period" tick={{ fontSize: 12 }} />
            <YAxis tickFormatter={formatCurrency} tick={{ fontSize: 12 }} />
            <Tooltip formatter={(value: number) => [formatCurrency(value), '']} />
            <Legend />
            <Area type="monotone" dataKey="assets" stroke="#3b82f6" fillOpacity={1} fill="url(#colorAssets)" name="Total Assets" />
            <Area type="monotone" dataKey="liabilities" stroke="#ef4444" fillOpacity={1} fill="url(#colorLiabilities)" name="Total Liabilities" />
            <Line type="monotone" dataKey="equity" stroke="#22c55e" strokeWidth={3} dot={false} name="Equity" />
          </AreaChart>
        </ResponsiveContainer>
      </SectionCard>

      <SectionCard title="P&L Table">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-muted-foreground">
                <th className="pb-2">Period</th>
                <th className="pb-2 text-right">Revenue</th>
                <th className="pb-2 text-right">COGS</th>
                <th className="pb-2 text-right">Gross Profit</th>
                <th className="pb-2 text-right">OpEx</th>
                <th className="pb-2 text-right">EBITDA</th>
                <th className="pb-2 text-right">Net Income</th>
                <th className="pb-2 text-right">Margin</th>
              </tr>
            </thead>
            <tbody>
              {chartData.map((row: any, i: number) => (
                <tr key={i} className="border-b">
                  <td className="py-2 font-medium">{row.period}</td>
                  <td className="py-2 text-right">{formatCurrency(row.revenue)}</td>
                  <td className="py-2 text-right">{formatCurrency(row.revenue - row.grossProfit)}</td>
                  <td className="py-2 text-right">{formatCurrency(row.grossProfit)}</td>
                  <td className="py-2 text-right">{formatCurrency(row.operatingExpenses)}</td>
                  <td className="py-2 text-right">{formatCurrency(row.ebitda)}</td>
                  <td className="py-2 text-right">{formatCurrency(row.netIncome)}</td>
                  <td className="py-2 text-right font-medium">
                    {row.revenue > 0 ? formatPercent(row.netIncome / row.revenue) : 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SectionCard>

      {financial.assumptions && (
        <SectionCard title="Key Assumptions">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(financial.assumptions).map(([key, value]) => (
              <div key={key} className="p-4 bg-muted/50 rounded-lg">
                <p className="text-sm text-muted-foreground">{key.replace(/_/g, ' ')}</p>
                <p className="font-semibold">
                  {typeof value === 'number' && value < 1 ? formatPercent(value) : formatNumber(Number(value))}
                </p>
              </div>
            ))}
          </div>
        </SectionCard>
      )}
    </div>
  )
}