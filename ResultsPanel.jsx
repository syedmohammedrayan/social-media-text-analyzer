import React from 'react';
import WordList from './WordList';
import RepeatedChars from './RepeatedChars';

const getEngagement = (wordCount) => {
  if (wordCount > 30) return 'HIGH';
  if (wordCount > 12) return 'MODERATE';
  return 'LOW';
};

const ResultsPanel = ({ results }) => {
  if (!results) return null;

  const { stats, common, repeated, tone, frequency } = results;
  const uniqueWords = Object.keys(frequency || {}).length;
  const avgLen = stats.word_count > 0
    ? (Object.keys(frequency || {}).reduce((s, w) => s + w.length, 0) / uniqueWords).toFixed(1)
    : '0';
  const engagement = getEngagement(stats.word_count);

  return (
    <>
      {/* ── STATS ── */}
      <div className="stats-grid reveal">
        <div className="stat-card">
          <div className="stat-label">Total Words</div>
          <div className="stat-value">{stats.word_count}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Unique Words</div>
          <div className="stat-value">{uniqueWords}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Characters</div>
          <div className="stat-value">{stats.char_count}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Avg Length</div>
          <div className="stat-value">{avgLen}</div>
        </div>
      </div>

      {/* ── TONE ── */}
      <div className="insight-card reveal">
        <div className="insight-icon tone">〜</div>
        <div className="insight-inner">
          <span className="insight-label">Detected Tone</span>
          <span className="insight-value">{tone}</span>
        </div>
      </div>

      {/* ── ENGAGEMENT ── */}
      <div className="insight-card reveal">
        <div className="insight-icon engagement">⚡</div>
        <div className="insight-inner">
          <span className="insight-label">Engagement</span>
          <span className="insight-value amber">{engagement}</span>
        </div>
      </div>
    </>
  );
};

export default ResultsPanel;
