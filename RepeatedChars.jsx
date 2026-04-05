import React from 'react';

const RepeatedChars = ({ repeated }) => {
  return (
    <>
      <div className="panel-header" style={{ marginTop: '1.5rem' }}>
        <span className="panel-title">Repeated Chars</span>
      </div>

      {!repeated || repeated.length === 0 ? (
        <p className="no-data">No spam patterns detected.</p>
      ) : (
        <div className="spam-list">
          {repeated.map((item, idx) => (
            <div key={idx} className="spam-row reveal">
              <span className="spam-pattern">"{item.pattern}"</span>
              <span className="spam-insight">{item.insight}</span>
            </div>
          ))}
        </div>
      )}
    </>
  );
};

export default RepeatedChars;
