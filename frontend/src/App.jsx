import { useState, useEffect } from 'react'

function App() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/products')
      .then((res) => res.json())
      .then((data) => {
        setProducts(data)
        setLoading(false)
      })
      .catch(() => {
        setError('Could not load products. Is the backend running?')
        setLoading(false)
      })
  }, [])

  if (loading) return <p className="p-8 text-gray-500">Loading products...</p>
  if (error) return <p className="p-8 text-red-600">{error}</p>

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-indigo-600 text-white p-4 shadow">
        <h1 className="text-2xl font-bold">AI Smart Shopping Assistant</h1>
      </header>

      <main className="max-w-6xl mx-auto p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((p) => (
          <div key={p.id} className="bg-white rounded-xl shadow p-5">
            <span className="text-xs font-semibold text-indigo-600 uppercase">{p.category}</span>
            <h2 className="text-lg font-semibold mt-1">{p.name}</h2>
            <p className="text-sm text-gray-600 mt-2">{p.description}</p>
            <div className="flex justify-between items-center mt-4">
              <span className="text-xl font-bold">₹{p.price}</span>
              <span className="text-sm text-yellow-600">⭐ {p.rating}</span>
            </div>
          </div>
        ))}
      </main>
    </div>
  )
}

export default App