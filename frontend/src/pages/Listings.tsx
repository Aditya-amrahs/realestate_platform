import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

interface Property {
  id: number; title: string; city: string;
  price: number; type: string; size: number;
}

export default function Listings() {
  const [properties, setProperties] = useState<Property[]>([]);
  const [filters, setFilters] = useState({ city: "", min_price: "", max_price: "", type: "" });

  async function fetchProperties() {
    const params = Object.fromEntries(Object.entries(filters).filter(([, v]) => v !== ""));
    const res = await api.get("/properties/", { params });
    setProperties(res.data);
  }

  useEffect(() => { fetchProperties(); }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-semibold text-gray-800 mb-6">Property Listings</h1>

      <div className="bg-white rounded-xl shadow p-4 mb-6 flex flex-wrap gap-3">
        <input className="border rounded-lg px-3 py-2 text-sm flex-1 min-w-[140px]"
          placeholder="City" value={filters.city}
          onChange={e => setFilters({ ...filters, city: e.target.value })} />
        <input className="border rounded-lg px-3 py-2 text-sm flex-1 min-w-[120px]"
          placeholder="Min price" type="number" value={filters.min_price}
          onChange={e => setFilters({ ...filters, min_price: e.target.value })} />
        <input className="border rounded-lg px-3 py-2 text-sm flex-1 min-w-[120px]"
          placeholder="Max price" type="number" value={filters.max_price}
          onChange={e => setFilters({ ...filters, max_price: e.target.value })} />
        <select className="border rounded-lg px-3 py-2 text-sm flex-1 min-w-[120px]"
          value={filters.type} onChange={e => setFilters({ ...filters, type: e.target.value })}>
          <option value="">All types</option>
          <option value="apartment">Apartment</option>
          <option value="house">House</option>
          <option value="villa">Villa</option>
          <option value="plot">Plot</option>
        </select>
        <button onClick={fetchProperties}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-indigo-700">
          Search
        </button>
      </div>

      {properties.length === 0 ? (
        <p className="text-gray-500 text-sm">No properties found.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {properties.map(p => (
            <Link to={`/properties/${p.id}`} key={p.id}
              className="bg-white rounded-xl shadow hover:shadow-md transition p-5 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full">{p.type}</span>
                <span className="text-xs text-gray-400">{p.size} sqft</span>
              </div>
              <h2 className="font-medium text-gray-800">{p.title}</h2>
              <p className="text-sm text-gray-500">{p.city}</p>
              <p className="text-indigo-600 font-semibold">₹{p.price.toLocaleString()}</p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}