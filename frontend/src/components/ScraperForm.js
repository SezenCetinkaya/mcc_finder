import React, { useState } from 'react';
import './ScraperForm.css'; 

// Canlı renkler
const colors = [
  'bg-red-400 text-white',
  'bg-blue-400 text-white',
  'bg-green-400 text-white',
  'bg-yellow-400 text-gray-900',
  'bg-purple-400 text-white',
  'bg-pink-400 text-white',
  'bg-indigo-400 text-white',
];

function getRandomColor() {
  return colors[Math.floor(Math.random() * colors.length)];
}

export default function ScraperForm() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleScrape = async () => {
    if (!url) return;
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert('Backend ile bağlantı kurulamadı!');
    } finally {
      setLoading(false);
    }
  };

  // Metni indir
  const downloadText = () => {
    if (!result || !result.text) return;
    const blob = new Blob([result.text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'scraped_text.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="scraper-container">
      <h1 className="scraper-title">MCC Finder</h1>

      <div className="scraper-input-section">
        <input
          type="text"
          placeholder="URL girin"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="scraper-input"
        />
        <button
          onClick={handleScrape}
          className="scraper-button"
          disabled={loading}
        >
          {loading ? 'Scraping...' : 'Scrape Et'}
        </button>
      </div>

      {result && (
        <div className="scraper-results flex justify-between gap-4">
          {/* Görseller */}
          <div className="scraper-card w-1/2">
            <div className="flex justify-between items-center">
              <h2 className="scraper-card-title">Resimler</h2>
              <button
                onClick={() => {
                  result.images.forEach((src, i) => {
                    const a = document.createElement('a');
                    a.href = src;
                    a.download = `image-${i}.jpg`;
                    a.click();
                  });
                }}
                className="scraper-button text-sm"
              >
                Tümünü İndir
              </button>
            </div>
            <div className="images-grid mt-2">
              {result.images && result.images.length > 0 ? (
                result.images.map((src, i) => (
                  <div key={i} className="image-wrapper">
                    <img src={src} alt={`img-${i}`} className="scraped-image" />
                  </div>
                ))
              ) : (
                <p className="placeholder-text">Resim bulunamadı.</p>
              )}
            </div>
          </div>

          {/* Metin */}
          <div className="scraper-card w-1/2">
            <div className="flex justify-between items-center">
              <h2 className="scraper-card-title">Metin / Kelimeler</h2>
              <button
                onClick={downloadText}
                className="scraper-button text-sm"
              >
                Metni İndir
              </button>
            </div>

            <div className="words-grid mt-2">
              {result.text ? (
                result.text
                  .split(/(?<=[.!?])\s+/) 
                  .map((sentence, i) => (
                    <p key={i} className="word-badge">
                      {sentence}
                    </p>
                  ))
              ) : (
                <p className="placeholder-text">Metin bulunamadı.</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
