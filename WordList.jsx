import React from 'react';

const WordList = ({ words }) => {
  if (!words || words.length === 0) {
    return <p className="no-data">No words found.</p>;
  }

  const maxCount = words[0]?.count || 1;

  const handleCopy = () => {
    const txt = words.map((w, i) => `#${i+1} ${w.word.toUpperCase()} — ${w.count}`).join('\n');
    navigator.clipboard.writeText(txt);
  };

  return (
    <>
      <div className="panel-header">
        <span className="panel-title">Top Words</span>
        <button className="icon-btn" onClick={handleCopy} title="Copy results">⧉</button>
      </div>

      <div>
        {words.map((item, idx) => {
          const pct = Math.round((item.count / maxCount) * 100);
          return (
            <div key={idx} className="word-row reveal">
              <span className="word-rank">#{idx + 1}</span>
              {/* bar + name wrapper */}
              <div style={{ position: 'relative', overflow: 'hidden' }}>
                <div className="word-bar" style={{ width: `${pct}%` }} />
                <span className="word-name">{item.word.toUpperCase()}</span>
              </div>
              <span className="word-pct">{pct}%</span>
              <span className="word-count">{item.count}</span>
            </div>
          );
        })}
      </div>
    </>
  );
};

export default WordList;
