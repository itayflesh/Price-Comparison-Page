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
    <div className="flex flex-col items-center min-h-screen bg-gray-100">
      <header className="w-full bg-white shadow-md py-4">
        <div className="container mx-auto flex justify-center items-center px-4">
          <h1 className="text-2xl font-bold text-gray-800">Product Search</h1>
          <nav>
            {/* Add any additional navigation links here */}
          </nav>
        </div>
      </header>

      <main className="container mx-auto flex-grow flex flex-col justify-center items-center py-8">
        <div className="w-full max-w-3xl">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="mb-4">
              <input
                type="text"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                placeholder="Enter product name"
                className="border border-gray-300 rounded-md px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex justify-center">
              <button
                onClick={handleSearch}
                className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-md transition-colors duration-300"
              >
                Search
              </button>
            </div>
          </div>
        </div>

        <div className="mt-8 w-full max-w-3xl">
          {searchResults.length > 0 ? (
            <div className="bg-white rounded-lg shadow-md overflow-x-auto">
              <table className="w-full table-auto">
                <thead>
                  <tr className="bg-gray-200">
                    <th className="px-4 py-2 text-left font-medium text-gray-700">Site</th>
                    <th className="px-4 py-2 text-left font-medium text-gray-700">Item Title</th>
                    <th className="px-4 py-2 text-left font-medium text-gray-700">Price</th>
                  </tr>
                </thead>
                <tbody>
                  {searchResults.map((result, index) => (
                    <tr key={index} className={index % 2 === 0 ? 'bg-gray-100' : 'bg-white'}>
                      <td className="px-4 py-2 border-b border-gray-200">{result.website}</td>
                      <td className="px-4 py-2 border-b border-gray-200">
                        {result.price !== 'Price not found' && result.price !== 'No search results found' ? (
                          <a
                            href={result.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-500 hover:underline"
                          >
                            {result.title}
                          </a>
                        ) : (
                          <span>{result.title}</span>
                        )}
                      </td>
                      <td className="px-4 py-2 border-b border-gray-200">{result.price}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow-md p-6 text-center">
              { <p className="text-gray-600">No search has been made yet</p> }
            </div>
          )}
        </div>
      </main>

      <footer className="w-full bg-gray-800 py-4">
        <div className="container mx-auto text-center text-white">
          &copy; Itay & noya's Product Search
        </div>
      </footer>
    </div>
  );
};

export default ProductSearch;