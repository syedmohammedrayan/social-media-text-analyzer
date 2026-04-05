import React, { useState } from 'react'
import InputBox from './components/InputBox'
import ResultsPanel from './components/ResultsPanel'
import WordList from './components/WordList'
import RepeatedChars from './components/RepeatedChars'

function App() {
  const [text, setText] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    if (!text.trim()) return
    try {
      setLoading(true)
      setError(null)
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })
      if (!response.ok) throw new Error(`Server responded with ${response.status}`)
      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err.message || 'Failed to connect to the Python Analysis engine.')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setText('')
    setResults(null)
    setError(null)
  }

  return (
    <>
      {/* ── HEADER ── */}
      <header className="app-header">
        <div>
          <div className="logo"><span>Text</span>Pulse</div>
          <div className="logo-sub">Social Media Sentiment Analyzer</div>
        </div>
        <div className="engine-badge">
          Analysis Engine<br />
          <span className="version">v2.1.0</span>
        </div>
      </header>

      {/* ── BODY ── */}
      <div className="app-body">
        {/* LEFT COLUMN */}
        <div className="left-col">
          <InputBox
            text={text}
            setText={setText}
            onAnalyze={handleAnalyze}
            onClear={handleClear}
            loading={loading}
          />

          {error && (
            <div className="spam-row" style={{ borderColor: 'var(--red)' }}>
              <span className="spam-insight" style={{ color: 'var(--red)' }}>⚠ {error}</span>
            </div>
          )}

          {results && <ResultsPanel results={results} />}
        </div>

        {/* RIGHT COLUMN */}
        <div className="right-col">
          <div className="panel" style={{ flex: 1 }}>
            {results ? (
              <>
                <WordList words={
                  // Sort ALL frequency words by count descending — matches reference showing #1-#15+
                  Object.entries(results.frequency || {})
                    .sort((a, b) => b[1] - a[1])
                    .map(([word, count]) => ({ word, count }))
                } />
                <RepeatedChars repeated={results.repeated} />
              </>
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', minHeight: '300px' }}>
                <p className="no-data" style={{ textAlign: 'center', lineHeight: 2 }}>
                  Paste text and click <strong style={{ color: 'var(--red)' }}>⚡ Analyze</strong><br />
                  to see results here.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

export default App
