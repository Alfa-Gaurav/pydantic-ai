import { useEffect, useState } from 'react'
import './App.css'


type Cities = { cities: City[] }

type City = { name: string; country: string }

function App() {
  const [cities, setCities] = useState<City[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(false)

  useEffect(() => {
    let isMounted = true
    setError(null)
    setCities([])
    setLoading(true)

    const eventSource = new EventSource('http://localhost:8000/cities')

    eventSource.onopen = () => {
      if (!isMounted) return
      setError(null)
    }

    eventSource.onmessage = (event) => {
      if (!isMounted) return
      try {
        const data = JSON.parse(event.data) as Cities
        setCities(data.cities)
        setLoading(false)
      } catch (err) {
        console.error(err)
      }
    }

    eventSource.onerror = (event) => {
      console.error(event)
      if (!isMounted) return
      setLoading(false)
      eventSource.close()
    }

    return () => {
      isMounted = false
      eventSource.close()
    }
  }, [])

  return (
    <div>
      <h1>Cities</h1>
      {error && <p role="alert" className="error-text">{error}</p>}

      {loading && !error ? (
        <div className="city-grid">
          {Array.from({ length: 8 }).map((_, i) => (
            <div className="skeleton-card" key={`skeleton-${i}`} />
          ))}
        </div>
      ) : null}

      {!loading && !error && cities?.length > 0 ? (
        <div className="city-grid fade-in">
          {cities?.map((city, idx) => (
            <div className="city-item-card" key={`${city.name}-${city.country}-${idx}`}>
              <h3 className="city-item-title">{city.name}</h3>
              <p className="city-item-subtitle">{city.country}</p>
            </div>
          ))}
        </div>
      ) : null}

      {!loading && !error && cities?.length === 0 ? (
        <p className="muted-text">No cities found.</p>
      ) : null}
    </div>
  )
}

export default App
