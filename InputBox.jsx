import React from 'react';

const SAMPLE = `"Your client support is abysmal! I've been waiting for a response to my query for days. Unacceptable!"`;

const InputBox = ({ text, setText, onAnalyze, onClear, loading }) => {
  return (
    <div className="panel">
      <div className="panel-header">
        <span className="panel-title">Input</span>
        <div className="panel-meta">
          <button className="load-sample" onClick={() => setText(SAMPLE)}>
            ⚡ Load Sample
          </button>
          <span>{text.length} Chars</span>
        </div>
      </div>

      <div className="textarea-wrap">
        <textarea
          placeholder='Paste social media comments here… [tweets, YouTube comments, Reddit posts]'
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </div>

      <div className="analyze-row">
        <button
          className="analyze-btn"
          onClick={onAnalyze}
          disabled={loading || text.trim().length === 0}
        >
          {loading
            ? <><div className="spinner" /> Analyzing…</>
            : <>⚡ Analyze</>}
        </button>
        <button className="clear-btn" onClick={onClear} title="Clear">✕</button>
      </div>
    </div>
  );
};

export default InputBox;
