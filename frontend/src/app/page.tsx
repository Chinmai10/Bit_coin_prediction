"use client"

import { useState, useEffect } from "react"
import { ArrowRight, TrendingUp, Loader2, RefreshCcw } from "lucide-react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface PredictionData {
  symbol: string
  final_prediction: {
    date: string
    predicted_price_usdt: number
  }
}

// Sample data for demonstration when API is unavailable
const sampleData: Record<string, PredictionData> = {
  BTCUSDT: {
    symbol: "BTCUSDT",
    final_prediction: {
      date: "2026-05-18",
      predicted_price_usdt: 78245.32,
    },
  },
  ETHUSDT: {
    symbol: "ETHUSDT",
    final_prediction: {
      date: "2026-05-18",
      predicted_price_usdt: 3386.7,
    },
  },
  DOGEBTC: {
    symbol: "DOGEBTC",
    final_prediction: {
      date: "2026-05-18",
      predicted_price_usdt: 0.00000245,
    },
  },
  BNBUSDT: {
    symbol: "BNBUSDT",
    final_prediction: {
      date: "2026-05-18",
      predicted_price_usdt: 542.18,
    },
  },
}

const popularSymbols = ["BTCUSDT", "ETHUSDT", "DOGEBTC", "BNBUSDT", "ADAUSDT", "SOLUSDT", "XRPUSDT", "DOTUSDT"]

export default function Home() {
  const [symbol, setSymbol] = useState("DOGEBTC")
  const [prediction, setPrediction] = useState<PredictionData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [useDemo, setUseDemo] = useState(false)

  const fetchPrediction = async (sym: string) => {
    if (useDemo) {
      // Use sample data in demo mode
      setTimeout(() => {
        const data = sampleData[sym] || null
        setPrediction(data)
        if (!data) {
          setError("No sample data available for this symbol")
        } else {
          setError(null)
        }
        setLoading(false)
      }, 500) // Simulate network delay
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Add a timeout to the fetch request
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000)

      const response = await fetch(`http://127.0.0.1:8000/predict?symbol=${sym}`, {
        signal: controller.signal,
        // Add cache control to prevent caching issues
        cache: "no-store",
        // Add mode to handle CORS issues
        mode: "cors",
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`)
      }

      const data = await response.json()
      if (!data || !data.symbol || !data.final_prediction) {
        setPrediction(null)
        setError("No data available for this symbol")
        return
      }
      setPrediction(data)
    } catch (err) {
      console.error("Error fetching prediction:", err)

      // Handle specific error types
      if (err instanceof TypeError && err.message.includes("fetch")) {
        setError("Cannot connect to the prediction API. The server might be offline or unreachable.")
      } else if (err.name === "AbortError") {
        setError("Request timed out. The API server is taking too long to respond.")
      } else {
        setError("Failed to fetch prediction data. Please try again later.")
      }

      setPrediction(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // fetchPrediction(symbol)
  }, [])

  const handleSymbolChange = (value: string) => {
    setSymbol(value)
    fetchPrediction(value)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  const toggleDemoMode = () => {
    setUseDemo(!useDemo)
    fetchPrediction(symbol)
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100 sm:text-4xl">
            Crypto Price Predictor
          </h1>
          <p className="mt-3 text-gray-500 dark:text-gray-400">
            Get future price predictions for your favorite cryptocurrencies
          </p>
        </div>

        <div className="flex items-center space-x-4">
          <Select value={symbol} onValueChange={handleSymbolChange}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select a symbol" />
            </SelectTrigger>
            <SelectContent>
              {popularSymbols.map((sym) => (
                <SelectItem key={sym} value={sym}>
                  {sym}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Button onClick={() => fetchPrediction(symbol)} disabled={loading} className="flex-shrink-0">
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Predict"}
          </Button>
        </div>



        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {loading ? (
          <div className="flex justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        ) : prediction ? (
          <Card className="w-full shadow-lg hover:shadow-xl transition-shadow duration-300">
            <CardHeader className="bg-primary/5 dark:bg-primary/10">
              <CardTitle className="text-2xl flex items-center">
                <span className="text-primary">{prediction.symbol}</span>
                <TrendingUp className="ml-2 h-5 w-5 text-green-500" />
              </CardTitle>
              <CardDescription>Future price prediction</CardDescription>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Predicted Price</p>
                  <p className="text-3xl font-bold text-green-600 dark:text-green-400">
                    $
                    {prediction.final_prediction.predicted_price_usdt.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 8,
                    })}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Prediction Date</p>
                  <p className="text-lg font-medium">{formatDate(prediction.final_prediction.date)}</p>
                </div>
              </div>
            </CardContent>
            <CardFooter className="bg-gray-50 dark:bg-gray-800/50 flex justify-between">
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {useDemo ? "Sample data for demonstration" : "Based on historical data analysis"}
              </p>
              <Button variant="ghost" size="sm" className="text-primary">
                Details <ArrowRight className="ml-1 h-4 w-4" />
              </Button>
            </CardFooter>
          </Card>
        ) : (
          <Card className="w-full shadow-lg">
            <CardContent className="pt-6 pb-6 flex flex-col items-center justify-center">
              <div className="text-center py-8">
                <p className="text-xl font-medium text-gray-500 dark:text-gray-400">No data available</p>
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                  {useDemo ? "No sample data for this symbol" : "Try selecting a different symbol or enable demo mode"}
                </p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  )
}
