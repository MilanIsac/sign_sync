import React from 'react';

function TranslationOutput({ translation }) {
    if (!translation) return null;

    return (
        <div className="translation-container">
            <h3 className="subtitle">Translation</h3>
            <p className="translation-text">{translation}</p>
        </div>
    );
}

export default TranslationOutput;