from typing import Dict, Any, List
from datetime import datetime, timedelta


class FinancialEngine:
    def __init__(self):
        pass
    
    def build_projections(
        self,
        assumptions: Dict[str, float],
        starting_revenue: float = 0,
        months: int = 36
    ) -> Dict[str, Any]:
        
        revenue_growth = assumptions.get("revenue_growth_rate", 0.15)
        gross_margin = assumptions.get("gross_margin", 0.60)
        opex_ratio = assumptions.get("operating_expense_ratio", 0.50)
        tax_rate = assumptions.get("tax_rate", 0.21)
        interest_rate = assumptions.get("interest_rate", 0.05)
        depreciation_rate = assumptions.get("depreciation_rate", 0.10)
        wc_days = assumptions.get("working_capital_days", 30)
        capex_pct = assumptions.get("capex_percentage_of_revenue", 0.05)
        
        monthly_growth = (1 + revenue_growth) ** (1/12) - 1
        
        pnl = []
        cashflow = []
        balance_sheet = []
        
        cash_balance = starting_revenue * 0.5
        current_assets = cash_balance
        fixed_assets = starting_revenue * 2
        current_liabilities = 0
        longterm_liabilities = starting_revenue * 0.5
        equity = current_assets + fixed_assets - current_liabilities - longterm_liabilities
        retained_earnings = 0
        
        for month in range(1, months + 1):
            period_label = self._get_period_label(month)
            
            if month == 1:
                revenue = starting_revenue
            else:
                revenue = pnl[-1]["revenue"] * (1 + monthly_growth)
            
            cogs = revenue * (1 - gross_margin)
            gross_profit = revenue - cogs
            operating_expenses = revenue * opex_ratio
            ebitda = gross_profit - operating_expenses
            depreciation = fixed_assets * depreciation_rate / 12
            interest = longterm_liabilities * interest_rate / 12
            ebt = ebitda - depreciation - interest
            tax = max(0, ebt * tax_rate)
            net_income = ebt - tax
            retained_earnings += net_income
            
            pnl.append({
                "period": period_label,
                "revenue": round(revenue, 2),
                "cogs": round(cogs, 2),
                "gross_profit": round(gross_profit, 2),
                "operating_expenses": round(operating_expenses, 2),
                "ebitda": round(ebitda, 2),
                "depreciation": round(depreciation, 2),
                "interest": round(interest, 2),
                "tax": round(tax, 2),
                "net_income": round(net_income, 2),
            })
            
            wc_change = (revenue * wc_days / 365) - (current_assets - cash_balance)
            capex = revenue * capex_pct / 12
            cf_operating = net_income + depreciation - wc_change
            cf_investing = -capex
            cf_financing = 0
            net_cash_flow = cf_operating + cf_investing + cf_financing
            cash_balance += net_cash_flow
            
            current_assets = cash_balance + (revenue * wc_days / 365)
            fixed_assets += capex - depreciation
            total_assets = current_assets + fixed_assets
            
            current_liabilities = revenue * 0.1
            equity = total_assets - current_liabilities - longterm_liabilities
            
            cashflow.append({
                "period": period_label,
                "operating": round(cf_operating, 2),
                "investing": round(cf_investing, 2),
                "financing": round(cf_financing, 2),
                "net_cash_flow": round(net_cash_flow, 2),
                "cash_balance": round(cash_balance, 2),
            })
            
            balance_sheet.append({
                "period": period_label,
                "current_assets": round(current_assets, 2),
                "fixed_assets": round(fixed_assets, 2),
                "total_assets": round(total_assets, 2),
                "current_liabilities": round(current_liabilities, 2),
                "longterm_liabilities": round(longterm_liabilities, 2),
                "total_liabilities": round(current_liabilities + longterm_liabilities, 2),
                "equity": round(equity, 2),
            })
        
        key_metrics = self._calculate_key_metrics(pnl, cashflow, assumptions)
        
        return {
            "assumptions": assumptions,
            "pnl": pnl,
            "cash_flow": cashflow,
            "balance_sheet": balance_sheet,
            "key_metrics": key_metrics,
        }
    
    def _get_period_label(self, month: int) -> str:
        if month % 12 == 0:
            return f"Year {month // 12}"
        elif month % 3 == 0:
            return f"Q{(month - 1) // 3 + 1} Year {(month - 1) // 12 + 1}"
        return f"Month {month}"
    
    def _calculate_key_metrics(
        self,
        pnl: List[Dict],
        cashflow: List[Dict],
        assumptions: Dict[str, float]
    ) -> Dict[str, Any]:
        
        final_cash = cashflow[-1]["cash_balance"]
        monthly_burn = abs(min(cf["net_cash_flow"] for cf in cashflow))
        runway = final_cash / monthly_burn if monthly_burn > 0 else 0
        
        break_even_month = None
        for i, row in enumerate(pnl):
            if row["net_income"] > 0:
                break_even_month = i + 1
                break
        
        ltv_cac = 3.0
        payback = 12
        
        if assumptions.get("business_model") == "subscription":
            arr = pnl[-1]["revenue"] * 12 if pnl else 0
            cac = assumptions.get("cac", 1000)
            ltv = arr * assumptions.get("gross_margin", 0.7) / assumptions.get("churn_rate", 0.05)
            ltv_cac = ltv / cac if cac > 0 else 3.0
            payback = cac / (arr / 12 * assumptions.get("gross_margin", 0.7)) * 12 if arr > 0 else 12
        
        return {
            "runway_months": round(runway, 1),
            "break_even_month": break_even_month,
            "ltv_cac_ratio": round(ltv_cac, 1),
            "payback_period_months": round(payback, 1),
            "final_cash": round(final_cash, 2),
            "total_revenue_3yr": round(sum(row["revenue"] for row in pnl), 2),
            "final_net_income": round(pnl[-1]["net_income"], 2) if pnl else 0,
        }
    
    def sensitivity_analysis(
        self,
        base_assumptions: Dict[str, float],
        starting_revenue: float,
        variables: List[str] = None
    ) -> Dict[str, Any]:
        
        if variables is None:
            variables = ["revenue_growth_rate", "gross_margin", "operating_expense_ratio"]
        
        scenarios = {
            "base": base_assumptions.copy(),
            "optimistic": base_assumptions.copy(),
            "pessimistic": base_assumptions.copy(),
        }
        
        for var in variables:
            if var in base_assumptions:
                base_val = base_assumptions[var]
                if "rate" in var or "margin" in var or "ratio" in var:
                    scenarios["optimistic"][var] = base_val * 1.2
                    scenarios["pessimistic"][var] = base_val * 0.8
                else:
                    scenarios["optimistic"][var] = base_val * 1.1
                    scenarios["pessimistic"][var] = base_val * 0.9
        
        results = {}
        for name, assumptions in scenarios.items():
            proj = self.build_projections(assumptions, starting_revenue)
            results[name] = {
                "assumptions": assumptions,
                "key_metrics": proj["key_metrics"],
                "final_revenue": proj["pnl"][-1]["revenue"],
                "final_net_income": proj["pnl"][-1]["net_income"],
            }
        
        return results