'use client';
import { useState } from 'react';
import axios from 'axios';

interface SearchResult {
  website: string;
  url: string;
  title: string;
  price: string;
}

const ProductSearch = () => {
  const [productName, setProductName] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

  const handleSearch = async () => {
    try {
      const walmartResponse = await axios.post<SearchResult>('http://localhost:8000/search', {
        name: productName,
        website: 'walmart',
      });
      const neweggResponse = await axios.post<SearchResult>('http://localhost:8000/search', {
        name: productName,
        website: 'newegg',
      });
      const bestbuyResponse = await axios.post<SearchResult>('http://localhost:8000/search', {
        name: productName,
        website: 'bestbuy',
      });
      setSearchResults([walmartResponse.data, neweggResponse.data, bestbuyResponse.data]);
    } catch (error) {
      console.error('Error searching for product:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">Product Search</h1>
      <div className="flex justify-center mb-4">
        <div className="w-full max-w-3xl">
          <input
            type="text"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            placeholder="Enter product name"
            className="border border-gray-700 rounded px-4 py-2 w-full"
          />
        </div>
      </div>
      <div className="flex justify-center">
        <button
          onClick={handleSearch}
          className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
        >
          Search
        </button>
      </div>

      <div className="mt-8">
        <table className="table-auto w-full">
          <thead>
            <tr>
              <th className="px-4 py-2 border border-gray-700">Site</th>
              <th className="px-4 py-2 border border-gray-700">Item Title Name</th>
              <th className="px-4 py-2 border border-gray-700">Price</th>
            </tr>
          </thead>
          <tbody>
            {searchResults.map((result, index) => (
              <tr key={index}>
                <td className="border border-gray-700 px-4 py-2">{result.website}</td>
                <td className="border border-gray-700 px-4 py-2">
                  {result.price !== 'Price not found' && result.price !== 'No search results found' ? (
                    <a
                      href={result.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-500 underline"
                    >
                      {result.title}
                    </a>
                  ) : (
                    <span>{result.title}</span>
                  )}
                </td>
                <td className="border border-gray-700 px-4 py-2">{result.price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ProductSearch;