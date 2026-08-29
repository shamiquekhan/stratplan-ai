"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

type TabsContextValue = {
  value: string
  onValueChange: (value: string) => void
}

const TabsContext = React.createContext<TabsContextValue | null>(null)

function useTabsContext() {
  const ctx = React.useContext(TabsContext)
  if (!ctx) {
    throw new Error("Tabs components must be used within <Tabs>")
  }
  return ctx
}

const Tabs = React.forwardRef<
  React.ElementRef<"div">,
  React.ComponentPropsWithoutRef<"div"> & {
    value: string
    onValueChange: (value: string) => void
    defaultValue?: string
    orientation?: "horizontal" | "vertical"
  }
>(({ className, value, onValueChange, orientation = "horizontal", children, ...props }, ref) => {
  return (
    <TabsContext.Provider value={{ value, onValueChange }}>
      <div
        ref={ref}
        className={cn(
          "flex",
          orientation === "vertical" ? "flex-col" : "flex-col",
          className
        )}
        {...props}
      >
        {children}
      </div>
    </TabsContext.Provider>
  )
})
Tabs.displayName = "Tabs"

const TabsList = React.forwardRef<
  React.ElementRef<"div">,
  React.ComponentPropsWithoutRef<"div"> & { ariaLabel?: string }
>(({ className, children, ariaLabel, ...props }, ref) => {
  return (
    <div
      ref={ref}
      role="tablist"
      aria-label={ariaLabel}
      className={cn(
        "inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
})
TabsList.displayName = "TabsList"

const TabsTrigger = React.forwardRef<
  React.ElementRef<"button">,
  React.ComponentPropsWithoutRef<"button"> & { value: string; disabled?: boolean }
>(({ className, value, disabled, children, onClick, ...props }, ref) => {
  const { value: selected, onValueChange } = useTabsContext()
  const isSelected = selected === value

  return (
    <button
      ref={ref}
      type="button"
      role="tab"
      aria-selected={isSelected}
      aria-disabled={disabled}
      data-state={isSelected ? "active" : "inactive"}
      data-disabled={disabled ? "" : undefined}
      data-value={value}
      disabled={disabled}
      onClick={(event) => {
        if (!disabled) onValueChange(value)
        onClick?.(event)
      }}
      className={cn(
        "inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm",
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
})
TabsTrigger.displayName = "TabsTrigger"

const TabsContent = React.forwardRef<
  React.ElementRef<"div">,
  React.ComponentPropsWithoutRef<"div"> & { value: string; forceMount?: boolean }
>(({ className, value, forceMount, children, ...props }, ref) => {
  const { value: selected } = useTabsContext()
  const isActive = selected === value

  if (!forceMount && !isActive) return null

  return (
    <div
      ref={ref}
      role="tabpanel"
      data-value={value}
      data-state={isActive ? "active" : "inactive"}
      hidden={!isActive}
      className={cn(
        "mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
})
TabsContent.displayName = "TabsContent"

export { Tabs, TabsList, TabsTrigger, TabsContent }
