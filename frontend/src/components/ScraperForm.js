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

      {result && result.meaningful && (
        <div className="scraper-results">
          {/* Kelimeler */}
          <div className="scraper-card">
            <h2 className="scraper-card-title">Anlamlı Kelimeler</h2>
            <div className="words-grid">
              {result.meaningful.words.length > 0 ? (
                result.meaningful.words.map((w, i) => (
                  <span
                    key={i}
                    className={`word-badge ${getRandomColor()}`}
                  >
                    {w}
                  </span>
                ))
              ) : (
                <p className="placeholder-text">Kelime bulunamadı.</p>
              )}
            </div>
          </div>

          {/* Cümleler */}
          <div className="scraper-card">
            <h2 className="scraper-card-title">Anlamlı Cümleler</h2>
            <div className="sentences-grid">
              {result.meaningful.sentences.length > 0 ? (
                result.meaningful.sentences.map((s, i) => (
                  <p key={i} className="sentence-badge">{s}</p>
                ))
              ) : (
                <p className="placeholder-text">Cümle bulunamadı.</p>
              )}
            </div>
          </div>

          {/* visual content */}
          <div className="scraper-card">
            <h2 className="scraper-card-title">Resimler</h2>
            <div className="images-grid">
              {result.images && result.images.length > 0 ? (
                result.images.map((src, i) => (
                  <div key={i} className="image-wrapper">
                    <img src={src} alt={`img-${i}`} className="scraped-image" />
                    <a
                      href={src}
                      download={`image-${i}.jpg`}
                      className="download-button"
                    >
                      İndir
                    </a>
                  </div>
                ))
              ) : (
                <p className="placeholder-text">Resim bulunamadı.</p>
              )}
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
